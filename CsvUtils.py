import csv
from pymoo.visualization.scatter import Scatter
import numpy as np
from Keyboard import Main, Doigts



def load_csv_res(file_path):
    # Ouvrir le fichier CSV
    with open(file_path, newline='', encoding="UTF-8") as csvfile:
        csvreader = csv.reader(csvfile)

        # Lire les en-têtes de colonnes
        headers = next(csvreader)

        # Créer une liste de listes pour stocker toutes les données
        #data = []

        # Créer une deuxième liste pour stocker uniquement les colonnes requises
        selected_columns = []

        for row in csvreader:
            # Ajouter la ligne complète à la liste data
            #data.append(row)

            # Extraire les colonnes requises et les ajouter à selected_columns
            selected_row = [float(row[headers.index("total_weight")]), float(row[headers.index("total_sfb")]), float(row[headers.index("total_weighted_weakness")])]
            selected_columns.append(selected_row)
        
        return selected_columns

def visualize(coord):
    plot = Scatter(legend=True)
    plot.add(np.array(coord[2:]))
    plot.add(np.array([coord[0]]), color="red")
    plot.add(np.array([coord[1]]), color="green")
    plot.show().save("representation.png")

def sort_cols(in_path, out_path, cols):
    # Ouvrir le fichier CSV en entrée et créer un fichier de sortie
    with open(in_path, newline='', encoding="UTF-8") as csvfile_in, open(out_path, "w", newline='', encoding="UTF-8") as csvfile_out:
        csvreader = csv.DictReader(csvfile_in)
        
        # Crée un dictionnaire de correspondance entre les noms de colonnes d'origine et les nouveaux noms
        correspondance = {col: col for col in csvreader.fieldnames}

        # Crée un dictionnaire inversé pour rechercher les nouvelles colonnes en fonction de l'ancien nom
        correspondance_inverse = {v: k for k, v in correspondance.items()}

        # Affiche les noms de colonnes qui ne sont pas dans nouvel_ordre_des_colonnes
        for col in correspondance_inverse:
            if col not in cols:
                print(f"La colonne '{col}' n'est pas dans cols.")

        # Réorganise les colonnes en fonction de l'ordre souhaité
        for i, col in enumerate(cols):
            if col in correspondance_inverse:
                correspondance[col] = correspondance_inverse[col]
                correspondance_inverse[correspondance[col]] = col

        # Réécrit le fichier de sortie avec les nouvelles colonnes dans l'ordre spécifié
        writer = csv.DictWriter(csvfile_out, fieldnames=cols)
        writer.writeheader()

        for row in csvreader:
            new_row = {col: row[correspondance[col]] for col in cols}
            writer.writerow(new_row)


#coord = load_csv_res("mon_fichier.csv")
#visualize(coord)

start = ["numero", "total_weight", "total_sfb", "ratio_roll", "total_weighted_weakness", "total_left", "total_right", "total_alternate", "total_saut_doigt", "total_ligne_diff", "total_row_jump", "total_roll_in", "total_roll_out", "total_redirect"]
end = ["left_min", "left_max", "right_min", "right_max", "sfb_left_max", "sfb_left_min", "sfb_right_max", "sfb_right_min", "jump_auri", "diff_annu", "sfb_auri", "sfb_annu", "sfb_maj", "sfb_ind", "missing", "weakness", "string rep"]

lst_doigts = ['G_AURICULAIRE', 'G_ANNULAIRE', 'G_MAJEUR', 'G_INDEX', 'D_INDEX', 'D_MAJEUR', 'D_ANNULAIRE', 'D_AURICULAIRE']
prefix = ["", "sfb_", "roll_in_", "roll_out_", "row_jump_", "repet_", "ligne_diff_"]

mid = []

for p in prefix:
    for d in lst_doigts:
        mid.append(p + d)

all_cols = start + mid + end

#sort_cols("mon_fichier.csv", "keyboard_clean.csv", start + mid + end)