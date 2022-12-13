from dataclasses import dataclass
import pandas as pd
from src.data_structures.lesson_data_structures.lesson_subobject import LessonSubobject


@dataclass
class Teacher(LessonSubobject):
    def change_availability_matrix(self, solution, group: int, period: int, day: int, available: bool):
        super().change_availability_matrix(solution, group, period, day, available)


def teachers_factory(file_path: str):
    teachers = {}

    file = pd.read_csv(file_path)

    for index, row in file.iterrows():
        teachers[row['teacher_id']] = Teacher(row['teacher_id'], row['teacher_name'])

    return teachers
