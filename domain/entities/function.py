import numpy as np
import math


class RastriginFunction:
    def __init__(self, dimensions):
        self.dimensions = dimensions

    def evaluate(self, X):
        A = 10
        return A * self.dimensions + sum([(x**2 - A * np.cos(2 * math.pi * x)) for x in X])