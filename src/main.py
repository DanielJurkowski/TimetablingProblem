import pandas as pd

from data_structures.lesson_data_structures import group
from data_structures.lesson_data_structures import room
from data_structures.lesson_data_structures import subject
from data_structures.lesson_data_structures import teacher
from data_structures.solution import Solution


def main():
    groups_file_path = "data/groups.csv"
    rooms_file_path = "data/rooms.csv"
    subjects_file_path = "data/subjects.csv"
    teachers_file_path = "data/teachers.csv"

    number_days = 5
    number_periods = 12

    groups = group.groups_factory(groups_file_path)
    rooms = room.rooms_factory(rooms_file_path)
    subjects = subject.subjects_factory(subjects_file_path)
    teachers = teacher.teachers_factory(teachers_file_path)

    solution = Solution(len(groups), len(teachers), len(rooms), number_days, number_periods)

    solution.create_initial_solution(groups, teachers, subjects, rooms)

    data_frames_groups = {}
    for group_number in range(len(groups)):
        data_frames_groups[group_number] = pd.DataFrame(solution.solution_matrix[group_number],
                                                        columns=['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'])

        data_frames_groups[group_number].to_csv(f'data/generated/group_{group_number}.csv')

    solution.compute_cost()
    print(solution.cost)

main()
