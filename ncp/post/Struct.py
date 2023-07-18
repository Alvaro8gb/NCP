from ncp.post.Normalizer import Normalizer
from datetime import datetime

class Struct:
    def __init__(self, good_values_path) -> None:
        self.good_values_path = good_values_path
    
    def struct(self, ehr:str, text:str, ents:dict, creation_date=str(datetime.now())):
        start = 0
        diag = {}
        diags = []
        n_diags = 0
        elems = 0

        doc_clinical = ents["clinical"]
        clincal_labels = [(ent.label_ , ent.text) for ent in doc_clinical ]
        neg_uncert_labels = [ (ent.label_, ent.text) for ent in  ents["neg_unc"]]

        for ent in doc_clinical:
            if ent.label_ in diag.keys():
                if ent.label_ == "CANCER_CONCEPT" and len(diag["CANCER_CONCEPT"]) == 1:
                    diag["text"] = text[start : ent.start_char]

                    diags.append(diag)

                    diag = {ent.label_ : [ent.text]}
                    elems = 1
                    start = ent.start_char
                    n_diags+=1

                else:
                    diag[ent.label_].append(ent.text)
        
            else:
                diag[ent.label_] = [ent.text]
                elems+=1
              
        
        if elems > 0:
                diag["text"] = text[start : len(text)]                  
                diags.append(diag)
                n_diags+=1

        if n_diags > 0:
            hz = Normalizer(self.good_values_path)
            diags = hz.normalize(diags)
            ehr_info = { "ehr": ehr,  "creation_date": creation_date , "text": text, "diags": diags, "neg_uncert": neg_uncert_labels}

        else : # No detecta diagnostico
            ehr_info = { "ehr": ehr, "clinical_labels": clincal_labels, "text": text, "neg_uncert": neg_uncert_labels}

        return n_diags, ehr_info
