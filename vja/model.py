import typing
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Namespace:
    json: dict = field(repr=False)
    id: int
    title: str
    description: str

    @classmethod
    def from_json(cls, json):
        return cls(json, json['id'], json['title'], json['description'])

    def output(self):
        return f'{self.id:d} {self.title} {self.description}'


@dataclass(frozen=True)
class List:
    json: dict = field(repr=False)
    id: int
    title: str
    description: str
    is_favorite: bool
    namespace: Namespace

    @classmethod
    def from_json(cls, json, namespace):
        return cls(json, json['id'], json['title'], json['description'], json['is_favorite'], namespace)

    def output(self):
        namespace_id = self.namespace.id if self.namespace else 0
        return f'{self.id:d} {self.title} {self.description} {namespace_id:d}'

    def has_higher_priority(self):
        return 'next' in self.title.lower()


@dataclass(frozen=True)
class Label:
    json: dict = field(repr=False)
    id: int
    title: str

    @classmethod
    def from_json(cls, json):
        return cls(json, json['id'], json['title'])

    def output(self):
        return f'{self.id:d} {self.title}'

    def has_higher_priority(self):
        return 'next' in self.title.lower()


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

    def urgency(self):
        today = datetime.today()
        if self.due_date:
            duedate = self.due_date
            datediff = (duedate - today).days
            if datediff < 0:
                datepoints = 6
            elif datediff == 0:
                datepoints = 5
            elif datediff == 1:
                datepoints = 4
            elif 1 < datediff <= 2:
                datepoints = 3
            elif 2 < datediff <= 5:
                datepoints = 3
            elif 5 < datediff <= 10:
                datepoints = 1
            elif datediff > 10:
                datepoints = -1
            else:
                datepoints = 0
        else:
            datepoints = 0
        statuspoints = 0
        if self.tasklist.has_higher_priority() or any(label.has_higher_priority() for label in self.labels):
            statuspoints = 1
        return 2 + statuspoints + datepoints + int(self.priority) + (1 if self.is_favorite else 0)

    def representation(self):
        output = [f'{self.id:4}',
                  f'({self.priority})',
                  f'{"*"}' if self.is_favorite else ' ',
                  f'{self.title:50.50}',
                  f'{format_date(self.due_date) :9.9}',
                  f'{format_time(self.due_date) :5.5}',
                  f'{self.tasklist.namespace.title:15.15}',
                  f'{self.tasklist.title:15.15}',
                  f'{" ".join(map(lambda label: label.title, self.labels or [])) :15.15}',
                  f'{self.urgency():3}']
        return ' '.join(output)


def _date_from_json(json_date):
    if json_date and json_date > '0001-01-01T00:00:00Z':
        return datetime.fromisoformat(json_date.replace("Z", "")).replace(tzinfo=None)
    return None


def format_date(timestamp):
    return timestamp.strftime('%a %d.%m') if timestamp else ''


def format_time(timestamp):
    return timestamp.strftime('%H:%M') if timestamp else ''
