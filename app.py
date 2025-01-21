from rich.console import Console
from game import TetrisGame
from disp_tetrimino import DispencerTetrimino
from board import Board 

def main():
    game = TetrisGame(DispencerTetrimino(), Board(10, 10))
    console = Console()

    while True:
        print("\033[H\033[J", end="")
        game.printTetrimino()
        console.print(game.board.view)
        entrada = input("\nEscoje el mov(a, w, s, d, e): ")

        game.clearTetrimino()

        if entrada == "a":
            game.mov_left()

        elif entrada == "w":
            game.mov_rotate()

        elif entrada == "s":
            game.mov_bot()

        elif entrada == "d":
            game.mov_right()

        elif entrada == "e":
            game.mov_max_bot()

        game.iteration()
    

if __name__ == "__main__":
    main()        