from typing import Generic, TypeVar

T = TypeVar("T")



class Observer(Generic[T]):
    __observed: "Observed" = None

    @property
    def observed(self) -> T: 
        if self.__observed == None:
            raise Exception("No se tiene un observed implementado")
        
        return self.__observed

    @observed.setter
    def observed(self, observed: "Observed"):
        self.__observed = observed
        observed.observer = self


    def react_changes(self): ...



class Observed:
    __observer: "Observer" = None

    @property
    def observer(self) -> "Observer": 
        if self.__observer == None:
            raise Exception("No se tiene un observer implementado")
        
        return self.__observer

    @observer.setter
    def observer(self, observer: "Observer"): 
        self.__observer = observer


    def report_changes(self):
        self.observer.react_changes()
