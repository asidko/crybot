import datetime

_generate_id = 0


def generate_id() -> int:
    global _generate_id
    _generate_id += 1
    return _generate_id


def date():
    return datetime.datetime.now().replace(microsecond=0).isoformat()
