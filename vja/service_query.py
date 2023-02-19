import logging
from datetime import datetime

from vja.apiclient import ApiClient
from vja.filter import create_filter
from vja.list_service import ListService
from vja.model import Namespace, Label, User, Bucket

logger = logging.getLogger(__name__)


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
    def find_filtered_tasks(self, include_completed, filter_args):
        task_object_array = [self._list_service.task_from_json(x) for x in
                             self._api_client.get_tasks(exclude_completed=not include_completed)]
        filtered_tasks = self._filter(task_object_array, filter_args)
        filtered_tasks.sort(key=lambda x: (x.done, -x.urgency,
                                           (x.due_date or datetime.max),
                                           -x.priority,
                                           x.tasklist.title.upper(),
                                           x.title.upper()))
        return filtered_tasks

    def find_task_by_id(self, task_id: int):
        return self._list_service.task_from_json(self._api_client.get_task(task_id))

    @staticmethod
    def _filter(task_object_array, filter_args):
        filters = create_filter(filter_args)
        return list(filter(lambda x: all(f(x) for f in filters), task_object_array))
