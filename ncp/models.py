from pydantic import BaseModel
from typing import Dict, List, Union, Literal, Optional

from datetime import date

TRAT = "TRAT"
DIAG = "CANCER_CONCEPT"
DIAG_ENTS = {'CANCER_EXP', 'CANCER_GRADE', 'CANCER_INTRTYPE', 'CANCER_LOC','CANCER_TYPE', 'CANCER_SUBTYPE', "TNM"} 
TRAT_ENTS = {'TRAT', 'TRAT_DRUG', 'TRAT_FREQ', 'TRAT_INTERVAL', 'TRAT_QUANTITY', 'TRAT_SHEMA', 'SURGERY'}


FORMAT_DATE = "%d/%m/%Y"

class TNM(BaseModel):
    t: str
    n: str
    m: str

class Concept(BaseModel):
    concept: str
    date: Optional[str] = None

class Diag(Concept):
    loc: Optional[str] = None
    tnm : Optional[TNM] = None
    exp: Optional[str] = None
    grade: Optional[str] = None
    type: Optional[str] = None
    subtype: Optional[str] = None

class Treatment(Concept):
    drug: Optional[str] = None
    freq: Optional[str] = None
    interval: Optional[str] = None
    quantity: Optional[str] = None
    schme: Optional[str] = None

class Entity(BaseModel):
    name: str
    value: str

class Note(BaseModel):
    ehr: int
    text: str
    text_pre: Optional[str] = None
    creation_date: Optional[str] = date.today().isoformat()
    entities: Optional[List[Entity]] = None
    diags: Optional[List[Diag]] = []
    treatms: Optional[List[Treatment]] = []
    metastasis: Optional[List[Entity]] = None
    recaidas: Optional[List[Entity]] = None