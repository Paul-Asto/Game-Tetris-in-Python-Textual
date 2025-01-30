from typing import Literal
from abc import ABC, abstractmethod
from observer_interface import Observed

from cardinal import Coord
from rich.text import Text



Color = Literal[
    "black",
    "grey",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "light_grey",
    "dark_grey",
    "light_red",
    "light_green",
    "light_yellow",
    "light_blue",
    "light_magenta",
    "light_cyan",
    "white",
]



class Square(Observed):
    freeze: bool = False
    is_occupiable: bool = False

    def __init__(self, style: Color):
        self.__style: Color = style
        

    @property
    def style(self) -> Color:
        return self.__style

    @style.setter
    def style(self, value: Color) -> Color:
        if self.style == value:
            return 
        
        self.__style = value
        self.report_changes()

    def get_data_style(self) -> tuple[str, bool]:
        return (self.style, self.is_occupiable)
    

    def set_data_style(self, data_style: tuple[str, bool]):
        style, is_ocuppiable = data_style

        self.style = style
        self.is_occupiable = is_ocuppiable



class IBoard(ABC): 
    content: list[list[Square]]

    @property
    @abstractmethod
    def view(self) -> Text: ...

    @abstractmethod
    def print_coords(self, *coords: Coord, style: str, is_ocupiable: bool): ...

    @abstractmethod
    def clear_coords(self, *coords: Coord): ...

    @abstractmethod
    def get_square(self, coord: Coord) -> Square: ...

    @abstractmethod
    def get_file(self, index: int) -> tuple[Square]: ...

    @abstractmethod
    def clear_square(self, square: Square): ...

    @abstractmethod
    def clear_file(self, index: int): ...

    @abstractmethod
    def clear_content(self): ...

    @abstractmethod
    def square_is_empty(self, *coords: Coord) -> bool: ...    

    @abstractmethod
    def square_is_occupiable(self, *coords: Coord) -> bool: ... 

    
    @abstractmethod
    def file_is_occupiable(self, index: int) -> bool: ...

    @abstractmethod
    def file_is_empty(self, index: int) -> bool: ...


    @abstractmethod
    def is_valid_coords(self, *coords: Coord) -> bool: ...

    @abstractmethod
    def is_valid_coord_y(self, index: int) -> bool: ...

    @abstractmethod
    def is_valid_coord_x(self, index: int) -> bool: ...


    @abstractmethod
    def get_data_style_off_file(self, index: int) -> tuple[tuple[str, int]]: ...

    @abstractmethod
    def set_data_style_to_file(self, index: int, tuple_data_style: tuple[tuple[str, int]]): ...




class Board(IBoard):
    default_color: Color = "white"

    size_y: int 
    size_x: int 

    content:list[list[Square]]


    def __init__(self, size_y: int, size_x: int):
        self.size_y = size_y
        self.size_x = size_x

        self.content = [
            [
                Square(self.default_color) for _ in range(self.size_x)
            ] for _ in range(self.size_y)
        ]


    @property
    def view(self):
        result: Text = Text()

        for column in self.content:
            for square in column:
                if square.is_occupiable:
                    result.append("[]", style= f"bold on {square.style}")  
                else: 
                    result.append("..", style= f"bold on {square.style}")

            result.append("\n")

        return result

        
    def print_coords(self, *coords: Coord, style: str, is_ocupiable: bool = True):
        for coord in coords:
            square: Square = self.get_square(coord)
            square.style = style
            square.is_occupiable = is_ocupiable


    def clear_coords(self, *coords: Coord):
        for coord in coords:
            square: Square = self.get_square(coord)
            self.clear_square(square)


    def clear_square(self, square: Square):
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


    def get_square(self, coord: Coord) -> Square:
        return self.content[coord.y][coord.x]
    

    def get_file(self, index: int) -> tuple[Square]:
        return tuple(self.content[index])


    def is_valid_coords(self, *coords: Coord) -> bool:
        return all([
            self.is_valid_coord_y(coord.y) and self.is_valid_coord_x(coord.x)
            for coord in coords
        ])
    

    def is_valid_coord_y(self, index: int) -> bool:
        return 0 <= index < self.size_y 


    def is_valid_coord_x(self, index: int) -> bool:
        return 0 <= index < self.size_x


    def square_is_empty(self, *coords: Coord) -> bool:
        if not self.is_valid_coords(*coords):
            return False
        
        return all([not self.get_square(coord).is_occupiable for coord in coords])
    

    def square_is_occupiable(self, *coords: Coord) -> bool:
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
    def in_max_limit_left(self, *coords: Coord) -> bool:
        return any([coord.x == 0 for coord in coords])


    def in_max_limit_right(self, *coords: Coord) -> bool:
        return any([coord.x == self.size_x - 1 for coord in coords])


    def in_max_limit_top(self, *coords: Coord) -> bool:
        return any([coord.y == 0 for coord in coords])


    def in_max_limit_bot(self, *coords: Coord) -> bool:
        return any([coord.y == self.size_y - 1 for coord in coords])    

    
    def in_max_limits(self, *coords: Coord) -> bool:
        return any((
            self.in_max_limit_top(*coords),
            self.in_max_limit_bot(*coords),
            self.in_max_limit_left(*coords),
            self.in_max_limit_right(*coords),
        ))
    

    def get_data_style_off_file(self, index) -> tuple[tuple[str, int]]:
        file = self.get_file(index)
        return tuple([square.get_data_style() for square in file])

    def set_data_style_to_file(self, index, tuple_data_style: tuple[tuple[str, int]]):
        file = self.get_file(index)

        for square, data_style in zip(file, tuple_data_style):
            square.set_data_style(data_style)
        



class TetrisBoard(Board):

    def __init__(self):
        self.size_y = 10
        self.size_x = 10
        super().__init__(self.size_y, self.size_x)
