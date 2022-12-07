from dataclasses import dataclass
import pandas as pd


@dataclass
class Subject:
    subject_id: int
    subject_name: str
    subject_teacher: int
    times_in_week: int


def subjects_factory(file_path: str):
    subjects = {}

    file = pd.read_csv(file_path)

    for index, row in file.iterrows():
        subjects[row['subject_id']] = Subject(row['subject_id'], row['subject_name'], row['subject_teacher'],
                                              row['times_in_week'])

    return subjects
