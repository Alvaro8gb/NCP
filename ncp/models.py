from pydantic import BaseModel
from typing import Dict, List, Union, Literal, Optional, TypedDict

from datetime import date

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
    creation_date: Optional[date] = date.today().strftime("%d/%m/%Y")
    entities: Optional[List[Entity]] = None
    events: Optional[List[Event]] = None