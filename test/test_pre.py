import csv 

from ncp.pre.Preprocesing import Preprocesing

from test import TestPreprocessException

class PreprocesingTest:

    __COLOR_RESET = '\033[0m' #RESET COLOR
    __COLOR_GREEN = '\033[92m'

    def __init__(self, preprocesing, path_sentences):
        self.preprocesing = preprocesing
        self.path_sentences = path_sentences
        print("Unit Test to test class Preprocesing")

    def __check(self, in_text, expected_out_text, module):
        text_preprocess = self.preprocesing.fix(in_text)
        if text_preprocess != expected_out_text :
            raise TestPreprocessException(module, expected_out_text,  text_preprocess )

    def __test(self, module, cmps:list):

        for test, expected in cmps:
            self.__check(test, expected, module)

        print( module + self.__COLOR_GREEN + " all right" + self.__COLOR_RESET )


    def start(self, option=0):

        tests = [self.__basic_test(self.path_sentences), 
                self.__dates(), 
                self.__molec_marker(), 
                self.__acronims(), 
                self.__grades(), 
                self.__surgery(), 
                self.__general()]

        for t in tests:
            t

        print(self.__COLOR_GREEN+ "Everything all right" + self.__COLOR_RESET)

    def __basic_test(self, path):

        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quoting = csv.QUOTE_ALL)
            
            for row in reader:
                text = row[0]
                cmps = [(text, self.preprocesing.fix(text))]

        self.__test("Basic test", cmps)

    def __molec_marker(self):
        cmps = [ ("re-,rpg-, her2 neg","re- , rpg- , her2 neg"),
            ("re+/rp-/her2-/ki67 20%", "re+ / rp- / her2- / ki67 20%"),
            ("re-,rpg-, her2 neg","re- , rpg- , her2 neg")]

        self.__test("MOLEC_MARKER", cmps)
  
    def __dates(self):
        cmps = [(" 23.4.2022", "23-4-2022")]
        self.__test("DATES", cmps)

    def __grades(self):
        m = "CANCER_GRADE"
        cmps = [ ("izquierdag3", "izquierda g3")]
        self.__test(m, cmps)

    def __surgery(self):
        cmps = [ ("masectomia +bsgc", "masectomia + biopsia selectiva del ganglio centinela"),
            ("tumorectomia izquierda+lindanectomia. ", "tumorectomia izquierda + lindanectomia."),
            ("*mastectomia izquierda+bgc+reconstruccion inmediata enero 2010.","* mastectomia izquierda + biopsia ganglio centinela + reconstruccion inmediata enero 2010."),
            ("tratada con tumorectomia +la+rt +fecx6.","tratada con tumorectomia + la + radioterapia + fecx6.")]
        
        self.__test("SURGERY", cmps)

    def __acronims(self):
        cmps = [ ("cirugia conservadora+bsgc","cirugia conservadora + biopsia selectiva del ganglio centinela"),
            ("bsgc+masectomia","biopsia selectiva del ganglio centinela + masectomia"),
            ("cirugia conservadora+bsgc+masectomia","cirugia conservadora + biopsia selectiva del ganglio centinela + masectomia"),
            ("*qt","* quimioterapia"),
            ("*pte. biopsia","* pendiente biopsia")]
        
        self.__test("ACRONIMOS", cmps)

    def __general(self):
        m = "GENERAL : "

        cmps = [("estrogeno 30%progesterona 22%her-","estrogeno 30% progesterona 22% her-"),
                ("*diagnostico: ...\n *recaida en 1999:","* diagnostico: ...\n * recaida en 1999:")]
        self.__test(m + 'Añadir espacio despues de "%" o "*" seguido de cadena', cmps)

        cmps = [("en csi;tratada con qt;sin metastasis", "en cuadrante superior interno; tratada con quimioterapia; sin metastasis"),
                ("diagnostico:carcinoma ductal infiltrante csi;ganglios afectados:3/12", "diagnostico: carcinoma ductal infiltrante cuadrante superior interno; ganglios afectados: 3/12")]
        self.__test(m +'Añadir espacio tras cadena de texto seguido de signo de ";" o ":"', cmps)

        cmps = [("g2,re","g2, re"), 
                ("sin ilv.pendiente de tto con ht", "sin infiltracion linfovascular. pendiente de tratamiento con hormonoterapia")]
        self.__test(m + 'Añadir espacio tras signo de "," o "."  seguido de cadena)', cmps)
       
        cmps = [("estrogeno+progesterona+her-", "estrogeno + progesterona + her-")]
        self.__test(m + "Añadir espacio entre palabras unidas por un + y Añadir espacio entre + seguido de una palabra", cmps)

        cmps = [("bsgc(2 de 13 ganglios afectados)", "biopsia selectiva del ganglio centinela (2 de 13 ganglios afectados)"),
            ("... pendiente de ihq)tto con rt sobre ...", "... pendiente de inmunohistoquimica) tratamiento con radioterapia sobre ..."),
            ("rmi(junio 2000)sin tratamiento", "recontruccion mamaria interna (junio 2000) sin tratamiento")]

        self.__test(m + "Añadir espacio antes de cadena de texto seguido de ( y Añadir espacio tras cadena de texto seguida de )", cmps)

        cmps = [("cancer -mama izquierda", "cancer - mama izquierda")]
        self.__test(m + "Añadir espacio entre guion y letra , cuando antes del guion hay un espacio", cmps)

        cmps = [("-diagnostico:carcinoma ...", "- diagnostico: carcinoma ...")]
        self.__test("Añadir espacio entre guion y letra , cuando empieza la sentencia por guion", cmps)


if __name__ == "__main__" :
    ppg = Preprocesing("ncp/pre/acronimos.json")
    PreprocesingTest(ppg, "test/test_sentences.csv").start()
