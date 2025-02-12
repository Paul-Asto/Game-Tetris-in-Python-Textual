from src.cardinal import Coord
import asyncio 
from typing import TYPE_CHECKING
from time import sleep

from textual import on
from textual.app import App
from textual.widgets import Button
from textual.containers import Vertical, Horizontal


from src.UI_Textual.witgets import (
    ReactiveBlock,
    ReactiveInfo,
    PrincipalBoard, 
    NextPieceBoard, 
    Block,
    )

if TYPE_CHECKING:
    from src.core_game.game import TetrisGame
    from textual.events import Key
    from asyncio import Task


def secuence_coord_widget(size_y: int, size_x: int):
    for y in range(size_y):
        for x in range(size_x):
            yield Coord(y, x)



class TetrisApp(App):
    CSS_PATH = "style.tcss"
    is_busy: bool = False
    clear_animated: bool
    speed_clear_animated: tuple
    task_automov: "Task" = None

    def __init__(self, game: "TetrisGame", clear_animated: bool = False, speed_clear_animated: tuple = 0.035):
        super().__init__()

        self.game = game
        self.clear_animated = clear_animated
        self.speed_clear_animated = speed_clear_animated


    def compose(self):
        with Horizontal():
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

            with Vertical():
                yield ReactiveInfo("Nivel", self.game.data, "current_nivel")
                yield ReactiveInfo("Speed", self.game.data, "speed_dificult")
                yield ReactiveInfo("N_filas", self.game.data, "n_files_colapse")
                yield ReactiveInfo("Meta", self.game.data, "meta_next_level")
                yield ReactiveInfo("Puntos", self.game.data, "points")
                yield Button("Reiniciar", id= "btn_reiniciar")

    
    def on_mount(self):
        # Enlazando los blocks con los squares 
        for block in self.principal_board.blocks:
            square = self.game.board.get_square(block.coord)
            block.observed = square

        # Enlazando el next_piece_board al dispensador de teriminos
        self.next_piece_board.observed = self.game.disp_tetrimino


    async def on_key(self, event: "Key") -> None:
        if not self.game.is_active:
            return

        if self.is_busy:
            return
        
        self.game.clear_Tetrimino()

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
        
        await self.iteration()


    async def auto_mov_down(self):
        while True:
            await asyncio.sleep(self.game.data.speed_dificult)
        
            if not self.game.is_active:
                return
            
            if self.is_busy:
                continue
            
            self.game.clear_Tetrimino()
            self.game.mov_bot()

            await self.iteration()


    async def iteration(self):
        if self.clear_animated:
            self.is_busy = True
            await self.animated_iteration()
            self.is_busy = False

        else:
            self.game.iteration()


    async def animated_iteration(self):
        self.game.print_Tetrimino()

        if self.game.current_tetrimino.is_active:
            return
        
        n_files_update = len(self.game.index_files_update)

        if n_files_update != 0:

            for column_square in self.game.iterator_squares_update():
                for square in column_square:
                    self.game.board.clear_square(square)
                
                await asyncio.sleep(self.speed_clear_animated)

            self.game.collapse_files_floating()
            self.game.data.add_data_point(n_files_update)
        
        self.game.current_tetrimino.reset()
        self.game.current_tetrimino = self.game.disp_tetrimino.next_item
        self.game.print_Tetrimino()


    def reset_task_automov(self):
        if self.task_automov != None:
            self.task_automov.cancel()

        self.task_automov = asyncio.create_task(self.auto_mov_down())


    @on(Button.Pressed, "#btn_reiniciar")
    async def reset(self):
        if self.is_busy:
            return
        
        self.game.reset()
        self.game.run()
        self.reset_task_automov()
