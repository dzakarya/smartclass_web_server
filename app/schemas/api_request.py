from pydantic import BaseModel

class LightRequest(BaseModel):
    zone : int
    value : int


class TempRequest(BaseModel):
    value : int