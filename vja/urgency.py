from datetime import datetime

from vja.config import VjaConfiguration
from vja.model import Task


class Urgency:

    def __init__(self, urgency_coefficients: dict, list_keywords, label_keywords):
        self._urgency_coefficients = urgency_coefficients
        self._list_keywords = list_keywords
        self._label_keywords = label_keywords

    def compute_for(self, task: Task):
        if task.done:
            return 0
        due_date_score = self._get_due_date_score(task) * self._urgency_coefficients.get('due_date_weight', 1.0)
        priority_score = task.priority * self._urgency_coefficients.get('priority_weight', 1.0)
        favorite_score = int(task.is_favorite) * self._urgency_coefficients.get('favorite_weight', 1.0)
        list_name_score = self._get_list_score(task) * self._urgency_coefficients.get('list_keyword', 1.0)
        lable_name_score = self._get_label_score(task) * self._urgency_coefficients.get('label_keyword', 1.0)

        return 1 + due_date_score + priority_score + favorite_score + list_name_score + lable_name_score

    def _get_label_score(self, task):
        task_label_title = task.label_titles.lower()
        return int(any(label_name.lower() in task_label_title for label_name in
                       self._label_keywords)) if self._label_keywords else 0

    def _get_list_score(self, task):
        task_list_title = task.tasklist.title.lower()
        return int(any(list_name.lower() in task_list_title for list_name in
                       self._list_keywords)) if self._list_keywords else 0

    @staticmethod
    def _get_due_date_score(task: Task):
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
            elif due_days > 14:
                result = -1
            else:
                result = 0
        else:
            result = 0
        return result

    @classmethod
    def from_config(cls, config: VjaConfiguration):
        config_list_keywords = config.get_urgency_list_keywords()
        list_keywords = [x.strip() for x in config_list_keywords.split(',')] if config_list_keywords else []
        config_label_keywords = config.get_urgency_label_keywords()
        label_keywords = [x.strip() for x in config_label_keywords.split(',')] if config_label_keywords else []

        urgency_coefficients = {k: float(v) for k, v in config.get_urgency_coefficients().items()}
        return cls(urgency_coefficients, list_keywords, label_keywords)
