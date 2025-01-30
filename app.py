from typing import TYPE_CHECKING, TypeVar, Generic
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



class Block(Widget):

    def __init__(self, coord: Coord) -> None:
        super().__init__()

        self.coord: Coord = coord


    def clear_classes(self):
        for class_name in list(self.classes):
            self.remove_class(class_name)



class ReactiveBlock(Block, Observer[Square]):

    def react_changes(self):
        self.set_classes(self.observed.style)



T = TypeVar('T', bound=Block)



class ViewBoard(Vertical, Generic[T]):
    def __init__(self, children: list[T], id = None):
        super().__init__(id=id)

        self.dict_blocks: dict[Coord, T] = {}

        for block in children:
            self.dict_blocks[block.coord] = block
            self._add_child(block)

    
    def get_block(self, coord: Coord) -> T:
        return self.dict_blocks[coord]
    


class PrincipalBoard(ViewBoard[ReactiveBlock]):

    @property
    def blocks(self) -> list[ReactiveBlock]:
        return list(self.dict_blocks.values())



class NextPieceBoard(ViewBoard[Block], Observer[DispencerTetrimino]):

    def react_changes(self):
        self.clear()

        pieces = self.observed.content

        piece_1 = pieces[0]
        piece_1.coord_core.set_value((2, 2))
        self.add_class_to_blocks(*piece_1.coords_blocks, clase = piece_1.color)

        piece_2 = pieces[1]
        piece_2.coord_core.set_value((5, 2))
        self.add_class_to_blocks(*piece_2.coords_blocks, clase = piece_2.color)

        piece_3 = pieces[2]
        piece_3.coord_core.set_value((8, 2))
        self.add_class_to_blocks(*piece_3.coords_blocks, clase = piece_3.color)


    def add_class_to_blocks(self, *coords: Coord, clase: str):
        for coord in coords:
            block = self.get_block(coord)
            block.add_class(clase)


    def clear(self):
        for block in self.dict_blocks.values():
            block.clear_classes()



class TetrisApp(App):
    CSS_PATH = "style.tcss"

    def __init__(self, game: TetrisGame):
        super().__init__()

        self.game = game


    def compose(self):
        self.principal_board = PrincipalBoard(
            [ReactiveBlock(coord) for coord in secuence_coord_widget(20, 10)],
            id= "board_principal",
        )
        yield self.principal_board

        self.next_piece_board = NextPieceBoard(
            [Block(coord) for coord in secuence_coord_widget(10, 6)],
            id= "board_next_pieces",
            )
        yield self.next_piece_board

    
    def on_mount(self):
        # Enlazando los blocks con los squares 
        for block in self.principal_board.blocks:
            square = self.game.board.get_square(block.coord)
            block.observed = square

        # Enlazando el next_piece_board al dispensador de teriminos
        self.next_piece_board.observed = game.disp_tetrimino

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