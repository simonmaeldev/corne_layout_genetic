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



from MySampling import MySampling
from MyCrossover import MyCrossover
from MyMutation import MyMutation
from MyDuplicateElimination import MyDuplicateElimination
from MyProblem import MyProblem
from MyCallback import MyCallback
from ReferenceKeyboard import qwerty_keyboard


algorithm = NSGA2(pop_size=100,
                  sampling=MySampling(),
                  crossover=MyCrossover(),
                  mutation=MyMutation(),
                  eliminate_duplicates=MyDuplicateElimination())


res = minimize(MyProblem(),
               algorithm,
               ('n_gen', 1000),
               callback = MyCallback(),
               seed=1,
               save_history=True,
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
    print(flat_list)
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


running = RunningMetricAnimation(delta_gen=250,
                        n_plots=1,
                        key_press=False,
                        do_show=True)

for algorithm in res.history:
    running.update(algorithm)



X, F = res.opt.get("X", "F")

ideal_point, nadir_point = determine_ideal_nadir_points(X)

qwerty_keyboard.evaluate()
keys = ("total_weight", "sfb","ratio_roll","ratio_voisin_saut")  # Les clés pour le tri
statsX = [kbd.get_stats() for sublist in X for kbd in sublist]
X, F = custom_sort(X, F, statsX, keys)
#X = np.insert(X, 0, qwerty_keyboard, axis=0)

with open("keyboards.txt", "w") as file:
    file.write("qwerty: \nX = \n%s\nstats = %s\n" % (qwerty_keyboard, json.dumps(qwerty_keyboard.get_stats(), indent=4)))
    file.write("Best solution found: \nX = \n%s\nstats = %s\n" % (X[0][0], json.dumps(statsX[0], indent=4)))
    file.write("\n========================================\n")
    X = X[:9]
    for i,sublist in enumerate(X):
        file.write("\n" + str(i) + "\n")
        file.write(str(sublist[0]) + "\n")
        file.write(json.dumps(sublist[0].get_stats(), indent=4) + "\n")
keyboards = np.array([tonp(kbd.get_stats()) for sublist in X for kbd in sublist])
labels = list(X[0][0].get_stats().keys())
plot = Radar(bounds=[tonp(ideal_point), tonp(nadir_point)], labels=labels)
start = 0
end = 3
while end < keyboards.shape[0]:
    plot.add(keyboards[start:end])
    start = end
    end += 3
plot.add(keyboards[start:keyboards.shape[0]])
plot.show()
plot.save("keyboards.png")


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

