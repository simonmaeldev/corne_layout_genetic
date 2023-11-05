import numpy as np
from pymoo.core.problem import ElementwiseProblem


class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=1, n_obj=3, n_ieq_constr=5)
    
    def _evaluate(self, x, out, *args, **kwargs):
        keyboard = x[0]
        res = keyboard.evaluate()
        g1 = res["left_max"] - res["left_min"]
        g2 = res["right_max"] - res["right_min"]
        g3 = res["sfb_left_max"] - res["sfb_left_min"]
        g4 = res["sfb_right_max"] - res["sfb_right_min"]
        g5 = abs(res["total_left"] - res["total_right"]) - 20
        out["F"] = np.array([res["total_weight"], res["total_sfb"], res["total_weighted_weakness"]], dtype=float)
        out["G"] = np.array([g1, g2, g3, g4, g5], dtype=float)
        
