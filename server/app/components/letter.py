class Letter:
    def __init__(self, code, letterCode ,name, type , status):
        
        self._code = code
        self._name = name
        self._letterCode = letterCode
        self._type = type
        self._status = status
        

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def letterCode(self):
        return self._letterCode
    
    @letterCode.setter
    def letterCode(self, value):
        self._letterCode = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value):
        self._type = value  
    
    @property
    def status(self):
        return self._status 
    
    @status.setter
    def status(self, value):
        self._status = value

    def strRelatorio(self):
        return f"{self._code} - {self._name}"
    

class ReciprocalLetter (Letter):
    def __init__(self, code, letterCode ,name, type , status, ageBracket, questions):
        super().__init__(code, letterCode ,name, type , status)
        self._questions= questions
        self._ageBracket = ageBracket
    
    @property
    def ageBracket(self):
        return self._ageBracket
    
    @ageBracket.setter
    def ageBracket(self, value):
        self._ageBracket = value
    
    @property
    def questions(self):
        return self._questions
    
    @questions.setter
    def questions(self, value):
        self._questions = value

class NslLetter (Letter):
    def __init__(self, code, letterCode ,name, type , status):
        super().__init__(code, letterCode ,name, type , status)


class ThankyouLetter (Letter):
    def __init__(self, code, letterCode ,name, type , status, questions):
        super().__init__(code, letterCode ,name, type , status)
        self._questions= questions
        
    @property
    def questions(self):
        return self._questions
    
    @questions.setter
    def questions(self, value):
        self._questions = value
        


