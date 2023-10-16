import json
from ncp.post.ent_normalizers.SimilarityNormalizer import SimilarityNormalizer 
from ncp.post.ent_normalizers.RegexNormalizer import *


class Normalizer:
       
    def __init__(self, good_values_path):

        dic_vals = self.__load_good_values(good_values_path)

        regex_normalizers = {
             "MOLEC_MARKER" : MolecNormalize(),
             "TNM" : TnmNormalize(),
             "CANCER_GRADE" : GradeNormalizer()
        }

        sim_normalizers = {key: SimilarityNormalizer(dic_vals[key]) for key in dic_vals}

        self.normalizers = {**regex_normalizers, **sim_normalizers}

    def __load_good_values(cls, path):
        with open(path) as f :
            dict_vals = json.load(f)

        return dict_vals
    
    def normalize(self, concepts):
        for c in concepts:
            for key, val: 
            if isinstance(c, str):
                
                if label in diag:
                    diag[label] = normalizer.normalize(diag[label])
        
        return diags
