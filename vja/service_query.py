import logging

from vja.apiclient import ApiClient
from vja.filter import create_filters
from vja.model import Label, User, Bucket
from vja.parse import rgetattr
from vja.project_service import ProjectService
from vja.task_service import TaskService

logger = logging.getLogger(__name__)
DEFAULT_SORT_STRING = 'done, -urgency, due_date, -priority, project.title, title'


class QueryService:
    def __init__(self, project_service: ProjectService, task_service: TaskService, api_client: ApiClient):
        self._project_service = project_service
        self._task_service = task_service
        self._api_client = api_client

    # user
    def find_current_user(self):
        return User.from_json(self._api_client.get_user())

    # project
    def find_all_projects(self):
        return self._project_service.find_all_projects()

    def find_project_by_id(self, project_id):
        return self._project_service.find_project_by_id(project_id)

    # bucket
    def find_all_buckets_in_project(self, project_id):
        return Bucket.from_json_array(self._api_client.get_buckets(project_id))

    # label
    def find_all_labels(self):
        return Label.from_json_array(self._api_client.get_labels())

    # tasks
    def find_filtered_tasks(self, include_completed, sort_string, filter_args):
        task_object_array = [self._task_service.task_from_json(x) for x in
                             self._api_client.get_tasks(exclude_completed=not include_completed)]
        filtered_tasks = self._filter(task_object_array, filter_args)
        return self._sort(filtered_tasks, sort_string)

    def find_task_by_id(self, task_id: int):
        return self._task_service.task_from_json(self._api_client.get_task(task_id))

    @staticmethod
    def _filter(task_object_array, filter_args):
        filters = create_filters(filter_args)
        return list(filter(lambda x: all(f(x) for f in filters), task_object_array))

    @staticmethod
    def _sort(filtered_tasks, sort_string):
        sort_string = sort_string or DEFAULT_SORT_STRING
        sort_fields = [{'name': x.strip().strip('-'),
                        'reverse': x.strip().startswith('-')}
                       for x in sort_string.split(',')]
        for sort_field in reversed(sort_fields):
            filtered_tasks.sort(
                key=lambda x, field=sort_field['name']: (
                    sortable_task_value(x, field) is None, sortable_task_value(x, field)),
                reverse=sort_field['reverse'])
        return filtered_tasks


def sortable_task_value(task, field):
    field_name = field
    if field in ('label', 'labels'):
        field_name = 'labels'
    field_value = rgetattr(task, field_name)
    if isinstance(field_value, str):
        return field_value.upper()
    return field_value
