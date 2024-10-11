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

def plot_barchart(stat_name, stat_values, keyboard_names, colors):
    plt.figure(figsize=(12, 6))
    bars = plt.bar(keyboard_names, stat_values, color=colors)
    plt.title(f'{stat_name} Comparison')
    plt.xlabel('Keyboards')
    plt.ylabel(stat_name)
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}',
                 ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

def printbarcharts(stats_comp, print=set()):
    keyboard_names = ['QWERTY', 'NEU', 'POLYGLOT'] + [f'Keyboard {i}' for i in range(3, len(stats_comp))]
    colors = ['red', 'green', 'orange'] + ['blue'] * (len(stats_comp) - 3)

    for stat_name in stats_comp[0][1].keys():
        if len(print) == 0 or stat_name in print:
            stat_values = [kbd.get_stats()[stat_name] for kbd, _ in stats_comp]
            plot_barchart(stat_name, stat_values, keyboard_names, colors)

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
print(f"{len(statsX)} individuals are on the pareto front and in the constraints")
stats_comp = [(qwerty_keyboard, qwerty_keyboard.get_stats()), (neu_keyboard, neu_keyboard.get_stats()), (polyglot_keyboard, polyglot_keyboard.get_stats())] + statsX

print_to_txt(stats_comp)
write_to_csv(stats_comp)


coord = [[statistics["total_weight"], statistics["total_sfb"], statistics["total_redirect"]] for _, statistics in stats_comp]

visualize(coord)
printbarcharts(stats_comp, print={"total_weight", "total_sfb", "total_alternate", "total_saut_doigt", "total_ligne_diff", "total_row_jump", "total_redirect"})
sort_cols("mon_fichier.csv", "keyboard_clean.csv", all_cols)
