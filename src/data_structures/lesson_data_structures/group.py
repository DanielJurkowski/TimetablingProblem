from dataclasses import dataclass
import pandas as pd
from src.data_structures.lesson_data_structures.lesson_subobject import LessonSubobject


@dataclass
class Group(LessonSubobject):
    def change_availability_matrix(self, solution, group: int, period: int, day: int, available: bool):
        super().change_availability_matrix(solution, group, period, day, available)


def groups_factory(file_path: str):
    groups = {}

    file = pd.read_csv(file_path)

    for index, row in file.iterrows():
        groups[row['group_id']] = Group(row['group_id'], row['group_name'])

    return groups
