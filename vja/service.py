import logging
import time
from collections import defaultdict
from datetime import datetime

from dateutil import tz
from parsedatetime import parsedatetime

from vja import VjaError
from vja.list_service import ListService, convert_list_json
from vja.login import get_client
from vja.model import Task, Namespace, Label, List

logger = logging.getLogger(__name__)


def authenticate(username, password):
    get_client(username, password)


# namespace
def print_namespaces():
    namespaces_json = get_client().get_namespaces()
    logger.debug(namespaces_json)
    for x in namespaces_json:
        print(Namespace.from_json(x).output())


# list
def print_lists():
    lists_json = get_client().get_lists()
    logger.debug(lists_json)
    for list_json in lists_json:
        list_object = convert_list_json(list_json)
        print(list_object.output())


def print_list(list_id):
    list_json = get_client().get_list(list_id)
    logger.debug(list_json)
    list_object = convert_list_json(list_json)
    print(list_object)
    print(list_object.output())


def add_list(namespace_id, title):
    if not namespace_id:
        namespaces = get_client().get_namespaces()
        namespace_id = min(namespace['id'] if namespace['id'] > 0 else 99999 for namespace in namespaces)
    get_client().put_list(namespace_id, title)


# label
def print_labels():
    labels_json = get_client().get_labels()
    logger.debug(labels_json)
    for label_json in labels_json:
        label_object = Label.from_json(label_json)
        print(label_object.output())


def add_label(title):
    get_client().put_label(title)


# tasks
def list_tasks():
    tasks_json = get_client().get_tasks(exclude_completed=True)
    tasks_object = [task_from_json(x) for x in tasks_json]
    tasks_object.sort(key=lambda x: ((x.due_date or datetime.max),
                                     -x.priority,
                                     x.tasklist.title.upper(),
                                     x.title.upper()))
    print_tasks(tasks_object)


def print_tasks(tasks, priority_level_sort=False):
    if not tasks:
        print('No tasks found. Go home early!')
    if priority_level_sort:
        tasks_by_prio = defaultdict(list)
        for task in tasks:
            tasks_by_prio[task.urgency()].append(task)
        for prio, items in tasks_by_prio.items():
            print()
            _print_task_list(tasks, items)
    else:
        _print_task_list(tasks, tasks)


def print_task(task_id: int):
    task_json = get_client().get_task(task_id)
    logger.debug(task_json)
    task_object = task_from_json(task_json)
    print(task_object)
    print(task_object.output())


arg_to_json = {'title': {'field': 'title', 'mapping': (lambda x: x)},
               'note': {'field': 'description', 'mapping': (lambda x: x)},
               'prio': {'field': 'priority', 'mapping': (lambda x: int(x))},
               'due': {'field': 'due_date', 'mapping': (lambda x: _parse_date_text(x))},
               'favorite': {'field': 'is_favorite', 'mapping': (lambda x: bool(x))},
               'completed': {'field': 'done', 'mapping': (lambda x: bool(x))},
               'reminder': {'field': 'reminder_dates', 'mapping': (lambda x: [_parse_date_text(x)])}
               }


def add_task(title, args: dict):
    args.update({'title': title})
    list_id = args.pop('list_id') if args.get('list_id') else None or _get_default_list().id
    label_id = _label_id_from_name(args.pop('tag')) if args.get('tag') else None

    payload = {}
    for arg_name, arg_value in args.items():
        mapper = arg_to_json[arg_name]
        payload[mapper['field']] = mapper['mapping'](arg_value)
    task = get_client().put_task(list_id, label_id, payload)
    logger.info('Created task %s in list %s', task['id'], task['list_id'])


def edit_task(task_id: int, args: dict):
    label_id = _label_id_from_name(args.pop('tag')) if args.get('tag') else None

    payload = {}
    for arg_name, arg_value in args.items():
        mapper = arg_to_json[arg_name]
        payload[mapper['field']] = mapper['mapping'](arg_value)
    task = get_client().post_task(task_id, label_id, payload)
    logger.info('Modified task %s in list %s', task['id'], task['list_id'])


def task_from_json(task_json: dict) -> Task:
    list_object = ListService.find_list_by_id(task_json['list_id'])
    labels = Label.from_json_array(task_json['labels'])
    task_object = Task.from_json(task_json, list_object, labels)
    return task_object


def _get_default_list() -> List:
    list_objects = [convert_list_json(x) for x in get_client().get_lists()]
    if not list_objects:
        raise VjaError('No lists exist. Go and create at least one.')
    list_objects.sort(key=lambda x: x.id)
    favorite_lists = [x for x in list_objects if x.is_favorite]
    if favorite_lists:
        return favorite_lists[0]
    return list_objects[0]


def _print_task_list(tasks, items):
    for item in items:
        print(f'{str(tasks.index(item) + 1):3}' + ' ' + item.output())


def _label_id_from_name(name) -> int:
    if not name:
        return None
    labels_remote = Label.from_json_array(get_client().get_labels())
    label_found = [label for label in labels_remote if label.title == name]
    if not label_found:
        logger.warning("Label does not exist on server: %s", name)
        return None
    return label_found[0].id


def _parse_date_text(text):
    timetuple = parsedatetime.Calendar().parse(text)[0]
    datetime_date = datetime.fromtimestamp(time.mktime(timetuple))
    return datetime_date.astimezone(tz.tzlocal()).isoformat()
