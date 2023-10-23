import numpy as np
from pymoo.core.mutation import Mutation
import random


class MyMutation(Mutation):
    def __init__(self):
        super().__init__()

    def _do(self, problem, X, **kwargs):

        # for each individual
        for i in range(len(X)):

            r = np.random.random()

            # with a probabilty of 5% - intervert 2 keys
            if r < 0.05:
                keyboard = X[i, 0]
                key1, key2 = random.sample(range(36), 2)
                char1 = keyboard.get_char(key1)
                char2 = keyboard.get_char(key2)
                keyboard.set_key_char(key2, char1)
                keyboard.set_key_char(key1, char2)

        return X

