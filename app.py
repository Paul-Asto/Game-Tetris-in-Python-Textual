from typing import TYPE_CHECKING
from observer_interface import Observer, Observed
from cardinal import Coord

from textual.app import App
from textual.widget import Widget
from textual.containers import Vertical
from textual.events import Key

from disp_tetrimino import DispencerTetrimino
from board import Board 



from game import TetrisGame

from board import Square


def secuence_coord_widget(size_y: tuple[int, int], size_x: tuple[int, int]):
    for y in range(size_y):
        for x in range(size_x):
            yield Coord(y, x)



class Block(Widget, Observer[Square]):

    def __init__(self, coord: Coord) -> None:
        super().__init__()

        self.coord: Coord = coord


    def react_changes(self):
        self.set_classes(self.observed.style)
        


class GroupBlocks(Vertical):
    def __init__(self, children: list[Block], id = None):
        super().__init__(id=id)

        self.dict_blocks: dict[Coord, Block] = {}

        for block in children:
            self.dict_blocks[block.coord] = block
            self._add_child(block)


    @property
    def blocks(self) -> list[Block]:
        return list(self.dict_blocks.values())



class TetrisApp(App):
    CSS_PATH = "style.tcss"

    def __init__(self, game: TetrisGame):
        super().__init__()

        self.game = game


    def compose(self):
        self.principal_board = GroupBlocks(
            [Block(coord) for coord in secuence_coord_widget(20, 10)],
            id= "board_principal",
        )
        yield self.principal_board

        self.next_piece_board = GroupBlocks(
            [Block(coord) for coord in secuence_coord_widget(10, 6)],
            id= "board_next_pieces",
            )
        
        #yield self.next_piece_board

    
    def on_mount(self):
        # Enlazando los blocks con los squares 
        for block in self.principal_board.blocks:
            square = self.game.board.get_square(block.coord)
            block.observed = square

        self.game.run()

    async def on_key(self, event: Key) -> None:
        self.game.clearTetrimino()

        if event.key == "left":
            self.game.mov_left()

        elif event.key == "right":
            self.game.mov_right()
            
        elif event.key == "up":
            self.game.mov_rotate()
            
        elif event.key == "down":
            self.game.mov_bot()

        elif event.key == "space":
            self.game.mov_max_bot()
        
        self.game.iteration()



game = TetrisGame(DispencerTetrimino(), Board(20, 10))
app = TetrisApp(game)
app.run()