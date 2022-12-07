def more_than_one_lesson_groups(solution, weight):
    cost = 0

    for group in range(solution.number_groups):
        for period in range(solution.number_periods):
            for day in range(solution.number_days):
                if len(solution.solution_matrix[group][period][day]) > 1:
                    cost += weight * len(solution.solution_matrix[group][period][day])

    return weight * cost


def more_than_one_lesson_teachers_and_rooms(solution, weight):
    cost = 0

    for period in range(solution.number_periods):
        for day in range(solution.number_days):
            teachers_in_one_period = []
            rooms_in_one_period = []
            for group in range(len(solution.groups)):
                if bool(solution.solution_matrix[group][period][day]):
                    for index, lesson in solution.solution_matrix[group][period][day].items():
                        teachers_in_one_period.append(lesson.lesson_teacher.teacher_id)
                        rooms_in_one_period.append(lesson.lesson_room.room_id)

            set_teachers_in_one_period = set(teachers_in_one_period)
            set_rooms_in_one_period = set(rooms_in_one_period)

            cost += (len(teachers_in_one_period) - len(set_teachers_in_one_period)) + (
                    len(rooms_in_one_period) - len(set_rooms_in_one_period))

    return weight * cost


def same_subject_in_day(solution, weight):
    cost = 0

    for group in range(solution.number_groups):
        for day in range(solution.number_days):
            subjects_in_one_day = []
            for period in range(solution.number_periods):
                if bool(solution.solution_matrix[group][period][day]):
                    for index, lesson in solution.solution_matrix[group][period][day].items():
                        subjects_in_one_day.append(lesson.lesson_subject.subject_id)

            set_subjects_in_one_day = set(subjects_in_one_day)

            cost += (len(subjects_in_one_day) - len(set_subjects_in_one_day))

    return weight * cost


def free_periods_in_day_groups(solution, weight):
    cost = 0

    for group in range(solution.number_groups):
        for day in range(solution.number_days):
            free_periods = 0
            lessons_start = False
            start_index = 0
            end_index = 0
            for period in range(solution.number_periods):
                if bool(solution.solution_matrix[group][period][day]):
                    if not lessons_start:
                        lessons_start = True
                        start_index = period

                    if lessons_start:
                        end_index = period

            for period in range(start_index, end_index):
                if not bool(solution.solution_matrix[group][period][day]):
                    if lessons_start:
                        free_periods += 1

            cost += free_periods

    return weight * cost


def free_periods_in_day_teachers(solution, weight):
    cost = 0

    for index, teacher in solution.teachers.items():
        for group in range(solution.number_groups):
            for day in range(solution.number_days):
                free_periods = 0
                lessons_start = False
                start_index = 0
                end_index = 0
                for period in range(solution.number_periods):
                    if not teacher.availability_matrix[group][period][day]:
                        if not lessons_start:
                            lessons_start = True
                            start_index = period

                        if lessons_start:
                            end_index = period

                for period in range(start_index, end_index):
                    if teacher.availability_matrix[group][period][day]:
                        if lessons_start:
                            free_periods += 1

                if free_periods > 2:
                    cost += free_periods
                else:
                    cost = 0

    return weight * cost


def min_and_max_lessons_in_day_groups(solution, weight):
    cost = 0

    for group in range(solution.number_groups):
        for day in range(solution.number_days):
            lessons_in_day = 0
            for period in range(solution.number_periods):
                if bool(solution.solution_matrix[group][period][day]):
                    lessons_in_day += 1

            if lessons_in_day < 4:
                cost += 4 - lessons_in_day

            if lessons_in_day > 8:
                cost += lessons_in_day - 8

    return weight * cost


def min_and_max_lessons_in_day_teachers(solution, weight):
    cost = 0

    for index, teacher in solution.teachers.items():
        for group in range(solution.number_groups):
            for day in range(solution.number_days):
                lessons_in_day = 0
                for period in range(solution.number_periods):
                    if not teacher.availability_matrix[group][period][day]:
                        lessons_in_day += 1

                if lessons_in_day < 4:
                    cost += 4 - lessons_in_day

                if lessons_in_day > 8:
                    cost += lessons_in_day - 8

    return weight * cost
