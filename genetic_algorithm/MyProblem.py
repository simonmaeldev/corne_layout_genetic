import numpy as np
from pymoo.core.problem import ElementwiseProblem


class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=1, n_obj=3, n_ieq_constr=1)
    
    def _evaluate(self, x, out, *args, **kwargs):
        keyboard = x[0]
        res = keyboard.evaluate()
        constraints = []
        # constraints.append(res["left_max"] - res["left_min"])
        # constraints.append(res["right_max"] - res["right_min"])
        # constraints.append(res["sfb_left_max"] - res["sfb_left_min"])
        # constraints.append(res["sfb_right_max"] - res["sfb_right_min"])
        # constraints.append(abs(res["total_left"] - res["total_right"]) - 15)
        # constraints.append(res["total_weight"] - 85)
        # constraints.append(res["total_weighted_weakness"] - 11.55)
        constraints.append(res["total_sfb"] - 6.6) # 6.6 is the sfb of qwerty
        # constraints.append(res["jump_auri"] - 1)
        # constraints.append(res["diff_annu"] - 2.5)
        # constraints.append(res["sfb_auri"] - 0.1)
        # constraints.append(res["sfb_annu"] - 0.5)
        # constraints.append(res["sfb_maj"] - 0.1)
        # constraints.append(res["sfb_ind"] - 1.5)
        # F is the objective function value
        out["F"] = np.array([res["total_weight"], res["total_sfb"], res["ratio_roll"]], dtype=float)
        # G is the constraint values
        out["G"] = np.array(constraints, dtype=float)
        
