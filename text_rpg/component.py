

class Component:
    """  组件  """

    __type__ = "base"

    def __init__(self, owner):
        pass

    def update(self, owner):
        pass

from typing import Iterable, Callable
from typing import TypeVar
from typing_extensions import ParamSpec, Concatenate
from _typeshed import SupportsKeysAndGetItem
from functools import wraps
from collections import defaultdict

TSelf = TypeVar("TSelf")
T = TypeVar("T")
P = ParamSpec("P")


def component_type_key(func:Callable[Concatenate[TSelf, str, P], T]) -> Callable[Concatenate[TSelf, str|type[Component], P], T]:
    @wraps(func)
    def wrapper(self:TSelf, key:str|type[Component], *args:P.args, **kw:P.kwargs):
        if hasattr(key, "__type__"):
            key:str = key.__type__
        return func(self, key, *args, **kw)
    return wrapper

class Components(defaultdict[str, list[Component]]):

    def __init__(self, _map:SupportsKeysAndGetItem | Iterable[tuple[str,list[Component]]]=None, **kw):
        """  对 defaultdict 的简单封装，用来装组件  """
        if _map is None:
            super().__init__(list, **kw)
        else:
            super().__init__(list, _map, **kw)

    def add(self, c:Component):
        """  添加一个组件  """
        self[c.__type__].append(c)

    @component_type_key
    def __getitem__(self, key):
        return super().__getitem__(key)
    
    @component_type_key
    def __setitem__(self, key, value):
        return super().__setitem__(key, value)

    @component_type_key
    def __delitem__(self, key):
        return super().__delitem__(key)
    
    @component_type_key
    def __contains__(self, key) -> bool:
        return super().__contains__(key)
    
    @component_type_key
    def get(self, key, default=None):
        return super().get(key, default)

    @component_type_key
    def pop(self, key, default=None):
        return super().pop(key, default)

    @component_type_key
    def setdefault(self, key, default=None):
        return super().setdefault(key, default)
