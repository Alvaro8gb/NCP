from ncp.post.ent_normalizers.I_Normalize import I_Normalize
import re

class Molec_Normalize(I_Normalize):

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
        

    def normalize(self, markers:list):
        normalized = {}

        for marker in markers:

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