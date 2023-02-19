import logging
import re
from datetime import datetime

from vja.apiclient import ApiClient
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
    def find_filtered_tasks(self, include_completed, namespace_filter, list_filter, label_filter,
                            favorite_filter, title_filter, urgency_filter):
        task_object_array = [self._list_service.task_from_json(x) for x in
                             self._api_client.get_tasks(exclude_completed=not include_completed)]
        task_object_array = self._filter(task_object_array, namespace_filter, list_filter, label_filter,
                                         favorite_filter, title_filter, urgency_filter)
        task_object_array.sort(key=lambda x: (x.done, -x.urgency,
                                              (x.due_date or datetime.max),
                                              -x.priority,
                                              x.tasklist.title.upper(),
                                              x.title.upper()))
        return task_object_array

    def find_task_by_id(self, task_id: int):
        return self._list_service.task_from_json(self._api_client.get_task(task_id))

    @staticmethod
    def _filter(task_object_array, namespace_filter, list_filter, label_filter, favorite_filter, title_filter,
                urgency_filter: int):
        filters = []
        if favorite_filter is not None:
            filters.append(lambda x: x.is_favorite == bool(favorite_filter))
        if label_filter or label_filter == '':
            if str(label_filter).isdigit():
                filters.append(lambda x: any(label.id == int(label_filter) for label in x.labels))
            elif str(label_filter).strip() == '':
                filters.append(lambda x: not x.labels)
            else:
                filters.append(lambda x: any(label.title == label_filter for label in x.labels))
        if list_filter:
            if str(list_filter).isdigit():
                filters.append(lambda x: x.tasklist.id == int(list_filter))
            else:
                filters.append(lambda x: x.tasklist.title == list_filter)
        if namespace_filter:
            if str(namespace_filter).isdigit():
                filters.append(lambda x: x.tasklist.namespace.id == int(namespace_filter))
            else:
                filters.append(lambda x: x.tasklist.namespace.title == namespace_filter)
        if title_filter is not None:
            filters.append(lambda x: bool(re.search(re.compile(title_filter), x.title)))
        if urgency_filter is not None:
            filters.append(lambda x: x.urgency >= urgency_filter)
        return list(filter(lambda x: all(f(x) for f in filters), task_object_array))
