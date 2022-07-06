from datetime import datetime, timedelta
from typing import Any

import ujson
from pydantic import BaseModel
from pydantic.json import timedelta_isoformat


class ErrorMessage(BaseModel):
    type: str = ""
    message: str = ""


class HTTPResponseWrapper(BaseModel):
    """Generic wrapper for any http response"""

    class Config:
        anystr_strip_whitespace = True
        title = "HTTPResponseWrapper"
        json_loads = ujson.loads
        json_dumps = ujson.dumps
        json_encoders = {
            datetime: lambda v: v.timestamp(),
            timedelta: timedelta_isoformat,
        }

        schema_extra = {
            'examples': [
                {
                    'error': False,
                    'errors': None,
                    'data': None,
                    'meta': None
                }
            ]
        }

    error: bool = False
    data: Any = None
    meta: Any = None
