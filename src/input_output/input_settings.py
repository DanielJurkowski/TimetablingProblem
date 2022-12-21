import re
import sys
import os

pattern = re.compile("^.*\.(csv)$")


def input_settings(setting: str, temperature_max=None, temperature_min=None, k_max=None, alpha=None,
                   max_iterations=None):

    if setting == "groups":
        input_file_path = input('\033[31m' + 'File path to groups CSV file (default "data/initial_data/groups.csv"): '
                                + '\033[0m')

        if len(input_file_path) > 0:
            while not re.match(pattern, input_file_path) and len(input_file_path) > 0:
                print('\033[31m', "Wrong file extension", '\033[0m')
                input_file_path = input(
                    '\033[31m' + 'File path to groups CSV file (default "data/initial_data/groups.csv"): ' +
                    '\033[0m')

                if len(input_file_path) == 0:
                    input_file_path = 'data/initial_data/groups.csv'
                    print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
                    return input_file_path

            print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
            return input_file_path

        if len(input_file_path) == 0:
            input_file_path = 'data/initial_data/groups.csv'
            print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
            return input_file_path

    if setting == "rooms":
        input_file_path = input('\033[31m' + 'File path to rooms CSV file (default "data/initial_data/rooms.csv)": '
                                + '\033[0m')

        if len(input_file_path) > 0:
            while not re.match(pattern, input_file_path) and len(input_file_path) > 0:
                print('\033[31m', "Wrong file extension", '\033[0m')
                input_file_path = input(
                    '\033[31m' + 'File path to rooms CSV file (default "data/initial_data/rooms.csv"): ' +
                    '\033[0m')

                if len(input_file_path) == 0:
                    input_file_path = "data/initial_data/rooms.csv"
                    print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
                    return input_file_path

            print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
            return input_file_path

        if len(input_file_path) == 0:
            input_file_path = "data/initial_data/rooms.csv"
            print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
            return input_file_path

    if setting == "subjects":
        input_file_path = input('\033[31m' + 'File path to subjects CSV file (default '
                                             '"data/initial_data/subjects.csv"): ' + '\033[0m')

        if len(input_file_path) > 0:
            while not re.match(pattern, input_file_path) and len(input_file_path) > 0:
                print('\033[31m', "Wrong file extension", '\033[0m')
                input_file_path = input(
                    '\033[31m' + 'File path to subjects CSV file (default "data/initial_data/subjects.csv"): ' +
                    '\033[0m')

                if len(input_file_path) == 0:
                    input_file_path = "data/initial_data/subjects.csv"
                    print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
                    return input_file_path

            print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
            return input_file_path

        if len(input_file_path) == 0:
            input_file_path = "data/initial_data/subjects.csv"
            print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
            return input_file_path

    if setting == "teachers":
        input_file_path = input('\033[31m' + 'File path to teachers CSV file (default '
                                             '"data/initial_data/teachers.csv"): ' + '\033[0m')

        if len(input_file_path) > 0:
            while not re.match(pattern, input_file_path) and len(input_file_path) > 0:
                print('\033[31m', "Wrong file extension", '\033[0m')
                input_file_path = input(
                    '\033[31m' + 'File path to teachers CSV file (default "data/initial_data/teachers.csv"): ' +
                    '\033[0m')

                if len(input_file_path) == 0:
                    input_file_path = "data/initial_data/teachers.csv"
                    print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
                    return input_file_path

            print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
            return input_file_path

        if len(input_file_path) == 0:
            input_file_path = "data/initial_data/teachers.csv"
            print('\033[31m', "File path set to: ", '\033[0m', input_file_path)
            return input_file_path

    if setting == "temperature_max":
        try:
            temperature_max = input('\033[31m' + 'Max temperature (default "150"): ' + '\033[0m')

            while int(temperature_max) <= 0:
                print('\033[31m', "Must be positive", '\033[0m')
                temperature_max = input_settings(setting)

                return temperature_max

            print('\033[31m', "Max temperature set to: ", '\033[0m', temperature_max)
            return int(temperature_max)

        except ValueError:
            if temperature_max == '':
                print('\033[31m', "Max temperature set to: ", '\033[0m', 150)
                return 150

            print('\033[31m', "Must be a number", '\033[0m')
            temperature_max = input_settings(setting)

            return int(temperature_max)

    if setting == "temperature_min":
        try:
            temperature_min = input('\033[31m' + 'Min temperature (default "5"): ' + '\033[0m')

            while int(temperature_min) <= 0 or int(temperature_min) >= temperature_max:
                print('\033[31m', "Must be positive and lower than max temperature", '\033[0m')
                temperature_min = input_settings(setting, temperature_max)

                return temperature_min

            print('\033[31m', "Min temperature set to: ", '\033[0m', temperature_min)
            return int(temperature_min)

        except ValueError:
            if temperature_min == '':
                print('\033[31m', "Min temperature set to: ", '\033[0m', 5)
                return 5

            print('\033[31m', "Must be a number", '\033[0m')
            temperature_min = input_settings(setting, temperature_max)

            return int(temperature_min)

    if setting == "k_max":
        try:
            k_max = input('\033[31m' + 'Iterations at given temperature: (default "20"): ' + '\033[0m')

            while int(k_max) <= 0:
                print('\033[31m', "Must be positive", '\033[0m')
                k_max = input_settings(setting)

                return k_max

            print('\033[31m', "Iterations at given temperature set to: ", '\033[0m', k_max)
            return int(k_max)

        except ValueError:
            if k_max == '':
                print('\033[31m', "Iterations at given temperature set to: ", '\033[0m', 20)
                return 20

            print('\033[31m', "Must be a number", '\033[0m')
            k_max = input_settings(setting)

            return int(k_max)

    if setting == "alpha":
        try:
            alpha = input('\033[31m' + 'Alpha (default "0.9999"): ' + '\033[0m')

            while float(alpha) <= 0 or float(alpha) >= 1:
                print('\033[31m', "Must be positive and less than one", '\033[0m')
                alpha = input_settings(setting)

                return alpha

            print('\033[31m', "Alpha set to: ", '\033[0m', alpha)
            return float(alpha)

        except ValueError:
            if alpha == '':
                print('\033[31m', "Alpha set to: ", '\033[0m', 0.9999)
                return 0.9999

            print('\033[31m', "Must be a number", '\033[0m')
            alpha = input_settings(setting)

            return float(alpha)

    if setting == "max_iterations":
        try:
            max_iterations = input('\033[31m' + 'Max iterations (default "10e6"): ' + '\033[0m')

            while int(max_iterations) < 0:
                print('\033[31m', "Must be positive", '\033[0m')
                max_iterations = input_settings(setting)

                return max_iterations

            print('\033[31m', "Max iterations set to: ", '\033[0m', max_iterations)
            return int(max_iterations)

        except ValueError:
            if max_iterations == '':
                print('\033[31m', "Max iterations set to: ", '\033[0m', 1000000)
                return 10e6

            print('\033[31m', "Must be a number", '\033[0m')
            max_iterations = input_settings(setting)

            return int(max_iterations)

    if setting == "neighbor":
        neighbor = input('\033[31m' + 'Create neighbor with lesson swap (default "True"): ' + '\033[0m')

        if neighbor == 'True':
            print('\033[31m', "Create neighbor with lesson swap set to: ", '\033[0m', False)
            return True

        if neighbor == 'False':
            print('\033[31m', "Create neighbor with lesson swap set to: ", '\033[0m', False)
            return False

        if len(neighbor) == 0:
            print('\033[31m', "Create neighbor with lesson swap set to: ", '\033[0m', True)
            return True

        else:
            print('\033[31m', "Must be a bool value", '\033[0m')
            input_settings(setting)
