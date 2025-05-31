
from calendar import c
from app.components.letter import Letter

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

    def to_dict(self):

        parent_dict = super().to_dict()
        child_dict = {
            'questions': self._questions,
            'ageBracket': self._ageBracket
        }   
        parent_dict.update(child_dict)
    
        return parent_dict