import spacy
from spacy.tokens import Doc
from spacy.tokens import Span
from models import Entity

def __has_negated_uncertanly(doc):
    ents = set([ ent.label_ for ent in doc.ents])
    if "NEG" in ents  :
        return True
    elif  "UNC" in ents :
       return True
    else :
        return False

Doc.set_extension("has_negated_uncertanly", method = __has_negated_uncertanly)

class NLP_NER:
    __CONFLICTS_ENTS = {"CANCER_CONCEPT", "CANCER_MET", "CANCER_LOC"}

    def __init__(self, mama_ner_path, neg_uncert_ner_path):
        self.mama_ner = spacy.load(mama_ner_path)
        self.neg_uncert_ner = spacy.load(neg_uncert_ner_path)
        self.labels = spacy.info(mama_ner_path)["labels"]["ner"]
        print("\n","---"*20+"\n",self.labels,"\n","---"*20+"\n")
        #self.assembly()

    def get_ents(self, text:str):
        return self.__net_ner(text)

    def get_labels(self):
        return self.labels

    def __net_ner(self, text:str) -> any:
        doc_neg_uncert = self.neg_uncert_ner(text)
        doc_clinial = self.mama_ner(text)
        
        #if doc_neg_uncert._.has_negated_uncertanly() :
        #    for i, token in enumerate(doc_neg_uncert):
        #        
        #        if doc_mama[i].ent_type_ in self.__CONFLICTS_ENTS:
        #            if token.ent_type_ == "NSCO": #or token.ent_type_ == "USCO":
        #                    #print(token)
        #                    doc_mama.set_ents(Span(doc_mama, i, i, "outside"))


        return doc_clinial, doc_neg_uncert

    #def assembly(self):
    #    Doc.set_extension("has_negated_uncertanly", method = self.__has_negated_uncertanly())

