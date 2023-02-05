import json
import logging
from datetime import datetime

from vja.apiclient import ApiClient
from vja.list_service import ListService
from vja.model import Task, Namespace, Label
from vja.urgency import Urgency

logger = logging.getLogger(__name__)


class QueryService:
    def __init__(self, list_service: ListService, api_client: ApiClient):
        self._list_service = list_service
        self._api_client = api_client

    # namespace
    def print_namespaces(self, is_json, is_jsonvja):
        object_array = Namespace.from_json_array(self._api_client.get_namespaces())
        self._dump_array(object_array, is_json, is_jsonvja)

    # list
    def print_lists(self, is_json, is_jsonvja):
        lists_json = self._api_client.get_lists()
        object_array = [self._list_service.convert_list_json(list_json) for list_json in lists_json]
        self._dump_array(object_array, is_json, is_jsonvja)

    def print_list(self, list_id, is_json, is_jsonvja):
        list_json = self._api_client.get_list(list_id)
        list_object = self._list_service.convert_list_json(list_json)
        self._dump(list_object, is_json, is_jsonvja)

    # label
    def print_labels(self, is_json, is_jsonvja):
        object_array = Label.from_json_array(self._api_client.get_labels())
        self._dump_array(object_array, is_json, is_jsonvja)

    # tasks
    def print_tasks(self, is_json, is_jsonvja, exclude_completed, namespace_filter, list_filter, label_filter,
                    favorite_filter):
        task_object_array = [self.task_from_json(x) for x in
                             self._api_client.get_tasks(exclude_completed=exclude_completed)]
        task_object_array = self._filter(task_object_array, namespace_filter, list_filter, label_filter,
                                         favorite_filter)
        task_object_array.sort(key=lambda x: (x.done, -Urgency.compute(x),
                                              (x.due_date or datetime.max),
                                              -x.priority,
                                              x.tasklist.title.upper(),
                                              x.title.upper()))
        self._dump_array(task_object_array, is_json, is_jsonvja)

    def print_task(self, task_id: int, is_json, is_jsonvja):
        task_json = self._api_client.get_task(task_id)
        task_object = self.task_from_json(task_json)
        self._dump(task_object, is_json, is_jsonvja)

    def task_from_json(self, task_json: dict) -> Task:
        list_object = self._list_service.find_list_by_id(task_json['list_id'])
        labels = Label.from_json_array(task_json['labels'])
        task_object = Task.from_json(task_json, list_object, labels)
        return task_object

    @staticmethod
    def _dump_array(object_array, is_json, is_jsonvja):
        if is_json:
            print(json.dumps([x.json for x in object_array]))
        elif is_jsonvja:
            print(json.dumps([x.data_dict() for x in object_array], default=str))
        else:
            for x in object_array:
                print(x.output())

    @staticmethod
    def _dump(element, is_json, is_jsonvja):
        if is_json:
            print(json.dumps(element.json))
        elif is_jsonvja:
            print(json.dumps(element.data_dict(), default=str))
        else:
            print(element.output())
            print(element)

    @staticmethod
    def _filter(task_object_array, namespace_filter, list_filter, label_filter, favorite_filter):
        filters = []
        if namespace_filter:
            if str(namespace_filter).isdigit():
                filters.append(lambda x: x.tasklist.namespace.id == int(namespace_filter))
            else:
                filters.append(lambda x: x.tasklist.namespace.title == namespace_filter)
        if list_filter:
            if str(list_filter).isdigit():
                filters.append(lambda x: x.tasklist.id == int(list_filter))
            else:
                filters.append(lambda x: x.tasklist.title == list_filter)
        if label_filter:
            if str(label_filter).isdigit():
                filters.append(lambda x: any(label.id == int(label_filter) for label in x.labels))
            else:
                filters.append(lambda x: any(label.title == label_filter for label in x.labels))
        if favorite_filter is not None:
            filters.append(lambda x: x.is_favorite == bool(favorite_filter))
        return list(filter(lambda x: all(f(x) for f in filters), task_object_array))
