import datetime
import logging

from vja import VjaError
from vja.apiclient import ApiClient
from vja.model import Bucket, Label, Project
from vja.parse import parse_date_arg_to_iso, parse_json_date, parse_date_arg_to_timedelta, datetime_to_isoformat
from vja.project_service import ProjectService
from vja.task_service import TaskService

logger = logging.getLogger(__name__)


class CommandService:
    def __init__(self, project_service: ProjectService, task_service: TaskService, api_client: ApiClient):
        self._project_service = project_service
        self._task_service = task_service
        self._api_client = api_client

    def login(self, username, password, totp_passcode):
        self._api_client.authenticate(True, username, password, totp_passcode)

    def logout(self):
        self._api_client.logout()
        logger.info('Logged out')

    # project
    def add_project(self, parent_project, title):
        if parent_project:
            if str(parent_project).isdigit():
                parent_project_id = parent_project
            else:
                parent_project_id = self._project_service.find_project_by_title(parent_project).id
        else:
            parent_project_id = None
        project_json = self._api_client.put_project(parent_project_id, title)
        return Project.from_json(project_json, [])

    # bucket
    def add_bucket(self, project_query, title):
        if str(project_query).isdigit():
            project = self._project_service.find_project_by_id(project_query)
        else:
            project = self._project_service.find_project_by_title(project_query)
        project_view = next(x for x in project.views if x.view_kind == "kanban")
        bucket_json = self._api_client.put_bucket(project.id, project_view.id, title)
        return Bucket.from_json(bucket_json)

    # label
    def add_label(self, title):
        label_json = self._api_client.put_label(title)
        return Label.from_json(label_json)

    # tasks
    _arg_to_json = {'title': {'field': 'title', 'mapping': (lambda x: x)},
                    'note': {'field': 'description', 'mapping': (lambda x: x)},
                    'prio': {'field': 'priority', 'mapping': int},
                    'due': {'field': 'due_date', 'mapping': (lambda x: x)},
                    'favorite': {'field': 'is_favorite', 'mapping': bool},
                    'completed': {'field': 'done', 'mapping': bool},
                    'position': {'field': 'position', 'mapping': int},
                    'project_id': {'field': 'project_id', 'mapping': int},
                    'bucket_id': {'field': 'bucket_id', 'mapping': int},
                    'kanban_position': {'field': 'kanban_position', 'mapping': int},
                    'reminder': {'field': 'reminders', 'mapping': (lambda x: x)}
                    }

    def _args_to_payload(self, args: dict):
        payload = {}
        for arg_name, arg_value in args.items():
            mapper = self._arg_to_json[arg_name]
            payload[mapper['field']] = mapper['mapping'](arg_value)
        return payload

    def add_task(self, title, args: dict):
        args.update({'title': title})
        if args.get('project_id'):
            project_arg = args.pop('project_id')
            if str(project_arg).isdigit():
                project_id = project_arg
            else:
                project_id = self._project_service.find_project_by_title(project_arg).id
        else:
            project_id = self._project_service.get_default_project().id
        label_names = args.pop('label')
        is_force = args.pop('force_create') if args.get('force_create') is not None else False
        if args.get('due') is not None:
            args.update({'due': parse_date_arg_to_iso(args.get('due'))})
        self._parse_reminder_arg(args.get('reminder'), args)

        payload = self._args_to_payload(args)

        if not is_force:
            self._validate_add_task(title, label_names)
        logger.debug('put task: %s', payload)
        task_json = self._api_client.put_task(project_id, payload)
        task = self._task_service.task_from_json(task_json)
        for label_name in label_names:
            label = self._label_from_name(label_name, is_force) if label_name else None
            if label:
                self._api_client.add_label_to_task(task.id, label.id)
        return task

    def clone_task(self, task_id: int, title: str):
        task_remote = self._api_client.get_task(task_id)
        task_remote.update({'id': None})
        task_remote.update({'title': title})
        task_remote.update({'position': 0})
        task_remote.update({'bucket_id': 0})

        logger.debug('put task: %s', task_remote)
        task_json = self._api_client.put_task(task_remote['project_id'], task_remote)
        task = self._task_service.task_from_json(task_json)

        for label in task_remote['labels']:
            self._api_client.add_label_to_task(task.id, label['id'])
        return task

    def edit_task(self, task_id: int, args: dict):
        task_remote = self._api_client.get_task(task_id)
        label_name = args.pop('label') if args.get('label') else None
        is_force = args.pop('force_create') if args.get('force_create') is not None else False

        if args.get('due') is not None:
            self._update_due_date(args, task_remote)
        self._update_reminder(args, task_remote)
        if args.get('note_append'):
            append_note = args.pop('note_append')
            args.update({
                'note': task_remote['description'] + '\n' + append_note if task_remote['description'] else append_note
            })

        payload = self._args_to_payload(args)
        logger.debug('update fields: %s', payload)
        task_remote.update(payload)
        logger.debug('post task: %s', task_remote)
        task_json = self._api_client.post_task(task_id, task_remote)
        task_new = self._task_service.task_from_json(task_json)

        label = self._label_from_name(label_name, is_force) if label_name else None
        if label:
            if task_new.has_label(label):
                self._api_client.remove_label_from_task(task_new.id, label.id)
            else:
                self._api_client.add_label_to_task(task_new.id, label.id)
        return task_new

    @staticmethod
    def _update_due_date(args, task_remote):
        # keep using time of remote task, if none is given
        arg_due = args.get('due')
        remote_date = parse_json_date(task_remote['due_date'])
        if remote_date:
            arg_date = parse_date_arg_to_iso(arg_due, remote_date.hour, remote_date.minute)
        else:
            arg_date = parse_date_arg_to_iso(arg_due)
        args.update({'due': arg_date})

    @staticmethod
    def _update_reminder(args, task_remote):
        reminder_arg = args.get('reminder')
        CommandService._parse_reminder_arg(reminder_arg, args)

        # replace the first existing reminder with our entry
        new_reminder = args.pop('reminder')[0] if reminder_arg else None
        if new_reminder is not None:
            old_reminders = task_remote['reminders']
            if old_reminders and len(old_reminders) > 0:
                if new_reminder:
                    old_reminders[0] = new_reminder  # overwrite first remote reminder
                else:
                    old_reminders.pop(0)  # remove first remote reminder
            else:
                if new_reminder:
                    old_reminders = [new_reminder]  # create single reminder
            args.update({'reminder': old_reminders})

    @staticmethod
    def _parse_reminder_arg(reminder_arg, args):
        if reminder_arg is None:
            return
        if reminder_arg == 'due':
            args.update(
                {'reminder': [{'relative_to': 'due_date', 'relative_period': 0}]})  # --reminder=due or --reminder
        elif 'due' in reminder_arg:
            reminder_due_args = reminder_arg.split(" ", 2)
            duration = int(parse_date_arg_to_timedelta(reminder_due_args[0]).total_seconds())
            sign = -1 if reminder_due_args[1] == 'before' else 1
            args.update(
                {'reminder': [{'relative_to': 'due_date',
                               'relative_period': sign * duration}]})  # --reminder="1h before due_date"
        elif reminder_arg == '':
            args.update(
                {'reminder': None})  # --reminder=""
        else:
            args.update(
                {'reminder': [{'reminder': parse_date_arg_to_iso(reminder_arg)}]})

    def toggle_task_done(self, task_id):
        task_remote = self._api_client.get_task(task_id)
        task_remote.update({'done': not task_remote['done']})
        task_json = self._api_client.post_task(task_id, task_remote)
        return self._task_service.task_from_json(task_json)

    def defer_task(self, task_id, delay_by):
        timedelta = parse_date_arg_to_timedelta(delay_by)
        args = {}

        task_remote = self._api_client.get_task(task_id)
        due_date = parse_json_date(task_remote['due_date'])
        if due_date:
            now = datetime.datetime.now().replace(microsecond=0)
            if due_date < now:
                args.update({'due': datetime_to_isoformat(now + timedelta)})
            else:
                args.update({'due': datetime_to_isoformat(due_date + timedelta)})

        old_reminders = task_remote['reminders']
        if old_reminders and len(old_reminders) > 0:
            reminder_date = parse_json_date(old_reminders[0]['reminder'])
            is_absolute_reminder = not old_reminders[0]['relative_to']
            if reminder_date and is_absolute_reminder:
                args.update({'reminder': datetime_to_isoformat(reminder_date + timedelta)})
                self._update_reminder(args, task_remote)

        payload = self._args_to_payload(args)
        logger.debug('update fields: %s', payload)
        task_remote.update(payload)
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

    def _validate_add_task(self, title, label_names):
        tasks_remote = self._api_client.get_tasks(exclude_completed=True)
        if any(task for task in tasks_remote if task['title'] == title):
            raise VjaError("Task with title does exist. You may want to run with --force-create.")
        for label_name in label_names:
            labels_remote = Label.from_json_array(self._api_client.get_labels())
            if not any(label for label in labels_remote if label.title == label_name):
                raise VjaError(
                    "Label does not exist. You may want to execute \"label add\" or run with --force-create.")
