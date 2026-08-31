import dataclasses
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from vja import VjaError
from vja.parse import html2text, parse_json_date

ID_TITLE = "id={},title={}"


def required_fields(json: dict):
    """Returns a reader for mandatory api response fields."""

    def read(*path: str) -> Any:
        value = json
        for key in path:
            if not isinstance(value, dict) or key not in value:
                msg = (
                    f"Field '{'.'.join(path)}' is missing in the api response. "
                    "Please check whether your Vikunja server version is supported."
                )
                raise VjaError(msg)
            value = value[key]
        return value

    return read


def custom_output(cls):
    hidden_attribute_names = ["json", "description_text"]

    def __str__(self) -> str:
        """Returns a string containing only the non-null attribute values, excluding hidden attributes ."""
        return "\n".join(
            f"{attribute.name}: {_str_value(getattr(self, attribute.name))}"
            for attribute in dataclasses.fields(self)
            if attribute.name not in hidden_attribute_names
            and getattr(self, attribute.name)
        )

    def _str_value(v):
        if isinstance(v, datetime):
            return v.strftime("%a %Y-%m-%d %H:%M:%S")
        if hasattr(v, "short_str"):
            return v.short_str()
        if isinstance(v, list):
            return [_str_value(x) for x in v]
        return str(v)

    cls.__str__ = __str__
    return cls


def data_dict(cls):
    def data_dict_function(self):
        return {k: _transform_value(v) for k, v in self.__dict__.items() if k != "json"}

    def _transform_value(v):
        if isinstance(v, datetime):
            return v.isoformat()
        if _is_data_dict(v):
            return v.data_dict()
        if isinstance(v, list):
            return [_transform_value(x) for x in v]
        return v

    def _is_data_dict(v):
        return hasattr(v, "data_dict") and callable(v.data_dict)

    cls.data_dict = data_dict_function
    return cls


@dataclass(frozen=True)
@data_dict
class User:
    json: dict = field(repr=False, compare=False, hash=False)
    id: int
    username: str
    name: str
    default_project_id: int

    @classmethod
    def from_json(cls, json: dict) -> "User":
        read = required_fields(json)
        return cls(
            json=json,
            id=read("id"),
            username=read("username"),
            name=read("name"),
            default_project_id=read("settings", "default_project_id"),
        )


@dataclass
@data_dict
# pylint: disable=too-many-instance-attributes
class ProjectView:
    json: dict = field(repr=False, compare=False)
    id: int
    title: str
    project_id: int
    view_kind: str  # The kind of this view. Can be list, gantt, table or kanban.
    bucket_configuration_mode: str  # Can be none, manual or filter. manual
    default_bucket_id: int
    done_bucket_id: int

    @classmethod
    def from_json(cls, json: dict) -> "ProjectView":
        read = required_fields(json)
        return cls(
            json=json,
            id=read("id"),
            title=read("title"),
            project_id=read("project_id"),
            view_kind=read("view_kind"),
            bucket_configuration_mode=read("bucket_configuration_mode"),
            default_bucket_id=read("default_bucket_id"),
            done_bucket_id=read("done_bucket_id"),
        )

    @classmethod
    def from_json_array(cls, json_array: list[dict] | None) -> list["ProjectView"]:
        return [ProjectView.from_json(x) for x in json_array or []]

    def short_str(self) -> str:
        return ID_TITLE.format(self.id, self.title)


@dataclass
@custom_output
@data_dict
# pylint: disable=too-many-instance-attributes
class Project:
    json: dict = field(repr=False, compare=False)
    id: int
    title: str
    description: str
    is_favorite: bool
    is_archived: bool
    parent_project_id: int
    ancestor_projects: list["Project"]
    views: list["ProjectView"]

    @classmethod
    def from_json(cls, json: dict, ancestor_projects: list["Project"]) -> "Project":
        read = required_fields(json)
        return cls(
            json=json,
            id=read("id"),
            title=read("title"),
            description=read("description"),
            is_favorite=read("is_favorite"),
            is_archived=read("is_archived"),
            parent_project_id=json.get("parent_project_id", 0),
            ancestor_projects=ancestor_projects,
            views=ProjectView.from_json_array(read("views")),
        )

    @classmethod
    def from_json_array(
        cls, json_array: list[dict] | None, ancestor_projects: list["Project"]
    ) -> list["Project"]:
        return [Project.from_json(x, ancestor_projects) for x in json_array or []]

    def get_first_kanban_project_view(self) -> "ProjectView":
        view = next((x for x in self.views if x.view_kind == "kanban"), None)
        if not view:
            raise VjaError(f"Project '{self.title}' has no kanban view.")
        return view

    def short_str(self) -> str:
        return ID_TITLE.format(self.id, self.title)


@dataclass(frozen=True)
@data_dict
class Bucket:
    json: dict = field(repr=False, compare=False, hash=False)
    id: int
    title: str
    limit: int
    position: int
    count_tasks: int

    @classmethod
    def from_json(cls, json: dict) -> "Bucket":
        read = required_fields(json)
        return cls(
            json=json,
            id=read("id"),
            title=read("title"),
            limit=read("limit"),
            position=read("position"),
            count_tasks=read("count"),
        )

    @classmethod
    def from_json_array(cls, json_array: list[dict] | None) -> list["Bucket"]:
        return [Bucket.from_json(x) for x in json_array or []]


@dataclass(frozen=True)
@data_dict
class Label:
    json: dict = field(repr=False, compare=False, hash=False)
    id: int
    title: str

    @classmethod
    def from_json(cls, json: dict) -> "Label":
        read = required_fields(json)
        return cls(json=json, id=read("id"), title=read("title"))

    @classmethod
    def from_json_array(cls, json_array: list[dict] | None) -> list["Label"]:
        return [Label.from_json(x) for x in json_array or []]

    def short_str(self) -> str:
        return ID_TITLE.format(self.id, self.title)


@dataclass(frozen=True)
@data_dict
class Assignee:
    json: dict = field(repr=False, compare=False, hash=False)
    id: int
    username: str
    name: str

    @classmethod
    def from_json(cls, json: dict) -> "Assignee":
        read = required_fields(json)
        return cls(
            json=json,
            id=read("id"),
            username=read("username"),
            name=json.get("name", ""),
        )

    @classmethod
    def from_json_array(cls, json_array: list[dict] | None) -> list["Assignee"]:
        return [Assignee.from_json(x) for x in json_array or []]

    def short_str(self) -> str:
        return f"id={self.id},username={self.username}"


@dataclass(frozen=True)
@data_dict
class TaskBucket:
    json: dict = field(repr=False, compare=False, hash=False)
    id: int
    project_view_id: int
    title: str

    @classmethod
    def from_json(cls, json: dict) -> "TaskBucket":
        read = required_fields(json)
        return cls(
            json=json,
            id=read("id"),
            project_view_id=read("project_view_id"),
            title=read("title"),
        )

    @classmethod
    def from_json_array(cls, json_array: list[dict] | None) -> list["TaskBucket"]:
        return [TaskBucket.from_json(x) for x in json_array or []]

    def short_str(self) -> str:
        return f"id={self.id},project_view_id={self.project_view_id},title={self.title}"


@dataclass
@custom_output
@data_dict
class TaskReminder:
    json: dict = field(repr=False, compare=False)
    reminder: datetime | None
    relative_period: int
    relative_to: str

    @classmethod
    def from_json(cls, json: dict) -> "TaskReminder":
        read = required_fields(json)
        return cls(
            json=json,
            reminder=parse_json_date(read("reminder")),
            relative_period=read("relative_period"),
            relative_to=read("relative_to"),
        )

    @classmethod
    def from_json_array(cls, json_array: list[dict] | None) -> list["TaskReminder"]:
        return [TaskReminder.from_json(x) for x in json_array or []]

    def short_str(self) -> str:
        return (
            f'reminder={self.reminder.isoformat() if self.reminder else " "},'
            f"period={self.relative_period},"
            f"relative_to={self.relative_to}"
        )


RELATION_KINDS = (
    "subtask",
    "parenttask",
    "related",
    "duplicateof",
    "duplicates",
    "blocking",
    "blocked",
    "precedes",
    "follows",
    "copiedfrom",
    "copiedto",
)


@dataclass(frozen=True)
@data_dict
class TaskRelation:
    json: dict = field(repr=False, compare=False, hash=False)
    kind: str
    other_task_id: int
    other_task_title: str

    @classmethod
    def from_json_map(cls, related_tasks: dict | None) -> list["TaskRelation"]:
        return [
            cls.from_json(kind, task_json)
            for kind, tasks in (related_tasks or {}).items()
            for task_json in tasks or []
        ]

    @classmethod
    def from_json(cls, kind: str, json: dict) -> "TaskRelation":
        read = required_fields(json)
        return cls(
            json=json,
            kind=kind,
            other_task_id=read("id"),
            other_task_title=read("title"),
        )

    def short_str(self) -> str:
        return (
            f"{self.kind}: {ID_TITLE.format(self.other_task_id, self.other_task_title)}"
        )


@dataclass
@custom_output
@data_dict
# pylint: disable=too-many-instance-attributes
class Task:
    json: dict = field(repr=False, compare=False)
    id: int
    title: str
    description: str
    description_text: str
    priority: int
    is_favorite: bool
    due_date: datetime | None
    reminders: list[TaskReminder]
    repeat_mode: int
    repeat_after: timedelta
    start_date: datetime | None
    end_date: datetime | None
    percent_done: float
    done: bool
    done_at: datetime | None
    label_objects: list[Label]
    assignee_objects: list[Assignee]
    relations: list[TaskRelation]
    project: Project
    position: int
    bucket_objects: list[TaskBucket]
    created: datetime | None
    updated: datetime | None
    urgency: float = field(init=False, compare=False, default=0.0)

    @property
    def labels(self) -> str:
        return ",".join(label.title for label in self.label_objects)

    @property
    def assignees(self) -> str:
        return ",".join(a.username for a in self.assignee_objects)

    @property
    def buckets(self) -> str:
        return ",".join(b.title for b in self.bucket_objects)

    @classmethod
    def from_json(
        cls,
        json: dict,
        project_object: Project,
    ) -> "Task":
        read = required_fields(json)
        description = read("description")
        return cls(
            json=json,
            id=read("id"),
            title=read("title"),
            description=description,
            description_text=html2text(description),
            priority=read("priority"),
            is_favorite=read("is_favorite"),
            due_date=parse_json_date(read("due_date")),
            reminders=TaskReminder.from_json_array(read("reminders")),
            repeat_mode=read("repeat_mode"),
            repeat_after=timedelta(seconds=read("repeat_after")),
            start_date=parse_json_date(read("start_date")),
            end_date=parse_json_date(read("end_date")),
            percent_done=read("percent_done"),
            done=read("done"),
            done_at=parse_json_date(read("done_at")),
            label_objects=Label.from_json_array(read("labels")),
            assignee_objects=Assignee.from_json_array(read("assignees")),
            relations=TaskRelation.from_json_map(read("related_tasks")),
            project=project_object,
            position=read("position"),
            bucket_objects=TaskBucket.from_json_array(json.get("buckets", [])),
            created=parse_json_date(read("created")),
            updated=parse_json_date(read("updated")),
        )

    def has_label(self, label: Label) -> bool:
        return any(x.id == label.id for x in self.label_objects)

    def has_assignee(self, assignee: Assignee) -> bool:
        return any(x.id == assignee.id for x in self.assignee_objects)
