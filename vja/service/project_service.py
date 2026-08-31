import logging

from vja import VjaError
from vja.adapter.apiclient import ApiClient
from vja.model import Project, User

logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client
        # Cache for constructed Project objects with resolved ancestors.
        # Avoids repeated object creation on every find_project_by_id call (once per task).
        self._project_by_id_cache: dict[int, Project] = {}

    def find_all_projects(self) -> list[Project]:
        if not self._project_by_id_cache:
            self._project_by_id_cache = {x["id"]: Project.from_json(x, []) for x in self._api_client.get_projects()}
            self._fill_ancestors()
        return list(self._project_by_id_cache.values())

    def find_project_by_id_or_title(self, project: str) -> Project:
        if project.isdigit():
            return self.find_project_by_id(int(project))
        return self.find_project_by_title(project)

    def find_project_by_id(self, project_id: int) -> Project:
        self.find_all_projects()
        result = self._project_by_id_cache.get(project_id)
        if result is None:
            msg = f"Project with id {project_id} does not exist."
            raise VjaError(msg)
        return result

    def find_project_by_title(self, title: str) -> Project:
        project_objects = self.find_all_projects()
        project_found = [x for x in project_objects if x.title == title]
        if not project_found:
            msg = f"Project with title {title} does not exist."
            raise VjaError(msg)
        return project_found[0]

    def get_default_project(self) -> Project:
        user = User.from_json(self._api_client.get_user())
        if user.default_project_id == 0:
            project_objects = self.find_all_projects()
            if not project_objects:
                msg = "No projects exist. Go and create at least one."
                raise VjaError(msg)
            favorite_projects = [x for x in project_objects if x.is_favorite]
            if favorite_projects:
                return min(favorite_projects, key=lambda x: x.id)  # first favorite
            return min(project_objects, key=lambda x: x.id)  # first project at all
        return self.find_project_by_id(user.default_project_id)

    def _fill_ancestors(self) -> None:
        for project in self._project_by_id_cache.values():
            ancestor_projects = []
            visited: set[int] = set()
            ancestor = self._get_ancestor_project(project.id, project.parent_project_id)
            while ancestor and ancestor.id not in visited:
                visited.add(ancestor.id)
                ancestor_projects.append(ancestor)
                ancestor = self._get_ancestor_project(ancestor.id, ancestor.parent_project_id)
            project.ancestor_projects = ancestor_projects

    def _get_ancestor_project(self, project_id: int, parent_project_id: int) -> Project | None:
        if parent_project_id in (project_id, 0) or project_id == 0:
            return None
        return self._project_by_id_cache.get(parent_project_id)
