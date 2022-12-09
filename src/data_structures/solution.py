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
    more_than_one_lesson_teachers_and_rooms, free_periods_min_and_max_lessons_in_day_teachers, \
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
                        teacher = self.teachers[subject.teacher]

                        room = self.rooms[random.randint(self.number_rooms)]
                        period = random.randint(self.number_periods)
                        day = random.randint(self.number_days)

                        lesson = Lesson(room, teacher, subject, group)

                        lessons_cell = copy(self.solution_matrix[group_index][period][day])
                        lessons_cell[len(lessons_cell)] = lesson

                        self.solution_matrix[group_index, period, day] = lessons_cell

                        if len(self.solution_matrix[group_index, period, day]) > 1:
                            self.move_lesson_to_random_free(group_index, period, day)

                        teacher.change_availability_matrix(self, group_index, period, day, False)
                        room.change_availability_matrix(self, group_index, period, day, False)

            for teacher in range(self.number_teachers):
                self.fix_double_lessons_for_teacher(teacher)

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

    def move_lesson(self, group: int, period: int, day: int, new_period: int, new_day: int):
        if self.solution_matrix[group][period][day] and not self.solution_matrix[group][new_period][new_day]:
            lesson_cell = copy(self.solution_matrix[group][period][day])
            lesson_to_move = lesson_cell[len(lesson_cell) - 1]
            del lesson_cell[len(lesson_cell) - 1]
            self.solution_matrix[group][period][day] = lesson_cell

            lessons_cell_destination = copy(self.solution_matrix[group][new_period][new_day])
            lessons_cell_destination[len(lessons_cell_destination)] = lesson_to_move

            self.solution_matrix[group][new_period][new_day] = lessons_cell_destination
            self.move_teacher_availability(group, lesson_to_move, period, day, new_period, new_day)
            self.move_room_availability(group, lesson_to_move, period, day, new_period, new_day)

    def swap_lessons(self, group: int, period_1: int, day_1: int, period_2: int, day_2: int):
        if self.solution_matrix[group][period_1][day_1] and self.solution_matrix[group][period_2][day_2]:
            lesson_cell_1 = copy(self.solution_matrix[group][period_1][day_1])
            lesson_cell_2 = copy(self.solution_matrix[group][period_2][day_2])

            lesson_to_move_1 = lesson_cell_1[len(lesson_cell_1) - 1]
            del lesson_cell_1[len(lesson_cell_1) - 1]

            lesson_to_move_2 = lesson_cell_1[len(lesson_cell_2) - 1]
            del lesson_cell_2[len(lesson_cell_2) - 1]

            lesson_cell_1[len(lesson_cell_1)] = lesson_to_move_2
            lesson_cell_2[len(lesson_cell_2)] = lesson_to_move_1

            self.solution_matrix[group][period_1][day_1] = lesson_cell_2
            self.solution_matrix[group][period_2][day_2] = lesson_cell_1
            self.swap_teachers_availability(group, lesson_cell_1, period_1, day_1, lesson_cell_2, period_2, day_2)
            self.swap_rooms_availability(group, lesson_cell_1, period_1, day_1, lesson_cell_2, period_2, day_2)

    def move_lesson_to_random_free(self, group: int, period: int, day: int):
        if self.solution_matrix[group][period][day]:
            random_period = random.randint(self.number_periods)
            random_day = random.randint(self.number_days)

            while self.solution_matrix[group][random_period][random_day]:
                random_period = random.randint(self.number_periods)
                random_day = random.randint(self.number_days)

            self.move_lesson(group, period, day, random_period, random_day)

    # do zrobienia tego potrzeba jednak macierzy 3d dla dostępności nauczycieli => funkcja kary do zmiany

    # zamiar taki zeby sprawdzić czy dla danego terminu czy ma wiecej niz 1 lekcje, jezeli tak to przenosimy kazda
    # kolejna w randomowe wolne takie gdzie nauczyciel ma wolny termin dla danej grupy
    # jeżeli by zdarzyło się tak ze nauczyciel ma wolny termin ale w danym terminie wystepuje inna lekcja
    # to przeniesienie tej lekcji do randomowego wolnego gdzie nauczyciel tej lekcji ma wolny termin wtedy co grupa
    # jeżeli nie to tak samo itd.

    # wip

    # pokrywaja sie macierze count false_in_2d != count false_in_3d
    # problem jest w tym ze kiedy przenosimy lekcje to moze zmienic w 2d na true/false gdzie dalszej grupie w macierzy
    def fix_double_lessons_for_teacher(self, teacher: int):
        teacher = self.teachers[teacher]

        for period in range(self.number_periods):
            for day in range(self.number_days):
                for group in range(self.number_groups):
                    first_lesson_appeared = False

                    if not first_lesson_appeared:
                        if not teacher.availability_matrix_3d[group][period][day]:
                            first_lesson_appeared = True

                    if first_lesson_appeared and not teacher.availability_matrix_3d[group][period][day]:
                        free_slot = np.argwhere(teacher.availability_matrix)

                        free_slot_index = 0
                        free_slot_period = free_slot[free_slot_index][0]
                        free_slot_day = free_slot[free_slot_index][1]

                        while self.solution_matrix[group][free_slot_period][free_slot_day]:
                            free_slot_index += 1

                            if free_slot_index < len(free_slot):
                                free_slot_period = free_slot[free_slot_index][0]
                                free_slot_day = free_slot[free_slot_index][1]

                            else:
                                self.move_lesson_to_random_free(group, period, day)
                                self.fix_double_lessons_for_teacher(teacher.id)

                        self.move_lesson(group, period, day, free_slot_period, free_slot_day)

    def move_teacher_availability(self, group: int, lesson: Lesson, period: int, day: int, new_period: int,
                                  new_day: int):
        self.teachers[lesson.teacher.id].change_availability_matrix(self, group, period, day, True)
        self.teachers[lesson.teacher.id].change_availability_matrix(self, group, new_period, new_day, False)

    def swap_teachers_availability(self, group: int, lesson_1: Lesson, period_1: int, day_1: int, lesson_2: Lesson,
                                   period_2: int, day_2: int):
        self.move_teacher_availability(group, lesson_1, period_1, day_1, period_2, day_2)
        self.move_teacher_availability(group, lesson_2, period_2, day_2, period_1, day_1)

    def move_room_availability(self, group: int, lesson: Lesson, period: int, day: int, new_period: int, new_day: int):
        self.rooms[lesson.room.id].change_availability_matrix(self, group, period, day, True)
        self.rooms[lesson.room.id].change_availability_matrix(self, group, new_period, new_day, False)

    def swap_rooms_availability(self, group: int, lesson_1: Lesson, period_1: int, day_1: int, lesson_2: Lesson,
                                period_2: int, day_2: int):
        self.move_room_availability(group, lesson_1, period_1, day_1, period_2, day_2)
        self.move_room_availability(group, lesson_2, period_2, day_2, period_1, day_1)
