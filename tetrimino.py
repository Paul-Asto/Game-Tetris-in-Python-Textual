from typing import TypeAlias

class CardinalPair:

    def __init__(self, y: int, x: int):
        self.__y: int = y
        self.__x: int = x


    @property
    def value(self) -> tuple[int, int]:
        return (self.__y, self.__x)
    
    @value.setter
    def value(self, value: tuple[int, int]):
        y, x = value

        if len(value) != 2:
            raise ValueError("El valor pasado como parametro tiene que ser una coleccion de 2 Ints")

        if not isinstance(y, int):
            raise TypeError("El valor y ingresado no es un Int")
        
        if not isinstance(x, int):
            raise TypeError("El valor x ingresado no es un Int")    
        
        self.__y = y
        self.__x = x


    @property
    def y(self) -> int:
        return self.__y

    @property
    def x(self) -> int:
        return self.__x


    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.__y}, {self.__x})"
    

    def __eq__(self, other: object) -> bool:
        if issubclass(other, CardinalPair):
            return self.value == other.value
        
        return False
    

    def __iter__(self) -> tuple[int, int]:
        return iter(self.value)


    def __getitem__(self, key: int) -> int:
        if key == 0:
                return self.__y

        elif key == 1:
                return self.__x
        else:
            raise IndexError("Indice fuera de rango")



class Vector(CardinalPair):

    def __init__(self, y, x):
        super().__init__(y, x)



class Coord(CardinalPair):

    def __sub__(self, other: object) -> "Coord":
        if isinstance(other, CardinalPair):
            return Coord(self.y - other.y, self.x - other.x)
        
        raise TypeError("El objeto Coord solo puede ser restado por un objeto derivado de CardinalPair")
        
    
    def __add__(self, other: object) -> "Coord":
        if isinstance(other, CardinalPair):
            return Coord(self.y + other.y, self.x + other.x)      
        
        raise TypeError("El objeto Coord solo puede ser sumado por un objeto derivado de CardinalPair")


    def move(self, vector: Vector):
        if not isinstance(vector, Vector):
            raise TypeError("El parametro no es un Vector")

        self.value += vector
        




class Tetrimino:

    is_active: bool
    color: str

    __vectors_gen_coords_blocks: tuple[Vector] = ()

    def __init__(self):
        self.__coord_core: Coord = Coord(0, 0)


    #Propertys

    @property
    def coord_core(self) -> Coord:
        return self.__coord_core


    @property
    def vectors_gen_coords_blocks(self) -> tuple[Vector]:
        return self.__vectors_gen_coords_blocks
    
    @vectors_gen_coords_blocks.setter
    def vectors_gen_coords_blocks(self, value: tuple[Vector]):
        list_conditions: list[bool] = [isinstance(vector, Vector) for vector in value]

        if not all(list_conditions):
            return ValueError("El valor pasado como parmetro tiene que ser exclusivamente una coleccion de Vectores")
        
        self.__vectors_gen_coords_blocks = value


    @property
    def coords_blocks(self) -> tuple[Coord]:
        return tuple(
            [self.coord_core] + \
            [self.coord_core + vector for vector in self.__vectors_gen_coords_blocks]
        )
    

    # Funciones de Movimiento

    def rotate(self): ...

    def mov_max_bot(self): ...

    def mov_top(self): ...

    def mov_bot(self): ...

    def mov_left(self): ...

    def mov_right(self): ...


