
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
        if isinstance(other, CardinalPair):
            return self.value == other.value
        
        return False


    def __hash__(self):
        return hash(self.value)
    

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

    
    def get_rotate_left(self) -> "Vector":
        return Vector(-(self.x), self.y)

    def get_rotate_right(self)-> "Vector":
        return Vector(self.x, -(self.y))



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

        new_value = self + vector
        self.set_value(new_value.value)

    
    def set_value(self, value: tuple[int, int]):
        self.value = value
        
    
    def copy(self) -> "Coord":
        return Coord(self.y, self.x)