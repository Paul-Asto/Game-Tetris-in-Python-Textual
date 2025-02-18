from typing import TYPE_CHECKING, TypeVar, Generic
from src.observer_interface import Observer

from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Vertical

if TYPE_CHECKING:
    from src.cardinal import Coord
    from src.core_game.board import Square
    from src.core_game.disp_tetrimino import DispencerTetrimino
    from src.observer_interface import Observed



T = TypeVar("T")

class ReactiveInfo(Widget, Generic[T], Observer[T]):

    def __init__(self, title: str, react_class:"Observed", react_attr: str, id: str = None, classes: str = None):
        super().__init__(id=id, classes=classes)

        self.title: str = title

        self.observed: "Observed" = react_class
        self.react_attr: str = react_attr

        self.border_title = self.title

        self.static_content = Static(str(getattr(self.observed, self.react_attr)))
        

        self._add_children(self.static_content,)


    def react_changes(self):
        self.static_content.update(str(getattr(self.observed, self.react_attr)))



class Block(Widget):

    def __init__(self, coord: "Coord") -> None:
        super().__init__()

        self.coord: "Coord" = coord


    def clear_classes(self):
        for class_name in list(self.classes):
            self.remove_class(class_name)



class ReactiveBlock(Block, Observer["Square"]):

    def react_changes(self):
        self.set_classes(self.observed.style)



TYPE_BLOCK = TypeVar('type_block', bound=Block)



class ViewBoard(Vertical, Generic[TYPE_BLOCK]):
    def __init__(self, children: list[TYPE_BLOCK], id = None):
        super().__init__(id=id)

        self.dict_blocks: dict["Coord", TYPE_BLOCK] = {}

        for block in children:
            self.dict_blocks[block.coord] = block
            self._add_child(block)

    
    def get_block(self, coord: "Coord") -> TYPE_BLOCK:
        return self.dict_blocks[coord]
    


class PrincipalBoard(ViewBoard[ReactiveBlock]):

    @property
    def blocks(self) -> list[ReactiveBlock]:
        return list(self.dict_blocks.values())



class NextPieceBoard(ViewBoard[Block], Observer["DispencerTetrimino"]):

    def react_changes(self):
        self.clear()

        pieces = self.observed.content

        piece_1 = pieces[0]
        piece_1.coord_core.set_value((2, 2))
        self.add_class_to_blocks(*piece_1.coords_blocks, clase = piece_1.color_block)

        piece_2 = pieces[1]
        piece_2.coord_core.set_value((5, 2))
        self.add_class_to_blocks(*piece_2.coords_blocks, clase = piece_2.color_block)

        piece_3 = pieces[2]
        piece_3.coord_core.set_value((8, 2))
        self.add_class_to_blocks(*piece_3.coords_blocks, clase = piece_3.color_block)


    def add_class_to_blocks(self, *coords: "Coord", clase: str):
        for coord in coords:
            block = self.get_block(coord)
            block.add_class(clase)


    def clear(self):
        for block in self.dict_blocks.values():
            block.clear_classes()
