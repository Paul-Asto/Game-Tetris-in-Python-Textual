from abc import ABC, abstractmethod
from typing import TypeVar, Generic, TYPE_CHECKING
from random import choice

if TYPE_CHECKING:
    from src.core_game.tetrimino import Tetrimino


T = TypeVar("T")


class ProviderRandomNumbers:

    def __init__(self, start: int, end: int):
        self.start: int = start
        self.end: int = end

        self.content: list[int] = list(range(start, end))
        pass

    @property
    def is_empty(self) -> bool:
        return len(self.content) == 0
    
    @property
    def next_item(self) -> int:
        if self.is_empty:
            self.reset_content()

        item = self.get_item()
        
        return item
    
    def get_item(self) -> int:
        item = choice(self.content)
        self.content.remove(item)
        return item
    
    def reset_content(self):
        self.content = list(range(self.start, self.end))



class IDispencer(ABC, Generic[T]):

    @property
    @abstractmethod
    def content(self) -> list[T]: ...

    @property
    @abstractmethod
    def next_item(self) -> T: ...

    @abstractmethod
    def reset(self): ...



class Queue(IDispencer[T]):

    def __init__(self):
        self.queues: list[T] = []


    @property
    def is_empty(self) -> bool:
        return len(self.queues) == 0


    @property
    def content(self) -> list[T]:
        return self.queues


    @property 
    def next_item(self) -> T: 
        if self.is_empty:
            raise IndexError("No hay elementos en la cola")
        
        return self.queues.pop(0)
    
    
    def add_item(self, item: T):
        self.queues.append(item)

    def reset(self):
        self.queues.clear()



class DispencerTetrimino(IDispencer["Tetrimino"]):
    pieces: tuple["Tetrimino"] 
    queues: Queue["Tetrimino"]
    provider_index: ProviderRandomNumbers

    def __init__(self, *pieces: "Tetrimino"):
        super().__init__()

        self.pieces = pieces
        self.queues = Queue()
        self.provider_index = ProviderRandomNumbers(0, len(self.pieces))

        self.add_item()
        self.add_item()
        self.add_item()
    

    @property
    def content(self) -> list["Tetrimino"]:
        return self.queues.content
    
    
    @property
    def next_item(self) -> "Tetrimino":
        if self.queues.is_empty:
            raise IndexError("No hay elementos en la cola")
        
        self.add_item() 
        return self.queues.next_item
    

    def add_item(self):
        self.queues.add_item(self.pieces[self.provider_index.next_item])


    def reset(self):
        self.queues.reset()
        self.provider_index.reset_content()

        self.add_item()
        self.add_item()
        self.add_item()