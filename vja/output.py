import json
import logging

import click

from vja.model import User, List, Task

NAMESPACE_LIST_FORMAT_DEFAULT = '{x.id:5} {x.title:20.20} {x.description:20.20}'

LIST_LIST_FORMAT_DEFAULT = '{x.id:5} {x.title:20.20} {x.description:20.20}  ' \
                           '{x.namespace.title:20.20} {x.namespace.id:5}'

BUCKET_LIST_FORMAT_DEFAULT = '{x.id:5} {x.title:20.20} {x.is_done_bucket:2} {x.limit:3} {x.count_tasks:5}'

LABEL_LIST_FORMAT_DEFAULT = '{x.id:5} {x.title:20.20}'

TASK_LIST_FORMAT_DEFAULT = '{x.id:5} ({x.priority}) {"*" if x.is_favorite else " "} {x.title:50.50} ' \
                           '{x.due_date.strftime("%a %d.%m %H:%M") if x.due_date else "":15.15} ' \
                           '{"R" if x.reminder_dates else " "} {x.tasklist.title:20.20} ' \
                           '{x.label_titles:20.20} {x.urgency:3.1f}'

logger = logging.getLogger(__name__)


class Output:

    def user(self, user: User, is_json, is_jsonvja):
        self._dump(user, is_json, is_jsonvja)

    def list(self, task_list: List, is_json, is_jsonvja):
        self._dump(task_list, is_json, is_jsonvja)

    def task(self, task: Task, is_json, is_jsonvja):
        self._dump(task, is_json, is_jsonvja)

    def namespace_array(self, object_array, is_json, is_jsonvja, custom_format=None):
        line_format = custom_format or NAMESPACE_LIST_FORMAT_DEFAULT
        self._dump_array(object_array, line_format, is_json, is_jsonvja)

    def list_array(self, object_array, is_json, is_jsonvja, custom_format=None):
        line_format = custom_format or LIST_LIST_FORMAT_DEFAULT
        self._dump_array(object_array, line_format, is_json, is_jsonvja)

    def bucket_array(self, object_array, is_json, is_jsonvja, custom_format=None):
        line_format = custom_format or BUCKET_LIST_FORMAT_DEFAULT
        self._dump_array(object_array, line_format, is_json, is_jsonvja)

    def label_array(self, object_array, is_json, is_jsonvja, custom_format=None):
        line_format = custom_format or LABEL_LIST_FORMAT_DEFAULT
        self._dump_array(object_array, line_format, is_json, is_jsonvja)

    def task_array(self, object_array, is_json, is_jsonvja, custom_format=None):
        line_format = custom_format or TASK_LIST_FORMAT_DEFAULT
        self._dump_array(object_array, line_format, is_json, is_jsonvja)

    @staticmethod
    def _dump(element, is_json, is_jsonvja):
        if is_json:
            click.echo(json.dumps(element.json))
        elif is_jsonvja:
            click.echo(json.dumps(element.data_dict(), default=str))
        else:
            click.echo(element)

    @staticmethod
    def _dump_array(object_array, line_format, is_json, is_jsonvja):
        if is_json:
            click.echo(json.dumps([x.json for x in object_array]))
        elif is_jsonvja:
            click.echo(json.dumps([x.data_dict() for x in object_array], default=str))
        else:
            for x in object_array:
                # https://stackoverflow.com/a/53671539/2935741
                # Note: Using eval() is risky, because arbitrary code may be introduced via the configured formatting
                # templates.
                # Do not use custom templates, if you are unsure what you are doing.
                click.echo(eval(f"f'{line_format}'"))
