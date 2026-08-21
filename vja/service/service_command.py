import datetime
import logging

from vja import VjaError
from vja.adapter.apiclient import ApiClient
from vja.model import Assignee, Bucket, Label, Project, Task
from vja.parse import (
    datetime_to_isoformat,
    parse_date_arg_to_iso,
    parse_date_arg_to_timedelta,
    parse_json_date,
)
from vja.service.project_service import ProjectService
from vja.service.task_service import TaskService

logger = logging.getLogger(__name__)


class CommandService:
    def __init__(
        self,
        project_service: ProjectService,
        task_service: TaskService,
        api_client: ApiClient,
    ):
        self._project_service = project_service
        self._task_service = task_service
        self._api_client = api_client

    def login(self, username, password, totp_passcode):
        self._api_client.authenticate(True, username, password, totp_passcode)

    def logout(self):
        self._api_client.logout()
        logger.info("Logged out")

    # project
    def add_project(self, title: str, parent_project: str) -> Project:
        if parent_project:
            parent_project_id = self._project_service.find_project_by_id_or_title(
                parent_project
            ).id
        else:
            parent_project_id = None
        project_json = self._api_client.create_project(title, parent_project_id)
        return Project.from_json(project_json, [])

    # bucket
    def add_bucket(self, project_query: str, title: str) -> Bucket:
        project = self._project_service.find_project_by_id_or_title(project_query)
        project_view = project.get_first_kanban_project_view()
        bucket_json = self._api_client.create_bucket(project.id, project_view.id, title)
        return Bucket.from_json(bucket_json)

    # label
    def add_label(self, title: str) -> Label:
        label_json = self._api_client.create_label(title)
        return Label.from_json(label_json)

    # tasks
    _arg_to_json = {
        "title": {"field": "title", "mapping": (lambda x: x)},
        "note": {"field": "description", "mapping": (lambda x: x)},
        "prio": {"field": "priority", "mapping": int},
        "due": {"field": "due_date", "mapping": (lambda x: x)},
        "start": {
            "field": "start_date",
            "mapping": parse_date_arg_to_iso,
        },
        "end": {
            "field": "end_date",
            "mapping": parse_date_arg_to_iso,
        },
        "favorite": {"field": "is_favorite", "mapping": bool},
        "completed": {"field": "done", "mapping": bool},
        "position": {"field": "position", "mapping": int},
        "project_id": {"field": "project_id", "mapping": int},
        "bucket_id": {"field": "bucket_id", "mapping": int},
        "kanban_position": {"field": "kanban_position", "mapping": int},
        "reminder": {"field": "reminders", "mapping": (lambda x: x)},
    }

    def _args_to_payload(self, args: dict) -> dict:
        payload = {}
        for arg_name, arg_value in args.items():
            mapper = self._arg_to_json.get(arg_name)
            if mapper is None:
                raise VjaError(f"Unknown argument: {arg_name}")
            payload[mapper["field"]] = mapper["mapping"](arg_value)
        return payload

    def add_task(self, title, args: dict) -> Task:
        args["title"] = title
        if args.get("project_id"):
            project_id = self._project_service.find_project_by_id_or_title(
                args.pop("project_id")
            ).id
        else:
            project_id = self._project_service.get_default_project().id
        label_names = args.pop("label")
        assignee_names = args.pop("assignee")
        is_force = args.pop("force_create", False)
        if (due := args.get("due")) is not None:
            args["due"] = parse_date_arg_to_iso(due)
        if "reminder" in args:
            args["reminder"] = self._build_reminders(args["reminder"])

        if not is_force:
            self._validate_add_task(title, label_names)

        payload = self._args_to_payload(args)
        logger.debug("put task: %s", payload)
        task_json = self._api_client.create_task(project_id, payload)
        task = self._task_service.task_from_json(task_json)

        self._add_labels_to_task(task, label_names, is_force)
        self._add_assignees_to_task(task, assignee_names, project_id)
        return task

    def _add_labels_to_task(self, task: Task, label_names: list[str], is_force: bool):
        for label_name in label_names:
            label = self._label_from_name(label_name, is_force) if label_name else None
            if label:
                self._api_client.add_label_to_task(task.id, label.id)

    def _add_assignees_to_task(self, task: Task, assignee_names: list[str], project_id: int):
        for assignee_name in assignee_names:
            assignee = self._user_from_name(assignee_name, project_id)
            self._api_client.add_assignee_to_task(task.id, assignee.id)

    def clone_task(self, task_id: int, title: str) -> Task:
        task_remote = self._api_client.get_task(task_id)
        task_remote.update({"id": None, "title": title, "position": 0, "bucket_id": 0})

        logger.debug("put task: %s", task_remote)
        task_json = self._api_client.create_task(task_remote["project_id"], task_remote)
        task = self._task_service.task_from_json(task_json)

        for label in task_remote["labels"] or []:
            self._api_client.add_label_to_task(task.id, label["id"])
        for assignee in task_remote["assignees"] or []:
            self._api_client.add_assignee_to_task(task.id, assignee["id"])
        return task

    def edit_task(self, task_id: int, args: dict) -> Task:
        task_remote = self._api_client.get_task(task_id)
        label_name = args.pop("label") if args.get("label") else None
        assignee_name = args.pop("assignee") if args.get("assignee") else None
        is_force = args.pop("force_create", False)

        self._preprocess_edit_args(args, task_remote)
        payload = self._args_to_payload(args)
        logger.debug("update fields: %s", payload)
        task_remote.update(payload)
        logger.debug("post task: %s", task_remote)
        task_json = self._api_client.update_task(task_id, task_remote)
        task_new = self._task_service.task_from_json(task_json)

        self._toggle_label(task_new, label_name, is_force)
        self._toggle_assignee(task_new, assignee_name, int(task_remote["project_id"]))
        return task_new

    def _preprocess_edit_args(self, args: dict, task_remote: dict):
        """Resolve and transform CLI args into API-ready values for task editing."""
        if args.get("due") is not None:
            self._update_due_date(args, task_remote)
        self._update_reminder(args, task_remote)
        # note_append must be consumed before _args_to_payload (it is not in _arg_to_json)
        if args.get("note_append"):
            append_note = args.pop("note_append")
            args["note"] = (
                task_remote["description"] + "\n" + append_note
                if task_remote["description"]
                else append_note
            )
        if args.get("project_id"):
            args["project_id"] = self._project_service.find_project_by_id_or_title(
                args.pop("project_id")
            ).id

    def _toggle_label(self, task: Task, label_name: str | None, is_force: bool):
        label = self._label_from_name(label_name, is_force) if label_name else None
        if not label:
            return
        if task.has_label(label):
            self._api_client.remove_label_from_task(task.id, label.id)
        else:
            self._api_client.add_label_to_task(task.id, label.id)

    def _toggle_assignee(self, task: Task, assignee_name: str | None, project_id: int):
        if not assignee_name:
            return
        assignee = self._user_from_name(assignee_name, project_id)
        if task.has_assignee(assignee):
            self._api_client.remove_assignee_from_task(task.id, assignee.id)
        else:
            self._api_client.add_assignee_to_task(task.id, assignee.id)

    @staticmethod
    def _update_due_date(args: dict, task_remote: dict):
        # keep using time of remote task, if none is given
        arg_due = args.get("due")
        remote_date = parse_json_date(task_remote["due_date"])
        if remote_date:
            arg_date = parse_date_arg_to_iso(
                arg_due, remote_date.hour, remote_date.minute
            )
        else:
            arg_date = parse_date_arg_to_iso(arg_due)
        args["due"] = arg_date

    @staticmethod
    def _update_reminder(args: dict, task_remote: dict):
        reminder_arg = args.pop("reminder", None)
        if reminder_arg is None:
            return

        parsed = CommandService._build_reminders(reminder_arg)

        if parsed is None:
            # Clear all reminders (e.g. --reminder="")
            args["reminder"] = None
            return

        # Replace the first existing reminder with our entry
        new_reminder = parsed[0]
        old_reminders = task_remote["reminders"]
        if old_reminders and len(old_reminders) > 0:
            if new_reminder:
                old_reminders[0] = new_reminder  # overwrite first remote reminder
            else:
                old_reminders.pop(0)  # remove first remote reminder
        elif new_reminder:
            old_reminders = [new_reminder]  # create single reminder
        args["reminder"] = old_reminders

    @staticmethod
    def _build_reminders(reminder_arg: str | None) -> list | None:
        """Parse a reminder CLI argument and return the reminders list (or None to clear)."""
        if reminder_arg is None:
            return None
        if reminder_arg == "due":
            return [{"relative_to": "due_date", "relative_period": 0}]
        if "due" in reminder_arg:
            reminder_due_args = reminder_arg.split(" ", 2)
            duration = int(
                parse_date_arg_to_timedelta(reminder_due_args[0]).total_seconds()
            )
            sign = -1 if reminder_due_args[1] == "before" else 1
            return [{"relative_to": "due_date", "relative_period": sign * duration}]
        if reminder_arg == "":
            return None
        return [{"reminder": parse_date_arg_to_iso(reminder_arg)}]

    def toggle_task_done(self, task_id: int) -> Task:
        task_remote = self._api_client.get_task(task_id)
        task_remote["done"] = not task_remote["done"]
        task_json = self._api_client.update_task(task_id, task_remote)
        return self._task_service.task_from_json(task_json)

    def defer_task(self, task_id: int, delay_by: str) -> Task:
        timedelta = parse_date_arg_to_timedelta(delay_by)
        args = {}

        task_remote = self._api_client.get_task(task_id)
        due_date = parse_json_date(task_remote["due_date"])
        if due_date:
            now = datetime.datetime.now().replace(microsecond=0)
            if due_date < now:
                args["due"] = datetime_to_isoformat(now + timedelta)
            else:
                args["due"] = datetime_to_isoformat(due_date + timedelta)

        old_reminders = task_remote.get("reminders")
        if old_reminders:
            reminder_date = parse_json_date(old_reminders[0].get("reminder"))
            is_absolute_reminder = not old_reminders[0].get("relative_to")
            if reminder_date and is_absolute_reminder:
                deferred_iso = datetime_to_isoformat(reminder_date + timedelta)
                old_reminders[0] = {"reminder": deferred_iso}
                args["reminder"] = old_reminders

        payload = self._args_to_payload(args)
        logger.debug("update fields: %s", payload)
        task_remote.update(payload)
        task_json = self._api_client.update_task(task_id, task_remote)
        return self._task_service.task_from_json(task_json)

    def delete_task(self, task_id: int):
        self._api_client.delete_task(task_id)

    def add_relation(
        self, task_id: int, relation_kind: str, other_task_id: int
    ) -> Task:
        self._api_client.add_relation_to_task(task_id, relation_kind, other_task_id)
        return self._task_service.task_from_json(self._api_client.get_task(task_id))

    def remove_relation(
        self, task_id: int, relation_kind: str, other_task_id: int
    ) -> Task:
        self._api_client.remove_relation_from_task(
            task_id, relation_kind, other_task_id
        )
        return self._task_service.task_from_json(self._api_client.get_task(task_id))

    def _label_from_name(self, name: str | None, is_force: bool) -> Label | None:
        if not name:
            return None
        labels_remote = Label.from_json_array(self._api_client.get_labels())
        label_found = [label for label in labels_remote if label.title == name]
        if not label_found:
            if is_force:
                return self.add_label(name)
            logger.warning(
                'Ignoring non existing label [%s]. You may want to execute "label add" first.',
                name,
            )
            return None
        return label_found[0]

    def _user_from_name(self, name: str, project_id: int) -> Assignee:
        users_remote = Assignee.from_json_array(
            self._api_client.get_project_users(project_id)
        )
        user_found = [u for u in users_remote if u.username == name]
        if not user_found:
            msg = f"User '{name}' not found in project {project_id}."
            raise VjaError(msg)
        return user_found[0]

    def _validate_add_task(self, title: str, label_names: list[str]):
        tasks_remote = self._api_client.get_tasks(exclude_completed=True)
        if any(task for task in tasks_remote if task["title"] == title):
            msg = "Task with title does exist. You may want to run with --force-create."
            raise VjaError(msg)
        labels_remote = Label.from_json_array(self._api_client.get_labels())
        for label_name in label_names:
            if not any(label for label in labels_remote if label.title == label_name):
                msg = 'Label does not exist. You may want to execute "label add" or run with --force-create.'
                raise VjaError(msg)
