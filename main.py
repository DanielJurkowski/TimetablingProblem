import pandas as pd

from src.data_structures.solution import Solution
from src.algorithm.simulated_annealing import SimulatedAnnealing
from src.input_output.adjust_excel import adjust_excel
from src.input_output.factory_generation import factory_generation
from src.input_output.input_settings import input_settings


def main():
    # files input set up and create objects from files
    groups = factory_generation("groups")
    rooms = factory_generation("rooms")
    subjects = factory_generation("subjects")
    teachers = factory_generation("teachers")

    print('\033[31m', "\nFiles set up ready\n", '\033[0m')

    # number of days and periods
    number_days = 5
    number_periods = 12

    # create best_solution object
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

    simulated_annealing = SimulatedAnnealing(temperature_max=temperature_max, temperature_min=temperature_min,
                                             k_max=k_max, alpha=alpha, max_iterations=max_iterations,
                                             initial_solution=solution, swap=neighbor,
                                             cooling_schedule=cooling_schedule)

    simulated_annealing.initialize_algorithm()

    initial_solution, best_solution, initial_solution_cost, best_solution_cost, current_iteration, temperature_chart, \
    cost_chart, best_cost_chart, runtime = simulated_annealing.start_algorithm()

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
             '14:10-14:55', '15:00-15:45', '15:50-16:35', '16:40-17:25', '17:30-18:15']

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
