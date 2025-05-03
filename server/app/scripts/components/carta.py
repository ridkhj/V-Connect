class Carta:
    def __init__(self, code, letterCode ,name, type ,questions, status ):
        self._code = code
        self._name = name
        self._letterCode = letterCode
        self._type = type
        self._questions = questions
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
    def questions(self):
        return self._questions  
    
    @questions.setter
    def questions(self, value):
        self._questions = value
    
    @property
    def status(self):
        return self._status 
    
    @status.setter
    def status(self, value):
        self._status = value

    def strRelatorio(self):
        return f"{self._code} - {self._name}"