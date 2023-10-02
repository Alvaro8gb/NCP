from ncp.pre.Preprocesing import Preprocesing as Preprocesing
from ncp.clasificator import NLP_NET as nlp
from ncp.post import Struct as st

from spacy.tokens import Doc
from models import Note, Entity
from typing import List
    
__MAMA_MODEL_PATH = "ncp/models/mama-ents-trat"
__NEG_UNCERT_MODEL_PATH = "ncp/models/neg-uncert"
__ACRONYMS = "ncp/pre/acronimos.json"
__GOOD_VALUES = "ncp/post/ent_normalizers/good_values.json"

class NCP:

    def __init__(self, acronyms, good_vals, path_clinical_ner, path_neg_ner):
        self.net_ner = nlp.NLP_NER(path_clinical_ner, path_neg_ner)
        self.pre = Preprocesing(acronyms)
        self.post = st.Struct(good_vals)

    @staticmethod
    def extact_ents(doc:Doc)-> List[Entity]:
        return [Entity(name=ent.label_, value=ent.text) for ent in doc.ents]

class NCP_single(NCP):
    

    def pipeline(self, text:str, ehr:int=0, create_date:str=""):
        note = Note(ehr=ehr, text=text)

        note.text_pre = self.pre.fix(note.text) # preprocesar el texto:
        doc_clinical, doc_neg_unc = self.net_ner.get_ents(note.text_pre)

        note.entities = NCP.extact_ents(doc_clinical) + NCP.extact_ents(doc_neg_unc)
        note.events = self.post.struct(doc_clinical, note)

        return note.dict() 
   
if __name__ == "__main__" : 
    ehr_info = NCP_single(__ACRONYMS, __GOOD_VALUES, __MAMA_MODEL_PATH, __NEG_UNCERT_MODEL_PATH).pipeline("Presenta carcinoma de mama ductal, tratamiento quimioteria y masectomia")
    
    print(ehr_info)