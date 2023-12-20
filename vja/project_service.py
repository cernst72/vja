import logging
from typing import Optional, List

from vja import VjaError
from vja.apiclient import ApiClient
from vja.model import Project, User

logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client
        self._project_by_id: dict[int, Project] = {}

    def find_all_projects(self) -> List[Project]:
        if not self._project_by_id:
            self._project_by_id = {x['id']: Project.from_json(x, []) for x in self._api_client.get_projects()}
            self.fill_ancestors()
        return self._project_by_id.values()

    def find_project_by_id(self, project_id: int) -> Optional[Project]:
        if not self._project_by_id:
            self._project_by_id = {x['id']: Project.from_json(x, []) for x in self._api_client.get_projects()}
            self.fill_ancestors()
        return self._project_by_id.get(project_id)

    def find_project_by_title(self, title) -> Project:
        project_objects = [Project.from_json(x, []) for x in self._api_client.get_projects()]
        if not project_objects:
            raise VjaError('No projects exist. Go and create at least one.')
        project_found = [x for x in project_objects if x.title == title]
        if not project_found:
            raise VjaError(f'Project with title {title} does not exist.')
        return project_found[0]

    def get_default_project(self) -> Project:
        user = User.from_json(self._api_client.get_user())
        project_found = self.find_project_by_id(user.default_project_id)
        if project_found is None:
            project_objects = [Project.from_json(x, []) for x in self._api_client.get_projects()]
            if not project_objects:
                raise VjaError('No projects exist. Go and create at least one.')
            project_objects.sort(key=lambda x: x.id)
            favorite_projects = [x for x in project_objects if x.is_favorite]
            if favorite_projects:
                project_found = favorite_projects[0]
            else:
                project_found = project_objects[0]
        return project_found

    def fill_ancestors(self):
        for project in self._project_by_id.values():
            ancestor_projects = []
            ancestor = self.get_ancestor_project(project.id, project.parent_project_id)
            while ancestor:
                ancestor_projects.append(ancestor)
                ancestor = self.get_ancestor_project(ancestor.id, ancestor.parent_project_id)
            project.ancestor_projects = ancestor_projects

    def get_ancestor_project(self, project_id, parent_project_id) -> Optional[Project]:
        if project_id == parent_project_id or parent_project_id == 0 or project_id == 0:
            return None
        return self._project_by_id.get(parent_project_id)
