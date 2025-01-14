from cardinal import Coord, Vector


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


