class TestException(Exception):
    __COLOR_FAIL = '\033[91m' #RED
    __COLOR_MODULE = '\033[93m' #YELLOW
    __COLOR_RESET = '\033[0m' #RESET COLOR

    def __str__(self):
        return self.__COLOR_FAIL + "<--- Fail Test ---> \n" + self.__COLOR_RESET 


class TestPreprocessException(TestException):

    def __init__(self, fail_module, text_expected, text_preprocess):
        self.msg = "Error in : " + fail_module
        self.text_preprocess = text_preprocess
        self.text_expected = text_expected

    def __str__(self):
        msg = super().__str__()
        msg += self.__COLOR_MODULE + self.msg + self.__COLOR_RESET
        msg += "\nText expected: '"+ self.text_expected +"'"
        msg += "\nText fixed: '"+ self.text_preprocess +"'"

        return msg

class TestNormalizerException(TestException):

    def __init__(self, fail_module, text_introduced, text_expected, text_normalized):
        self.msg = "Error in : " + fail_module
        self.text_normalized = text_normalized
        self.text_expected = text_expected
        self.text_introduced = text_introduced

    def __str__(self):
        msg = super().__str__()
        msg += self.__COLOR_MODULE + self.msg + self.__COLOR_RESET
        msg += "\nText introduced: \'" + str(self.text_introduced) + "\'"
        msg += "\nText expected: \'" + str(self.text_expected) + "\'"
        msg += "\nText fixed: \'" + str(self.text_normalized) + "\'"

        return msg
