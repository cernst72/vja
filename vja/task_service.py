import logging

from vja.model import Task, Label, Assignee
from vja.project_service import ProjectService
from vja.urgency import Urgency

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, project_service: ProjectService, urgency: Urgency):
        self._project_service = project_service
        self._urgency = urgency

    def task_from_json(self, task_json: dict) -> Task:
        project_object = self._project_service.find_project_by_id(
            task_json["project_id"]
        )
        labels = Label.from_json_array(task_json["labels"])
        assignees = Assignee.from_json_array(task_json["assignees"])
        task = Task.from_json(task_json, project_object, labels, assignees)
        task.urgency = self._urgency.compute_for(task)
        return task
