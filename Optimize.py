from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import matplotlib.pyplot as plt
import json
import csv
from datetime import datetime

from genetic_algorithm.MySampling import MySampling
from genetic_algorithm.MyCrossover import MyCrossover
from genetic_algorithm.MyMutation import MyMutation
from genetic_algorithm.MyDuplicateElimination import MyDuplicateElimination
from genetic_algorithm.MyProblem import MyProblem
from genetic_algorithm.MyCallback import MyCallback
from models.ReferenceKeyboard import qwerty_keyboard, neu_keyboard, polyglot_keyboard
from utils.CsvUtils import visualize, all_cols, sort_cols


NB_GEN = 12
POP_SIZE = 300

print(f"[{datetime.now()}] nb gen: {NB_GEN}, nb individus: {POP_SIZE}")

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

plt.ioff()
print(f"[{datetime.now()}] FIN nb gen: {NB_GEN}, nb individus: {POP_SIZE}")
plt.show()


def print_to_txt(statsX):
    with open("keyboards.txt", "w", encoding="UTF-8") as file:
        for i, (kbd, statistics) in enumerate(statsX):
            file.write("\n" + str(i) + "\n")
            file.write(str(kbd) + "\n")
            file.write(json.dumps(statistics, indent=4) + "\n")

def write_to_csv(statsX):
    with open('mon_fichier.csv', 'w', newline='', encoding="UTF-8") as fichier_csv:
        writer = csv.writer(fichier_csv)
        keys = list(statsX[0][1].keys())
        writer.writerow(["numero"] + keys + ["string rep"])
        for i, (kbd, statistics) in enumerate(statsX):
            line = [i] + [statistics[k] for k in keys] + [";".join([kbd.get_char(j) for j in range(42)])]
            writer.writerow(line)

qwerty_keyboard.evaluate()
neu_keyboard.evaluate()
polyglot_keyboard.evaluate()

X, F = res.opt.get("X", "F")
statsX = [(kbd, kbd.get_stats()) for sublist in X for kbd in sublist]
stats_comp = [(qwerty_keyboard, qwerty_keyboard.get_stats()), (neu_keyboard, neu_keyboard.get_stats()), (polyglot_keyboard, polyglot_keyboard.get_stats())] + statsX

print_to_txt(stats_comp)
write_to_csv(stats_comp)


coord = [[statistics["total_weight"], statistics["total_sfb"], statistics["ratio_roll"]] for _, statistics in stats_comp]

visualize(coord)
sort_cols("mon_fichier.csv", "keyboard_clean.csv", all_cols)