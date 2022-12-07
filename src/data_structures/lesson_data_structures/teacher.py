from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class Teacher:
    teacher_id: int
    teacher_name: str
    availability_matrix: np.ndarray = None

    def change_availability_matrix(self, solution, group, period, day):
        self.availability_matrix = np.empty((solution.number_groups, solution.number_periods, solution.number_days), dtype=bool)
        self.availability_matrix[::] = True
        self.availability_matrix[group][period][day] = False

def teachers_factory(file_path: str):
    teachers = {}

    file = pd.read_csv(file_path)

    for index, row in file.iterrows():
        teachers[row['teacher_id']] = Teacher(row['teacher_id'], row['teacher_name'])

    return teachers
