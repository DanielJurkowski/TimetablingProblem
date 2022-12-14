from ctypes import Union
from dataclasses import dataclass
from random import random
from typing import Callable, List
import math

from src.data_structures.solution import Solution

CoolingSchedule = Callable[[float, float, int], float]


def exponential_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature * (alpha ** k)


def linear_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature - alpha * k


def logarithmic_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature / (alpha * math.log(k + 1))


def quadratic_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature / (1 + alpha * (k ** 2))


def bolzmann_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature / (1 + math.log(k))


def cauchy_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature / (1 + k)


@dataclass
class SimulatedAnnealing:
    temperature_max: float
    temperature_min: float
    k_max: int
    alpha: float
    max_iterations: int

    initial_solution: Solution
    best_solution: Solution = None
    initial_solution_cost: int = None
    best_solution_cost: int = None

    current_solution: Solution = None
    current_solution_cost: int = None

    current_temperature: float = None
    current_iteration: int = None

    new_solution: Solution = None
    new_solution_cost: int = None

    cooling_schedule: CoolingSchedule = exponential_cooling_schedule

    temperature_chart = []
    cost_chart = []
    cost_ten_iterations_ago: int = None

    def initialize_algorithm(self):
        self.initial_solution.compute_cost()
        self.initial_solution_cost = self.initial_solution.cost

        self.best_solution = self.initial_solution
        self.best_solution_cost = self.initial_solution_cost

        self.current_solution = self.initial_solution
        self.current_solution_cost = self.initial_solution_cost

        self.current_temperature = self.temperature_max
        self.current_iteration = 0

        self.current_solution.compute_cost()
        self.current_solution_cost = self.current_solution.cost

        self.temperature_chart.append(self.temperature_max)
        self.cost_chart.append(self.best_solution_cost)

    def start_algorithm(self):
        while self.current_temperature > self.temperature_min and self.current_iteration < self.max_iterations:
            for k in range(self.k_max):
                self.new_solution = self.current_solution.neighborhood_creation()
                self.new_solution.compute_cost()
                self.new_solution_cost = self.new_solution.cost

                # jakaś heurestyka do poprawy gdy po danej ilości iteracji nie nastąpi znaczna poprawa
                # if self.current_iteration % 25 == 0:
                #     if self.current_iteration == 0:
                #         self.cost_ten_iterations_ago = self.current_solution_cost
                #
                #     else:
                #         if abs(self.current_solution_cost - self.cost_ten_iterations_ago) <= 1000:
                #             self.new_solution.improve_solution()
                #
                #         self.cost_ten_iterations_ago = self.current_solution_cost

                delta = self.new_solution_cost - self.current_solution_cost

                if delta <= 0:
                    self.current_solution = self.new_solution
                    self.current_solution_cost = self.new_solution_cost

                    if self.new_solution_cost <= self.best_solution_cost:
                        self.best_solution = self.new_solution
                        self.best_solution_cost = self.new_solution_cost

                else:
                    sigma = random()

                    if sigma < math.exp(-delta / self.current_temperature):
                        self.current_solution = self.new_solution
                        self.current_solution_cost = self.new_solution_cost

                self.cost_chart.append(self.current_solution_cost)

                self.current_iteration += 1

            self.current_temperature = self.cooling_schedule(self.temperature_max, self.alpha, self.current_iteration)
            self.temperature_chart.append(self.current_temperature)

        return self.initial_solution, self.best_solution, self.initial_solution_cost, self.best_solution_cost, \
               self.current_iteration, self.temperature_chart, self.cost_chart
