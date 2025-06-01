
from app.components.letter import Letter

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

    def to_dict(self):
        
        parent_dict = super().to_dict()
        child_dict = {
            'questions': self._questions
        } 
        parent_dict.update(child_dict)
        return parent_dict