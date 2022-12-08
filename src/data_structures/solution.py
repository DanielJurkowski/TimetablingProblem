from copy import copy
from dataclasses import dataclass
from typing import Dict
import numpy as np
import numpy.random as random

from src.data_structures.lesson import Lesson
from src.data_structures.lesson_data_structures.group import Group
from src.data_structures.lesson_data_structures.room import Room
from src.data_structures.lesson_data_structures.subject import Subject
from src.data_structures.lesson_data_structures.teacher import Teacher
from src.optimization_functions.penalty_functions import more_than_one_lesson_same_subject_in_day_groups, \
    more_than_one_lesson_teachers_and_rooms, same_subject_in_day, free_periods_min_and_max_lessons_in_day_teachers, \
    free_periods_min_and_max_lessons_in_day_groups


@dataclass
class Solution:
    groups: Dict[int, Group]
    teachers: Dict[int, Teacher]
    rooms: Dict[int, Room]
    subjects: Dict[int, Subject]
    number_days: int
    number_periods: int

    number_groups: int = 0
    number_teachers: int = 0
    number_rooms: int = 0
    solution_matrix: np.ndarray = None
    cost = 0

    def create_initial_solution(self):
        if self.solution_matrix is None:
            self.number_groups = len(self.groups)
            self.number_teachers = len(self.teachers)
            self.number_rooms = len(self.rooms)

            self.solution_matrix = np.empty((self.number_groups, self.number_periods, self.number_days), dtype=dict)
            self.solution_matrix[::] = {}

            for group_index, group in self.groups.items():
                for _, subject in self.subjects.items():
                    for times in range(subject.times_in_week):
                        teacher = self.teachers[subject.subject_teacher]

                        room = self.rooms[random.randint(self.number_rooms)]
                        period = random.randint(self.number_periods)
                        day = random.randint(self.number_days)

                        lesson = Lesson(room, teacher, subject, group)

                        lessons_cell = copy(self.solution_matrix[group_index][period][day])
                        lessons_cell[len(lessons_cell)] = lesson

                        self.solution_matrix[group_index, period, day] = lessons_cell

                        teacher.change_availability_matrix(self, period, day, False)
                        room.change_availability_matrix(self, period, day, False)
                        group.change_availability_matrix(self, period, day, False)

    def compute_cost(self):
        weight_more_than_one_lesson_groups = 1
        weight_same_subject_in_day = 1

        weight_more_than_one_lesson_teachers = 1
        weight_more_than_one_lesson_rooms = 1

        weight_free_periods_in_day_groups = 1
        weight_free_periods_in_day_teachers = 1

        weight_min_and_max_lessons_in_day_groups = 1
        weight_min_and_max_lessons_in_day_teachers = 1

        cost = [
            more_than_one_lesson_same_subject_in_day_groups(self, weight_more_than_one_lesson_groups,
                                                            weight_same_subject_in_day),
            more_than_one_lesson_teachers_and_rooms(self, weight_more_than_one_lesson_teachers,
                                                    weight_more_than_one_lesson_rooms),
            free_periods_min_and_max_lessons_in_day_groups(self, weight_free_periods_in_day_groups,
                                                           weight_min_and_max_lessons_in_day_groups),
            free_periods_min_and_max_lessons_in_day_teachers(self, weight_free_periods_in_day_teachers,
                                                             weight_min_and_max_lessons_in_day_teachers)
        ]

        self.cost = cost

    def check_if_solution_acceptable(self):

        more_than_one_lesson_groups = self.cost[0][0]
        more_than_one_lesson_teachers = self.cost[1][0]
        more_than_one_lesson_rooms = self.cost[1][1]

        if more_than_one_lesson_groups == 0 and more_than_one_lesson_teachers == 0 and more_than_one_lesson_rooms == 0:
            return True

        else:
            return False




