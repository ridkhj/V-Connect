
class Cdpr:
    def __init__(self, code, name, age):
        self._code = code
        self._name = name
        self._age = age
        
        # self._overdue = overdue

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = value

    def strRelatorio(self):
        return f"{self._code} - {self._name}"