from ncp.post.ent_normalizers.I_Normalize import I_Normalize
import ncp.post.string_similarity as ssim


class TratNormalizer(I_Normalize):

    def normalize(self, cts: list):
        values = [
            "tratamiento hormonal",
            "hormonoterapia",
            "radioterapia",
            "quimioterapia neoadyuvante",
            "tratamiento conservador",
            "cirugia",
            "quimioterapia",
            "radioterapia adyuvante",
            "adyuvante",
            "quimioradioterapia",
            "neoadyuvante",
            "con intencion neoadyuvante",
            "fotoquimioterapia",
            "tch adyuvante",
            "qtneoadyuvante",
            "tac",
            "neoadyuvancia",
            "tratamiento hormonal adyuvante",
            "tratamiento con hormona",
            "quimioterapia adyuvante",
            "neoadyuvantes",
            "tratamiento quirurgico",
            "tratamiento neoadyuvante",
            "radioterpia",
            "tratamiento adyuvante",
            "intervenida",
            "adyuvancia",
            "terapia dirigida",
            "inmunoterapia",
            "trasplante de médula ósea",
            "terapia de células CAR-T",
            "terapia dirigida molecularmente"]
        
        return ssim.replace_by_similar(cts, values)


class TratDrugNormalizer(I_Normalize):

    def normalize(self, cts: list):
        values = [
            "Abraxane",
            "Avastin",
            "Adriamicina",
            "Paclitaxel",
            "Capecitabina",
            "Ciclofosfamida",
            "Taxotere",
            "Anastrozol",
            "Carboplatino",
            "TCH",  # docetaxel, carboplatino, trastuzumab
            "Taxol",
            "Bevacizumab",
            "Aromasin",  # exemestano
            "Epirrubicina",
            "Tacx6",  # docetaxel, doxorubicina, ciclofosfamida, fluorouracilo
            "FECx6",  # fluorouracilo, epirrubicina, ciclofosfamida
            "Tamoxifeno",
            "Zometa",  # ácido zoledrónico
            "Doxorubicina",
            "Exemestano",
            "Gemcitabina",
            "Letrozol",
            "Loxifan",  # fulvestrant
            "Corticoides",  # como la dexametasona, prednisona, etc.
            "Cabazitaxel",
            "Pertuzumab",
            "Faslodex",  # fulvestrant
            "Trastuzumab",  # Herceptin
            "Zoladex",  # goserelina
            "Oxaliplatino",
            "Carbotaxol",  # carboplatino, paclitaxel
            "Docetaxel",
            "Herceptin",  # trastuzumab
            "Tamoxifeno",
            "Sorafenib",
            "Goserelina",
            "Avastin",  # bevacizumab
            "Apocrina",
            "Arimidex"  # anastrozol
        ]

        return ssim.replace_by_similar(cts, values)

class SurgeryNormalizer(I_Normalize):

    def normalize(self, surgs:list):
        values = [
            "linfadenectomia",
            "mastectomia",
            "tumorectomia",
            "biopsia",
            "reconstruccion",
            "mastectomia de reconstruccion",
            "talcaje"
        ]

        return ssim.replace_by_similar(surgs, values)