import logging
import operator
import re
import typing
from datetime import datetime, timedelta

from vja.parse import (parse_bool_arg, parse_date_arg_to_datetime,
                       parse_date_arg_to_timedelta, rgetattr)

logger = logging.getLogger(__name__)


def _create_bucket_filter(value):
    return _create_general_filter([f'bucket_id eq {value}'])


def _create_due_date_filter(value: str):
    if value.strip() == '':
        return lambda x: not x.due_date
    return _create_general_filter([f'due_date {value}'])


def _create_general_filter(values: typing.List[str]):
    return [_create_single_general_filter(x) for x in values]


def _create_single_general_filter(value: str):
    arguments = value.split(" ", 2)
    field = arguments[0]
    operation = _operators[arguments[1]]
    value = arguments[2]
    logger.debug("filter %s: %s %s", field, operation.__name__, value)
    return lambda x: _general_filter(x, field, operation, value)


def _general_filter(task, field_name, operation, value):
    task_value = rgetattr(task, field_name)
    if task_value is not None:
        if isinstance(task_value, datetime):
            value = parse_date_arg_to_datetime(value)
        elif isinstance(task_value, timedelta):
            value = parse_date_arg_to_timedelta(value)
        elif isinstance(task_value, bool):
            value = parse_bool_arg(value)
        elif isinstance(task_value, int):
            value = int(value)
        elif isinstance(task_value, float):
            value = float(value)
        return operation(task_value, value)
    return False


def _create_favorite_filter(value):
    return _create_general_filter([f'is_favorite eq {value}'])


def _create_label_filter(value):
    logger.debug("filter labels %s", value)
    if str(value).isdigit():
        return lambda x: any(label.id == int(value) for label in x.labels)
    if str(value).strip() == '':
        return lambda x: not x.labels
    return lambda x: any(label.title == value for label in x.labels)


def _create_list_filter(value):
    if str(value).isdigit():
        return _create_general_filter([f'tasklist.id eq {value}'])
    return _create_general_filter([f'tasklist.title eq {value}'])


def _create_namespace_filter(value):
    if str(value).isdigit():
        return _create_general_filter([f'tasklist.namespace.id eq {value}'])
    return _create_general_filter([f'tasklist.namespace.title eq {value}'])


def _create_title_filter(value):
    return lambda x: bool(re.search(re.compile(value), x.title))


def _create_priority_filter(value):
    return _create_general_filter([f'priority {value}'])


def _create_urgency_filter(value):
    return _create_general_filter([f'urgency ge {value}'])


_operators = {
    'eq': operator.eq,
    'ne': operator.ne,
    'lt': operator.lt,
    'le': operator.le,
    'gt': operator.gt,
    'ge': operator.ge,
    'before': operator.lt,
    'after': operator.gt,
    'contains': operator.contains
}

_filter_mapping = {
    'bucket_filter': _create_bucket_filter,
    'due_date_filter': _create_due_date_filter,
    'favorite_filter': _create_favorite_filter,
    'general_filter': _create_general_filter,
    'label_filter': _create_label_filter,
    'list_filter': _create_list_filter,
    'namespace_filter': _create_namespace_filter,
    'title_filter': _create_title_filter,
    'priority_filter': _create_priority_filter,
    'urgency_filter': _create_urgency_filter,
}


def create_filters(filter_args):
    filters = []
    for filter_name, filter_value in filter_args.items():
        add_filter = _filter_mapping[filter_name](filter_value)
        filters.extend(add_filter if isinstance(add_filter, (list, tuple)) else [add_filter])
    return filters
