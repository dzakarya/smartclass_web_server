
import datetime
from decimal import Decimal
from enum import Enum
from types import GeneratorType
from uuid import UUID

import typing
import ujson
from pydantic import BaseModel
from starlette.responses import UJSONResponse


def isoformat(o: datetime) -> datetime.datetime:
    return o.isoformat()


ENCODERS_BY_TYPE = {
    UUID: str,
    datetime.datetime: isoformat,
    datetime.date: isoformat,
    datetime.time: isoformat,
    datetime.timedelta: lambda td: td.total_seconds(),
    set: list,
    frozenset: list,
    GeneratorType: list,
    bytes: lambda o: o.decode(),
    Decimal: float,
}

JSONABLE_OK = (str, int, float, type(None))
SEQUENCES = (list, set, frozenset, GeneratorType, tuple)


def pydantic_encoder(obj):
    if isinstance(obj, BaseModel):
        return obj.dict()
    elif isinstance(obj, Enum):
        return obj.value

    try:
        encoder = ENCODERS_BY_TYPE[type(obj)]
    except KeyError:
        raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")
    else:
        return encoder(obj)


def jsonable_encoder(obj):
    if isinstance(obj, JSONABLE_OK):
        return obj
    if isinstance(obj, dict):
        return {jsonable_encoder(key): jsonable_encoder(value) for key, value in obj.items()}
    if isinstance(obj, SEQUENCES):
        return [jsonable_encoder(item) for item in obj]

    if isinstance(obj, BaseModel):
        return jsonable_encoder(obj.dict())
    if isinstance(obj, Enum):
        return jsonable_encoder(obj.value)
    try:
        encoder = ENCODERS_BY_TYPE[type(obj)]
    except KeyError:
        raise TypeError(f"Object of type '{obj.__class__.__name__}' is not serializable")
    else:
        return encoder(obj)


class Jsonify(UJSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        assert ujson is not None, "ujson must be installed to use UJSONResponse"
        return ujson.dumps(jsonable_encoder(content), ensure_ascii=False).encode("utf-8")
