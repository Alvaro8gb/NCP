import json
import re
import json
from abc import ABC, abstractmethod

from textacy.preprocessing import normalize as normalize

class TextProcessor(ABC):
    @abstractmethod
    def convert(self, text:str)->str:
        pass

class Cleaner(TextProcessor):

    __REPLACEMENTS = [('`',""),('"',''),("\n  \n","\n")]

    def convert(self, text: str) -> str:

        # Eliminar espacios al principio o al final 
        text = text.strip()

        # Eliminar repeticiones de comas y espacios en blanco
        text = normalize.whitespace(text)
        text = normalize.repeating_chars(text, chars=",")
        text = normalize.repeating_chars(text, chars=":")
        text = normalize.repeating_chars(text, chars=";")

        # Eliminar caracteres no interesantes
        for old, new in self.__REPLACEMENTS:
            text = text.replace(old, new)

        return text


class PuntuactionFormater(TextProcessor):

    def convert(self, text: str) -> str:
         # Añadir espacio despues de "%" o "*" o "-" seguido de cadena
        text = re.sub(r"(%|\*|-)([a-z]+)", r"\1 \2", text) 

        # Añadir espacio tras cadena de texto seguido de signo de ";" o ":" 
        text = re.sub(r"([a-z])([:;])(\S)", r"\1\2 \3", text) 

        # Añadir espacio tras signo de "," o "."  seguido de cadena
        #self.__regex_show_test(text,r"(,|\.)([a-zA-Z]+)")
        text = re.sub(r"(,|\.)([a-zA-Z])", r"\1 \2", text) 
        
        # Añadir espacio entre palabras unidas por un "+""
        text = re.sub(r"([a-z])(\+)([a-z])", r"\1 \2 \3", text)

        # Añadir espacio entre "+"" seguido de una palabra
        text = re.sub(r"(\+)([a-z])", r"\1 \2", text)

        # Añadir espacio antes de cadena de texto seguido de (
        text = re.sub(r"([a-z])(\()", r"\1 \2", text)

        # Añadir espacio tras cadena de texto seguida de )
        text = re.sub(r"(\))([a-z])", r"\1 \2", text)
        
        # Añadir espacio entre guion y letra , cuando antes del guion hay un espacio
        text = re.sub(r"(\s)(-)([a-zA-Z])", r"\1\2 \3", text)

        # Añadir espacio entre guion y letra , cuando empieza la sentencia por guion
        text = re.sub(r"(\A-)([a-zA-Z])", r"\1 \2", text)

        return text
    
class Deacronimizer(TextProcessor):

    def __init__(self, acronimns) -> None:
        super().__init__()
        self.acronims = acronimns

    def convert(self, text: str) -> str:
        
        for old, new in self.acronims:
            regex = r"(\s|\(|\A)"+"("+old+")"+r"([\s),;:])"
            replace = r"\1"+ new +r"\3"
    
            #self.__regex_show_test(text, regex)
            text = re.sub(regex, replace, text)

        for old, new in self.acronims:
            regex = r"(\s|\(|\A)"+"("+old+")"+r"($)"
            replace = r"\1"+ new +r"\3"

            #self.__regex_show_test(text, regex)
            text = re.sub(regex, replace, text)

        for old, new in self.acronims:
            regex = r"(\s|\(|\A)"+"("+old+")"+r"(\.)"
            replace = r"\1"+ new 
    
            #self.__regex_show_test(text, regex)
            text = re.sub(regex, replace, text)

        return text

class SpecialDeacronimizer(TextProcessor):

    def __init__(self, acronimns) -> None:
        super().__init__()
        self.acronims = acronimns

    def convert(self, text: str) -> str:

        for old, new in self.acronims:
            regex = r"(\s|\(|\A)"+"("+old+")"+r"(\.)([a-z])"
            replace = r"\1"+ new + r"\3\4"
    
            #self.__regex_show_test(text, regex)
            text = re.sub(regex, replace, text)
        
        text = re.sub(r"n\.o\.s.", "nos", text) # n.o.s.

        return text
        
class DatesFormater(TextProcessor):
     def convert(self, text: str) -> str:
        """

         Normalizar fechas del estilo 2015.05.29 -> 2015-05-29

        """
  
        #self.__regex_show_test(text, r"([0-9]{1,4})\.([0-9]{1,2})\.([0-9]{2,4})")

        text = re.sub( r"([0-9]{1,4})\.([0-9]{1,2})\.([0-9]{2,4})", r"\1-\2-\3", text)

        return text
     
class MolecMarkerFormater(TextProcessor):
    def convert(self, text: str) -> str:
        """
         Normalizar molec markers 

        (1) re+/rp-/her2-/ki67 20%" ->  "re+ / rp- / her2- / ki67 20%" 
        (2) "re-,rpg-, her2 neg" -> "re-, rpg-, her2 neg"
        
        """

        # (1)
        text = re.sub( r"([\+\-])(/)([a-z])", r"\1 \2 \3", text)

        # (2)
        text = re.sub(r"(-)(,)", r"\1 \2", text)

        return text
    

class GradeFormater(TextProcessor):
        
    def convert(self, text: str) -> str:
     # Meter espacio entre g3\
        #self.__regex_show_test(text,r"(g[123])(/)")
        text = re.sub(r"(g[123])(/)", r"\1 \2", text)

        #self.__regex_show_test(text,r"([aeiou])(g[123])")
        text = re.sub(r"([aeiou])(g[123])", r"\1 \2", text) # !!!!
        
        return text


class Preprocesing:

    __acronims = [] # list of tuples -> be careful with not using a regex character

    def __init__(self, path_acronims):
        self.__acronims = self.__load_acronims(path_acronims)
        # print("\n","---"*20+"\n",pd.DataFrame(self.__acronims,columns=["Acronimo","Significado"]),"\n","---"*20+"\n",)
        
    def fix(self, text):
   
        steps = [ Cleaner(), DatesFormater(), MolecMarkerFormater(), 
                 GradeFormater(), SpecialDeacronimizer(self.__acronims), PuntuactionFormater(),
                 Deacronimizer(self.__acronims)]
        
        for step in steps:
            text = step.convert(text)

        return text
  
    def __regex_show_test(self, text, regex):

        match = re.search(regex,text)

        if match != None : 
            print(match.group())
            #print(text)

    def __load_acronims(cls, path):
        with open(path) as f :
            dict_acro = json.load(f)

        return dict_acro["acronimos"]

