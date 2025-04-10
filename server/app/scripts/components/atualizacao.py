class Atualizacao:
    def __init__(self, code, name, status):
        self._code = code
        self._name = name
        self._status = status
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
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def strRelatorio(self):
        return f"{self._code} - {self._name}"