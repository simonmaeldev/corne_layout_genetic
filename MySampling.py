import numpy as np
from pymoo.core.sampling import Sampling
from Keyboard import Keyboard
import copy

class MySampling(Sampling):
    def _do(self, problem, n_samples, **kwargs):
        X = np.full((n_samples, 1), None, dtype=object)

        for i in range(n_samples):
            X[i, 0] = Keyboard()
            print(X[i, 0])

        print("==========")
        for i in range(n_samples):
            print(X[i, 0])

        print(X)
        return X
