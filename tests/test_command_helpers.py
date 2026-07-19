import datetime
import json
import re

from tests.conftest import invoke

ADD_SUCCESS_PATTERN = re.compile(r".*Created task (\d+) in project .*")
TODAY = datetime.datetime.now().replace(microsecond=0)
TODAY_ISO = TODAY.isoformat()
YESTERDAY = TODAY + datetime.timedelta(days=-1)
YESTERDAY_ISO = YESTERDAY.isoformat()
TOMORROW = TODAY + datetime.timedelta(days=1)
TOMORROW_ISO = TOMORROW.isoformat()
TOMORROW_AT_8_ISO = (TOMORROW.replace(hour=8, minute=0, second=0)).isoformat()
DATE_1 = TODAY + datetime.timedelta(days=10)
DATE_2 = DATE_1 + datetime.timedelta(days=1)
DATE_1_ISO = DATE_1.isoformat()
DATE_2_ISO = DATE_2.isoformat()


def json_for_created_task(runner, message):
    assert re.match(ADD_SUCCESS_PATTERN, message), message
    task_id = ADD_SUCCESS_PATTERN.findall(message)[0]
    return json_for_task_id(runner, task_id)


def json_for_task_id(runner, task_id):
    res = invoke(runner, f"show {task_id} --jsonvja")

    assert res.exit_code == 0, res
    data = json.loads(res.output)
    return data


def has_label_with_title(labels, title):
    label_titles = [x["title"] for x in labels]
    return title in label_titles


def has_assignee_with_username(assignees, username):
    return username in [x["username"] for x in assignees]
