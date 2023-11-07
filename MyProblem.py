import numpy as np
from pymoo.core.problem import ElementwiseProblem


class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=1, n_obj=3, n_ieq_constr=8)
    
    def _evaluate(self, x, out, *args, **kwargs):
        keyboard = x[0]
        res = keyboard.evaluate()
        # g1 = res["left_max"] - res["left_min"]
        # g2 = res["right_max"] - res["right_min"]
        # g3 = res["sfb_left_max"] - res["sfb_left_min"]
        # g4 = res["sfb_right_max"] - res["sfb_right_min"]
        g5 = abs(res["total_left"] - res["total_right"]) - 15
        g6 = res["total_weight"] - 85
        #g7 = res["total_weighted_weakness"] - 11.55
        #g8 = res["total_sfb"] - 7
        g9 = res["jump_auri"] - 1
        g10 = res["diff_annu"] - 2.5
        g11 = res["sfb_auri"] - 0.1
        g12 = res["sfb_annu"] - 0.5
        g13 = res["sfb_maj"] - 0.1
        g14 = res["sfb_ind"] - 1.5
        out["F"] = np.array([res["total_weight"], res["total_sfb"], res["ratio_roll"]], dtype=float)
        out["G"] = np.array([g5, g6, g9, g10, g11, g12, g13, g14], dtype=float)
        
