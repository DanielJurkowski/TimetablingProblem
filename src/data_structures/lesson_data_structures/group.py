from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class Group:
    group_id: int
    group_name: str
    availability_matrix: np.ndarray = None

    # zmiana macierzy na 2d
    def change_availability_matrix(self, solution, period, day, available=False):
        if self.availability_matrix is None:
            self.availability_matrix = np.empty((solution.number_periods, solution.number_days), dtype=bool)
            self.availability_matrix[:] = True

        self.availability_matrix[period][day] = available


def groups_factory(file_path: str):
    groups = {}

    file = pd.read_csv(file_path)

    for index, row in file.iterrows():
        groups[row['group_id']] = Group(row['group_id'], row['group_name'])

    return groups
