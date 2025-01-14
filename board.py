from typing import Literal


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


    def clear_content(self):
        for column in self.content:
            for square in column:
                square.style = self.default_color
        

class TetrisBoard(Board):

    def __init__(self):
        self.size_y = 10
        self.size_x = 10
        super().__init__(self.size_y, self.size_x)
