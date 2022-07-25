from pydantic import BaseModel

class LightRequest(BaseModel):
    zone1 : int
    value1 : int
    zone2 : int
    value2: int


class TempRequest(BaseModel):
    value : int