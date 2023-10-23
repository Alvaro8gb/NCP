from ncp.pre.Preprocesing import Preprocesing as Preprocesing
from ncp.clasificator import NLP_NET as nlp
from ncp.post import Struct as st

from spacy.tokens import Doc
from models import Note, Entity
from typing import List

from threading import Thread
from ncp.libs.in_out import load_db, dump2files

__MAMA_MODEL_PATH = "ncp/models/mama-ents-trat"
__NEG_UNCERT_MODEL_PATH = "ncp/models/neg-uncert"
__ACRONYMS = "ncp/pre/acronimos.json"
__GOOD_VALUES = "ncp/post/ent_normalizers/good_values.json"



__IN_PATH = "/home/alvaro/Documents/CLARIFY/Notes_Clarify/Historiales/primer_juicio/notes.csv" # one_diag
__OUT_PATH = "out/"
__BATCH_SIZE = 100

class NCP():

    def __init__(self, acronyms, good_vals, path_clinical_ner, path_neg_ner):
        self.net_ner = nlp.NLP_NER(path_clinical_ner, path_neg_ner)
        self.pre = Preprocesing(acronyms)
        self.post = st.Struct(good_vals)

   

    def pipeline(self, note:Note)->dict:

        note.text_pre = self.pre.fix(note.text) # preprocesar el texto:
        doc_clinical, doc_neg_unc = self.net_ner.get_ents(note.text_pre)

        self.post.struct(doc_clinical, note)

        return note

def batch(ncp:NCP, notes:List[Note]):

    for n in notes:
        ncp.pipeline(n)
        
def run(ncp:NCP, batch_size:int, notes:List[Note]):
        
    print("Number total of notes:", len(notes))

    batchs = [ notes[i:i + batch_size] for i in range(0, len(notes), batch_size)]

    print("Number of batchs", len(batchs))
    threads = [ Thread(target=batch, args=(ncp, chunk)) for chunk in batchs ]

    for t in threads:
        print(t.name, "start")
        t.start()

    for t in threads:
        print(t.name, "finish")
        t.join()

    return notes
    
def multiple():
    ncp = NCP(__ACRONYMS, __GOOD_VALUES, __MAMA_MODEL_PATH, __NEG_UNCERT_MODEL_PATH)
    
    notes = load_db(__IN_PATH)[:100]
    
    notes = run(ncp, __BATCH_SIZE, notes)

    print("Procesadas #", len(notes), " notas")

    dump2files(notes, __OUT_PATH)

if __name__ == "__main__" : 
    #ehr_info = NCP_single(__ACRONYMS, __GOOD_VALUES, __MAMA_MODEL_PATH, __NEG_UNCERT_MODEL_PATH).pipeline("Presenta carcinoma de mama ductal, tratamiento quimioteria y masectomia")
    
    #print(ehr_info)

    multiple()
