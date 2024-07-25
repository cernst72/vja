import dataclasses
import typing
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from vja.parse import parse_json_date


def custom_output(cls):
    def __str__(self):
        """Returns a string containing only the non-null attribute values, excluding json attribute ."""
        return '\n'.join(f'{attribute.name}: {_str_value(getattr(self, attribute.name))}'
                         for attribute in dataclasses.fields(self)
                         if attribute.name != 'json' and getattr(self, attribute.name))

    def _str_value(v):
        if isinstance(v, datetime):
            return v.isoformat()
        if isinstance(v, (Project, ProjectView, Label, TaskReminder)):
            return v.short_str()
        if isinstance(v, list):
            return [_str_value(x) for x in v]
        return str(v)

    setattr(cls, '__str__', __str__)
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
class ProjectView:
    json: dict = field(repr=False)
    id: int
    title: str
    project_id: int
    view_kind: str  # The kind of this view. Can be list, gantt, table or kanban.
    bucket_configuration_mode: str  # Can be none, manual or filter. manual
    default_bucket_id: int
    done_bucket_id: int

    @classmethod
    def from_json(cls, json):
        return cls(json, json['id'], json['title'],
                   json['project_id'],
                   json['view_kind'],
                   json['bucket_configuration_mode'],
                   json['default_bucket_id'],
                   json['done_bucket_id'])

    @classmethod
    def from_json_array(cls, json_array):
        return [ProjectView.from_json(x) for x in json_array or []]

    def short_str(self):
        return 'id=' + str(self.id) + ',title=' + self.title


@dataclass
@custom_output
@data_dict
# pylint: disable=too-many-instance-attributes
class Project:
    json: dict = field(repr=False)
    id: int
    title: str
    description: str
    is_favorite: bool
    is_archived: bool
    parent_project_id: int
    ancestor_projects: typing.List['Project']
    views: typing.List[ProjectView]

    @classmethod
    def from_json(cls, json, ancestor_projects):
        return cls(json, json['id'], json['title'], json['description'],
                   json['is_favorite'], json['is_archived'],
                   json['parent_project_id'],
                   ancestor_projects,
                   ProjectView.from_json_array(json['views']))

    @classmethod
    def from_json_array(cls, json_array, ancestor_projects):
        return [Project.from_json(x, ancestor_projects) for x in json_array or []]

    def get_first_kanban_project_view(self):
        return next(x for x in self.views if x.view_kind == "kanban")

    def short_str(self):
        return 'id=' + str(self.id) + ',title=' + self.title


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

    def short_str(self):
        return 'id=' + str(self.id) + ',title=' + self.title


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

    def short_str(self):
        return 'reminder=' + self.reminder.isoformat() + ',relative_to=' + self.relative_to


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
                   parse_json_date(json['created']),
                   parse_json_date(json['updated'])
                   )

    def has_label(self, label):
        return any(x.id == label.id for x in self.label_objects)
