import logging
from typing import Optional

from vja import VjaError
from vja.apiclient import ApiClient
from vja.model import Namespace, List, User

logger = logging.getLogger(__name__)


class ListService:
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client
        self._namespace_by_id: Optional[dict] = None
        self._list_by_id: Optional[dict] = None

    def find_namespace_by_id(self, namespace_id: int) -> Namespace:
        if not self._namespace_by_id:
            self._namespace_by_id = {x['id']: Namespace.from_json(x) for x in self._api_client.get_namespaces()}
        namespace_object = self._namespace_by_id.get(namespace_id)
        if not namespace_object:
            logger.warning(
                'Inconsistent data: namespace_id %s is referring to non existing cached Namespace.', str(namespace_id))
        return namespace_object

    def find_list_by_id(self, list_id: int) -> List:
        if not self._list_by_id:
            self._list_by_id = {x['id']: self.convert_list_json(x) for x in self._api_client.get_lists()}
        return self._list_by_id.get(list_id)

    def find_list_by_title(self, title):
        list_objects = [self.convert_list_json(x) for x in self._api_client.get_lists()]
        if not list_objects:
            raise VjaError('No lists exist. Go and create at least one.')
        list_found = [x for x in list_objects if x.title == title]
        if not list_found:
            raise VjaError(f'List with title {title} does not exist.')
        return list_found[0]

    def get_default_list(self) -> List:
        user = User.from_json(self._api_client.get_user())
        list_found = self.find_list_by_id(user.default_list_id)
        if not list_found:
            list_objects = [self.convert_list_json(x) for x in self._api_client.get_lists()]
            if not list_objects:
                raise VjaError('No lists exist. Go and create at least one.')
            list_objects.sort(key=lambda x: x.id)
            favorite_lists = [x for x in list_objects if x.is_favorite]
            if favorite_lists:
                list_found = favorite_lists[0]
            else:
                list_found = list_objects[0]
        return list_found

    def convert_list_json(self, list_json: dict) -> List:
        namespace = self.find_namespace_by_id(list_json['namespace_id'])
        return List.from_json(list_json, namespace)
