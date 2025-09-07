from pydantic import BaseModel

class EventBase(BaseModel):
    name: str
    description: str
    date: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int

    model_config = {
        "from_attributes": True  # This replaces orm_mode in Pydantic v2
    }
