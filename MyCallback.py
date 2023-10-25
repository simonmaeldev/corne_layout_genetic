from pymoo.core.callback import Callback
import math


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

class MyCallback(Callback):
    def __init__(self) -> None:
        super().__init__()
        self.data["best"] = []

    def notify(self, algorithm):
        sorted_list = sorted(algorithm.pop.get("F"), key=sort_key(0, 1))
        self.data["best"].append(sorted_list[0])
