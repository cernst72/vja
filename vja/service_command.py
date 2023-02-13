import logging
import time
from datetime import datetime

from dateutil import tz
from parsedatetime import parsedatetime

from vja import VjaError
from vja.apiclient import ApiClient
from vja.list_service import ListService
from vja.model import Label, List, Task

logger = logging.getLogger(__name__)


def _parse_date_text(text: str):
    if not text:
        return None
    if isinstance(text, datetime):
        return text
    if len(text) > 10:
        text = text[:10] + text[10].replace("T", " ") + text[11:]
    timetuple = parsedatetime.Calendar(version=parsedatetime.VERSION_CONTEXT_STYLE).parse(text)[0]
    datetime_date = datetime.fromtimestamp(time.mktime(timetuple))
    return datetime_date.astimezone(tz.tzlocal()).isoformat()


class CommandService:
    def __init__(self, list_service: ListService, api_client: ApiClient):
        self._list_service = list_service
        self._api_client = api_client

    def authenticate(self, username, password):
        self._api_client.authenticate(username, password)

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
                    'due': {'field': 'due_date', 'mapping': _parse_date_text},
                    'favorite': {'field': 'is_favorite', 'mapping': bool},
                    'completed': {'field': 'done', 'mapping': bool},
                    'position': {'field': 'position', 'mapping': int},
                    'bucket_id': {'field': 'bucket_id', 'mapping': int},
                    'kanban_position': {'field': 'kanban_position', 'mapping': int},
                    'reminder': {'field': 'reminder_dates', 'mapping': (lambda x: [_parse_date_text(x)])}
                    }

    def _args_to_payload(self, args):
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
                list_id = self._find_list_by_title(list_arg).id
        else:
            list_id = self._get_default_list().id

        tag_name = args.pop('tag') if args.get('tag') else None
        is_force = args.pop('force_create') if args.get('force_create') is not None else False
        if args.get('reminder') == 'due':
            args.update({'reminder': args.get('due') or 'tomorrow'})
        payload = self._args_to_payload(args)
        # workaround: api server does not seem to set positions. But they should not be 0, because sorting between 0s
        # does not work.
        seconds = int(time.time() / 60)
        payload.update({'position': seconds, 'kanban_position': seconds})

        if not is_force:
            self._validate_add_task(title, tag_name)
        logger.debug('put task: %s', payload)
        task_json = self._api_client.put_task(list_id, payload)
        task = self._list_service.task_from_json(task_json)

        label = self._label_from_name(tag_name, is_force) if tag_name else None
        if label:
            self._api_client.add_label_to_task(task.id, label.id)
        return task

    def edit_task(self, task_id: int, args: dict):
        task_remote = self._api_client.get_task(task_id)
        tag_name = args.pop('tag') if args.get('tag') else None
        is_force = args.pop('force_create') if args.get('force_create') is not None else False
        if args.get('reminder') == 'due':
            if args.get('due'):
                args.update({'reminder': args.get('due')})
            else:
                args.update({'reminder': task_remote['due_date'] if task_remote['due_date'] else 'tomorrow'})
        payload = self._args_to_payload(args)
        logger.debug('post task: %s', payload)

        task_remote.update(payload)

        task_json = self._api_client.post_task(task_id, task_remote)
        task = self._list_service.task_from_json(task_json)

        label = self._label_from_name(tag_name, is_force) if tag_name else None
        if label:
            if task.has_label(label):
                self._api_client.remove_label_from_task(task.id, label.id)
            else:
                self._api_client.add_label_to_task(task.id, label.id)
        return task

    def toggle_task_done(self, task_id):
        task_existing = Task.from_json(self._api_client.get_task(task_id), None, None)
        payload = {'done': not task_existing.done}
        task_json = self._api_client.post_task(task_id, payload)
        return self._list_service.task_from_json(task_json)

    def _get_default_list(self) -> List:
        list_objects = [self._list_service.convert_list_json(x) for x in self._api_client.get_lists()]
        if not list_objects:
            raise VjaError('No lists exist. Go and create at least one.')
        list_objects.sort(key=lambda x: x.id)
        favorite_lists = [x for x in list_objects if x.is_favorite]
        if favorite_lists:
            return favorite_lists[0]
        return list_objects[0]

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

    def _find_list_by_title(self, list_arg):
        list_objects = [self._list_service.convert_list_json(x) for x in self._api_client.get_lists()]
        if not list_objects:
            raise VjaError('No lists exist. Go and create at least one.')
        list_found = [x for x in list_objects if x.title == list_arg]
        if not list_found:
            raise VjaError(f'List with title {list_arg} does not exist.')
        return list_found[0]
