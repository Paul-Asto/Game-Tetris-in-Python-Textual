from src.core_game.board import Square, Board
from src.core_game.data_games import AdminDataGame
from src.core_game.disp_tetrimino import DispencerTetrimino

from src.observer_interface import Observed

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.color import Color
    from src.core_game.tetrimino import Tetrimino


class ReactSquare(Square, Observed):
    __style: "Color"

    def __init__(self, style):
        super().__init__(style)
        Observed.__init__(self)
        self.__style = style

    @property
    def style(self) -> "Color":
        return self.__style

    @style.setter
    def style(self, value: "Color"):
        if self.style == value:
            return 
        
        self.__style = value
        self.report_changes()



class ReactAdminDataGame(AdminDataGame, Observed):

    def __init__(self, *data, nivel_init = 0):
        super().__init__(*data, nivel_init=nivel_init)
        Observed.__init__(self)

    def add_data_point(self, n_files):
        super().add_data_point(n_files)
        self.report_changes()

    def reset(self):
        super().reset()
        self.report_changes()


class ReactDispenserTetrimino(DispencerTetrimino, Observed):

    def __init__(self, *pieces):
        super().__init__(*pieces)
        Observed.__init__(self)
    
    @property
    def next_item(self) -> "Tetrimino":
        item = super().next_item
        self.report_changes()

        return item
    
    def reset(self):
        super().reset()
        self.report_changes()