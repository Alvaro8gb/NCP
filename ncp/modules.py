from ncp.pre.Preprocesing import Preprocesing as Preprocesing
from ncp.clasificator import NLP_NET as nlp
from ncp.post import Struct as st


__MAMA_MODEL_PATH = "ncp/models/clinical"
__NEG_UNCERT_MODEL_PATH = "ncp/models/neg-uncert"
__ACRONYMS = "ncp/pre/acronimos.json"

class NCP:

    def __init__(self, acronyms, path_clinical_ner, path_neg_ner):
        self.net_ner = nlp.NLP_NER(path_clinical_ner, path_neg_ner)
        self.pre = Preprocesing(acronyms)
        self.post = st.Struct()

class NCP_single(NCP):

    def pipeline(self, note, ehr=0):
        text = self.pre.fix(note) # preprocesar el texto:
        ents = self.net_ner.get_ents(text)
        struct_result = self.post.struct(text=text, ents=ents, ehr=ehr)
        n_diags, ehr_info = struct_result
        return ehr_info    # json resultante
   
if __name__ == "__main__" : 
    ehr_info = NCP_single(__ACRONYMS, __MAMA_MODEL_PATH, __NEG_UNCERT_MODEL_PATH).pipeline("Presenta carcinoma de mama ductal, tratamiento quimioteria y masectomia")
    
    print(ehr_info)