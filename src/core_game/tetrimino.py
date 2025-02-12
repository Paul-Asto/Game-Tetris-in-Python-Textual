from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from src.cardinal import Coord, Vector
from copy import deepcopy

if TYPE_CHECKING:
    from src.core_game.board import Board


class ITetrimino(ABC):
    is_active: bool 
    color: str
    color_shadow: str

    board: "Board"

    coord_core: Coord
    vectors_gen_coords_blocks: tuple[Vector]
    coords_blocks: tuple[Coord]
    shadow_coords_blocks: tuple[Coord]

    @abstractmethod
    def reset(self): ...

    @abstractmethod
    def rotate(self): ...

    @abstractmethod
    def mov_max_bot(self): ...

    @abstractmethod
    def mov_top(self): ...

    @abstractmethod
    def mov_bot(self): ...

    @abstractmethod
    def mov_left(self): ...

    @abstractmethod
    def mov_right(self): ...



class Tetrimino(ITetrimino):
    is_active: bool = True
    color_shadow: str = "black"
    color: str = "black"

    __board: "Board"
    default_vectors_gen_coords_blocks: tuple[Vector] 
    private_vectors_gen_coords_blocks: tuple[Vector] 
    __coord_core: Coord

    def __init__(self):
        self.__coord_core = Coord(0, 0)
        self.vectors_gen_coords_blocks = ()


    #Propertys
    @property
    def coord_core(self) -> Coord:
        return self.__coord_core


    @property
    def vectors_gen_coords_blocks(self) -> tuple[Vector]:
        return self.private_vectors_gen_coords_blocks
    
    @vectors_gen_coords_blocks.setter
    def vectors_gen_coords_blocks(self, value: tuple[Vector]):
        list_conditions: list[bool] = [isinstance(vector, Vector) for vector in value]

        if not all(list_conditions):
            return ValueError("El valor pasado como parmetro tiene que ser exclusivamente una coleccion de Vectores")
        
        self.default_vectors_gen_coords_blocks = value
        self.private_vectors_gen_coords_blocks = deepcopy(value)


    @property
    def coords_blocks(self) -> tuple[Coord]:
        return self.gen_coords_blocks()
    

    @property
    def shadow_coords_blocks(self) -> tuple[Coord]:
        new_coord_core: Coord = self.coord_core
        result_coords_blocks: tuple[Coord] = ()

        while True:
            new_coord_core += Vector(1, 0)
            new_coords_blocks = self.gen_coords_blocks(coord_core= new_coord_core)

            if not self.board.square_is_empty(*new_coords_blocks):
                break
            
            result_coords_blocks = new_coords_blocks

            if self.board.in_max_limit_bot(*new_coords_blocks):
                break
        
        return result_coords_blocks



    @property
    def board(self) -> "Board":
        try:
            self.__board

        except AttributeError:
            raise Exception("El tetrimino, no se encuentra en un board para realizar esta funcion")
        
        return self.__board
    
    @board.setter
    def board(self, value: "Board"):
        self.__board = value
    
    @board.deleter
    def board(self):
        del self.__board

    
    def reset(self):
        self.coord_core.set_value((0, 0))
        self.private_vectors_gen_coords_blocks = deepcopy(self.default_vectors_gen_coords_blocks)
        self.is_active = True
        del self.board 


    def gen_coords_blocks(self, coord_core: Coord = None, vectors: tuple[Vector] = None) -> tuple[Coord]:
        if vectors == None:
            vectors = self.vectors_gen_coords_blocks

        if coord_core == None:
            coord_core = self.coord_core

        return tuple(
            [coord_core] + \
            [coord_core + vector for vector in vectors]
        )
    

    def gen_vectors_rotate(self, vectors: tuple[Vector] = None) -> tuple[Vector]:
            if vectors == None:
                vectors = self.vectors_gen_coords_blocks

            return tuple([vector.get_rotate_right() for vector in vectors])


    # Funciones de Movimiento
    def mov(self, vector: Vector, altern_vectors:list[Vector] = [], is_frezzable: bool = False):
        altern_vectors.insert(0, vector)

        for vector in altern_vectors:
            new_coord_core: Coord = self.coord_core + vector
            new_coords_blocks: tuple[Coord] = self.gen_coords_blocks(coord_core= new_coord_core)

            if self.board.square_is_empty(*new_coords_blocks):
                self.coord_core.move(vector)
                return

        else:
            if is_frezzable: self.is_active = False
    

    def rotate(self):
        coords_core_test: tuple[Coord] = (
            self.coord_core,
            self.coord_core + Vector(0, -1),
            self.coord_core + Vector(0, 1),
            self.coord_core + Vector(-1, 0),
        )

        new_vectors: tuple[Vector] = self.gen_vectors_rotate()

        for coord in coords_core_test:
            new_coords_blocks: tuple[Coord] = self.gen_coords_blocks(coord_core= coord, vectors= new_vectors)

            if not self.board.square_is_empty(*new_coords_blocks):
                continue
            
            self.coord_core.set_value(coord.value)
            self.private_vectors_gen_coords_blocks = new_vectors

            break 


    def mov_max_bot(self):
        if self.shadow_coords_blocks != ():
            new_coord = self.shadow_coords_blocks[0]
            self.coord_core.set_value(new_coord.value)

        self.is_active = False        


    def mov_top(self):
        self.mov(Vector(-1, 0))


    def mov_bot(self): 
        if self.board.in_max_limit_bot(*self.coords_blocks):
            self.is_active = False
            return

        self.mov(Vector(1, 0), is_frezzable= True)


    def mov_left(self): 
        if self.board.in_max_limit_left(*self.coords_blocks):
            return
        
        self.mov(Vector(0, -1), altern_vectors= [Vector(-1, -1)])


    def mov_right(self): 
        if self.board.in_max_limit_right(*self.coords_blocks):
            return
        
        self.mov(Vector(0, 1), altern_vectors= [Vector(-1, 1)])



# Clases de las Piezas
class Tetrimino_O(Tetrimino):

    def __init__(self):
        super().__init__()

        self.vectors_gen_coords_blocks = (Vector(0, 1), Vector(-1, 0), Vector(-1, 1))

    def rotate(self): pass



class Tetrimino_T(Tetrimino):

    def __init__(self):
        super().__init__()

        self.vectors_gen_coords_blocks = (Vector(-1, 0), Vector(0, 1), Vector(0, -1))



class Tetrimino_S(Tetrimino):

    def __init__(self):
        super().__init__()

        self.vectors_gen_coords_blocks = (Vector(0, -1), Vector(-1, 0), Vector(-1, 1))



class Tetrimino_Z(Tetrimino):

    def __init__(self):
        super().__init__()

        self.vectors_gen_coords_blocks = (Vector(0, 1), Vector(-1, 0), Vector(-1, -1))



class Tetrimino_J(Tetrimino):
    
    def __init__(self):
        super().__init__()

        self.vectors_gen_coords_blocks = (Vector(0, -1), Vector(0, 1), Vector(-1, -1))



class Tetrimino_L(Tetrimino):
    
    def __init__(self):
        super().__init__()
        self.vectors_gen_coords_blocks = (Vector(0, -1), Vector(0, 1), Vector(-1, 1))



class Tetrimino_I(Tetrimino):

    def __init__(self):
        super().__init__()

        self.vectors_gen_coords_blocks = (Vector(0, -1), Vector(0, 1), Vector(0, 2))
        self.index_rotate: Cycle = Cycle(0, 3)


    def rotate(self):
        coord_init_test: Coord = self.coord_core.copy()

        if self.board.in_max_limit_left(coord_init_test):
            coord_init_test.move(Vector(0, 1))

        elif self.board.in_max_limit_right(coord_init_test):
            coord_init_test.move(Vector(0, -1))

        elif self.board.in_max_limit_bot(coord_init_test):
            coord_init_test.move(Vector(-1, 0))

        state_rotate = self.index_rotate.index_pointer

        if state_rotate == 0:
            coord_init_test.move(Vector(0, 1))

        elif state_rotate == 1:
            coord_init_test.move(Vector(1, 0))

        elif state_rotate == 2:
            coord_init_test.move(Vector(0, -1))

        elif state_rotate == 3:
            coord_init_test.move(Vector(-1, 0))

        coords_core_test: tuple[Coord] = (
            coord_init_test,
            coord_init_test + Vector(0, -1),
            coord_init_test + Vector(0, 1),
            coord_init_test + Vector(-1, 0),
        )

        new_vectors: tuple[Vector] = self.gen_vectors_rotate()

        for coord in coords_core_test:
            new_coords_blocks: tuple[Coord] = self.gen_coords_blocks(coord_core= coord, vectors= new_vectors)

            if not self.board.square_is_empty(*new_coords_blocks):
                continue
            
            self.coord_core.set_value(coord.value)
            self.private_vectors_gen_coords_blocks = new_vectors
            self.index_rotate.add_pointer()
            break    


    def reset(self):
        self.index_rotate.reset()
        super().reset()



class Cycle:

    def __init__(self, start: int, end: int):
        self.start: int = start
        self.end: int = end

        self.index_pointer: int = start 

    def reset(self):
        self.index_pointer = self.start

    def add_pointer(self):
        if not self.index_pointer < self.end:
            self.reset()
            return
        
        self.index_pointer += 1
