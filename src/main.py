import pandas as pd

from data_structures.lesson_data_structures import group
from data_structures.lesson_data_structures import room
from data_structures.lesson_data_structures import subject
from data_structures.lesson_data_structures import teacher
from data_structures.solution import Solution
from src.algorithm.simulated_annealing import SimulatedAnnealing
import matplotlib.pyplot as plt


def main():
    # files input set up
    groups_file_path = "data/groups.csv"
    rooms_file_path = "data/rooms.csv"
    subjects_file_path = "data/subjects.csv"
    teachers_file_path = "data/teachers.csv"

    # solution settings
    number_days = 5
    number_periods = 14

    # create objects from files
    groups = group.groups_factory(groups_file_path)
    rooms = room.rooms_factory(rooms_file_path)
    subjects = subject.subjects_factory(subjects_file_path)
    teachers = teacher.teachers_factory(teachers_file_path)

    # create solution object
    solution = Solution(groups, teachers, rooms, subjects, number_days, number_periods)
    solution.create_initial_solution()

    # create simulated annealing object
    simulated_annealing = SimulatedAnnealing(temperature_max=100, temperature_min=5, k_max=5, alpha=0.9999,
                                             max_iterations=10e8, initial_solution=solution)

    simulated_annealing.initialize_algorithm()

    initial_solution, best_solution, initial_solution_cost, best_solution_cost, current_iteration, temperature_chart, \
    cost_chart = simulated_annealing.start_algorithm()

    print(initial_solution_cost)
    print(best_solution_cost)
    print(current_iteration)
    print(best_solution.check_if_solution_acceptable())
    print(temperature_chart)
    print(cost_chart)

    # generate data frames of timetables from solutions
    data_frames_groups = {}
    for group_number in range(len(groups)):
        data_frames_groups[group_number] = pd.DataFrame(best_solution.solution_matrix[group_number],
                                                        columns=['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'])

        data_frames_groups[group_number].to_csv(f'data/generated/group_{group_number}.csv')

    plt.plot(temperature_chart)
    plt.show()

    plt.plot(cost_chart)
    plt.show()


main()
