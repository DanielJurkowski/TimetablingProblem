from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np


@dataclass
class LessonSubobject(ABC):
    id: int
    name: str
    availability_matrix: np.ndarray = None
    availability_matrix_3d: np.ndarray = None

    @abstractmethod
    def change_availability_matrix(self, solution, group: int, period: int, day: int, available: bool):
        if self.availability_matrix is None and self.availability_matrix_3d is None:
            self.availability_matrix = np.empty((solution.number_periods, solution.number_days), dtype=bool)
            self.availability_matrix_3d = np.empty((solution.number_groups, solution.number_periods,
                                                    solution.number_days), dtype=bool)

            self.availability_matrix[:] = True
            self.availability_matrix_3d[::] = True

        self.availability_matrix[period][day] = available
        self.availability_matrix_3d[group][period][day] = available
