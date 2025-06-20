from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.config import ConfigDict

class EventCreate(BaseModel):
    name: str
    location: str 
    start_time: datetime
    end_time: datetime 
    max_capacity: int 

class EventOut(BaseModel):
    id: int
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int

    model_config = ConfigDict(from_attributes=True)
