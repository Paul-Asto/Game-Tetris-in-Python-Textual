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
        observed.add_observer(self)


    def react_changes(self): ...



class Observed:
    __observers: list["Observer"] 

    def __init__(self):
        self.__observers = []


    @property
    def observers(self) -> list["Observer"]: 
        return self.__observers

    
    def add_observer(self, observer: "Observer"): 
        self.__observers.append(observer)


    def report_changes(self):
        for observer in self.observers:
            observer.react_changes()
