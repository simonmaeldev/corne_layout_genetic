from pymoo.visualization.scatter import Scatter
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
from pymoo.util.running_metric import RunningMetricAnimation
import math
from pyrecorder.recorder import Recorder
from pyrecorder.writers.video import Video
from pymoo.visualization.radar import Radar
import json
import csv

from MySampling import MySampling
from MyCrossover import MyCrossover
from MyMutation import MyMutation
from MyDuplicateElimination import MyDuplicateElimination
from MyProblem import MyProblem
from MyCallback import MyCallback
from ReferenceKeyboard import qwerty_keyboard


NB_GEN = 80
POP_SIZE = 300


algorithm = NSGA2(pop_size=POP_SIZE,
                  sampling=MySampling(),
                  crossover=MyCrossover(),
                  mutation=MyMutation(),
                  eliminate_duplicates=MyDuplicateElimination())

callback = MyCallback()

res = minimize(MyProblem(),
               algorithm,
               ('n_gen', NB_GEN),
               callback = callback,
               seed=1,
               save_history=False,
               verbose=True)


def print_to_txt(statsX):
    with open("keyboards.txt", "w") as file:
        for i, (kbd, statistics) in enumerate(statsX):
            file.write("\n" + str(i) + "\n")
            file.write(str(kbd) + "\n")
            file.write(json.dumps(statistics, indent=4) + "\n")

def write_to_csv(statsX):
    with open('mon_fichier.csv', 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        keys = list(statsX[0][1].keys())
        writer.writerow(["numero"] + keys)
        for i, (kbd, statistics) in enumerate(statsX):
            line = [i] + [statistics[k] for k in keys] + [";".join([kbd.get_char(j) for j in range(42)])]
            writer.writerow(line)

fig, axs = plt.subplots(4, sharex=True)
fig.suptitle("Convergence")

axs[0].plot(callback.n_gen, callback.avr_total, label='average')
axs[0].plot(callback.n_gen, callback.min_total, label='min')
axs[0].set(ylabel="total_weight")

axs[1].plot(callback.n_gen, callback.avr_sfb, label='average')
axs[1].plot(callback.n_gen, callback.min_sfb, label='min')
axs[1].set(ylabel="sfb")

axs[2].plot(callback.n_gen, callback.avr_weakness, label='average')
axs[2].plot(callback.n_gen, callback.min_weakness, label='min')
axs[2].set(ylabel="weakness")

axs[3].plot(callback.n_gen, callback.avr_hv, label='average')
axs[3].plot(callback.n_gen, callback.max_hv, label='max')
axs[3].set(ylabel="hypervolume")

plt.show()

X, F = res.opt.get("X", "F")

qwerty_keyboard.evaluate()
statsX = [(kbd, kbd.get_stats()) for sublist in X for kbd in sublist]

stats_comp = [(qwerty_keyboard, qwerty_keyboard.get_stats())] + statsX

print_to_txt(stats_comp)
write_to_csv(stats_comp)


coord = [[statistics["total_weight"], statistics["sfb"], statistics["roll_out"]] for _, statistics in stats_comp]

Scatter(legend=True).add(np.array(coord)).show().save("representation.png")