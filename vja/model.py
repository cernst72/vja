import dataclasses
import typing
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from vja.parse import parse_json_date


def custom_output(cls):
    def str_function(self):
        """Returns a string containing only the non-null attribute values, excluding json attribute ."""
        return '\n'.join(f'{attribute.name}: {_str_value(getattr(self, attribute.name))}'
                         for attribute in dataclasses.fields(self)
                         if attribute.name != 'json' and getattr(self, attribute.name))

    def _str_value(attribute_value):
        if isinstance(attribute_value, datetime):
            return attribute_value.isoformat()
        if isinstance(attribute_value, list):
            return [_str_value(x) for x in attribute_value]
        return str(attribute_value)

    setattr(cls, '__str__', str_function)
    return cls


def data_dict(cls):
    def data_dict_function(self):
        return {k: _transform_value(v) for k, v in self.__dict__.items() if k != 'json'}

    def _transform_value(v):
        if isinstance(v, datetime):
            return v.isoformat()
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
    default_project_id: int

    @classmethod
    def from_json(cls, json):
        return cls(json, json['id'], json['username'], json['name'], json['settings']['default_project_id'])


@dataclass
@data_dict
# pylint: disable=too-many-instance-attributes
class Project:
    json: dict = field(repr=False)
    id: int
    title: str
    description: str
    is_favorite: bool
    is_archived: bool
    default_bucket_id: int
    done_bucket_id: int
    parent_project_id: int
    ancestor_projects: typing.List['Project']

    @classmethod
    def from_json(cls, json, ancestor_projects):
        return cls(json, json['id'], json['title'], json['description'], json['is_archived'], json['is_favorite'],
                   json['default_bucket_id'], json['done_bucket_id'],
                   json['parent_project_id'],
                   ancestor_projects)

    @classmethod
    def from_json_array(cls, json_array, ancestor_projects):
        return [Project.from_json(x, ancestor_projects) for x in json_array or []]


@dataclass(frozen=True)
@data_dict
class Bucket:
    json: dict = field(repr=False)
    id: int
    title: str
    limit: int
    position: int
    count_tasks: int

    @classmethod
    def from_json(cls, json):
        return cls(json, json['id'], json['title'],
                   json['limit'],
                   json['position'],
                   json['count'])

    @classmethod
    def from_json_array(cls, json_array):
        return [Bucket.from_json(x) for x in json_array or []]


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


@dataclass
@custom_output
@data_dict
# pylint: disable=too-many-instance-attributes
class TaskReminder:
    json: dict = field(repr=False)
    reminder: datetime
    relative_period: int
    relative_to: str

    @classmethod
    def from_json(cls, json):
        return cls(json, parse_json_date(json['reminder']), json['relative_period'], json['relative_to'])

    @classmethod
    def from_json_array(cls, json_array):
        return [TaskReminder.from_json(x) for x in json_array or []]


@dataclass
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
    reminders: typing.List[TaskReminder]
    repeat_mode: int
    repeat_after: timedelta
    start_date: datetime
    end_date: datetime
    percent_done: float
    done: bool
    done_at: datetime
    label_objects: typing.List[Label]
    project: Project
    position: int
    bucket_id: int
    kanban_position: int
    created: datetime
    updated: datetime
    urgency: float = field(init=False)

    @property
    def labels(self):
        return ",".join(map(lambda label: label.title, self.label_objects or []))

    @classmethod
    def from_json(cls, json, project_object, labels):
        return cls(json, json['id'], json['title'], json['description'],
                   json['priority'],
                   json['is_favorite'],
                   parse_json_date(json['due_date']),
                   TaskReminder.from_json_array(json["reminders"]),
                   json['repeat_mode'],
                   timedelta(seconds=json['repeat_after']),
                   parse_json_date(json['start_date']),
                   parse_json_date(json['end_date']),
                   json['percent_done'],
                   json['done'],
                   parse_json_date(json['done_at']),
                   labels,
                   project_object,
                   json['position'],
                   json['bucket_id'],
                   json['kanban_position'],
                   parse_json_date(json['created']),
                   parse_json_date(json['updated'])
                   )

    def has_label(self, label):
        return any(x.id == label.id for x in self.label_objects)
