from dataclasses import dataclass

from src.data_structures.lesson_data_structures.group import Group
from src.data_structures.lesson_data_structures.room import Room
from src.data_structures.lesson_data_structures.subject import Subject
from src.data_structures.lesson_data_structures.teacher import Teacher


@dataclass
class Lesson:
    lesson_room: Room
    lesson_teacher: Teacher
    lesson_subject: Subject
    lesson_group: Group

    def __repr__(self):
        repr = self.lesson_room.room_name + " | " + self.lesson_teacher.teacher_name + " | " + self.lesson_subject.subject_name

        return repr

    def __str__(self):
        str = self.lesson_room.room_name + " | " + self.lesson_teacher.teacher_name + " | " + self.lesson_subject.subject_name

        return str
