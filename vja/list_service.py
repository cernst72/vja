import logging
from typing import Optional

from vja import VjaError
from vja.apiclient import ApiClient
from vja.model import Namespace, List

logger = logging.getLogger(__name__)


class ListService:
    def __init__(self, api_client: ApiClient):
        self._api_client = api_client
        self._namespace_dict: Optional[dict] = None
        self._list_dict: Optional[dict] = None

    def find_namespace_by_id(self, namespace_id: int) -> Namespace:
        if not self._namespace_dict:
            self._namespace_dict = {x['id']: Namespace.from_json(x) for x in self._api_client.get_namespaces()}
        namespace_object = self._namespace_dict.get(namespace_id)
        if not namespace_object:
            logger.info(self._namespace_dict)
            raise VjaError(
                f'Inconsistent data: namespace_id {str(namespace_id)} is referring to non existing cached Namespace.')
        return namespace_object

    def find_list_by_id(self, list_id: int) -> List:
        if not self._list_dict:
            self._list_dict = {list_json['id']: self.convert_list_json(list_json) for list_json in
                               self._api_client.get_lists()}
        list_object = self._list_dict.get(list_id)
        if not list_object:
            logger.info(self._list_dict)
            raise VjaError(f'Inconsistent data: list_id {str(list_id)} is referring to non existing cached List.')
        return list_object

    def convert_list_json(self, list_json: dict) -> List:
        namespace = self.find_namespace_by_id(list_json['namespace_id'])
        return List.from_json(list_json, namespace)
