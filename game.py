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



    @property
    def current_tetrimino(self) -> "ITetrimino":
        return self.__current_tetrimino
    
    @current_tetrimino.setter
    def current_tetrimino(self, value: "ITetrimino"):
        self.__current_tetrimino = value
        self.__current_tetrimino.coord_core.set_value((1, 4))
        self.__current_tetrimino.board = self.board


    def run(self):
        self.current_tetrimino = self.disp_tetrimino.next_item
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
        
        self.file_collapse()
        
        self.current_tetrimino.reset()
        self.current_tetrimino = self.disp_tetrimino.next_item
        self.printTetrimino()


    def file_collapse(self):
        # get index files update
        index_files_update = [
            coord.y for coord in self.current_tetrimino.coords_blocks
            if self.board.file_is_occupiable(coord.y)
            ]
        
        index_files_update = list(set(index_files_update)) # se elminina repeticiones
        index_files_update.sort()

        if len(index_files_update) == 0:
            return

        # limpiando las filas actualizadas si estan llenas
        for index_update in index_files_update:
            self.board.clear_file(index_update)

        # iniciando colapso de filas flotantes
        for index_update in index_files_update:
            current_index = index_update

            while True:
                top_index = current_index - 1
                
                if not self.board.is_valid_coord_y(top_index):
                    break

                if self.board.file_is_empty(top_index):
                    break

                style_top_file = self.board.get_data_style_off_file(top_index)
                style_current_file = self.board.get_data_style_off_file(current_index)

                self.board.set_data_style_to_file(top_index, style_current_file)
                self.board.set_data_style_to_file(current_index, style_top_file)

                current_index -= 1


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
