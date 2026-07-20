import logging

from vja import VjaError
from vja.adapter.apiclient import ApiClient
from vja.model import Project, User

logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client
        self._project_by_id_cache: dict[int, Project] = {}

    def find_all_projects(self) -> list[Project]:
        if not self._project_by_id_cache:
            self._project_by_id_cache = {
                x["id"]: Project.from_json(x, [])
                for x in self._api_client.get_projects()
            }
            self.fill_ancestors()
        return list(self._project_by_id_cache.values())

    def find_project_by_id_or_title(self, project: str) -> Project:
        if project.isdigit():
            return self.find_project_by_id(int(project))
        return self.find_project_by_title(project)


    def find_project_by_id(self, project_id: int) -> Project:
        if not self._project_by_id_cache:
            self._project_by_id_cache = {
                x["id"]: Project.from_json(x, [])
                for x in self._api_client.get_projects()
            }
            self.fill_ancestors()
        result = self._project_by_id_cache.get(project_id)
        if not result:
            msg = f"Project with id {project_id} does not exist."
            raise VjaError(msg)
        return result

    def find_project_by_title(self, title) -> Project:
        project_objects = [
            Project.from_json(x, []) for x in self._api_client.get_projects()
        ]
        if not project_objects:
            msg = "No projects exist. Go and create at least one."
            raise VjaError(msg)
        project_found = [x for x in project_objects if x.title == title]
        if not project_found:
            msg = f"Project with title {title} does not exist."
            raise VjaError(msg)
        return project_found[0]

    def get_default_project(self) -> Project:
        user = User.from_json(self._api_client.get_user())
        project_found = self.find_project_by_id(user.default_project_id)
        if project_found is None:
            project_objects = [
                Project.from_json(x, []) for x in self._api_client.get_projects()
            ]
            if not project_objects:
                msg = "No projects exist. Go and create at least one."
                raise VjaError(msg)
            project_objects.sort(key=lambda x: x.id)
            favorite_projects = [x for x in project_objects if x.is_favorite]
            if favorite_projects:
                project_found = favorite_projects[0]
            else:
                project_found = project_objects[0]
        return project_found

    def fill_ancestors(self):
        for project in self._project_by_id_cache.values():
            ancestor_projects = []
            ancestor = self.get_ancestor_project(project.id, project.parent_project_id)
            while ancestor:
                ancestor_projects.append(ancestor)
                ancestor = self.get_ancestor_project(
                    ancestor.id, ancestor.parent_project_id
                )
            project.ancestor_projects = ancestor_projects

    def get_ancestor_project(self, project_id, parent_project_id) -> Project | None:
        if parent_project_id in (project_id, 0) or project_id == 0:
            return None
        return self._project_by_id_cache.get(parent_project_id)
