from ncp.post.ent_normalizers import Tnm_Normalize as tnmn
from ncp.post.ent_normalizers import Molec_Normalize as moln
from ncp.post.ent_normalizers.CancerNormalizers import *
from ncp.post.ent_normalizers.TratNormalizers import *


class Normalizer:
       
    def __init__(self):
        self.normalizers = {
             "MOLEC_MARKER" : moln.Molec_Normalize(),
             "TNM" : tnmn.Tnm_Normalize(),
             "CANCER_CONCEPT" : ConceptNormalizer(),
             "CANCER_TYPE" : TypeNormalizer(),
             "CANCER_SUBTYPE" : SubtypeNormalizer(),
             "CANCER_INTRTYPE" : IntrtypeNormalizer(),
             "CANCER_LOC" : LocNormalizer(),
             "CANCER_EXP" : ExpNormalizer(),
             "CANCER_MET" : MetNormalizer(),
             "CANCER_REC" : RecNormalizer(),
             "CANCER_GRADE" : GradeNormalizer(),
             "SURGERY" : SurgeryNormalizer(),
             "TRAT": TratNormalizer(),
             "TRAT_DRUG": TratDrugNormalizer()
        }

    def normalize(self, diags):
        for diag in diags:
            for label, normalizer in self.normalizers.items():
                if label in diag:
                    diag[label] = {"old": diag[label],
                            "new" : normalizer.normalize(diag[label])
                        }
        return diags
