from pymoo.core.crossover import Crossover
from Keyboard import Keyboard
import numpy as np


class MyCrossover(Crossover):
    def __init__(self):

        # define the crossover: number of parents and number of offsprings
        super().__init__(2, 2)

    def _do(self, problem, X, **kwargs):
        # The input of has the following shape (n_parents, n_matings, n_var)
        _, n_matings, n_var = X.shape

        # The output owith the shape (n_offsprings, n_matings, n_var)
        # Because there the number of parents and offsprings are equal it keeps the shape of X
        Y = np.full_like(X, None, dtype=object)

        # for each mating provided
        for k in range(n_matings):

            # get the first and the second parent
            a, b = X[0, k, 0], X[1, k, 0]

            # join the character list and set the output
            Y[0, k, 0], Y[1, k, 0] = a.mate_with(b)

        return Y