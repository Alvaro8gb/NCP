import re

def normalize(grade_list:list):
    if len(grade_list) == 1:

        numeros = re.findall(r'\d+', grade_list[0])

        if len(numeros) == 1:
            return numeros[1]
        else:
            pass
    else:
        print()
        pass