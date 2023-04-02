import logging
from typing import Optional

from vja import VjaError
from vja.apiclient import ApiClient
from vja.model import Namespace, Project, User

logger = logging.getLogger(__name__)


class ListService:
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client
        self._namespace_by_id: Optional[dict] = None
        self._project_by_id: Optional[dict] = None

    def find_namespace_by_id(self, namespace_id: int) -> Namespace:
        if not self._namespace_by_id:
            self._namespace_by_id = {x['id']: Namespace.from_json(x) for x in self._api_client.get_namespaces()}
        namespace_object = self._namespace_by_id.get(namespace_id)
        if not namespace_object:
            logger.warning(
                'Inconsistent data: namespace_id %s is referring to non existing cached Namespace.', str(namespace_id))
        return namespace_object

    def find_project_by_id(self, project_id: int) -> Project:
        if not self._project_by_id:
            self._project_by_id = {x['id']: self.convert_project_json(x) for x in self._api_client.get_projects()}
        return self._project_by_id.get(project_id)

    def find_project_by_title(self, title):
        project_objects = [self.convert_project_json(x) for x in self._api_client.get_projects()]
        if not project_objects:
            raise VjaError('No projects exist. Go and create at least one.')
        project_found = [x for x in project_objects if x.title == title]
        if not project_found:
            raise VjaError(f'Project with title {title} does not exist.')
        return project_found[0]

    def get_default_project(self) -> Project:
        user = User.from_json(self._api_client.get_user())
        project_found = self.find_project_by_id(user.default_project_id)
        if not project_found:
            project_objects = [self.convert_project_json(x) for x in self._api_client.get_projects()]
            if not project_objects:
                raise VjaError('No projects exist. Go and create at least one.')
            project_objects.sort(key=lambda x: x.id)
            favorite_projects = [x for x in project_objects if x.is_favorite]
            if favorite_projects:
                project_found = favorite_projects[0]
            else:
                project_found = project_objects[0]
        return project_found

    def convert_project_json(self, project_json: dict) -> Project:
        namespace = self.find_namespace_by_id(project_json['namespace_id'])
        return Project.from_json(project_json, namespace)
