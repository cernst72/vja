from datetime import datetime

from vja.login import get_client


def format_date(timestamp):
    return timestamp.strftime("%a %d.%m") if timestamp else ""


def format_time(timestamp):
    return timestamp.strftime("%H:%M") if timestamp else ""


class PrintableTask:
    def __init__(self, task):
        self.id = task.id
        self.title = task.title
        self.priority = task.priority
        self.is_favorite = task.is_favorite

        self.due_date = None
        if task.due_date and task.due_date > "0001-01-01T00:00:00Z":
            self.due_date = datetime.fromisoformat(
                task.due_date.replace("Z", "")
            ).replace(tzinfo=None)

        self.list_id = task.list_id
        self.label_ids = []
        if task.labels:
            self.label_ids = [x.id for x in task.labels]

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
        if "next" in self.list_name().lower() or "next" in " ".join(self.label_names()).lower():
            statuspoints = 1
        return 2 + statuspoints + datepoints + int(self.priority) + (1 if self.is_favorite else 0)

    def due_date_format(self):
        return format_date(self.due_date)

    def due_time_format(self):
        return format_time(self.due_date)

    def _list(self):
        list_dict = {x.id: x for x in get_client().get_lists()}
        return list_dict.get(self.list_id)

    def list_name(self):
        return self._list().title

    def namespace_name(self):
        namespaces_dict = {x.id: x for x in get_client().get_namespaces()}
        namespace = namespaces_dict.get(self._list().namespace_id)
        return namespace.title

    def label_names(self):
        all_labels = get_client().get_labels() or []
        label_dict = {x.id: x for x in all_labels}
        label_names = [str(label_dict.get(x).title) for x in self.label_ids]
        return " ".join(label_names)

    def representation(self):
        output = [f"{self.id:4}",
                  "(%s)" % self.priority,
                  "%s" % "*" if self.is_favorite else " ",
                  f"{self.title:50.50}",
                  f"{self.due_date_format():9.9}",
                  f"{self.due_time_format():5.5}",
                  f"{self.namespace_name():15.15}",
                  f"{self.list_name():15.15}",
                  f"{self.label_names():15.15}",
                  f"{self.urgency():3}"]
        return " ".join(output)
