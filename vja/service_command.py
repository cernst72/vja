import logging
import time

from vja import VjaError
from vja.apiclient import ApiClient
from vja.list_service import ListService
from vja.model import Label
from vja.parse import parse_date_arg_to_iso, parse_json_date
from vja.task_service import TaskService

logger = logging.getLogger(__name__)


class CommandService:
    def __init__(self, list_service: ListService, task_service: TaskService, api_client: ApiClient):
        self._list_service = list_service
        self._task_service = task_service
        self._api_client = api_client

    def login(self, username, password, totp_passcode):
        self._api_client.authenticate(True, username, password, totp_passcode)

    def logout(self):
        self._api_client.logout()
        logger.info('Logged out')

    # list
    def add_list(self, namespace_id, title):
        if not namespace_id:
            namespaces = self._api_client.get_namespaces()
            namespace_id = min(namespace['id'] if namespace['id'] > 0 else 99999 for namespace in namespaces)
        list_json = self._api_client.put_list(namespace_id, title)
        return self._list_service.convert_list_json(list_json)

    # label
    def add_label(self, title):
        label_json = self._api_client.put_label(title)
        return Label.from_json(label_json)

    # tasks
    _arg_to_json = {'title': {'field': 'title', 'mapping': (lambda x: x)},
                    'note': {'field': 'description', 'mapping': (lambda x: x)},
                    'prio': {'field': 'priority', 'mapping': int},
                    'due': {'field': 'due_date', 'mapping': parse_date_arg_to_iso},
                    'favorite': {'field': 'is_favorite', 'mapping': bool},
                    'completed': {'field': 'done', 'mapping': bool},
                    'position': {'field': 'position', 'mapping': int},
                    'list_id': {'field': 'list_id', 'mapping': int},
                    'bucket_id': {'field': 'bucket_id', 'mapping': int},
                    'kanban_position': {'field': 'kanban_position', 'mapping': int},
                    'reminder': {'field': 'reminder_dates', 'mapping': (lambda x: x)}
                    }

    def _args_to_payload(self, args: dict):
        payload = {}
        for arg_name, arg_value in args.items():
            mapper = self._arg_to_json[arg_name]
            payload[mapper['field']] = mapper['mapping'](arg_value)
        return payload

    def add_task(self, title, args: dict):
        args.update({'title': title})
        if args.get('list_id'):
            list_arg = args.pop('list_id')
            if str(list_arg).isdigit():
                list_id = list_arg
            else:
                list_id = self._list_service.find_list_by_title(list_arg).id
        else:
            list_id = self._list_service.get_default_list().id
        tag_name = args.pop('tag') if args.get('tag') else None
        is_force = args.pop('force_create') if args.get('force_create') is not None else False
        if args.get('reminder') == 'due':
            args.update({'reminder': args.get('due') or 'tomorrow'})
        if args.get('reminder'):
            args.update({'reminder': [parse_date_arg_to_iso(args.get('reminder'))]})

        payload = self._args_to_payload(args)
        # Workaround: api server does not seem to set positions. But they should not be 0, because sorting between 0s
        # does not work. TODO: The following two lines can be removed after
        # https://kolaente.dev/vikunja/api/commit/1efa1696bf46f5a31d96e7862d33f6e4d275816a is productive
        seconds = int(time.time() / 60)
        payload.update({'position': seconds, 'kanban_position': seconds})

        if not is_force:
            self._validate_add_task(title, tag_name)
        logger.debug('put task: %s', payload)
        task_json = self._api_client.put_task(list_id, payload)
        task = self._task_service.task_from_json(task_json)

        label = self._label_from_name(tag_name, is_force) if tag_name else None
        if label:
            self._api_client.add_label_to_task(task.id, label.id)
        return task

    def edit_task(self, task_id: int, args: dict):
        task_remote = self._api_client.get_task(task_id)
        tag_name = args.pop('tag') if args.get('tag') else None
        is_force = args.pop('force_create') if args.get('force_create') is not None else False

        self._update_reminder(args, task_remote)
        if args.get('note_append'):
            append_note = args.pop('note_append')
            args.update({
                'note': task_remote['description'] + '\n' + append_note if task_remote['description'] else append_note
            })

        payload = self._args_to_payload(args)
        logger.debug('post task: %s', payload)
        task_remote.update(payload)
        task_json = self._api_client.post_task(task_id, task_remote)
        task_new = self._task_service.task_from_json(task_json)

        label = self._label_from_name(tag_name, is_force) if tag_name else None
        if label:
            if task_new.has_label(label):
                self._api_client.remove_label_from_task(task_new.id, label.id)
            else:
                self._api_client.add_label_to_task(task_new.id, label.id)
        return task_new

    @staticmethod
    def _update_reminder(args, task_remote):
        if args.get('reminder') == 'due':
            if args.get('due'):
                args.update({'reminder': args.get('due')})  # reminder = cli argument --due
            else:
                if parse_json_date(task_remote['due_date']):
                    args.update({'reminder': task_remote['due_date']})  # reminder = due_date
                else:
                    args.update({'reminder': 'tomorrow'})  # reminder default
        if args.get('reminder') is not None:
            # replace the first existing reminder
            new_reminder = parse_date_arg_to_iso(args.pop('reminder'))
            old_reminders = task_remote['reminder_dates']
            if old_reminders and len(old_reminders) > 0:
                if new_reminder:
                    old_reminders[0] = new_reminder  # overwrite first remote reminder_date
                else:
                    old_reminders.pop(0)  # remove first remote reminder_date
            else:
                if new_reminder:
                    old_reminders = [new_reminder]  # create single reminder_date
            args.update({'reminder': old_reminders})

    def toggle_task_done(self, task_id):
        task_remote = self._api_client.get_task(task_id)
        task_remote.update({'done': not task_remote['done']})
        task_json = self._api_client.post_task(task_id, task_remote)
        return self._task_service.task_from_json(task_json)

    def _label_from_name(self, name, is_force):
        if not name:
            return None
        labels_remote = Label.from_json_array(self._api_client.get_labels())
        label_found = [label for label in labels_remote if label.title == name]
        if not label_found:
            if is_force:
                return Label.from_json(self._api_client.put_label(name))
            logger.warning("Ignoring non existing label [%s]. You may want to execute \"label add\" first.", name)
            return None
        return label_found[0]

    def _validate_add_task(self, title, tag_name):
        tasks_remote = self._api_client.get_tasks(exclude_completed=True)
        if any(task for task in tasks_remote if task['title'] == title):
            raise VjaError("Task with title does exist. You may want to run with --force-create.")
        if tag_name:
            labels_remote = Label.from_json_array(self._api_client.get_labels())
            if not any(label for label in labels_remote if label.title == tag_name):
                raise VjaError(
                    "Label does not exist. You may want to execute \"label add\" or run with --force-create.")
