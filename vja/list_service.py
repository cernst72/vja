import logging

from vja import VjaError
from vja.login import get_client
from vja.model import Namespace, List

logger = logging.getLogger(__name__)


class ListService:
    namespace_dict = None
    list_dict: dict = None

    @staticmethod
    def find_namespace_by_id(namespace_id: int) -> Namespace:
        if not ListService.namespace_dict:
            ListService.namespaces_dict = {x['id']: Namespace.from_json(x) for x in get_client().get_namespaces()}
        namespace_object = ListService.namespaces_dict.get(namespace_id)
        if not namespace_object:
            logger.info(ListService.namespaces_dict)
            raise VjaError(
                f'Inconsistent data: namespace_id {str(namespace_id)} is referring to non existing cached Namespace.')
        return namespace_object

    @staticmethod
    def find_list_by_id(list_id: int) -> List:
        if not ListService.list_dict:
            ListService.list_dict = {list_json['id']: convert_list_json(list_json)
                                     for list_json in get_client().get_lists()}
        list_object = ListService.list_dict.get(list_id)
        if not list_object:
            logger.info(ListService.list_dict)
            raise VjaError(f'Inconsistent data: list_id {str(list_id)} is referring to non existing cached List.')
        return list_object


def convert_list_json(list_json: dict) -> List:
    namespace = ListService.find_namespace_by_id(list_json['namespace_id'])
    return List.from_json(list_json, namespace)
