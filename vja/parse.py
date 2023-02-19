import time
from datetime import datetime

import dateutil.parser
from dateutil import tz
from parsedatetime import parsedatetime


def parse_date_arg_to_datetime(text: str):
    if not text:
        return None
    try:
        return dateutil.parser.isoparse(text)
    except ValueError:
        timetuple = parsedatetime.Calendar(version=parsedatetime.VERSION_CONTEXT_STYLE).parse(text)[0]
        datetime_date = datetime.fromtimestamp(time.mktime(timetuple))
        return datetime_date


def parse_date_arg(text: str):
    result = parse_date_arg_to_datetime(text)
    return result.astimezone(tz.tzlocal()).isoformat() if result else None
