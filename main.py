import os

import pandas as pd

from src.data_structures.lesson_data_structures import group, room, subject, teacher
from src.algorithm.simulated_annealing import SimulatedAnnealing
from src.data_structures.solution import Solution
from src.input_output.adjust_excel import adjust_excel
from src.input_output.factory_generation import factory_generation
from src.input_output.input_settings import input_settings
from src.algorithm.cooling_schedules.cooling_schedule import pick_cooling_schedule


def main():
    # number of days and periods
    number_days = 5
    number_periods = 13

    test_mode = input_settings("test")

    # test mode
    if test_mode:
        for directory in os.listdir("tests/data/initial_data"):
            groups = None
            rooms = None
            subjects = None
            teachers = None

            for filename in os.listdir("tests/data/initial_data/" + directory):
                path = "tests/data/initial_data/" + directory + "/" + filename

                # create objects for each size of data sets
                if filename == "data.ipynb":
                    pass

                else:
                    if filename == "groups.csv":
                        groups = group.groups_factory(path)

                    if filename == "rooms.csv":
                        rooms = room.rooms_factory(path)

                    if filename == "subjects.csv":
                        subjects = subject.subjects_factory(path)

                    if filename == "teachers.csv":
                        teachers = teacher.teachers_factory(path)

            for filename in os.listdir("tests/data/parameters"):
                path = "tests/data/parameters/" + filename

                if filename == 'parameters.ipynb':
                    pass

                else:
                    parameters = pd.read_csv(path)
                    parameters = parameters['value'].to_list()

                    cooling_schedule = pick_cooling_schedule(str(parameters[0]))
                    temperature_max = float(parameters[1])
                    temperature_min = float(parameters[2])
                    k_max = int(parameters[3])
                    alpha = float(parameters[4])
                    max_iterations = int(parameters[5])
                    neighbor = True if str(parameters[6]) == "TRUE" else False

                    # create solution object
                    solution = Solution(groups, teachers, rooms, subjects, number_days, number_periods)
                    solution.create_initial_solution()

                    # algorithm
                    simulated_annealing = SimulatedAnnealing(temperature_max=temperature_max,
                                                             temperature_min=temperature_min,
                                                             k_max=k_max, alpha=alpha, max_iterations=5000,
                                                             initial_solution=solution, swap=neighbor,
                                                             cooling_schedule=cooling_schedule)

                    simulated_annealing.initialize_algorithm()

                    print('\033[31m', f"\n{directory}_{filename}", '\033[0m')
                    initial_solution, best_solution, initial_solution_cost, best_solution_cost, current_iteration, \
                    temperature_chart, cost_chart, best_cost_chart, runtime, range_iterations = simulated_annealing.start_algorithm()

                    try:
                        results = pd.read_excel(f'tests/results/{directory}.xlsx', index_col=0)

                    except FileNotFoundError:
                        logs = {f'{filename}': [temperature_max, temperature_min, k_max, alpha, max_iterations,
                                                neighbor, cooling_schedule, initial_solution_cost, best_solution_cost,
                                                current_iteration, best_solution.check_if_solution_acceptable(),
                                                runtime, range_iterations, float(current_iteration / range_iterations)]}

                        results = pd.DataFrame(logs, index=[
                            'Max temperature',
                            'Min temperature',
                            'K max',
                            'Alpha',
                            'Max iterations',
                            'Neighbor with lesson swap',
                            'Cooling schedule',
                            'Initial solution cost',
                            'Best solution cost',
                            'Iterations',
                            'Is best solution acceptable',
                            'Runtime',
                            'Iterations to run',
                            '% of completion'
                        ])

                        results.to_excel(f'tests/results/{directory}.xlsx')

                    results[f'{filename}'] = [temperature_max, temperature_min, k_max, alpha, max_iterations,
                                              neighbor, cooling_schedule, initial_solution_cost, best_solution_cost,
                                              current_iteration, best_solution.check_if_solution_acceptable(),
                                              runtime, range_iterations, float(current_iteration / range_iterations)]

                    results.to_excel(f'tests/results/{directory}.xlsx')

    # normal mode
    else:
        # files input set up and create objects from files
        groups = factory_generation("groups")
        rooms = factory_generation("rooms")
        subjects = factory_generation("subjects")
        teachers = factory_generation("teachers")

        print('\033[31m', "\nFiles set up ready\n", '\033[0m')

        # create solution object
        solution = Solution(groups, teachers, rooms, subjects, number_days, number_periods)
        solution.create_initial_solution()

        # create simulated annealing object
        cooling_schedule = input_settings("cooling_schedule")
        temperature_max = input_settings("temperature_max")
        temperature_min = input_settings("temperature_min", temperature_max)
        k_max = input_settings("k_max")
        alpha = input_settings("alpha")
        max_iterations = input_settings("max_iterations")
        neighbor = input_settings("neighbor")

        print('\033[31m', "\nAlgorithm set up ready", '\033[0m')
        print('\033[31m', "\nProgress:", '\033[0m')

        # algorithm
        simulated_annealing = SimulatedAnnealing(temperature_max=temperature_max, temperature_min=temperature_min,
                                                 k_max=k_max, alpha=alpha, max_iterations=max_iterations,
                                                 initial_solution=solution, swap=neighbor,
                                                 cooling_schedule=cooling_schedule)

        simulated_annealing.initialize_algorithm()

        initial_solution, best_solution, initial_solution_cost, best_solution_cost, current_iteration, temperature_chart, \
        cost_chart, best_cost_chart, runtime, _ = simulated_annealing.start_algorithm()

        print('\033[31m', '\nThe algorithm has completed the search for the optimal solution.'
                          '\nThe generated solution was placed in ', '\033[0m',
              'data/generated_data/best_solution/solution.ipynb', '\033[31m',
              '\nGenerated plans are available in excel format in ', '\033[0m',
              'data/generated_data/best_solution/timetables')
        print('\033[31m', "Initial solution cost: ", '\033[0m', initial_solution_cost)
        print('\033[31m', "Best solution cost: ", '\033[0m', best_solution_cost)
        print('\033[31m', "Iterations: ", '\033[0m', current_iteration)
        print('\033[31m', "Is best solution acceptable: ", '\033[0m', best_solution.check_if_solution_acceptable())
        print('\033[31m', "Runtime: ", '\033[0m', "{time:.4f} [s]".format(time=runtime))

        # generate data frames of timetables from solutions
        hours = ['8:00-8:45', '8:50-9:35', '9:40-10:45', '10:50-11:35', '11:40-12:25', '12:30-13:15', '13:20-14:05',
                 '14:10-14:55', '15:00-15:45', '15:50-16:35', '16:40-17:25', '17:30-18:15', '18:20-19:05']

        data_frames_groups_initial_solution = {}
        for group_number in range(len(groups)):
            data_frames_groups_initial_solution[group_number] = \
                pd.DataFrame(initial_solution.solution_matrix[group_number],
                             columns=['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'])

            data_frames_groups_initial_solution[group_number].insert(0, 'Hours', hours)

            data_frames_groups_initial_solution[group_number]. \
                to_csv(f'data/generated_data/initial_solution/timetables/group_{group_number}.csv', index=False)

        data_frames_groups_best_solution = {}
        for group_number in range(len(groups)):
            data_frames_groups_best_solution[group_number] = \
                pd.DataFrame(best_solution.solution_matrix[group_number],
                             columns=['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'])

            data_frames_groups_best_solution[group_number].insert(0, 'Hours', hours)

            data_frames_groups_best_solution[group_number]. \
                to_excel(f'data/generated_data/best_solution/timetables/group_{group_number}.xlsx')

            adjust_excel(f'data/generated_data/best_solution/timetables/group_{group_number}.xlsx',
                         data_frames_groups_best_solution[group_number])

        logs = {'Value': [temperature_max, temperature_min, k_max, alpha, max_iterations,
                          neighbor, cooling_schedule, initial_solution_cost, best_solution_cost, current_iteration,
                          best_solution.check_if_solution_acceptable(), runtime]}

        data_frame_logs = pd.DataFrame(logs, index=[
            'Max temperature',
            'Min temperature',
            'K max',
            'Alpha',
            'Max iterations',
            'Neighbor with lesson swap',
            'Cooling schedule',
            'Initial solution cost',
            'Best solution cost',
            'Iterations',
            'Is best solution acceptable',
            'Runtime'
        ])
        data_frame_logs.to_csv('data/generated_data/best_solution/logs.csv')

        data_frame_temperature = pd.DataFrame(temperature_chart, columns=["Temperature"])
        data_frame_cost = pd.DataFrame(cost_chart, columns=["Cost"])
        data_frame_best_cost = pd.DataFrame(best_cost_chart, columns=["Cost"])
        data_frame_temperature.to_csv('data/generated_data/best_solution/charts_data/temperature.csv', index=False)
        data_frame_cost.to_csv('data/generated_data/best_solution/charts_data/cost.csv', index=False)
        data_frame_best_cost.to_csv('data/generated_data/best_solution/charts_data/best_cost.csv', index=False)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print('\n\033[31m', "Keyboard Interrupt", '\033[0m')
