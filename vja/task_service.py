import logging

from vja.list_service import ListService
from vja.model import Task, Label
from vja.urgency import Urgency

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, list_service: ListService, urgency: Urgency):
        self._list_service = list_service
        self._urgency = urgency

    def task_from_json(self, task_json: dict) -> Task:
        list_object = self._list_service.find_list_by_id(task_json['list_id'])
        labels = Label.from_json_array(task_json['labels'])
        task = Task.from_json(task_json, list_object, labels)
        task.urgency = self._urgency.compute_for(task)
        return task
