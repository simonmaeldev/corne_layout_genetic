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

#Scatter().add(res.F).show()



def custom_round(n):
    # Trouver l'unité juste au-dessus
    unit = 10 ** (math.ceil(math.log10(n)) - 1)
    upper_unit = n + unit - (n % unit)

    # Calculer la tranche de 5%
    step = 0.05 * upper_unit

    # Soustraire des tranches de 5% jusqu'à obtenir une valeur inférieure à n
    rounded = upper_unit
    while rounded > n:
        rounded -= step

    return rounded

def sort_key(*keys):
    def key_func(item):
        return [custom_round(item[key]) for key in keys] + [item[key] for key in keys]
    return key_func

def custom_sort(x, f, scores, keys):
    # Combinez les deux listes et triez-les en utilisant f comme base pour le tri
    sorted_pairs = sorted(zip(x, f, scores), key=lambda pair: sort_key(*keys)(pair[2]))

    # Séparez les paires triées en deux listes
    sorted_x, sorted_f, _ = zip(*sorted_pairs)

    return list(sorted_x), list(sorted_f)

def determine_ideal_nadir_points(X):
    # Initialize ideal and nadir points with extreme values
    flat_list = [item for sublist in X for item in sublist]
    ideal_point = {}
    nadir_point = {}
    for keyboard in flat_list:
        stats = keyboard.get_stats()
        for key, value in stats.items():
            if key not in ideal_point:
                ideal_point[key] = float('inf')
            if key not in nadir_point:
                nadir_point[key] = float('-inf')
            if value < ideal_point[key]:
                ideal_point[key] = value
            if value > nadir_point[key]:
                nadir_point[key] = value

    return ideal_point, nadir_point

def tonp(dict):
    return np.array(list(dict.values()))

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


#running = RunningMetricAnimation(delta_gen=NB_GEN,
#                        n_plots=1,
#                        key_press=False,
#                        do_show=True)
#
#for algorithm in res.history:
#    running.update(algorithm)

fig, axs = plt.subplots(4, sharex=True)
fig.suptitle("Convergence")

axs[0].plot(callback.n_gen, callback.avr_total, label='average')
axs[0].plot(callback.n_gen, callback.min_total, label='min')
axs[0].set(ylabel="total_weight")

axs[1].plot(callback.n_gen, callback.avr_sfb, label='average')
axs[1].plot(callback.n_gen, callback.min_sfb, label='min')
axs[1].set(ylabel="sfb")

axs[2].plot(callback.n_gen, callback.avr_ratio, label='average')
axs[2].plot(callback.n_gen, callback.min_ratio, label='min')
axs[2].set(ylabel="ratio_roll")

#axs[3].plot(callback.n_gen, callback.avr_voisin, label='average')
#axs[3].plot(callback.n_gen, callback.min_voisin, label='min')
#axs[3].set(ylabel="voisin_ligne_diff")

axs[3].plot(callback.n_gen, callback.avr_hv, label='average')
axs[3].plot(callback.n_gen, callback.max_hv, label='max')
axs[3].set(ylabel="hypervolume")

plt.show()

X, F = res.opt.get("X", "F")

ideal_point, nadir_point = determine_ideal_nadir_points(X)

qwerty_keyboard.evaluate()
keys = ("total_weight", "sfb","ratio_roll","voisin_ligne_diff")  # Les clés pour le tri
statsX = [(kbd, kbd.get_stats()) for sublist in X for kbd in sublist]

stats_comp = [(qwerty_keyboard, qwerty_keyboard.get_stats())] + statsX

print_to_txt(stats_comp)
write_to_csv(stats_comp)


coord = [[statistics["total_weight"], statistics["sfb"], statistics["roll_out"]] for _, statistics in stats_comp]

Scatter(legend=True).add(np.array(coord)).show().save("representation.png")

#X, F = custom_sort(X, F, statsX, keys)
#X = X[:9]








#X = np.insert(X, 0, qwerty_keyboard, axis=0)
#qwerty_keyboard.evaluate()
#keys = ("total_weight", "sfb","ratio_roll","voisin_ligne_diff")  # Les clés pour le tri
#statsX = [kbd.get_stats() for sublist in X for kbd in sublist]
#X, F = custom_sort(X, F, statsX, keys)
#X = X[:9]
#print_to_txt(qwerty_keyboard, X, statsX)

#keyboards = np.array([tonp(kbd.get_stats()) for sublist in X for kbd in sublist])
#labels = list(X[0][0].get_stats().keys())
#plot = Radar(bounds=[tonp(ideal_point), tonp(nadir_point)], labels=labels)
#start = 0
#end = 3
#while end <= keyboards.shape[0]:
#    plot.add(keyboards[start:end])
#    start = end
#    end += 3
#plot.add(keyboards[start:keyboards.shape[0]])
#plot.show()
#plot.save("keyboards.png")


# Créer un dictionnaire pour les titres
titles = {
    0: 'Total poids fréquence + matrice poids',
    1: 'Total poids index',
    2: 'Poids sfb',
    3: 'Poids row jumps',
    4: 'Poids répetition autre que majeur',
    5: 'Poids annulaire ligne différente que voisins',
    6: 'Ratio roll out / roll in',
    7: 'Ratio doigt voisin ligne diff / saut de doigt'
}

#fig, axs = plt.subplots(8, sharex=True, figsize=(10, 10))
#for i in range(8):
#    val = res.algorithm.callback.data["best"][i]
#    axs[i].plot(np.arange(len(val)), val)
#    axs[i].set_title(titles[i])  # Ajouter le titre au graphique
#plt.show()



#results = res.X[np.argsort(res.F[:, 0])]
#count = [np.sum([e == "a" for e in r]) for r in results[:, 0]]
#print(np.column_stack([results, count]))

