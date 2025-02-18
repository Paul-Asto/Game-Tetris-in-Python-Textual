from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, Generic


if TYPE_CHECKING:
    from src.cardinal import Coord
    from src.color import Color



class Square:
    freeze: bool = False
    is_occupiable: bool = False

    def __init__(self, style: "Color"):
        super().__init__()

        self.__style: "Color" = style
        

    @property
    def style(self) -> "Color":
        return self.__style

    @style.setter
    def style(self, value: "Color") -> "Color":
        if self.style == value:
            return 
        
        self.__style = value


    def get_data_style(self) -> tuple[str, bool]:
        return (self.style, self.is_occupiable)
    

    def set_data_style(self, data_style: tuple[str, bool]):
        style, is_ocuppiable = data_style

        self.style = style
        self.is_occupiable = is_ocuppiable



TYPE_SQUARE = TypeVar('type_block', bound= Square)



class IBoard(ABC, Generic[TYPE_SQUARE]): 
    content: list[list[TYPE_SQUARE]]
    size_y: int 
    size_x: int 

    @abstractmethod
    def print_coords(self, *coords: "Coord", style: str, is_ocupiable: bool): ...

    @abstractmethod
    def clear_coords(self, *coords: "Coord"): ...

    @abstractmethod
    def get_square(self, coord: "Coord") -> TYPE_SQUARE: ...

    @abstractmethod
    def get_file(self, index: int) -> tuple[TYPE_SQUARE]: ...

    @abstractmethod
    def clear_square(self, square: TYPE_SQUARE): ...

    @abstractmethod
    def clear_file(self, index: int): ...

    @abstractmethod
    def clear_content(self): ...

    @abstractmethod
    def square_is_empty(self, *coords: "Coord") -> bool: ...    

    @abstractmethod
    def square_is_occupiable(self, *coords: "Coord") -> bool: ... 

    
    @abstractmethod
    def file_is_occupiable(self, index: int) -> bool: ...

    @abstractmethod
    def file_is_empty(self, index: int) -> bool: ...


    @abstractmethod
    def is_valid_coords(self, *coords: "Coord") -> bool: ...

    @abstractmethod
    def is_valid_coord_y(self, index: int) -> bool: ...

    @abstractmethod
    def is_valid_coord_x(self, index: int) -> bool: ...


    @abstractmethod
    def get_data_style_off_file(self, index: int) -> tuple[tuple[str, int]]: ...

    @abstractmethod
    def set_data_style_to_file(self, index: int, tuple_data_style: tuple[tuple[str, int]]): ...

    @abstractmethod
    def trade_style_files(self, index_file_a: int, index_file_b: int): ...



class Board(IBoard[TYPE_SQUARE], Generic[TYPE_SQUARE]):
    default_color: "Color" = "white"

    size_y: int 
    size_x: int 

    content:list[list[TYPE_SQUARE]]
    cls_square: TYPE_SQUARE

    def __init__(self, size_y: int, size_x: int, cls_square: TYPE_SQUARE = Square):
        self.size_y = size_y
        self.size_x = size_x
        
        self.cls_square = cls_square

        self.content = self.init_content()


    def init_content(self):
        return [
            [
                self.cls_square(self.default_color) for _ in range(self.size_x)
            ] for _ in range(self.size_y)
        ]

        
    def print_coords(self, *coords: "Coord", style: str, is_ocupiable: bool = True):
        for coord in coords:
            square = self.get_square(coord)
            square.style = style
            square.is_occupiable = is_ocupiable


    def clear_coords(self, *coords: "Coord"):
        for coord in coords:
            square = self.get_square(coord)
            self.clear_square(square)


    def clear_square(self, square: TYPE_SQUARE):
        square.style = self.default_color
        square.freeze = False
        square.is_occupiable = False


    def clear_content(self):
        for column in self.content:
            for square in column:
                self.clear_square(square)


    def clear_file(self, index: int):
        for square in self.get_file(index):
            self.clear_square(square)


    def get_square(self, coord: "Coord") -> TYPE_SQUARE:
        return self.content[coord.y][coord.x]
    

    def get_file(self, index: int) -> tuple[TYPE_SQUARE]:
        return tuple(self.content[index])


    def is_valid_coords(self, *coords: "Coord") -> bool:
        return all([
            self.is_valid_coord_y(coord.y) and self.is_valid_coord_x(coord.x)
            for coord in coords
        ])
    

    def is_valid_coord_y(self, index: int) -> bool:
        return 0 <= index < self.size_y 


    def is_valid_coord_x(self, index: int) -> bool:
        return 0 <= index < self.size_x


    def square_is_empty(self, *coords: "Coord") -> bool:
        if not self.is_valid_coords(*coords):
            return False
        
        return all([not self.get_square(coord).is_occupiable for coord in coords])
    

    def square_is_occupiable(self, *coords: "Coord") -> bool:
        if not self.is_valid_coords(*coords):
            return False
        
        return all([self.get_square(coord).is_occupiable for coord in coords])
    

    def file_is_empty(self, index: int) -> bool:
        if not self.is_valid_coord_y(index):
            return False
        
        return all([not square.is_occupiable for square in self.get_file(index)])
        

    def file_is_occupiable(self, index: int) -> bool:
        if not self.is_valid_coord_y(index):
            return False
        
        return all([square.is_occupiable for square in self.get_file(index)])
        

    # Funcions Coords in Limits
    def in_max_limit_left(self, *coords: "Coord") -> bool:
        return any([coord.x == 0 for coord in coords])


    def in_max_limit_right(self, *coords: "Coord") -> bool:
        return any([coord.x == self.size_x - 1 for coord in coords])


    def in_max_limit_top(self, *coords: "Coord") -> bool:
        return any([coord.y == 0 for coord in coords])


    def in_max_limit_bot(self, *coords: "Coord") -> bool:
        return any([coord.y == self.size_y - 1 for coord in coords])    


    def get_data_style_off_file(self, index) -> tuple[tuple[str, int]]:
        file = self.get_file(index)
        return tuple([square.get_data_style() for square in file])


    def set_data_style_to_file(self, index, tuple_data_style: tuple[tuple[str, int]]):
        file = self.get_file(index)

        for square, data_style in zip(file, tuple_data_style):
            square.set_data_style(data_style)
        

    def trade_style_files(self, index_file_a: int, index_file_b: int):
        style_a = self.get_data_style_off_file(index_file_a)
        style_b = self.get_data_style_off_file(index_file_b)

        self.set_data_style_to_file(index_file_a, style_b)
        self.set_data_style_to_file(index_file_b, style_a)



