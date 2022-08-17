from pydantic import BaseModel

class LightRequest(BaseModel):
    zone1 : int
    zone2 : int


class TempRequest(BaseModel):
    value : float 

class DatalogRequest(BaseModel):
    date : str
    time : str