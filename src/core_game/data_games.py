from dataclasses import dataclass
from abc import abstractmethod, ABC


@dataclass
class DataGame:
    current_nivel: int
    value_point: int
    bonnus_point_for_file: tuple[int, int, int]

    speed_dificult: float
    meta_files: int



class IAdminDataGame(ABC):

    @property
    @abstractmethod
    def points(self) -> int: ...

    @property
    @abstractmethod
    def n_files_colapse(self) -> int: ...

    @property
    @abstractmethod
    def speed_dificult(self) -> float: ...

    @property
    @abstractmethod
    def meta_next_level(self) -> int: ...

    @abstractmethod
    def add_data_point(self, n_files: int): ...

    @abstractmethod
    def set_nivel(self, nivel: int): ...

    @abstractmethod
    def reset(self): ...



class AdminDataGame(IAdminDataGame):

    def __init__(self, *data: DataGame, nivel_init: int = 0):
        self.__point = 0
        self.__n_files_colapse = 0
        self.n_file_colapse_in_level = 0
        self.current_nivel = nivel_init

        self.content_data: dict[int, DataGame] = {dt.current_nivel : dt for dt in data}


    @property
    def current_data(self) -> DataGame:
        return self.content_data.get(self.current_nivel, None)


    @property
    def points(self) -> int:
        return self.__point
    
    @points.setter
    def points(self, value: int):
        self.__point = value

    
    @property
    def n_files_colapse(self) -> int:
        return self.__n_files_colapse
    
    @n_files_colapse.setter
    def n_files_colapse(self, value):
        self.__n_files_colapse = value


    @property
    def speed_dificult(self) -> float:
        return self.current_data.speed_dificult
    
    
    @property
    def meta_next_level(self) -> int:
        return self.current_data.meta_files - self.n_file_colapse_in_level


    def get_bonnus_for_file(self, n_files: int) -> int:
        if n_files == 1:
            return 0

        elif n_files == 2:
            return self.current_data.bonnus_point_for_file[0]

        elif n_files == 3:
            return self.current_data.bonnus_point_for_file[1]

        elif n_files == 4:
            return self.current_data.bonnus_point_for_file[2]
        

    def add_data_point(self, n_files: int):
        points = self.current_data.value_point * n_files
        points += self.get_bonnus_for_file(n_files)
        self.points += points

        self.n_files_colapse += n_files

        self.n_file_colapse_in_level += n_files

        if self.n_file_colapse_in_level >= self.current_data.meta_files:
            self.n_file_colapse_in_level = 0
            self.current_nivel += 1

            if self.current_data == None:
                self.current_nivel -= 1


    def set_nivel(self, nivel: int):
        self.current_nivel = nivel


    def reset(self):
        self.points = 0
        self.n_file_colapse_in_level = 0
        self.n_files_colapse = 0
        self.current_nivel = 0
        