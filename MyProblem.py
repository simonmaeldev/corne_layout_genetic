import numpy as np
from pymoo.core.problem import ElementwiseProblem

class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=1, n_obj=3, n_ieq_constr=0)
    
    def _evaluate(self, x, out, *args, **kwargs):
        # TODO
        pass