import math
import time
from dataclasses import dataclass
from random import random

import numpy as np
import tqdm

from src.data_structures.solution import Solution
from src.algorithm.cooling_schedules.cooling_schedule import CoolingSchedule, exponential_cooling_schedule, \
    linear_cooling_schedule, logarithmic_cooling_schedule, quadratic_cooling_schedule, \
    boltzmann_cooling_schedule, cauchy_cooling_schedule


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

    cooling_schedule: CoolingSchedule = None

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
        if self.cooling_schedule is exponential_cooling_schedule:
            range_iterations = np.ceil(
                (math.log(self.temperature_min) - math.log(self.temperature_max)) /
                math.log(self.alpha)) * self.k_max

        if self.cooling_schedule is linear_cooling_schedule:
            range_iterations = np.ceil((self.temperature_max - self.temperature_min) / self.alpha) * self.k_max

        if self.cooling_schedule is logarithmic_cooling_schedule:
            range_iterations = np.ceil(math.pow(math.e, (self.temperature_max - self.temperature_min) /
                                                (self.alpha * self.temperature_min)) - 1) * self.k_max

        if self.cooling_schedule is quadratic_cooling_schedule:
            range_iterations = np.ceil(
                (math.sqrt(self.temperature_max - self.temperature_min)/(math.sqrt(self.alpha) *
                                                                         math.sqrt(self.temperature_min)))) * self.k_max

        if self.cooling_schedule is boltzmann_cooling_schedule:
            range_iterations = np.ceil(math.pow(math.e, self.temperature_max / self.temperature_min - 1)) * self.k_max

        if self.cooling_schedule is cauchy_cooling_schedule:
            range_iterations = np.ceil(self.temperature_max / self.temperature_min - 1) * self.k_max

        start_time = time.time()
        progress_bar = tqdm.tqdm(total=int(range_iterations))

        temperature_iteration = 1
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

            self.current_temperature = self.cooling_schedule(self.temperature_max, self.alpha, temperature_iteration)
            self.temperature_chart.append(self.current_temperature)
            temperature_iteration += 1

        end_time = time.time()
        runtime = end_time - start_time

        return self.initial_solution, self.best_solution, self.initial_solution_cost, self.best_solution_cost, \
               self.current_iteration, self.temperature_chart, self.cost_chart, self.best_cost_chart, runtime
