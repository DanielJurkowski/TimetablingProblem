import math
import time
from dataclasses import dataclass
from random import random
from typing import Callable

import numpy as np
import tqdm

from src.data_structures.solution import Solution

CoolingSchedule = Callable[[float, float, int], float]


def exponential_cooling_schedule(temperature: float, alpha: float, k: int) -> float:
    return temperature * (alpha ** k)


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

    swap: bool = True

    cooling_schedule: CoolingSchedule = exponential_cooling_schedule

    temperature_chart = []
    cost_chart = []
    best_cost_chart = []

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
        range_iterations = np.ceil(
            (math.log(self.temperature_min, 10) - math.log(self.temperature_max, 10)) /
            math.log(self.alpha ** self.k_max, 10) * self.k_max)
        start_time = time.time()
        progress_bar = tqdm.tqdm(total=int(range_iterations))

        while self.current_temperature > self.temperature_min and self.current_iteration < self.max_iterations:
            for _ in range(self.k_max):
                self.new_solution = self.current_solution.neighborhood_creation(swap=self.swap)
                self.new_solution.compute_cost()
                self.new_solution_cost = self.new_solution.cost

                delta = self.new_solution_cost - self.current_solution_cost

                # dodać heurestyke, jeżeli przez n iteracji (pare tysięcy) wartość się nie poprawiła o daną stała
                # to wykonujemy metody poprawy danego rozwiazania

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

                self.current_iteration += 1

                self.best_cost_chart.append(self.best_solution_cost)
                self.cost_chart.append(self.current_solution_cost)
                progress_bar.update(1)

            self.current_temperature = self.cooling_schedule(self.temperature_max, self.alpha, self.current_iteration)
            self.temperature_chart.append(self.current_temperature)

        end_time = time.time()
        runtime = end_time - start_time

        return self.initial_solution, self.best_solution, self.initial_solution_cost, self.best_solution_cost, \
               self.current_iteration, self.temperature_chart, self.cost_chart, self.best_cost_chart, runtime
