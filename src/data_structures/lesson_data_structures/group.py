from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class Group:
    group_id: int
    group_name: str


def groups_factory(file_path: str):
    groups = {}

    file = pd.read_csv(file_path)

    for index, row in file.iterrows():
        groups[row['group_id']] = Group(row['group_id'], row['group_name'])

    return groups
