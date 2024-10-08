import functools
import re
import time
from datetime import datetime, timedelta
from html.parser import HTMLParser
from typing import Optional

from dateutil import tz, parser
from parsedatetime import parsedatetime

# if dates are given like 'tomorrow' or 'next mon' then this will be used as time
DEFAULT_DATE_HOUR = 8
DEFAULT_DATE_MINUTE = 0

_timedelta_regex = re.compile(r'^((?P<weeks>[.\d]+?)w)? *'
                              r'^((?P<days>[.\d]+?)d)? *'
                              r'((?P<hours>[.\d]+?)h)? *'
                              r'((?P<minutes>[.\d]+?)m)? *'
                              r'((?P<seconds>[.\d]+?)s?)?$')


def parse_date_arg_to_datetime(text: str,
                               default_hour=DEFAULT_DATE_HOUR,
                               default_minute=DEFAULT_DATE_MINUTE) -> Optional[datetime]:
    if not text:
        return None

    if re.compile(r'.*\dT\d.*').match(text):
        text = text.replace("T", " ")  # workaround for https://github.com/bear/parsedatetime/issues/15

    timetuple, pdt_context = parsedatetime.Calendar(version=parsedatetime.VERSION_CONTEXT_STYLE).parse(text)
    result = datetime.fromtimestamp(time.mktime(timetuple))
    if not pdt_context.hasTime:
        result = result.replace(hour=default_hour, minute=default_minute, second=0)
    return result


def parse_date_arg_to_iso(text: str,
                          default_hour=DEFAULT_DATE_HOUR,
                          default_minute=DEFAULT_DATE_MINUTE) -> Optional[str]:
    date_value = parse_date_arg_to_datetime(text, default_hour, default_minute)
    return datetime_to_isoformat(date_value) if date_value else None


def datetime_to_isoformat(date: datetime) -> Optional[str]:
    return date.astimezone(tz.tzlocal()).isoformat() if date else None


def parse_date_arg_to_timedelta(time_str: str) -> Optional[timedelta]:
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


def parse_json_date(json_date: str) -> Optional[datetime]:
    if json_date and json_date > '0001-01-02T00:00:00Z':
        return parser.isoparse(json_date).astimezone(tz.tzlocal()).replace(tzinfo=None)
    return None


def parse_bool_arg(text: str) -> bool:
    return text.lower() in ['true', '1', 't', 'y', 'yes'] if text else False


class HTMLFilter(HTMLParser):
    inner_text = ""

    def handle_data(self, data):
        self.inner_text += data


def html2text(text: str) -> str:
    html_parser = HTMLFilter()
    html_parser.feed(text)
    return html_parser.inner_text


def rgetattr(obj, path: str, *default):
    attrs = path.split('.')
    try:
        return functools.reduce(getattr, attrs, obj)
    except AttributeError:
        if default:
            return default[0]
        raise
