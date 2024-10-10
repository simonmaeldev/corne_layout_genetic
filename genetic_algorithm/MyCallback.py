from pymoo.core.callback import Callback
from pymoo.indicators.hv import HV
import numpy as np
import matplotlib.pyplot as plt

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

        self.fig, self.axs = plt.subplots(4, sharex=True)
        plt.ion()

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
        
        self.axs[0].clear()
        self.axs[1].clear()
        self.axs[2].clear()
        self.axs[3].clear()
        self.fig.suptitle("Convergence")

        self.axs[0].plot(self.n_gen, self.avr_total, label='average')
        self.axs[0].plot(self.n_gen, self.min_total, label='min')
        self.axs[0].set(ylabel="total_weight")

        self.axs[1].plot(self.n_gen, self.avr_sfb, label='average')
        self.axs[1].plot(self.n_gen, self.min_sfb, label='min')
        self.axs[1].set(ylabel="sfb")

        self.axs[2].plot(self.n_gen, self.avr_weakness, label='average')
        self.axs[2].plot(self.n_gen, self.min_weakness, label='min')
        self.axs[2].set(ylabel="ratio roll")

        self.axs[3].plot(self.n_gen, self.avr_hv, label='average')
        self.axs[3].plot(self.n_gen, self.max_hv, label='max')
        self.axs[3].set(ylabel="hypervolume")

        plt.draw()
        # allow for user to move the window on the first generation
        stop_time = 10 if len(self.n_gen) == 1 else 0.01
        plt.pause(stop_time)

