import dataclasses
import typing
from dataclasses import dataclass, field
from datetime import datetime

import dateutil.parser


def custom_output(cls):  # Decorator for class.
    def __str__(self):
        """Returns a string containing only the non-default attribute values."""
        s = '\n'.join(f'{attribute.name}: {getattr(self, attribute.name)}'
                      for attribute in dataclasses.fields(self)
                      if attribute.name != 'json' and getattr(self, attribute.name))
        return f'{s}'

    setattr(cls, '__str__', __str__)
    return cls


def data_dict(cls):  # Decorator for class.
    def data_dict_function(self):
        return {k: _transform_value(v) for k, v in self.__dict__.items() if k != 'json'}

    def _transform_value(v):
        if _is_data_dict(v):
            return v.data_dict()
        if isinstance(v, list):
            return [_transform_value(x) for x in v]
        return v

    def _is_data_dict(v):
        return hasattr(v, 'data_dict') and callable(v.data_dict)

    setattr(cls, 'data_dict', data_dict_function)
    return cls


@dataclass(frozen=True)
@data_dict
class User:
    json: dict = field(repr=False)
    id: int
    username: str
    name: str
    default_list_id: int

    @classmethod
    def from_json(cls, json):
        return cls(json, json['id'], json['name'], json['username'], json['settings']['default_list_id'])

    def output(self):
        return f'{self.id:5} {self.username:15.15} {self.name:15.15} {self.default_list_id:5}'


@dataclass(frozen=True)
@data_dict
class Namespace:
    json: dict = field(repr=False)
    id: int
    title: str
    description: str
    is_archived: bool

    @classmethod
    def from_json(cls, json):
        return cls(json, json['id'], json['title'], json['description'], json['is_archived'])

    @classmethod
    def from_json_array(cls, json_array):
        return [Namespace.from_json(x) for x in json_array or []]

    def output(self):
        return f'{self.id:5} {self.title:15.15} {self.description:20.20}'


@dataclass(frozen=True)
@data_dict
class List:
    json: dict = field(repr=False)
    id: int
    title: str
    description: str
    is_favorite: bool
    is_archived: bool
    namespace: Namespace

    @classmethod
    def from_json(cls, json, namespace):
        return cls(json, json['id'], json['title'], json['description'], json['is_archived'], json['is_favorite'],
                   namespace)

    @classmethod
    def from_json_array(cls, json_array, namespace):
        return [List.from_json(x, namespace) for x in json_array or []]

    def output(self):
        namespace_title = self.namespace.title if self.namespace else ''
        namespace_id = self.namespace.id if self.namespace else 0
        return f'{self.id:5} {self.title:15.15} {self.description:20.20} {namespace_title:15.15}  {namespace_id:5}'


@dataclass(frozen=True)
@data_dict
class Bucket:
    json: dict = field(repr=False)
    id: int
    title: str
    is_done_bucket: bool
    limit: int
    position: int
    count_tasks: int

    @classmethod
    def from_json(cls, json):
        return cls(json, json['id'], json['title'],
                   json['is_done_bucket'],
                   json['limit'],
                   json['position'],
                   len(json['tasks']) if json['tasks'] else 0)

    @classmethod
    def from_json_array(cls, json_array):
        return [Bucket.from_json(x) for x in json_array or []]

    def output(self):
        return f'{self.id:5} {self.title:15.15} {self.is_done_bucket:2} {self.limit:3} {self.count_tasks:5}'


@dataclass(frozen=True)
@data_dict
class Label:
    json: dict = field(repr=False)
    id: int
    title: str

    @classmethod
    def from_json(cls, json):
        return cls(json, json['id'], json['title'])

    @classmethod
    def from_json_array(cls, json_array):
        return [Label.from_json(x) for x in json_array or []]

    def output(self):
        return f'{self.id:5} {self.title:15.15}'


@dataclass(frozen=True)
@custom_output
@data_dict
# pylint: disable=too-many-instance-attributes
class Task:
    json: dict = field(repr=False)
    id: int
    title: str
    description: str
    priority: int
    is_favorite: bool
    due_date: datetime
    created: datetime
    updated: datetime
    reminder_dates: typing.List[datetime]
    done: bool
    tasklist: List
    position: int
    bucket_id: int
    kanban_position: int
    labels: typing.List[Label]

    @classmethod
    def from_json(cls, json, list_object, labels):
        return cls(json, json['id'], json['title'], json['description'],
                   json['priority'],
                   json['is_favorite'],
                   _date_from_json(json['due_date']),
                   _date_from_json(json['created']),
                   _date_from_json(json['updated']),
                   [_date_from_json(reminder) for reminder in json['reminder_dates'] or []],
                   json['done'],
                   list_object,
                   json['position'],
                   json['bucket_id'],
                   json['kanban_position'],
                   labels
                   )

    def output(self):
        output = [f'{self.id:5}',
                  f'({self.priority})',
                  f'{"*"}' if self.is_favorite else ' ',
                  f'{self.title:50.50}',
                  f'{format_date(self.due_date) :15.15}',
                  f'{"R" if self.reminder_dates else "" :1}',
                  f'{self.tasklist.namespace.title if self.tasklist and self.tasklist.namespace else "":15.15}',
                  f'{self.tasklist.title if self.tasklist else "":15.15}',
                  f'{",".join(map(lambda label: label.title, self.labels or [])) :20.20}',
                  f'{Urgency.compute(self):3}']
        return ' '.join(output)

    def has_label(self, label):
        return any(x.id == label.id for x in self.labels)


urgency_score_coefficients = {'due_date': 1.0, 'priority': 1.0, 'favorite': 1.0, 'list_keyword': 1.0,
                              'label_keyword': 1.0}


class Urgency:

    @staticmethod
    def compute(task: Task):
        if task.done:
            return 0
        due_date_score = Urgency.get_due_date_score(task) * urgency_score_coefficients['due_date']
        priority_score = task.priority * urgency_score_coefficients['priority']
        favorite_score = int(task.is_favorite) * urgency_score_coefficients['favorite']
        list_name_score = int('next' in task.tasklist.title.lower()) * urgency_score_coefficients['list_keyword']
        lable_name_score = int(any('next' in label.title.lower()
                                   for label in task.labels)) * urgency_score_coefficients['label_keyword']

        return 1 + due_date_score + priority_score + favorite_score + list_name_score + lable_name_score

    @staticmethod
    def get_due_date_score(task):
        if task.due_date:
            due_days = (task.due_date - datetime.today()).days
            if due_days < 0:
                result = 6
            elif due_days == 0:
                result = 5
            elif due_days == 1:
                result = 4
            elif 1 < due_days <= 2:
                result = 3
            elif 2 < due_days <= 5:
                result = 2
            elif 5 < due_days <= 10:
                result = 1
            elif due_days > 10:
                result = -1
            else:
                result = 0
        else:
            result = 0
        return result


def _date_from_json(json_date):
    if json_date and json_date > '0001-01-01T00:00:00Z':
        return dateutil.parser.isoparse(json_date).replace(tzinfo=None)
    return None


def format_date(timestamp):
    return timestamp.strftime('%a %d.%m %H:%M') if timestamp else ''
