from pymoo.core.callback import Callback
from pymoo.indicators.hv import HV
import numpy as np

ind = HV(ref_point=np.array([150, 200, 200]))

def average(lst): 
    return sum(lst) / len(lst) 


class MyCallback(Callback):
    def __init__(self) -> None:
        super().__init__()
        self.n_gen = []
        self.min_total = []
        self.avr_total = []
        self.min_sfb = []
        self.avr_sfb = []
        self.min_weakness = []
        self.avr_weakness = []
        self.avr_hv = []
        self.max_hv = []

    def notify(self, algorithm):
        X, F = algorithm.pop.get("X", "F")
        total = []
        sfb = []
        weakness = []
        all_hv = []
        for stats in F:
            all_hv.append(ind(stats))
            total.append(stats[0])
            sfb.append(stats[1])
            weakness.append(stats[2])
        self.avr_total.append(average(total))
        self.min_total.append(min(total))
        self.avr_sfb.append(average(sfb))
        self.min_sfb.append(min(sfb))
        self.avr_weakness.append(average(weakness))
        self.min_weakness.append(min(weakness))
        self.avr_hv.append(average(all_hv))
        self.max_hv.append(max(all_hv))
        self.n_gen.append(algorithm.n_gen)

