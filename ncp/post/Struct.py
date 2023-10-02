from ncp.post.Normalizer import Normalizer
from datetime import datetime
from spacy.tokens import Doc

from typing import List
from models import Event

class Struct:
    def __init__(self, good_values_path) -> None:
        self.good_values_path = good_values_path
        
    def serialize(self, doc_clinical:Doc)-> List[dict]:
        elems = 0
        diag = {}
        diags = []
        
        for ent in doc_clinical.ents:
            if ent.label_ in diag.keys():
                if ent.label_ == "CANCER_CONCEPT" and len(diag["CANCER_CONCEPT"]) == 1:
                    diags.append(diag)

                    diag = {ent.label_ : [ent.text]}
                    elems = 1
                    print(diag)
                else:
                    diag[ent.label_].append(ent.text)
                    elems+=1

        
            else:
                diag[ent.label_] = [ent.text]
                elems+=1
        
        if elems > 0:
            diags.append(diag)
        
        return diags

    def struct(self, doc_clinical:Doc, creation_date=str(datetime.now()))-> List[Event]:
        
        diags = self.serialize(doc_clinical)

        events = [Event(concepts=d) for d in diags]

        if len(diags) > 0:
            hz = Normalizer(self.good_values_path)
            diags = hz.normalize(diags)

        else : # No detecta diagnostico
           print("No se ha encontrado ")

        return events
