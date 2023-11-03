from pymoo.core.callback import Callback
import math
from pymoo.indicators.hv import HV
import numpy as np


#ind = HV(ref_point=np.array([150, 200, 200, 200]))
ind = HV(ref_point=np.array([150, 200, 200]))

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

def average(lst): 
    return sum(lst) / len(lst) 


class MyCallback(Callback):
    def __init__(self) -> None:
        super().__init__()
        #self.opt = []
        self.n_gen = []
        self.min_total = []
        self.avr_total = []
        self.min_sfb = []
        self.avr_sfb = []
        self.min_ratio = []
        self.avr_ratio = []
        #self.min_voisin = []
        #self.avr_voisin = []
        self.avr_hv = []
        self.max_hv = []

    def notify(self, algorithm):
        X, F = algorithm.pop.get("X", "F")
        total = []
        sfb = []
        ratio = []
        #voisin = []
        all_hv = []
        for stats in F:
            all_hv.append(ind(stats))
            total.append(stats[0])
            sfb.append(stats[1])
            ratio.append(stats[2])
            #voisin.append(stats[3])
        self.avr_total.append(average(total))
        self.avr_sfb.append(average(sfb))
        self.avr_ratio.append(average(ratio))
        #self.avr_voisin.append(average(voisin))
        self.min_total.append(min(total))
        self.min_sfb.append(min(sfb))
        self.min_ratio.append(min(ratio))
        #self.min_voisin.append(min(voisin))
        self.avr_hv.append(average(all_hv))
        self.max_hv.append(max(all_hv))
        self.n_gen.append(algorithm.n_gen)
        #keys = ("total_weight", "sfb","ratio_roll","voisin_ligne_diff")  # Les clés pour le tri
        #statsX = [kbd.get_stats() for sublist in X for kbd in sublist]
        #X, F = custom_sort(X, F, statsX, keys)


        #keys = ("total_weight", "sfb","ratio_roll","voisin_ligne_diff")  # Les clés pour le tri
        #sorted_list = sorted(algorithm.pop.get("X"), key=sort_key(keys))
        #self.opt.append(X[0][0])
