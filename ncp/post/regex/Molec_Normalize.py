import re
import I_Normalize

class Molec_Normalize(I_Normalize):

    def tokenize(text):
        tokens = []
        text = re.sub(r"([^ ,\.;:]*)([,\.;:])([^ ,\.;:]*)", r"\1 \2 \3", text)
        text = re.sub(r"\(([^ ]*)\)", r"\( \1 \)", text)
        text = re.sub(r"rec[a-z]* hor[a-z]*", r"rh", text)
        text = re.sub(r"her[-]*[2]*[^ \+\-]*", r"her2", text)
        text = re.sub(r"([^ ])\-", r"\1 -", text)
        text = re.sub(r"([^ ])\+", r"\1 +", text)
        tokens = text.split()
        return tokens

    def normalize(text, vocab):
        str_list = tokenize(text)
        result = []

        for i in range(0, len(str_list)):
            str = str_list[i]
            str = re.sub(r"pos[a-z]*", r"+", str)
            str = re.sub(r"neg[a-z]*", r"-", str)
            str = re.sub(r"estr[a-z]*", r"re", str)
            str = re.sub(r"prog[a-z]*", r"rp", str)
             
            if str in vocab or str[len(str) - 1] == "%":
                result.append(str)

        return result
