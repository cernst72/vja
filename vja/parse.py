import functools
import re
import time
from datetime import datetime, timedelta

import dateutil.parser
from dateutil import tz
from parsedatetime import parsedatetime

_timedelta_regex = re.compile(r'^((?P<weeks>[.\d]+?)w)? *'
                              r'^((?P<days>[.\d]+?)d)? *'
                              r'((?P<hours>[.\d]+?)h)? *'
                              r'((?P<minutes>[.\d]+?)m)? *'
                              r'((?P<seconds>[.\d]+?)s?)?$')


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


def parse_date_arg_to_timedelta(time_str: str):
    """
    Parse a time string e.g. '2h 13m' or '1.5d' into a timedelta object.
    Based on Peter's answer at https://stackoverflow.com/a/51916936/2445204
    and virhilo's answer at https://stackoverflow.com/a/4628148/851699
    :param time_str: A string identifying a duration, e.g. '2h13.5m'
    :return datetime.timedelta: A datetime.timedelta object
    """
    if not time_str:
        return None
    parts = _timedelta_regex.match(time_str)
    assert parts is not None, f"""Could not parse any time information from '{time_str}'.
    Examples of valid strings: '8h', '2d 8h 5m 2s', '2m4.3s'"""
    time_params = {name: float(param)
                   for name, param in parts.groupdict().items() if param}
    return timedelta(**time_params)


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


def parse_json_date(json_date):
    if json_date and json_date > '0001-01-02T00:00:00Z':
        return dateutil.parser.isoparse(json_date).astimezone(tz.tzlocal()).replace(tzinfo=None)
    return None
