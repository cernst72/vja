import re


def _create_favorite_filter(value):
    return lambda x: x.is_favorite == bool(value)


def _create_label_filter(value):
    if str(value).isdigit():
        return lambda x: any(label.id == int(value) for label in x.labels)
    if str(value).strip() == '':
        return lambda x: not x.labels
    return lambda x: any(label.title == value for label in x.labels)


def _create_list_filter(value):
    if str(value).isdigit():
        return lambda x: x.tasklist.id == int(value)
    return lambda x: x.tasklist.title == value


def _create_namespace_filter(value):
    if str(value).isdigit():
        return lambda x: x.tasklist.namespace.id == int(value)
    return lambda x: x.tasklist.namespace.title == value


def _create_title_filter(value):
    return lambda x: bool(re.search(re.compile(value), x.title))


def _create_urgency_filter(value):
    return lambda x: x.urgency >= value


_filter_mapping = {
    'favorite_filter': _create_favorite_filter,
    'label_filter': _create_label_filter,
    'list_filter': _create_list_filter,
    'namespace_filter': _create_namespace_filter,
    'title_filter': _create_title_filter,
    'urgency_filter': _create_urgency_filter,
}


def create_filter(filter_args):
    filters = []
    for filter_name, filter_value in filter_args.items():
        filters.append(_filter_mapping[filter_name](filter_value))
    return filters
