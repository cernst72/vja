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
        self._api_client.put_list(namespace_id, title)

    # label
    def add_label(self, title):
        self._api_client.put_label(title)

    # tasks
    _arg_to_json = {'title': {'field': 'title', 'mapping': (lambda x: x)},
                    'note': {'field': 'description', 'mapping': (lambda x: x)},
                    'prio': {'field': 'priority', 'mapping': (lambda x: int(x))},
                    'due': {'field': 'due_date', 'mapping': (lambda x: _parse_date_text(x))},
                    'favorite': {'field': 'is_favorite', 'mapping': (lambda x: bool(x))},
                    'completed': {'field': 'done', 'mapping': (lambda x: bool(x))},
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
        list_id = args.pop('list_id') if args.get('list_id') else None or self._get_default_list().id
        tag_name = args.pop('tag') if args.get('tag') else None
        payload = self._args_to_payload(args)

        task_json = self._api_client.put_task(list_id, payload)
        task = Task.from_json(task_json, None, None)

        label = self._label_from_name(tag_name) if tag_name else None
        if label:
            self._api_client.add_label_to_task(task.id, label.id)

        logger.info('Created task %s in list %s', task.id, list_id)

    def edit_task(self, task_id: int, args: dict):
        tag_name = args.pop('tag') if args.get('tag') else None
        payload = self._args_to_payload(args)

        task_json = self._api_client.post_task(task_id, payload)
        task = Task.from_json(task_json, None, Label.from_json_array(task_json['labels']))

        label = self._label_from_name(tag_name) if tag_name else None
        if label:
            if task.has_label(label):
                self._api_client.remove_label_from_task(task.id, label.id)
            else:
                self._api_client.add_label_to_task(task.id, label.id)

        logger.info('Modified task %s in list %s', task.id, task_json['list_id'])

    def _get_default_list(self) -> List:
        list_objects = [self._list_service.convert_list_json(x) for x in self._api_client.get_lists()]
        if not list_objects:
            raise VjaError('No lists exist. Go and create at least one.')
        list_objects.sort(key=lambda x: x.id)
        favorite_lists = [x for x in list_objects if x.is_favorite]
        if favorite_lists:
            return favorite_lists[0]
        return list_objects[0]

    def _label_from_name(self, name):
        if not name:
            return None
        labels_remote = Label.from_json_array(self._api_client.get_labels())
        label_found = [label for label in labels_remote if label.title == name]
        if not label_found:
            logger.warning("Ignoring non existing label [%s]. You may want to execute \"label add\" first.", name)
            return None
        return label_found[0]


def _parse_date_text(text):
    if not text:
        return None
    timetuple = parsedatetime.Calendar().parse(text)[0]
    datetime_date = datetime.fromtimestamp(time.mktime(timetuple))
    return datetime_date.astimezone(tz.tzlocal()).isoformat()
