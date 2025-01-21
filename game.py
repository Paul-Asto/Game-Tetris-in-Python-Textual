from typing import TYPE_CHECKING
from argparse import ArgumentParser

if TYPE_CHECKING:
    from tetrimino import ITetrimino
    from disp_tetrimino import IDispencer
    from board import IBoard


class TetrisGame:
    disp_tetrimino: "IDispencer[ITetrimino]"
    board: "IBoard"
    __current_tetrimino: "ITetrimino"

    def __init__(
            self,
            disp_tetrimino: "IDispencer[ITetrimino]",
            board: "IBoard",
        ):

        self.disp_tetrimino = disp_tetrimino
        self.board = board

        self.current_tetrimino = self.disp_tetrimino.next_item


    @property
    def current_tetrimino(self) -> "ITetrimino":
        return self.__current_tetrimino
    

    @current_tetrimino.setter
    def current_tetrimino(self, value: "ITetrimino"):
        self.__current_tetrimino = value
        self.__current_tetrimino.coord_core.set_value((1, 4))
        self.__current_tetrimino.board = self.board
        


    def run(self):
        self.printTetrimino()


    def printTetrimino(self):
        shadow_coords_blocks = self.current_tetrimino.shadow_coords_blocks
        color_shadow = self.current_tetrimino.color_shadow

        self.board.print_coords(
            *shadow_coords_blocks,
            style= color_shadow,
            is_ocupiable= False,
        )


        coords_blocks = self.current_tetrimino.coords_blocks
        color = self.current_tetrimino.color

        self.board.print_coords(
            *coords_blocks,
            style= color,
        )


    def clearTetrimino(self):
        self.board.clear_coords(*self.current_tetrimino.coords_blocks)
        self.board.clear_coords(*self.current_tetrimino.shadow_coords_blocks)


    def iteration(self):
        self.printTetrimino()

        if self.current_tetrimino.is_active:
            return
        
        self.current_tetrimino.reset()
        self.current_tetrimino = self.disp_tetrimino.next_item
        self.printTetrimino()


    # Funciones de movimiento

    def mov_max_bot(self):
        self.current_tetrimino.mov_max_bot()


    def mov_bot(self):
        self.current_tetrimino.mov_bot()


    def mov_left(self):
        self.current_tetrimino.mov_left()


    def mov_right(self):
        self.current_tetrimino.mov_right()


    def mov_rotate(self):
        self.current_tetrimino.rotate()
