from dataclasses import dataclass

from src.data_structures.lesson_data_structures.group import Group
from src.data_structures.lesson_data_structures.room import Room
from src.data_structures.lesson_data_structures.subject import Subject
from src.data_structures.lesson_data_structures.teacher import Teacher


@dataclass
class Lesson:
    room: Room
    teacher: Teacher
    subject: Subject
    group: Group

    def __repr__(self):
        representation = self.room.name + " | " + self.teacher.name + " | " + self.subject.name

        return representation

    def __str__(self):
        string = self.room.name + " | " + self.teacher.name + " | " + self.subject.name

        return string
