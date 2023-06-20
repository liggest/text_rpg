from typing import Callable, ParamSpec, TypeVar

from text_rpg.event import CallBackType

CallBackParam = ParamSpec("CallBackParam")
CallBackReturn = TypeVar("CallBackReturn")
CallBackType = Callable[CallBackParam, CallBackReturn]

class Event:
    """  事件  """

    def _register(self, func:CallBackType):
        raise NotImplementedError

    def register(self, func:CallBackType) -> CallBackType:
        """  为事件注册回调函数  """
        self._register(func)
        return func

    def emit(self, *args:CallBackParam.args, **kw:CallBackParam.kwargs) -> CallBackReturn:
        """  触发事件  """
        raise NotImplementedError
    
    __call__ = emit

    def _unregister(self, func:CallBackType):
        raise NotImplementedError

    def unregister(self, func:CallBackType) -> CallBackType:
        """  为事件移除回调函数  """
        self._unregister(func)
        return func

    def clear(self):
        """  清空事件的回调函数  """
        raise NotImplementedError


class SingleEvent(Event):

    _callback = None

    def _register(self, func):
        self._callback = func

    def emit(self, *args, **kw):
        if self._callback:
            return self._callback(*args, **kw)
    
    def _unregister(self, func):
        if func and func == self._callback:
            self.clear()
    
    def clear(self):
        if self._callback is not self.__class__._callback:
            del self._callback

class MultipleEvent(Event):

    __callbacks:list[CallBackType] = None

    @property
    def _callbacks(self):
        if not self.__callbacks:
            self.__callbacks = []
        return self.__callbacks

    @_callbacks.deleter
    def _callbacks(self):
        if self.__callbacks:
            self.__callbacks.clear()
        self.__callbacks = None

    def _register(self, func):
        self._callbacks.append(func)

    def emit(self, *args, **kw) -> list[tuple[CallBackType, CallBackReturn]]:
        return [(call, call(*args, **kw)) for call in self._callbacks]
    
    def _unregister(self, func):
        self._callbacks.remove(func)

    def clear(self):
        del self._callbacks
            
