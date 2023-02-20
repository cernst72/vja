import functools
import logging

from vja.apiclient import ApiClient
from vja.filter import create_filter
from vja.list_service import ListService
from vja.model import Namespace, Label, User, Bucket

logger = logging.getLogger(__name__)
DEFAULT_SORT_STRING = 'done, -urgency, due_date, -priority, tasklist.title, title'


def rgetattr(obj, path: str, *default):
    attrs = path.split('.')
    try:
        return functools.reduce(getattr, attrs, obj)
    except AttributeError:
        if default:
            return default[0]
        raise


class QueryService:
    def __init__(self, list_service: ListService, api_client: ApiClient):
        self._list_service = list_service
        self._api_client = api_client

    # user
    def find_current_user(self):
        return User.from_json(self._api_client.get_user())

    # namespace
    def find_all_namespaces(self):
        return Namespace.from_json_array(self._api_client.get_namespaces())

    # list
    def find_all_lists(self):
        return [self._list_service.convert_list_json(list_json) for list_json in (self._api_client.get_lists())]

    def find_list_by_id(self, list_id):
        return self._list_service.convert_list_json(self._api_client.get_list(list_id))

    # bucket
    def find_all_buckets_in_list(self, list_id):
        return Bucket.from_json_array(self._api_client.get_buckets(list_id))

    # label
    def find_all_labels(self):
        return Label.from_json_array(self._api_client.get_labels())

    # tasks
    def find_filtered_tasks(self, include_completed, sort_string, filter_args):
        task_object_array = [self._list_service.task_from_json(x) for x in
                             self._api_client.get_tasks(exclude_completed=not include_completed)]
        filtered_tasks = self._filter(task_object_array, filter_args)
        return self._sort(filtered_tasks, sort_string)

    def find_task_by_id(self, task_id: int):
        return self._list_service.task_from_json(self._api_client.get_task(task_id))

    @staticmethod
    def _filter(task_object_array, filter_args):
        filters = create_filter(filter_args)
        return list(filter(lambda x: all(f(x) for f in filters), task_object_array))

    @staticmethod
    def _sort(filtered_tasks, sort_string):
        sort_string = sort_string or DEFAULT_SORT_STRING
        sort_values = [(x.strip().strip('-'), x.strip().startswith('-')) for x in sort_string.split(',')]
        for sort_value in reversed(sort_values):
            field_name = 'sortable_due_date' if sort_value[0] == 'due_date' else sort_value[0]
            filtered_tasks.sort(key=lambda x, field=field_name: rgetattr(x, field), reverse=sort_value[1])
        return filtered_tasks
