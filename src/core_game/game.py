from typing import TYPE_CHECKING
from src.cardinal import Coord

if TYPE_CHECKING:
    from src.core_game.tetrimino import ITetrimino
    from src.core_game.disp_tetrimino import IDispencer
    from src.core_game.board import IBoard, Square
    from src.core_game.data_games import IAdminDataGame


class TetrisGame:
    disp_tetrimino: "IDispencer[ITetrimino]"
    board: "IBoard"
    __current_tetrimino: "ITetrimino"

    def __init__(
            self,
            disp_tetrimino: "IDispencer[ITetrimino]",
            board: "IBoard",
            data: "IAdminDataGame",
            coord_init: Coord = Coord(1, 4),
        ):

        self.is_active: bool = False
        self.coord_init: Coord = coord_init
        self.index_files_update: list[int] = []

        self.disp_tetrimino = disp_tetrimino
        self.board = board
        self.data = data


    @property
    def current_tetrimino(self) -> "ITetrimino":
        try:
            self.__current_tetrimino
        
        except:
            raise Exception("Error: El juego no e a inicializado, ejecute run()")

        return self.__current_tetrimino
    
    @current_tetrimino.setter
    def current_tetrimino(self, value: "ITetrimino"):
        self.__current_tetrimino = value
        self.__current_tetrimino.coord_core.set_value(self.coord_init.value)
        self.__current_tetrimino.board = self.board


    def reset(self):
        self.is_active = True
        self.board.clear_content()
        self.data.reset()
        self.disp_tetrimino.reset()

        try: self.current_tetrimino.reset() 
        except: pass
        

    def run(self):
        self.current_tetrimino = self.disp_tetrimino.next_item
        self.print_Tetrimino()


    def print_Tetrimino(self):
        shadow_coords_blocks = self.current_tetrimino.shadow_coords_blocks
        color_shadow = self.current_tetrimino.color_shadow

        coords_blocks = self.current_tetrimino.coords_blocks
        color = self.current_tetrimino.color

        if not self.board.square_is_empty(*coords_blocks):
            self.is_active = False
    
        blocks_no_repeat = all([not block in coords_blocks for block in shadow_coords_blocks])

        if blocks_no_repeat:

            self.board.print_coords(
                *shadow_coords_blocks,
                style= color_shadow,
                is_ocupiable= False,
            )


        self.board.print_coords(
            *coords_blocks,
            style= color,
        )


    def clear_Tetrimino(self):
        self.board.clear_coords(*self.current_tetrimino.coords_blocks)
        self.board.clear_coords(*self.current_tetrimino.shadow_coords_blocks)


    def iteration(self):
        self.print_Tetrimino()

        if self.current_tetrimino.is_active:
            return
        
        self.register_index_files_update()
        n_files_update = len(self.index_files_update)

        if n_files_update != 0:
            self.clear_files_update()
            self.collapse_files_floating()
            self.data.add_data_point(n_files_update)
        
        self.current_tetrimino.reset()
        self.current_tetrimino = self.disp_tetrimino.next_item
        self.print_Tetrimino()


    def register_index_files_update(self):
        indexs_update = [
            coord.y for coord in self.current_tetrimino.coords_blocks
            if self.board.file_is_occupiable(coord.y)
        ]

        indexs_update = list(set(indexs_update)) # se elminina repeticiones

        self.index_files_update.clear()
        self.index_files_update.extend(indexs_update)
        self.index_files_update.sort()


    def clear_files_update(self):
        for index_update in self.index_files_update:
            self.board.clear_file(index_update)


    def iterator_squares_update(self):
        coord = Coord(0, 0)

        for index_x in range(self.board.size_x):
            list_squares: list[Square] = []

            for index_y in self.index_files_update:
                coord.set_value((index_y, index_x))
                list_squares.append(self.board.get_square(coord))

            yield list_squares


    def collapse_files_floating(self):
        for index_update in self.index_files_update:
            current_index = index_update

            while True:
                top_index = current_index - 1
                
                if not self.board.is_valid_coord_y(top_index):
                    break

                if self.board.file_is_empty(top_index):
                    break

                self.board.trade_style_files(current_index, top_index)

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
