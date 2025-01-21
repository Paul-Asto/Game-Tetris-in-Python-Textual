from typing import Literal
from abc import ABC, abstractmethod
from cardinal import Coord
from rich.text import Text
from rich.console import Console   

from tetrimino import Tetrimino_O




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



class Square:
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



class IBoard(ABC): 

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
    def square_is_empty(self, *coords: Coord) -> bool: ...    
    



class Board:
    default_color: Color = "red"

    size_y: int 
    size_x: int 

    content:tuple[tuple[Square]]

    def __init__(self, size_y: int, size_x: int):
        self.size_y = size_y
        self.size_x = size_x

        self.content = tuple([
            tuple([
                Square(self.default_color) for _ in range(self.size_x)
            ]) for _ in range(self.size_y)
        ])


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
            square.style = self.default_color
            square.is_occupiable = False


    def clear_content(self):
        for column in self.content:
            for square in column:
                square.style = self.default_color


    def get_square(self, coord: Coord) -> Square:
        return self.content[coord.y][coord.x]


    def is_valid_coords(self, *coords: Coord) -> bool:
        return all([
            0 <= coord.y < self.size_y and 0 <= coord.x < self.size_x
            for coord in coords
        ])


    def square_is_empty(self, *coords: Coord) -> bool:
        if not self.is_valid_coords(*coords):
            return False
        
        return all([not self.get_square(coord).is_occupiable for coord in coords])
    

    # Funcions Coords in Limits
    def in_max_limit_left(self, *coords: Coord) -> bool:
        return any([coord.x == 0 for coord in coords])


    def in_max_limit_right(self, *coords: Coord) -> bool:
        return any([coord.x == self.size_x - 1 for coord in coords])


    def in_max_limit_top(self, *coords: Coord) -> bool:
        return any([coord.y == 0 for coord in coords])


    def in_max_limit_bot(self, *coords: Coord) -> bool:
        return any([coord.y >= self.size_y - 1 for coord in coords])
    
    def in_max_limits(self, *coords: Coord) -> bool:
        return any((
            self.in_max_limit_top(*coords),
            self.in_max_limit_bot(*coords),
            self.in_max_limit_left(*coords),
            self.in_max_limit_right(*coords),
        ))


class TetrisBoard(Board):

    def __init__(self):
        self.size_y = 10
        self.size_x = 10
        super().__init__(self.size_y, self.size_x)
