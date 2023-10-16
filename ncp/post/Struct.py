from ncp.post.Normalizer import Normalizer
from datetime import datetime
from spacy.tokens import Doc

from typing import List
from models import Event

DIAG_ENTS = {'CANCER_EXP', 'CANCER_GRADE', 'CANCER_INTRTYPE', 'CANCER_LOC','CANCER_TYPE', 'CANCER_SUBTYPE'} 
TRAT_ENTS = {'TRAT', 'TRAT_DRUG', 'TRAT_FREQ', 'TRAT_INTERVAL', 'TRAT_QUANTITY', 'TRAT_SHEMA'}

class Struct:
    def __init__(self, good_values_path) -> None:
        self.good_values_path = good_values_path
        
    def serialize(self, doc_clinical:Doc)-> List[dict]:
        diag = None
        trat = None
        events = []
        concepts = {}
        
        for ent in doc_clinical.ents:
            label = ent.label_
            if label == "CANCER_CONCEPT":

                if diag != None:
                    concepts["CANCER_DIAG"] = diag 
                    events

                diag = {"CANCER_CONCEPT" : ent.text }

            elif label == "TRAT":
                
                if trat == None:
                    concepts{"CANCER_TRAT":trat})

                diag = {"CANCER_CONCEPT" : ent.text }                   
                
            elif label in DIAG_ENTS:
                if diag != None:
                    diag[label] = ent.text 

            elif label in TRAT_ENTS:
                if trat != None:
                    diag[label] = ent.text 
            else:
                concepts.append({label:ent.text})
        
        return concepts

    def struct(self, doc_clinical:Doc, creation_date=str(datetime.now()))-> List[Event]:
        
        concepts = self.serialize(doc_clinical)

        if len(concepts) > 0:
            hz = Normalizer(self.good_values_path)
            concepts = hz.normalize(concepts)

        else : # No detecta diagnostico
           print("No se ha encontrado ")

        events = [Event(concepts=c) for c in concepts]

        return events
