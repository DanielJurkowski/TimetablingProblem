def more_than_one_lesson_same_subject_in_day_groups(solution, weight_more_than_one_lesson: int,
                                                    weight_same_subject: int):
    cost_more_than_one_lesson = 0
    cost_same_subject = 0

    for group in range(solution.number_groups):
        for day in range(solution.number_days):
            subjects_in_one_day = []

            for period in range(solution.number_periods):
                if len(solution.solution_matrix[group][period][day]) > 1:
                    cost_more_than_one_lesson += len(solution.solution_matrix[group][period][day])

                if bool(solution.solution_matrix[group][period][day]):
                    for _, lesson in solution.solution_matrix[group][period][day].items():
                        subjects_in_one_day.append(lesson.subject.id)

            set_subjects_in_one_day = set(subjects_in_one_day)

            cost_same_subject += (len(subjects_in_one_day) - len(set_subjects_in_one_day))

    return weight_more_than_one_lesson * cost_more_than_one_lesson, weight_same_subject * cost_same_subject


def more_than_one_lesson_teachers_and_rooms(solution, weight_teachers: int, weight_rooms: int):
    cost_teachers = 0
    cost_rooms = 0

    index_teacher = []
    index_rooms = []

    for period in range(solution.number_periods):
        for day in range(solution.number_days):
            teachers_in_one_period = []
            rooms_in_one_period = []

            for group in range(len(solution.groups)):
                if bool(solution.solution_matrix[group][period][day]):
                    for _, lesson in solution.solution_matrix[group][period][day].items():
                        teachers_in_one_period.append(lesson.teacher.id)
                        rooms_in_one_period.append(lesson.room.id)

            set_teachers_in_one_period = set(teachers_in_one_period)
            set_rooms_in_one_period = set(rooms_in_one_period)

            cost_teachers += (len(teachers_in_one_period) - len(set_teachers_in_one_period))
            cost_rooms += len(rooms_in_one_period) - len(set_rooms_in_one_period)

    return weight_teachers * cost_teachers, weight_rooms * cost_rooms


def free_periods_min_and_max_lessons_in_day_groups(solution, weight_free_periods: int, weight_min_max_lessons: int):
    cost_free_periods = 0
    cost_min_and_max_lessons = 0

    for group in range(solution.number_groups):
        for day in range(solution.number_days):
            free_periods = 0
            lessons_start = False
            start_index = 0
            end_index = 0

            lessons_in_day = 0

            for period in range(solution.number_periods):
                if bool(solution.solution_matrix[group][period][day]):
                    if not lessons_start:
                        lessons_start = True
                        start_index = period

                    if lessons_start:
                        end_index = period

                    lessons_in_day += 1

            for period in range(start_index, end_index):
                if not bool(solution.solution_matrix[group][period][day]):
                    if lessons_start:
                        free_periods += 1

            cost_free_periods += free_periods

            if lessons_in_day < 4:
                cost_min_and_max_lessons += 4 - lessons_in_day

            if lessons_in_day > 8:
                cost_min_and_max_lessons += lessons_in_day - 8

    return weight_free_periods * cost_free_periods, weight_min_max_lessons * cost_min_and_max_lessons


def free_periods_min_and_max_lessons_in_day_teachers(solution, weight_free_periods: int, weight_min_max_lessons: int):
    cost_free_periods = 0
    cost_min_and_max_lessons = 0

    for _, teacher in solution.teachers.items():
        for day in range(solution.number_days):
            free_periods = 0
            lessons_start = False
            start_index = 0
            end_index = 0

            lessons_in_day = 0

            for period in range(solution.number_periods):
                if not teacher.availability_matrix[period][day]:
                    lessons_in_day += 1

                if teacher.availability_matrix[period][day]:
                    if not lessons_start:
                        lessons_start = True
                        start_index = period

                    if lessons_start:
                        end_index = period

            for period in range(start_index, end_index):
                if not teacher.availability_matrix[period][day]:
                    if lessons_start:
                        free_periods += 1

            if lessons_in_day < 3:
                cost_min_and_max_lessons += 3 - lessons_in_day

            if lessons_in_day > 8:
                cost_min_and_max_lessons += lessons_in_day - 8

            if free_periods > 2:
                cost_free_periods += free_periods

            if free_periods < 2:
                cost_free_periods += 0.5 * free_periods

    return weight_free_periods * cost_free_periods, weight_min_max_lessons * cost_min_and_max_lessons
