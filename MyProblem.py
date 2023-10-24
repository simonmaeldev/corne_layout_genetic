import numpy as np
from pymoo.core.problem import ElementwiseProblem

weights = {
    'fr' : 0.4,
    'en' : 0.3,
    'java' : 0.1,
    'python' : 0.1,
    'md' : 0.1
}

class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=1, n_obj=8, n_ieq_constr=0)
    
    def _evaluate(self, x, out, *args, **kwargs):
        keyboard = x[0]
        res = keyboard.evaluate()
        res_lst = [0, 0, 0, 0, 0, 0, 0, 0]
        for language, values in res.items():
            for i, val in enumerate(values):
                res_lst[i] += weights[language] * val
        out["F"] = np.array(res_lst, dtype=float)
        
