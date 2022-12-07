from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class Room:
    room_id: int
    room_name: str
    availability_matrix: np.ndarray = None

    def change_availability_matrix(self, solution, group, period, day):
        self.availability_matrix = np.empty((solution.number_groups, solution.number_periods, solution.number_days), dtype=bool)
        self.availability_matrix[::] = True
        self.availability_matrix[group][period][day] = False


def rooms_factory(file_path: str):
    rooms = {}

    file = pd.read_csv(file_path)

    for index, row in file.iterrows():
        rooms[row['room_id']] = Room(row['room_id'], row['room_name'])

    return rooms
