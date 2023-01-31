import json
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from time import mktime

import parsedatetime as pdt
from dateutil import tz

from vja.login import get_client
from vja.model import PrintableTask

logger = logging.getLogger(__name__)


def authenticate(username, password):
    get_client(username, password)


def list_tasks():
    raw_tasks = get_client().get_tasks(exclude_completed=True)

    filtered_tasks = [PrintableTask(x) for x in raw_tasks]
    filtered_tasks.sort(key=lambda x: ((x.due_date or datetime.max),
                                       -x.priority,
                                       x.list_name().upper(),
                                       x.title.upper()))
    print_tasks(filtered_tasks)


def report_tasks(list_name, all_size, urgency_sort):
    tasks = _get_tasks(None, 'today', list_name)
    if all_size == 0:
        tasks += _get_tasks('today', 'in 3 days', list_name)
        tasks += _get_tasks(None, None, list_name)
    if all_size > 0:
        tasks += _get_tasks('today', 'tomorrow+364 days', list_name)
        tasks += _get_tasks(None, None, list_name)
    if urgency_sort:
        tasks.sort(key=lambda x: x.urgency(), reverse=True)
    print_tasks(tasks, urgency_sort)


def print_task(task_id):
    task = get_client().get_task(task_id)
    logger.debug(json.dumps(task, default=vars))
    print(PrintableTask(task).representation())

def print_namespaces():
    namespaces = get_client().get_namespaces()
    logger.debug(json.dumps(namespaces, default=vars))
    for x in namespaces:
        print("%d %s %s" % (x.id, x.title, x.description))


def print_lists():
    lists = get_client().get_lists()
    logger.debug(json.dumps(lists, default=vars))
    for x in lists:
        print("%d %s %s %d" % (x.id, x.title, x.description, x.namespace_id))


def print_labels():
    labels = get_client().get_labels()
    logger.debug(json.dumps(labels, default=vars))
    for x in labels:
        print("%d %s %s" % (x.id, x.title, x.description))


def add_list(namespace_id, line):
    namespace_id = namespace_id or get_client().get_namespaces()[0].id
    get_client().put_list(namespace_id, line)


def add_task(list_id, line):
    list_id = list_id or get_client().get_lists()[0].id
    get_client().put_task(list_id, line)


def _get_tasks(day_start, day_end, list_name):
    start = get_max_time(day_start) if day_start else None
    end = get_max_time(day_end) if day_end else None

    raw_tasks = get_client().get_tasks(exclude_completed=True)

    filtered_tasks = [PrintableTask(x) for x in raw_tasks if is_in(x, list_name, start, end)]
    filtered_tasks.sort(key=lambda x: ((x.due_date or datetime.max),
                                       -x.priority,
                                       x.list_name().upper(),
                                       x.title.upper()))
    return filtered_tasks


def get_max_time(day='today'):
    timest = pdt.Calendar().parse(day)[0]
    now = datetime.fromtimestamp(mktime(timest), tz.tzlocal())
    daystart = datetime(now.year, now.month, now.day, tzinfo=now.tzinfo)
    dayend = daystart + timedelta(days=1)
    utc_dayend = dayend.isoformat()
    return utc_dayend


def is_in(item, list_name, start_date, end_date):
    if ((not item.due_date and not start_date and not end_date)
        or (item.due_date and end_date and item.due_date < end_date)
        and (not start_date or (item.due_date and item.due_date > start_date))):
        return True
    else:
        return False


def print_tasks(tasks, priority_level_sort=False):
    if not tasks:
        print("No tasks found. Go home early!")
    if priority_level_sort:
        tasks_by_prio = defaultdict(list)
        for task in tasks:
            tasks_by_prio[task.urgency()].append(task)
        for prio, items in tasks_by_prio.items():
            print()
            print_task_list(tasks, items)
    else:
        print_task_list(tasks, tasks)


def print_task_list(tasks, items):
    for item in items:
        print(f"{str(tasks.index(item) + 1):3}" + " " + item.representation())
