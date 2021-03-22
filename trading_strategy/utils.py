import datetime

from .constants import DATE_FMT


def date_to_str(date: datetime.date, fmt=DATE_FMT) -> str:
    return date.strftime(fmt)


def str_to_date(str_date: str, fmt=DATE_FMT) -> datetime.date:
    return datetime.datetime.strptime(str_date, fmt).date()
