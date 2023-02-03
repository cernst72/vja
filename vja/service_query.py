import logging
from datetime import datetime

from vja.apiclient import ApiClient
from vja.list_service import ListService
from vja.model import Task, Namespace, Label

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
    def list_tasks(self, is_json, is_jsonvja):
        tasks_json = self._api_client.get_tasks(exclude_completed=True)
        tasks_object = [self.task_from_json(x) for x in tasks_json]
        tasks_object.sort(key=lambda x: ((x.due_date or datetime.max),
                                         -x.priority,
                                         x.tasklist.title.upper(),
                                         x.title.upper()))
        self._dump_array(tasks_object, is_json, is_jsonvja)

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
            print([x.json for x in object_array])
        elif is_jsonvja:
            print([x.data_dict() for x in object_array])
        else:
            for x in object_array:
                print(x.output())

    @staticmethod
    def _dump(element, is_json, is_jsonvja):
        if is_json:
            print(element.json)
        elif is_jsonvja:
            print(element.data_dict())
        else:
            print(element.output())
            print(element)
