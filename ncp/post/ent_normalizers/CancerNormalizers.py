from ncp.post.ent_normalizers.I_Normalize import I_Normalize
import ncp.post.string_similarity as ssim

class ConceptNormalizer(I_Normalize):

    def normalize(self, ccs:list):
        values = [
            "cancer", 
            "carcinoma", 
            "adenocarcinoma", 
            "adenoca", 
            "neoplasia", 
            "fibroma", 
            "fibrotecoma", 
            "fibroadenoma", 
            "mioma",
            "carcinomatosis"
        ]
            
        return ssim.replace_by_similar(ccs, values)
    
class ExpNormalizer(I_Normalize):
    
    def normalize(self, cexps:list):
        values = [
            "in situ", 
            "infiltrante", 
            "invasivo", 
            "microinfiltrante", 
            "multifocal", 
            "multicentrico", 
            "abundantes focos", 
            "multiples lineas", 
            "bifocal", 
            "unifocal", 
            "tres focos", 
            "cuatro focos"
        ]
            
        return ssim.replace_by_similar(cexps, values)
    

class GradeNormalizer(I_Normalize):

    def normalize(grade_list:list):
        if len(grade_list) == 1:
        
            numeros = re.findall(r'\d+', grade_list[0])
    
            if len(numeros) == 1:
                grado = numeros[1]

                if grado >=1 and grado <= 3:
                    return numeros[1]
            else:
                print(grade_list)
                pass
        else:
            print(grade_list)
            pass

class LocNormalizer(I_Normalize):

    def normalize(self, clcs:list):
        values = [
            "mama",
            "mama izquierda",
            "mama derecha",
            "izquierda",
            "derecha",
            "origen mamario",
            "bilateral",
            "linfovascular",
            "perineural"
        ]
        return ssim.replace_by_similar(clcs, values)

class TypeNormalizer(I_Normalize):
    
    def normalize(self, cts:list):
        values = [
            "lobulillar",
            "lobular",
            "ductal",
            "apocrino",
            "neuroendocrino",
            "endometrioide",
            "adenoide",
            "no especifico",
            "inespecifico",
            "intraductal",
            "enfermedad de paget",
            "phyllodes",
            "philoides",
            "filoides",
            "linfoma no de hodgkin",
            "linfoma de hodgkin",
        ]
        
        return ssim.replace_by_similar(cts, values)

class SubtypeNormalizer(I_Normalize):

    def normalize(self, csbts:list):
        values = [
            "clasico",
            "convencional",
            "medular",
            "papilar",
            "tubular",
            "mucosino",
            "coloide",
            "mucinoso",
            "mucoso",
            "mucinosa",
            "comedoniano",
            "comedo",
            "solido",
            "cribiforme",
            "micropapilar",
            "plano",
            "pleomorfico",
            "pleomorfica",
            "folicular"
        ]
        
        return ssim.replace_by_similar(csbts, values)
    

class IntrtypeNormalizer(I_Normalize):
    
    def normalize(self, elems:list):
        values = [
            "luminal A", 
            "luminal B", 
            "HER2 sobreexpresado", 
            "triple negativo"
        ]

        return ssim.replace_by_similar(elems, values)

        # ...

class MetNormalizer(I_Normalize):
    
    def normalize(self, cmts:list):
        values = [
            "metastasis",
            "micrometastasis",
            "progresion",
            "invasion",
            "infiltracion",
            "afeccion",
            "lesion"
        ]
        return ssim.replace_by_similar(cmts, values)
    
class RecNormalizer(I_Normalize):

    def normalize(self, crcs:list):
        values = [
            "recaida", 
            "recidiva", 
            "regresion"
        ]
        return ssim.replace_by_similar(crcs, values)