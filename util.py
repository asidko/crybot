import datetime

_generate_id = 0
date_format = "%Y-%m-%d %H:%M:%S"


def generate_id() -> int:
    global _generate_id
    _generate_id += 1
    return _generate_id


def date():
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def date_to_str(date: datetime) -> str:
    global date_format
    return date.strftime(date_format) if date is not None else ''
