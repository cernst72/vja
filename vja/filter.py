import logging
import operator
import re

from vja import parse

logger = logging.getLogger(__name__)


def _create_due_date_filter(value: str):
    if value.strip() == '':
        return lambda x: not x.due_date
    arguments = value.split(" ", 1)
    operator_name = arguments[0]
    operation = _operators[operator_name]
    value = parse.parse_date_arg_to_datetime(arguments[1])
    logger.debug("filter due date %s %s", operation.__name__, value)
    return lambda x: (operation(x.due_date, value) if x.due_date else False)


def _create_favorite_filter(value):
    logger.debug("filter favorite %s", value)
    return lambda x: x.is_favorite == bool(value)


def _create_label_filter(value):
    logger.debug("filter labels %s", value)
    if str(value).isdigit():
        return lambda x: any(label.id == int(value) for label in x.labels)
    if str(value).strip() == '':
        return lambda x: not x.labels
    return lambda x: any(label.title == value for label in x.labels)


def _create_list_filter(value):
    logger.debug("filter list %s", value)
    if str(value).isdigit():
        return lambda x: x.tasklist.id == int(value)
    return lambda x: x.tasklist.title == value


def _create_namespace_filter(value):
    logger.debug("filter namespace %s", value)
    if str(value).isdigit():
        return lambda x: x.tasklist.namespace.id == int(value)
    return lambda x: x.tasklist.namespace.title == value


def _create_title_filter(value):
    return lambda x: bool(re.search(re.compile(value), x.title))


def _create_priority_filter(value):
    arguments = str(value).split(" ", 1)
    operator_name = arguments[0]
    operation = _operators[operator_name]
    value = arguments[1]
    logger.debug("filter priority %s %s", operation.__name__, value)
    return lambda x: operation(x.priority, int(value))


def _create_urgency_filter(value):
    logger.debug("filter urgency %s", value)
    return lambda x: x.urgency >= value


_operators = {
    'eq': operator.eq,
    'ne': operator.ne,
    'lt': operator.lt,
    'le': operator.le,
    'gt': operator.gt,
    'ge': operator.ge,
    'before': operator.lt,
    'after': operator.gt
}

_filter_mapping = {
    'due_date_filter': _create_due_date_filter,
    'favorite_filter': _create_favorite_filter,
    'label_filter': _create_label_filter,
    'list_filter': _create_list_filter,
    'namespace_filter': _create_namespace_filter,
    'title_filter': _create_title_filter,
    'priority_filter': _create_priority_filter,
    'urgency_filter': _create_urgency_filter,
}


def create_filter(filter_args):
    filters = []
    for filter_name, filter_value in filter_args.items():
        filters.append(_filter_mapping[filter_name](filter_value))
    return filters
