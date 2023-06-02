import logging
from typing import Optional

from vja import VjaError
from vja.apiclient import ApiClient
from vja.model import Project, User

logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client
        self._project_by_id: Optional[dict] = None

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
        ancestor_projects = []
        # project_id = project_json['id']
        # parent_project_id = project_json['parent_project_id']
        # if parent_project_id != id find parent and add it to the ancestors and proceed with parent the same way
        # ancestor = self.get_ancestor_project(project_id, parent_project_id)
        # while ancestor:
        #     ancestor_projects.append(ancestor)
        #     ancestor = self.get_ancestor_project(ancestor.id, ancestor.parent_project_id)
        return Project.from_json(project_json, ancestor_projects)

    def get_ancestor_project(self, project_id, parent_project_id) -> Optional[Project]:
        if project_id == parent_project_id or parent_project_id == 0 or project_id == 0:
            return None
        ancestor = self.find_project_by_id(parent_project_id)
        return ancestor
