from typing import Literal
from cardinal import Coord


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
    is_empty: bool = True

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



class Board:
    default_color: Color = "white"

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


    def __str__(self):
        result: str = ""

        for column in self.content:
            for square in column:
                if square.is_empty: 
                    result += ".."
                else: 
                    result += "[]"

            result += "\n"

        return result

        

    def print_coords(self, *coords: Coord):
        for coord in coords:
            square: Square = self.get_square(coord)
            square.is_empty = False


    def clear_coords(self, *coords: Coord):
        for coord in coords:
            square: Square = self.get_square(coord)
            square.is_empty = True


    def clear_content(self):
        for column in self.content:
            for square in column:
                square.style = self.default_color


    def get_square(self, coord: Coord) -> Square:
        return self.content[coord.y][coord.x]


    def square_is_empty(self, *coords: Coord) -> bool:
        return all([self.get_square(coord).is_empty for coord in coords])
    

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
