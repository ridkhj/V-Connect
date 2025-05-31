

from app.components.letter import Letter


class NslLetter (Letter):
    def __init__(self, code, letterCode ,name, type , status):
        super().__init__(code, letterCode ,name, type , status)
    
    
    def to_dict(self):
        return super().to_dict()