import typing
from dataclasses import dataclass, field
from datetime import datetime

import dateutil.parser


@dataclass(frozen=True)
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

    def data_dict(self):
        return {k: v.data_dict() if hasattr(v, 'data_dict') and callable(v.data_dict) else v
                for k, v in self.__dict__.items() if k != 'json'}

    def output(self):
        return f'{self.id:5} {self.title:15.15} {self.description:20.20}'


@dataclass(frozen=True)
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

    def data_dict(self):
        return {k: v.data_dict() if hasattr(v, 'data_dict') and callable(v.data_dict) else v
                for k, v in self.__dict__.items() if k != 'json'}

    def output(self):
        namespace_title = self.namespace.title if self.namespace else ''
        namespace_id = self.namespace.id if self.namespace else 0
        return f'{self.id:5} {self.title:15.15} {self.description:20.20} {namespace_title:15.15}  {namespace_id:5}'


@dataclass(frozen=True)
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

    def data_dict(self):
        return {k: v.data_dict() if hasattr(v, 'data_dict') and callable(v.data_dict) else v
                for k, v in self.__dict__.items() if k != 'json'}

    def output(self):
        return f'{self.id:5} {self.title:15.15}'


@dataclass(frozen=True)
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
    reminder_dates: typing.List[str]
    done: bool
    tasklist: List
    labels: typing.List[Label]

    @classmethod
    def from_json(cls, json, list_object, labels):
        return cls(json, json['id'], json['title'], json['description'],
                   json['priority'],
                   json['is_favorite'],
                   _date_from_json(json['due_date']),
                   _date_from_json(json['created']),
                   _date_from_json(json['updated']),
                   json['reminder_dates'],
                   json['done'],
                   list_object,
                   labels
                   )

    def data_dict(self):
        return {k: v.data_dict() if hasattr(v, 'data_dict') and callable(v.data_dict) else v
                for k, v in self.__dict__.items() if k != 'json'}

    def output(self):
        from vja.urgency import Urgency
        output = [f'{self.id:5}',
                  f'({self.priority})',
                  f'{"*"}' if self.is_favorite else ' ',
                  f'{self.title:50.50}',
                  f'{format_date(self.due_date) :15.15}',
                  f'{"R" if self.reminder_dates else "" :1}',
                  f'{self.tasklist.namespace.title:15.15}',
                  f'{self.tasklist.title:15.15}',
                  f'{",".join(map(lambda label: label.title, self.labels or [])) :20.20}',
                  f'{Urgency.compute(self):3}']
        return ' '.join(output)

    def has_label(self, label):
        return any(x.id == label.id for x in self.labels)


def _date_from_json(json_date):
    if json_date and json_date > '0001-01-01T00:00:00Z':
        return dateutil.parser.isoparse(json_date).replace(tzinfo=None)
    return None


def format_date(timestamp):
    return timestamp.strftime('%a %d.%m %H:%M') if timestamp else ''
