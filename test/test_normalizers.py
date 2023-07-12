from test import TestNormalizerException


from ncp.post.ent_normalizers import Concept_Normalize as ccn
from ncp.post.ent_normalizers import Exp_Normalize as expn
from ncp.post.ent_normalizers import Intrtype_Normalize as itn
from ncp.post.ent_normalizers import Loc_Normalize as lcn
from ncp.post.ent_normalizers import Met_Normalize as mtn
from ncp.post.ent_normalizers import Grade_Normalize as grn
from ncp.post.ent_normalizers import Molec_Normalize as moln
from ncp.post.ent_normalizers import Rec_Normalize as recn
from ncp.post.ent_normalizers import Subtype_normalizer as subn
from ncp.post.ent_normalizers import Surgery_Normalize as surn
from ncp.post.ent_normalizers import Tnm_Normalize as tnmn
from ncp.post.ent_normalizers import Type_Normalize as typn

# Check the proper key names in normalizersTest.py
normalizers = {
    "CONCEPT NORMALIZE" : ccn.Concept_Normalize(),
    "EXP NORMALIZE" : expn.Exp_Normalize(),
    "GRADE NORMALIZE" : grn.Grade_Normalize(),
    "INTRTYPE NORMALIZE" : itn.Intrtype_Normalize(),
    "LOC NORMALIZE" : lcn.Loc_Normalize(),
    "MET NORMALIZE" : mtn.Met_Normalize(),
    "MOLEC NORMALIZE" : moln.Molec_Normalize(),
    "REC NORMALIZE" : recn.Rec_Normalize(),
    "SUBTYPE NORMALIZE" : subn.Subtype_Normalize(),
    "SURGERY NORMALIZE" : surn.Surgery_Normalize(),
    "TNM NORMALIZE" : tnmn.Tnm_Normalize(),
    "TYPE NORMALIZE" : typn.Type_Normalize()
}

class NormalizersTest:

    __COLOR_RESET = '\033[0m' #RESET COLOR
    __COLOR_GREEN = '\033[92m'

    def __init__(self, normalizers:dict):
        self.normalizers = normalizers # {"CONCEPT NORMALIZE" : Concept_Normalize()}
        print("Unit Test for Normalizers from ent_normalizers")
    
    def __check(self, input, expected_output, module):
        normalized = self.normalizers[module].normalize(input)
        if normalized != expected_output:
            raise TestNormalizerException(module, input, expected_output, normalized)

    def __test(self, module, cmps:list):
        for input, expected_output in cmps:
            self.__check(input, expected_output, module)

        print(module + self.__COLOR_GREEN + " tests passed" + self.__COLOR_RESET)

    def start(self):
        tests = [
            self.__concept_normalize,
            self.__exp_normalize,
            self.__grade_normalize,
            self.__intrtype_normalize,
            self.__loc_normalize,
            self.__met_normalize,
            self.__molec_normalize,
            self.__rec_normalize,
            self.__subtype_normalize,
            self.__surgery_normalize,
            self.__tnm_normalize,
            self.__type_normalize
        ]
        failed = []

        for t in tests:
            try:
                t()
            except TestNormalizerException as e:
                failed.append(str(e))

        if len(failed) == 0:
            print(self.__COLOR_GREEN + "All tests passed." + self.__COLOR_RESET)
        else:
            print("\n" + "=== Normalizers that failed tests ===")
            for failure in failed:
                print(failure + "\n")

    def __concept_normalize(self):
        cmps = [
            (["cracinoma"], ["carcinoma"]),
            (["canecer"], ["cancer"]),
            (["adenocarinoma"], ["adenocarcinoma"]),
        ]

        self.__test("CONCEPT NORMALIZE", cmps)
    
    def __exp_normalize(self):
        cmps = [
            (["insitu"], ["in situ"]),
            (["inflitrante"], ["infiltrante"]),
            (["invsivo", "miroinfiltraent", "multifolcal", "muticentrico"], ["invasivo", "microinfiltrante", "multifocal", "multicentrico"]),
            (["abundates focos", "multipleslineas", "bifolac", "unifocla"], ["abundantes focos", "multiples lineas", "bifocal", "unifocal"])
        ]
    
        self.__test("EXP NORMALIZE", cmps)
    
    def __grade_normalize(self):
        pass

    def __intrtype_normalize(self):
        cmps = [
            (["luminA", "lumina B", "liuminal A", "liuminalB"], ["luminal A", "luminal B", "luminal A", "luminal B"]),
            (["Her2sobreexpresado", "her2 sobrexpresado"], ["HER2 sobreexpresado", "HER2 sobreexpresado"]),
            (["tripleneg", "trinegativo"], ["triple negativo", "triple negativo"])
        ]

        self.__test("INTRTYPE NORMALIZE", cmps)

    def __loc_normalize(self):
        cmps = [
            (["amam", "mamama", "izqireda", "dercha"], ["mama", "mama", "izquierda", "derecha"]),
            (["amam izquierda", "amam derecha", "mama izquirda", "mama dereha"], ["mama izquierda", "mama derecha", "mama izquierda", "mama derecha"]),
            (["origenmamario", "bi lateral", "linfovacular", "perineal"], ["origen mamario", "bilateral", "linfovascular", "perineural"])
        ]

        self.__test("LOC NORMALIZE", cmps)

    def __met_normalize(self):
        cmps = [
            (["metatasis", "micrometastis", "metastatis", "micrometsastasis"], ["metastasis", "micrometastasis", "metastasis", "micrometastasis"]),
            (["pregresion", "inbasion", "infieltracion"], ["progresion", "invasion", "infiltracion"]),
            (["afectacion", "lision"], ["afeccion", "lesion"])
        ]

        self.__test("MET NORMALIZE", cmps)

    def __molec_normalize(self):
        cmps = [
            (["her-2 -"], {"her2" : "-"}),
            (["her2neu-"], {"her2" : "-"}),
            (["re pos. 100%"], {"re" : ["+", "100%"]}),
            (["rp 45%"], {"rp" : "45%"}),
            (["her2"], {"her2" : ""}),
            (["rp: 30%"], {"rp" : "30%"}),
            (["rp 28%"], {"rp" : "28%"}),
            (["re+"], {"re" : "+"}),
            (["re y p +)"], {"rh" : "+"}),
            (["re pos (70%)"], {"re" : ["+", "70%"]}),
            (["rp100%"], {"rp" : "100%"}),
            (["receptores de estrogenos: positivos (40%)"], {"re" : ["+", "40%"]}),
            (["receptores hormonales y her negativos"], {"rh" : "-", "her2" : "-"}),
            (["r. estrogenos + (100% )"], {"re" : ["+", "100%"]})
        ]

        self.__test("MOLEC NORMALIZE", cmps)

    def __rec_normalize(self):
        cmps = [
            (["recadia", "recidva", "regesion"], ["recaida", "recidiva", "regresion"]),
        ]

        self.__test("REC NORMALIZE", cmps)
    
    def __subtype_normalize(self):
        cmps = [
            (["clsico", "conbencional", "medulal", "paplirar", "tubilar"], ["clasico", "convencional", "medular", "papilar", "tubular"]),
            (["muquosino", "colioide", "mucicoso", "muciosa"], ["mucosino", "coloide", "mucinoso", "mucinosa"]),
            (["comedoniano", "comediano"], ["comedoniano", "comedoniano"]),
            (["criboforme", "micropalipar"], ["cribiforme", "micropapilar"]),
            (["pleomorfo", "pleomorfa", "folilucal"], ["pleomorfico", "pleomorfica", "folicular"])
        ]

        self.__test("SUBTYPE NORMALIZE", cmps)
    
    def __surgery_normalize(self):
        cmps = [
            (["linfadectonomia", "matestomia", "tumorecotomia"], ["linfadenectomia", "mastectomia", "tumorectomia"]),
            (["recontrucion", "metestomia de recontrucion", "taclaje"], ["reconstruccion", "mastectomia de reconstruccion", "talcaje"])
        ]

        self.__test("SURGERY NORMALIZE", cmps)
    
    def __tnm_normalize(self):
        cmps = [
            (["cT2N1M0"], [{
                   "t": "cT2",
                   "n": "N1",
                   "m": "M0"}]),

            (["cT1b,cN0,cMx"], [{
                   "t": "cT1b",
                   "n": "cN0",
                   "m": "cMx"}]),

            (["(CNCP cyT2cN2M0)"], [{
                   "t": "cyT2",
                   "n": "cN2",
                   "m": "M0"}]),

            (["ycT2N1M0 Her2 pos"], [{
                   "t": "ycT2",
                   "n": "N1",
                   "m": "M0"}]),

            (["cT1bcN0cM0"], [{
                   "t": "cT1b",
                   "n": "cN0",
                   "m": "cM0"}]),

            (["cT1b,cN0,cMx"], [{
                   "t": "cT1b",
                   "n": "cN0",
                   "m": "cMx"}]),

            (["pyT1b pN0(sn)."], [{
                   "t": "pyT1b",
                   "n": "pN0(sn)",
                   "m": ""}]),

            (["ypT1b (10 mm) pN0(sn)"], [{
                   "t": "ypT1b",
                   "n": "pN0(sn)",
                   "m": ""}]),

            (["pT1b (1 cm) pN0(sn)"], [{
                   "t": "pT1b",
                   "n": "pN0(sn)",
                   "m": ""}]),

            #(["(m)pT1b pN0 (sn) cM0"], [{
            #       "t": "(m)pT1b",
            #       "n": "pN0 (sn)",
            #       "m": "cM0"}]),

            (["  pT2; pN0 (sn)"], [{
                   "t": "pT2",
                   "n": "pN0 (sn)",
                   "m": ""}]),

            (["metástasis): pT3(m) N1a."], [{
                   "t": "pT3(m)",
                   "n": "N1a",
                   "m": ""}]),

            (["Estadio patológico pTNM (8ª ed.): pT1c(m); pN0(sn)"], [{
                   "t": "pT1c(m)",
                   "n": "pN0(sn)",
                   "m": ""}]),

            #(["Estadio patológico pTNM (7ª ed.): (y)pT1a(m); (y)pN2a"], [{
            #       "t": "(y)pT1a(m)",
            #       "n": "(y)pN2a",
            #       "m": ""}]),

            (["pT1b pN0(sn"], [{
                   "t": "pT1b",
                   "n": "pN0(sn",
                   "m": ""}]),

            (["pT1c(m); pN0(sn) cM0 "], [{
                   "t": "pT1c(m)",
                   "n": "pN0(sn)",
                   "m": "cM0"}]),

            (["cT2 (27 mm en ecografía); cN1a(f)"], [{
                   "t": "cT2",
                   "n": "cN1a(f)",
                   "m": ""}]),

            #(["pTis(1,8cm) pNx cM0"], [{
            #       "t": "pTis",
            #       "n": "pNx",
            #       "m": "cM0"}]),

            (["pT1b(m) pN0(sn) cMx"], [{
                   "t": "pT1b(m)",
                   "n": "pN0(sn)",
                   "m": "cMx"}]),

            #(["mpT1c (17mm) cN1mi"], [{
            #       "t": "mpT1c (17mm)",
            #       "n": "cN1mi",
            #       "m": ""}]),

            (["mpt1c pn0 cm0"], [{
                   "t": "mpt1c",
                   "n": "pn0",
                   "m": "cm0"}]),

            (["pTis(DCIS pN0 cM0"], [{
                   "t": "pTis(DCIS",
                   "n": "pN0",
                   "m": "cM0"}]),

            (["pT1 ( 16,5 mm),N1"], [{
                   "t": "pT1",
                   "n": "N1",
                   "m": ""}]),

            (["Tis(paget)N0(mol+)"], [{
                   "t": "Tis(paget)",
                   "n": "N0(mol+)",
                   "m": ""}]),

            (["T0N0cM0(i+)"], [{
                   "t": "T0",
                   "n": "N0",
                   "m": "cM0(i+)"}]),

            (["T2N0 I+)Mx"], [{
                   "t": "T2",
                   "n": "N0 I+)",
                   "m": "Mx"}]),

            (["pT1pN0sn(0/3)"], [{
                   "t": "pT1",
                   "n": "pN0sn(0/3)",
                   "m": ""}]),
                   
            (["pT2 cN0 (0/1) cM0,"], [{
                   "t": "pT2",
                   "n": "cN0 (0/1)",
                   "m": "cM0"}]),

            (["ypT1b (6 mm) N0sn (0/1 GC)"], [{
                   "t": "ypT1b",
                   "n": "N0sn (0/1 GC)",
                   "m": ""}]),

            (["pT3N1 (2+/6)M1"], [{
                   "t": "pT3",
                   "n": "N1 (2+/6)",
                   "m": "M1"}]),

            (["pT1 ( 16,5 mm),N1 ( 1/16)"], [{
                   "t": "pT1",
                   "n": "N1 ( 1/16)",
                   "m": ""}]),

            (["cT4a cN2 (al menos) M1"], [{
                   "t": "cT4a",
                   "n": "cN2 (al menos)",
                   "m": "M1"}]),       
        ]

        self.__test("TNM NORMALIZE", cmps)

    def __type_normalize(self):
        cmps = [
            (["lobullar", "ducatal", "aporcino"], ["lobular", "ductal", "apocrino"]),
            (["neuroendorino", "endometroide", "adinoide"], ["neuroendocrino", "endometrioide", "adenoide"]),
            (["nospecifico", "inespecico", "intraducatal", "enfermedad paget"], ["no especifico", "inespecifico", "intraductal", "enfermedad de paget"]),
            (["linfoma hodkins", "linfoma no hodkins"], ["linfoma de hodgkin", "linfoma no de hodgkin"])
        ]

        self.__test("TYPE NORMALIZE", cmps)

if __name__ == "__main__" :
    norm_tester = NormalizersTest(normalizers)
    norm_tester.start()