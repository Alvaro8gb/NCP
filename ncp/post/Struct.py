from ncp.post.Normalizer import Normalizer
from datetime import datetime
from spacy.tokens import Doc

from typing import List
from models import Note, Treatment, Diag, Entity, TNM, TRAT_ENTS, DIAG_ENTS, DIAG, TRAT


class Struct:
    def __init__(self, good_values_path) -> None:
        self.good_values_path = good_values_path

    @staticmethod
    def extract_ents(doc: Doc) -> List[Entity]:
        return [Entity(name=ent.label_, value=ent.text) for ent in doc.ents]

    def serialize(self, ents: List[Entity]) -> List[dict]:
        diag_ents = {}
        trat_ents = {}

        concepts = []

        for ent in ents:
            name = ent.name
            value = ent.value

            # print(ent)
            if name == DIAG:
                if not diag_ents:
                    diag_ents[name] = value
                else:
                    concepts.append(diag_ents)
                    diag_ents = {}

            elif name == TRAT:
                if not trat_ents:
                    trat_ents[name] = value
                else:
                    concepts.append(trat_ents)
                    trat_ents = {}

            elif name in DIAG_ENTS:
                if name in diag_ents:
                    diag_ents[name] += " " + value
                else:
                    diag_ents[name] = value

            elif name in TRAT_ENTS:
                if name in diag_ents:
                    diag_ents[name] += " " + value
                else:
                    diag_ents[name] = value

            else:
                concepts.append({name: value})

        if diag_ents:
            concepts.append(diag_ents)

        if trat_ents:
            concepts.append(trat_ents)

        return concepts

    def struct(self, doc_clinical: Doc, note: Note):

        ents = self.extract_ents(doc_clinical)

        note.entities = ents

        concepts = self.serialize(ents)

        if len(concepts) > 0:
            hz = Normalizer(self.good_values_path)
            concepts = hz.normalize(concepts)

            for c in concepts:
                if DIAG in c:
                    diag_data = {
                        "concept": c[DIAG],
                        "loc": c.get("CANCER_LOC"),
                        "exp": c.get("CANCER_EXP"),
                        "grade": c.get("CANCER_GRADE"),
                        "type": c.get("CANCER_TYPE"),
                        "subtype": c.get("CANCER_SUBTYPE"),
                    }

                    diag = Diag(**{k: v for k, v in diag_data.items() if v is not None})

                    tnm = c.get("TNM")
                    if tnm != None:
                        print(tnm)
                        print(c)
                        diag.tnm = TNM(**tnm)
                        
                    note.diags.append(diag)

                elif TRAT in c:
                    treat_data = {
                        "concept": c[TRAT],
                        "drug": c.get("CANCER_DRUG"),
                        "freq": c.get("CANCER_FREQ"),
                        "interval": c.get("CANCER_INTERVAL"),
                        "quantity": c.get("CANCER_QUANTITY"),
                        "schme": c.get("CANCER_SCHME")
                    }

                    treatment = Treatment(**{k: v for k, v in treat_data.items() if v is not None})
                    note.treatms.append(treatment)


        else:  # No detecta diagnostico
            print("No se ha encontrado concepts ")
