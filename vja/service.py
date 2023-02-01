import logging
from collections import defaultdict
from datetime import datetime

from vja.list_service import ListService, convert_list_json
from vja.login import get_client
from vja.model import Task, Namespace, Label

logger = logging.getLogger(__name__)


def authenticate(username, password):
    get_client(username, password)


def list_tasks():
    tasks_json = get_client().get_tasks(exclude_completed=True)
    tasks_object = [_convert_task_json(x) for x in tasks_json]
    tasks_object.sort(key=lambda x: ((x.due_date or datetime.max),
                                     -x.priority,
                                     x.tasklist.title.upper(),
                                     x.title.upper()))
    print_tasks(tasks_object)


def print_task(task_id):
    task_json = get_client().get_task(task_id)
    logger.debug(task_json)
    task_object = _convert_task_json(task_json)
    print(task_object)


def print_namespaces():
    namespaces_json = get_client().get_namespaces()
    logger.debug(namespaces_json)
    for x in namespaces_json:
        print(Namespace.from_json(x).output())


def print_lists():
    lists_json = get_client().get_lists()
    logger.debug(lists_json)
    for list_json in lists_json:
        list_object = convert_list_json(list_json)
        print(list_object.output())


def print_labels():
    labels_json = get_client().get_labels()
    logger.debug(labels_json)
    for label_json in labels_json:
        label_object = Label.from_json(label_json)
        print(label_object.output())


def _convert_task_json(task_json):
    list_object = ListService.find_list_by_id(task_json['list_id'])
    labels = [Label.from_json(x) for x in task_json['labels'] or []]
    task_object = Task.from_json(task_json, list_object, labels)
    return task_object


def add_task(list_id, line):
    list_id = list_id or get_client().get_lists()[0]['id']  # TODO handle empty list_id
    get_client().put_task(list_id, line)


def add_list(namespace_id, line):
    namespace_id = namespace_id or get_client().get_namespaces()[0]['id']  # TODO handle empty namespace_id
    get_client().put_list(namespace_id, line)


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


def _print_task_list(tasks, items):
    for item in items:
        print(f'{str(tasks.index(item) + 1):3}' + ' ' + item.representation())
