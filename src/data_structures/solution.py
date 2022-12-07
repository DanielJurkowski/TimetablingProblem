from copy import copy
from dataclasses import dataclass
from typing import Dict, List
import numpy as np
import numpy.random as random

from src.data_structures.lesson import Lesson
from src.data_structures.lesson_data_structures.group import Group
from src.data_structures.lesson_data_structures.room import Room
from src.data_structures.lesson_data_structures.subject import Subject
from src.data_structures.lesson_data_structures.teacher import Teacher
from src.optimization_functions.penalty_functions import free_periods_in_day, more_than_one_lesson, min_and_max_lessons_in_day, \
    same_subject_in_day


@dataclass
class Solution:
    number_groups: int
    number_teachers: int
    number_rooms: int
    number_days: int
    number_periods: int

    groups: Dict[int, Group] = None
    teachers: Dict[int, Teacher] = None
    subjects: Dict[int, Subject] = None
    rooms: Dict[int, Room] = None
    solution_matrix: np.ndarray = None
    cost = 0

    def compute_cost(self):
        weight_free_periods = 1
        weight_more_than_one_lesson = 1
        weight_min_and_max_lessons_in_day = 1
        weight_same_lesson_in_one_day = 1

        cost = [free_periods_in_day(self, weight_free_periods), more_than_one_lesson(self, weight_more_than_one_lesson),
                min_and_max_lessons_in_day(self, weight_min_and_max_lessons_in_day),
                same_subject_in_day(self, weight_same_lesson_in_one_day)]

        self.cost = cost

    def create_initial_solution(self, groups: Dict[int, Group], teachers: Dict[int, Teacher],
                                subjects: Dict[int, Subject], rooms: Dict[int, Room]):
        self.groups = groups
        self.teachers = teachers
        self.subjects = subjects
        self.rooms = rooms
        self.solution_matrix = np.empty((self.number_groups, self.number_periods, self.number_days), dtype=dict)
        self.solution_matrix[::] = {}

        self.number_groups = len(self.groups)
        self.number_teachers = len(self.teachers)
        self.number_rooms = len(self.rooms)

        for key_group, value_group in self.groups.items():
            for key_subject, value_subject in self.subjects.items():
                for times in range(value_subject.times_in_week):
                    room = rooms[random.randint(self.number_rooms)]
                    teacher = teachers[value_subject.subject_teacher - 1]
                    period = random.randint(self.number_periods)
                    day = random.randint(self.number_days)

                    lesson = Lesson(room, teacher, value_subject, value_group)

                    lessons = copy(self.solution_matrix[key_group][period][day])
                    lessons[len(lessons)] = lesson
                    self.solution_matrix[key_group, period, day] = lessons

                    teacher.change_availability_matrix(self, key_group, period, day)
                    room.change_availability_matrix(self, key_group, period, day)



