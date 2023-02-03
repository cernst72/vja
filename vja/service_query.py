import logging
import time
from collections import defaultdict
from datetime import datetime

from dateutil import tz
from parsedatetime import parsedatetime

from vja.apiclient import ApiClient
from vja.list_service import ListService
from vja.model import Task, Namespace, Label

logger = logging.getLogger(__name__)


class QueryService:
    def __init__(self, list_service: ListService, api_client: ApiClient):
        self._list_service = list_service
        self._api_client = api_client

    # namespace
    def print_namespaces(self):
        namespaces_json = self._api_client.get_namespaces()
        logger.debug(namespaces_json)
        for x in namespaces_json:
            print(Namespace.from_json(x).output())

    # list
    def print_lists(self):
        lists_json = self._api_client.get_lists()
        logger.debug(lists_json)
        for list_json in lists_json:
            list_object = self._list_service.convert_list_json(list_json)
            print(list_object.output())

    def print_list(self, list_id):
        list_json = self._api_client.get_list(list_id)
        logger.debug(list_json)
        list_object = self._list_service.convert_list_json(list_json)
        print(list_object)
        print(list_object.output())

    # label
    def print_labels(self):
        labels_json = self._api_client.get_labels()
        logger.debug(labels_json)
        for label_json in labels_json:
            label_object = Label.from_json(label_json)
            print(label_object.output())

    # tasks
    def list_tasks(self):
        tasks_json = self._api_client.get_tasks(exclude_completed=True)
        tasks_object = [self.task_from_json(x) for x in tasks_json]
        tasks_object.sort(key=lambda x: ((x.due_date or datetime.max),
                                         -x.priority,
                                         x.tasklist.title.upper(),
                                         x.title.upper()))
        self.print_tasks(tasks_object)

    def print_tasks(self, tasks, priority_level_sort=False):
        if not tasks:
            print('No tasks found. Go home early!')
        if priority_level_sort:
            tasks_by_prio = defaultdict(list)
            for task in tasks:
                tasks_by_prio[task.urgency()].append(task)
            for prio, items in tasks_by_prio.items():
                print()
                self._print_task_list(tasks, items)
        else:
            self._print_task_list(tasks, tasks)

    def print_task(self, task_id: int):
        task_json = self._api_client.get_task(task_id)
        logger.debug(task_json)
        task_object = self.task_from_json(task_json)
        print(task_object)
        print(task_object.output())

    def _print_task_list(self, tasks, items):
        for item in items:
            print(f'{str(tasks.index(item) + 1):3}' + ' ' + item.output())

    def _parse_date_text(self, text):
        timetuple = parsedatetime.Calendar().parse(text)[0]
        datetime_date = datetime.fromtimestamp(time.mktime(timetuple))
        return datetime_date.astimezone(tz.tzlocal()).isoformat()

    def task_from_json(self, task_json: dict) -> Task:
        list_object = self._list_service.find_list_by_id(task_json['list_id'])
        labels = Label.from_json_array(task_json['labels'])
        task_object = Task.from_json(task_json, list_object, labels)
        return task_object
