
from typing_extensions import Self

class Singleton:

    _instance:Self = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kw)
        return cls._instance

    @property
    def instance(self):
        return self._instance

