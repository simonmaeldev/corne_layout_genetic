from pymoo.visualization.scatter import Scatter
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
from pymoo.util.running_metric import RunningMetricAnimation
import math


from MySampling import MySampling
from MyCrossover import MyCrossover
from MyMutation import MyMutation
from MyDuplicateElimination import MyDuplicateElimination
from MyProblem import MyProblem
from MyCallback import MyCallback


algorithm = NSGA2(pop_size=10,
                  sampling=MySampling(),
                  crossover=MyCrossover(),
                  mutation=MyMutation(),
                  eliminate_duplicates=MyDuplicateElimination())


res = minimize(MyProblem(),
               algorithm,
               ('n_gen', 40),
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

def custom_sort(x, f, keys):
    # Combinez les deux listes et triez-les en utilisant f comme base pour le tri
    sorted_pairs = sorted(zip(x, f), key=lambda pair: sort_key(*keys)(pair[1]))

    # Séparez les paires triées en deux listes
    sorted_x, sorted_f = zip(*sorted_pairs)

    return list(sorted_x), list(sorted_f)



X, F = res.opt.get("X", "F")
keys = (0, 2, 6)  # Les clés pour le tri
X, F = custom_sort(X, F, keys)

print("Best solution found: \nX = \n%s\nF = %s" % (X[0][0], F[0]))

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


running = RunningMetricAnimation(delta_gen=10,
                        n_plots=1,
                        key_press=False,
                        do_show=True)

for algorithm in res.history:
    running.update(algorithm)

#results = res.X[np.argsort(res.F[:, 0])]
#count = [np.sum([e == "a" for e in r]) for r in results[:, 0]]
#print(np.column_stack([results, count]))

