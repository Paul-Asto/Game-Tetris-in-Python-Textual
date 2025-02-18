from src.core_game.data_games import DataGame
from src.core_game.board import Square, Board
from src.core_game.tetrimino import  ( 
    Tetrimino_I,
    Tetrimino_O,
    Tetrimino_T,
    Tetrimino_S,
    Tetrimino_Z,
    Tetrimino_J,
    Tetrimino_L,
    )

from src.reactive_components import (
    ReactSquare,
    ReactAdminDataGame,
    ReactDispenserTetrimino,
    )

from src.core_game.game import TetrisGame
from src.UI_Textual.app import TetrisApp



SIZE_BOARD_Y = 20 
SIZE_BOARD_X = 10

COLOR_SHADOW = "gray"
COLOR_PIECE_I = "magenta"
COLOR_PIECE_O = "yellow"
COLOR_PIECE_T = "purple"
COLOR_PIECE_S = "green"
COLOR_PIECE_Z = "red"
COLOR_PIECE_J = "blue"
COLOR_PIECE_L = "orange"



t_piece_I = Tetrimino_I()
t_piece_I.color_block = COLOR_PIECE_I
t_piece_I.color_shadow = COLOR_SHADOW

t_piece_O = Tetrimino_O()
t_piece_O.color_block = COLOR_PIECE_O
t_piece_O.color_shadow = COLOR_SHADOW

t_piece_T = Tetrimino_T()
t_piece_T.color_block = COLOR_PIECE_T 
t_piece_T.color_shadow = COLOR_SHADOW

t_piece_S = Tetrimino_S()
t_piece_S.color_block = COLOR_PIECE_S
t_piece_S.color_shadow = COLOR_SHADOW

t_piece_Z = Tetrimino_Z()
t_piece_Z.color_block = COLOR_PIECE_Z
t_piece_Z.color_shadow = COLOR_SHADOW

t_piece_J = Tetrimino_J()
t_piece_J.color_block = COLOR_PIECE_J
t_piece_J.color_shadow = COLOR_SHADOW

t_piece_L = Tetrimino_L()
t_piece_L.color_block = COLOR_PIECE_L
t_piece_L.color_shadow = COLOR_SHADOW


tetris_data = (
    DataGame(current_nivel= 0, value_point= 10, bonnus_point_for_file= (25, 50, 75), speed_dificult= 1.2, meta_files= 10),
    DataGame(current_nivel= 1, value_point= 13, bonnus_point_for_file= (30, 60, 100), speed_dificult= 1, meta_files= 15),
    DataGame(current_nivel= 2, value_point= 17, bonnus_point_for_file= (40, 90, 150), speed_dificult= 0.8, meta_files= 20),
    DataGame(current_nivel= 3, value_point= 22, bonnus_point_for_file= (50, 100, 200), speed_dificult= 0.6, meta_files= 25),
    DataGame(current_nivel= 4, value_point= 28, bonnus_point_for_file= (65, 140, 300), speed_dificult= 0.45, meta_files= 35),
    DataGame(current_nivel= 5, value_point= 35, bonnus_point_for_file= (75, 175, 350), speed_dificult= 0.37, meta_files= 40),
    DataGame(current_nivel= 6, value_point= 43, bonnus_point_for_file= (90, 200, 450), speed_dificult= 0.32, meta_files= 45),
    DataGame(current_nivel= 7, value_point= 56, bonnus_point_for_file= (100, 250, 600), speed_dificult= 0.26, meta_files= 50),
    DataGame(current_nivel= 8, value_point= 70, bonnus_point_for_file= (150, 350, 800), speed_dificult= 0.17, meta_files= 60),
    DataGame(current_nivel= 9, value_point= 90, bonnus_point_for_file= (200, 500, 1250), speed_dificult= 0.1, meta_files= 75),
)

disp_pieces = ReactDispenserTetrimino(
    t_piece_I,
    t_piece_O,
    t_piece_T,
    t_piece_S,
    t_piece_Z,
    t_piece_J,
    t_piece_L,
)

data_game = ReactAdminDataGame(*tetris_data, nivel_init= 0)

board = Board[ReactSquare](SIZE_BOARD_Y, SIZE_BOARD_X, ReactSquare)

game =  TetrisGame(
    disp_pieces,
    board,
    data_game,
)

app = TetrisApp(game, clear_animated= True)


if __name__ == "__main__":
    app.run()