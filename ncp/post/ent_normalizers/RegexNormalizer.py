from ncp.post.ent_normalizers.I_Normalize import I_Normalize
import ncp.post.string_similarity as ssim
import regex as re

class TnmNormalize(I_Normalize):

    def __init__(self) -> None:
        super().__init__()
        self.pattern = self.__getTnmRE()
    
    def normalize(self, tnm:str):
        
        finds = self.pattern.findall(tnm)
        if len(finds) == 0:
            return tnm
        
        tnm_tuple = finds[0]
        structured_tnm = {
                "t": "",
                "n": "",
                "m": ""
        }

        ts = ["ti", "tI", "tx", "tX", "t0", "t1", "t2", "t3", "t4", "TI", "Ti", "TX", "Tx", "T0", "T1", "T2", "T3", "T4"]
        ns = ["ni", "nI", "nx", "nX", "n0", "n1", "n2", "n3", "n4", "NI", "Ni", "NX", "Nx", "N0", "N1", "N2", "N3", "N4"]
        ms = ["mi", "mI", "mx", "mX", "m0", "m1", "m2", "m3", "m4", "MI", "Mi", "MX", "Mx", "M0", "M1", "M2", "M3", "M4"]

        for elem in tnm_tuple:
            result = elem.strip()
            for char in result:
                if char in [",", ".", ";"]:
                    result = result.replace(char, "")

            if any(t in elem for t in ts):
                
                structured_tnm["t"] = result
            elif any(n in elem for n in ns):
                structured_tnm["n"] = result
            elif any(m in elem for m in ms):
                structured_tnm["m"] = result

        return structured_tnm
    
    @staticmethod
    def __getTnmRE():
        tnmPrefixString = r"( (\(?[my]\)?)? (\(?[cp]\)?)? (\(?[my]\)?)? )"
        separatorString = r"([ \t]*[.:;,_]?[ \t]*)"

        return re.compile(
            # T - Tumor
            r"\b((?P<"+"tnm"+"TPrefix_all" 
                + r">"+tnmPrefixString+r")"
            # c = clinical staging (prior to surgery or neoadjuvant therapy)
            # p = pathological staging (defined at surgery)
            # y = post neoadjuvant therapy 
            + r" T"
            + r" (?P<"+"tnm"+"TCategory"
            +     r">"
            + r"  [X0-4]|"
            + r"  is|" # in situ 
            + r"  (is[ \t]*\(?Paget'?[ \t]*s?\)?)|" # in situ paget
            + r"  (is[ \t]*\(?(DCIS)|(DIN)|(ADH)|(LCIS)\)?)" # in situ 
            # DCIS = ductal carcinoma in situ (prev. Intraductal carcinoma)
            # DIN = Ductal intraepithelial neoplasia
            # ADH = atypical ductal hyperplasia
            # LCIS = lobular in situ *removed in 8th edition!
            + r" )"
            + r" (?P<"+"tnm"+"TSubCat"
            +     r">"
            + r"  ((?<=[14])(\(?mic?\)?|[a-d]))?"
            + r" )"
            + separatorString # optional separator/whitespace
            + r" (\(?(?P<"+"tnm"+"NFNA"
            +        r">f)\)?)?" # fine needle aspiration
            + r" (\(?(?P<"+"tnm"+"TSN"
            +        r">sn)\)?)?" # sentinel lymphNode biopsy
            + r" (\((?P<"+"tnm"+"TMultifoc"
            +        r">m\d*([.,]\d+)?(cm|mm)?)\)?)?" # multifocal tumor
            + r")" # Always require a T section!
            + separatorString # optional separator/whitespace
            # optional tumor size 
            + r"(\([ \t]*(?P<"+"tnm"+"TSizemm"
            +       r">\d+([.,]\d+)?)"
            + r" [ \t]*mm([ \t]|en|ecograf[ií]a)*\))?"
            + r"(\([ \t]*(?P<"+"tnm"+"TSizecm"
            +       r">\d+([.,]\d+)?)"
            + r" [ \t]*cm([ \t]|en|ecograf[ií]a)*\))?"
            + separatorString # optional separator/whitespace
            ##
            # N - Regional Nodes
            + r"((?P<"+"tnm"+"NPrefix_all"
            +     r">"+tnmPrefixString+r")"
            # see comments in T group
            + r" N"
            + r" (?P<"+"tnm"+"NCategory"
            +     r">"
            + r"  [X0-3]"
            + r" )"
            + r" (?P<"+"tnm"+"NSubCat"
            +     r">"
            + r"  (((?<=0)"
            + r"    ([ \t]*\(?[ \t]*(mol|i)[ \t]*[+]?[ \t]*\)?))|"
            + r"   ((?<=[1-3])(\(?mic?\)?|[a-c])))?"
            + r" )"
            + separatorString # optional separator/whitespace
            + r" (\(?(?P<"+"tnm"+"NFNA"
            +        r">f)\)?)?" # fine needle aspiration
            + r" (\(?(?P<"+"tnm"+"NSN"
            +        r">sn)\)?)?" # sentinel lymph node biopsy
            + separatorString # optional separator/whitespace
            + r" (\([ \t]*(?P<"+"tnm"+"NAffectNode"
            +        r">\d+)[ \t]*\+?[ \t]*\/[ \t]*" 
            + r"    (?P<"+"tnm"+"NExtractNode"
            +        r">\d+)[ \t]*(GC)?[ \t]*\))?" # affected/extracted nodes
            + r" (\(|\)|[ \t]|por|lo|al|menos|como|m[íi]nimo)*" # optional comment
            + r")" #  Always require a N section!
            + separatorString # optional separator/whitespace
            ##
            # M - Distant Metastases
            + r"((?P<"+"tnm"+"MPrefix_all" 
            +     r">"+tnmPrefixString+r")"
            # see comments in T group
            + r" M"
            + r" (?P<"+"tnm"+"MCategory"
            +     r">"
            + r"  [X01]"
            + r" )"
            + r" (?P<"+"tnm"+"MSubCat" 
            +     r">"
            + r"  (((?<=0)"
            + r"    ([ \t]*\(?[ \t]*(mol|i)[ \t]*[+]?[ \t]*\)?))|"
            + r"   ((?<=1)[a-c]))?"
            + r" )"
            + r")?", # Allow M to be optional
            ##
            # Other optional qualifiers at the end
            #  + r"(S(?P<"++">([0-3]|X)(C[1-5])?))|" # elevation of the serum tumor markers
            #  C1-5 is a certainty modifier optional in all
            #  + r"(R(?P<"++">([0-2]|X)(C[1-5])?))|" # the completeness of the operation
            #  + r"(L(?P<"++">(0|1|1a|1b|1ab|V0|V1|X)(C[1-5])?))|" # invasion into lymph vessels
            #  + r"(V(?P<"++">(0|1|1a|1b|1ab|2|X)(C[1-5])?))|" # invasion into vein
            #  + r"(LYM(?P<"++">(\(?[0-9]\\?[0-9][0-9]\)?)(C[1-5])?)) "
            re.X | re.IGNORECASE)

class MolecNormalize(I_Normalize):

    def __split(self, text):
        text = re.sub(r"([^ ,\.;:]*)([,\.;:])([^ ,\.;:]*)", r"\1 \2 \3", text)

        text = re.sub(r"\(([^ ]*)\)", r"\( \1 \)", text)
        text = re.sub(r"\(([^ ]*)", r"\( \1 ", text)
        text = re.sub(r"([^ ]*)\)", r" \1 \)", text)

        text = re.sub(r"rec[a-z]* hor[a-z]*", r"rh", text)
        text = re.sub(r"her[-]*[2]*[^ \+\-]*", r"her2", text)

        text = re.sub(r"(ki)( )*([^ 67])", r"ki67 \3", text)
        text = re.sub(r"(ki)( )*(67)([^ ]*)", r"ki67 \4", text)
        text = re.sub(r"(rey)([^ ])", r"re y \2", text)
        text = re.sub(r"(ryp)([^ ])", r"re y \2", text)

        text = re.sub(r"([a-z]+)(\d+(\.\d+)?%)", r" \1 \2 ", text)
        text = re.sub(r"(\d+(\.\d+)?\-\d+(\.\d+)?%)", r" \1 ", text)

        text = re.sub(r"(^[^ ]*)\-", r"\1 -", text)
        text = re.sub(r"(^[^ ]*)\+", r"\1 +", text) 

        return text.split()
        

    def normalize(self, marker:str):
        normalized = {}

        mdict = {
            "numerico": "",
            "estado": ""
        }

        mlist = self.__split(marker)

        for elem in mlist:
            elem = re.sub(r"pos[a-z]*", r"+", elem)
            elem = re.sub(r"neg[a-z]*", r"-", elem)
            elem = re.sub(r"estr[a-z]*", r"re", elem)
            elem = re.sub(r"prog[a-z]*", r"rp", elem)

            if elem == "e":
                elem = "re"
            if elem == "p":
                elem = "rp"

            if elem in ["re", "rp", "her2", "ki67"]:
                normalized[elem] = mdict
            if elem == "rh":
                normalized["re"] = mdict
                normalized["rp"] = mdict
            if elem[len(elem) - 1] == "%" or elem.isnumeric():
                mdict["numerico"] = elem
            if elem in ["+", "-"]:
                mdict["estado"] = elem

        return normalized


class GradeNormalizer(I_Normalize):

    def normalize(self, grade:str):
        #if len(grade_list) == 1:
        #
        #    numeros = re.findall(r'\d+', grade_list[0])
    #
        #    if len(numeros) == 1:
        #        grado = numeros[1]
#
        #        if grado >=1 and grado <= 3:
        #            return numeros[1]
        #    else:
        #        print(grade_list)
        #        pass
        #else:
        #    print(grade_list)
        #    pass
        
        return grade