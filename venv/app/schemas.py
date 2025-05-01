from typing import List, Optional
from pydantic import BaseModel

class ActivitySchema(BaseModel):
    name: str
    location: str

    class Config:
        orm_mode = True

class DaySchema(BaseModel):
    day_number: int
    hotel: str
    transfer: str
    activities: List[ActivitySchema]

    class Config:
        orm_mode = True

class ItineraryCreate(BaseModel):
    name: str
    nights: int
    days: List[DaySchema]

class ItineraryOut(BaseModel):
    id: int
    name: str
    nights: int
    days: List[DaySchema]

    class Config:
        orm_mode = True
