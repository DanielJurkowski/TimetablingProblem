import math
from typing import Callable

CoolingSchedule = Callable[[float, float, int], float]


def exponential_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature * (alpha ** k)


def linear_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature - alpha * k


def logarithmic_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature / (1 + alpha * math.log(k + 1))


def quadratic_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature / (1 + alpha * (k ** 2))


def boltzmann_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature / (1 + math.log(k))


def cauchy_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature / (1 + k)


def pick_cooling_schedule(cooling_schedule: str):
    if cooling_schedule == 'linear':
        return linear_cooling_schedule

    if cooling_schedule == 'logarithmic':
        return logarithmic_cooling_schedule

    if cooling_schedule == 'quadratic':
        return quadratic_cooling_schedule

    if cooling_schedule == 'boltzmann':
        return boltzmann_cooling_schedule

    if cooling_schedule == 'cauchy':
        return cauchy_cooling_schedule

    if len(cooling_schedule) == 0 or cooling_schedule == 'exponential':
        return exponential_cooling_schedule
