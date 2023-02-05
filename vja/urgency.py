from datetime import datetime

from vja.model import Task

score_coefficients = {'due_date': 1.0, 'priority': 1.0, 'favorite': 1.0, 'list_keyword': 1.0, 'label_keyword': 1.0}


class Urgency:

    @staticmethod
    def compute(task: Task):
        if task.done:
            return 0

        due_date_score = Urgency.get_due_date_score(task) * score_coefficients['due_date']
        priority_score = task.priority * score_coefficients['priority']
        favorite_score = int(task.is_favorite) * score_coefficients['favorite']
        list_name_score = int('next' in task.tasklist.title.lower()) * score_coefficients['list_keyword']
        lable_name_score = int(any('next' in label.title.lower() for label in task.labels)) * score_coefficients[
            'label_keyword']

        return 2 + due_date_score + priority_score + favorite_score + list_name_score + lable_name_score

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
                result = 3
            elif 5 < due_days <= 10:
                result = 1
            elif due_days > 10:
                result = -1
            else:
                result = 0
        else:
            result = 0
        return result
