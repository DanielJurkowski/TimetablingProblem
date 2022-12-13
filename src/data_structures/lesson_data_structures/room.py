from dataclasses import dataclass
import pandas as pd
from src.data_structures.lesson_data_structures.lesson_subobject import LessonSubobject


@dataclass
class Room(LessonSubobject):
    def change_availability_matrix(self, solution, group: int, period: int, day: int, available: bool):
        super().change_availability_matrix(solution, group, period, day, available)


def rooms_factory(file_path: str):
    rooms = {}

    file = pd.read_csv(file_path)

    for index, row in file.iterrows():
        rooms[row['room_id']] = Room(row['room_id'], row['room_name'])

    return rooms
