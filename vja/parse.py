import functools
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
        timetuple, pdt_context = parsedatetime.Calendar(version=parsedatetime.VERSION_CONTEXT_STYLE).parse(text)
        datetime_date = datetime.fromtimestamp(time.mktime(timetuple))
        if not pdt_context.hasTime:
            datetime_date = datetime_date.replace(hour=0, minute=0, second=0)
        return datetime_date


def parse_date_arg_to_iso(text: str):
    result = parse_date_arg_to_datetime(text)
    return result.astimezone(tz.tzlocal()).isoformat() if result else None


def parse_bool_arg(text: str):
    return text.lower() in ['true', '1', 't', 'y', 'yes'] if text else False


def rgetattr(obj, path: str, *default):
    attrs = path.split('.')
    try:
        return functools.reduce(getattr, attrs, obj)
    except AttributeError:
        if default:
            return default[0]
        raise
