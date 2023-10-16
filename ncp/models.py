from pydantic import BaseModel
from typing import Dict, List, Union, Literal, Optional, TypedDict

from datetime import date


FORMAT_DATE = "%d/%m/%Y"

class Event(BaseModel):
    concepts: Dict
    date_in: Optional[str] = None
    date_off: Optional[str] = None

class Entity(BaseModel):
    name: str
    value: str

class Note(BaseModel):
    ehr: int
    text: str
    text_pre: Optional[str]
    creation_date: Optional[str] = date.today().isoformat()
    entities: Optional[List[Entity]] = None
    events: Optional[List[Event]] = None