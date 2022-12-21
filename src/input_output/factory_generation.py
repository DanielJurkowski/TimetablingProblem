from src.data_structures.lesson_data_structures import group
from src.data_structures.lesson_data_structures import room
from src.data_structures.lesson_data_structures import subject
from src.data_structures.lesson_data_structures import teacher
from src.input_output.input_settings import input_settings


def factory_generation(file: str):
    if file == "groups":
        try:
            groups_file_path = input_settings(file)
            groups = group.groups_factory(groups_file_path)

            return groups

        except FileNotFoundError:
            print('\033[31m', 'File does not exist, set up new file path', '\033[0m')
            groups = factory_generation(file)

            return groups

    elif file == "rooms":
        try:
            rooms_file_path = input_settings(file)
            rooms = room.rooms_factory(rooms_file_path)

            return rooms

        except FileNotFoundError:
            print('\033[31m', 'File does not exist, set up new file path', '\033[0m')
            rooms = factory_generation(file)

            return rooms

    elif file == "subjects":
        try:
            subjects_file_path = input_settings(file)
            subjects = subject.subjects_factory(subjects_file_path)

            return subjects

        except FileNotFoundError:
            print('\033[31m', 'File does not exist, set up new file path', '\033[0m')
            subjects = factory_generation(file)

            return subjects

    elif file == "teachers":
        try:
            teachers_file_path = input_settings(file)
            teachers = teacher.teachers_factory(teachers_file_path)

            return teachers

        except FileNotFoundError:
            print('\033[31m', 'File does not exist, set up new file path', '\033[0m')
            teachers = factory_generation(file)

            return teachers
