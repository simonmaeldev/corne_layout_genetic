import os
import pandas as pd
import numpy as np
import unicodedata
from Data import accent_ignore
import csv



# Dossiers à analyser
folders = ["fr", "en", "java", "python", "md"]

# dictionnaire du ngram vers le nom du fichier
files = {
    1: "monogram_statistics.csv",
    2: "digram_statistics.csv",
    3: "trigram_statistics.csv",
}

def has_accent_replace(letter):
    if  len(letter) == 1 and letter.upper() not in accent_ignore:
        name = unicodedata.name(letter)
        return 'WITH CIRCUMFLEX' in name or 'WITH DIAERESIS' in name
    return False

def separate_accent(letter):
    decomposed = unicodedata.normalize('NFD', letter)
    if len(decomposed) > 1:
        return decomposed[0].upper(), decomposed[1].upper()
    else:
        return letter, None



def load_stats(folders, files, threshold = 0.01, limit = 1000):
    # Dictionnaire pour stocker les statistiques
    stats = {}
    # Parcourir chaque dossier
    for folder in folders:
        stats[folder] = {}
        
        # Parcourir chaque type de fichier dans le dossier
        # ordre important des ngrams, car on ajoute possiblement une partie des 1 aux 2
        for ngram in [3, 2, 1]:
            # Charger le fichier CSV
            df = pd.read_csv(f"stats/{folder}/{files[ngram]}")

            # supprime les lignes qui contiennent nan
            df = df.dropna()
            
            # Prendre les n premières colonnes et la dernière colonne
            df = df.iloc[:, list(range(ngram)) + [-1]]
            
            # Filtrer les lignes en fonction du seuil
            df = df[df.iloc[:, -1] > threshold]
            
            # Limiter à limit lignes
            df = df.head(limit)

            # remplace espace insécable
            df.replace({r'\u00A0': ' ', r'\u2019': "'", r'\u00AB': '"', r'\u00BB': '"', r'\u2013': "-"}, regex=True, inplace=True)

            # Stocker les statistiques dans le dictionnaire
            if ngram == 1 :
                dict_original = {row[0]: row[-1] for row in df.values}
                dict = {}
                stats[folder][ngram] = dict
                for char, value in dict_original.items():
                    char = char.upper()
                    if has_accent_replace(char):
                        letter_accent = separate_accent(char)
                        for char in letter_accent:
                            if char not in dict:
                                dict[char] = 0
                            dict[char] += value
                        stats[folder][2][letter_accent] = value
                        del dict[char]
                    else :
                        dict[char] = value
            else :
                dict_original = {tuple(row[:-1]): row[-1] for row in df.values}
                dict = {}
                stats[folder][ngram] = dict
                for seq, value in dict_original.items():
                    lst = []
                    for c in seq:
                        c = c.upper()
                        if has_accent_replace(c):
                            lst += separate_accent(c)
                        else:
                            lst += c
                    dict[tuple(lst)] = value
    return stats

#stats = load_stats(folders, files)

replace_dict = {'\n': 'RET', ' ': 'SPACE', '\t': 'TAB', "'" : "SQT", '"': 'DQT'}

def replace_key(key):
    if type(key) is tuple:
        key = tuple(replace_dict.get(key_item, key_item) for key_item in key)
    else:
        key = tuple([replace_dict.get(key, key)])
    return key

def writecsv(path_clean, path_no_space, clean_stats):
    with open(path_no_space, 'w', newline='', encoding='utf-8') as csvfile_no_space:
        writer_no_space = csv.writer(csvfile_no_space)
        with open(path_clean, 'w', newline='', encoding='utf-8') as csvfile_clean:
            writer_clean = csv.writer(csvfile_clean)
            #writer_clean.writeheader()  # Écrit la première ligne des en-têtes
            for ngram_tuple, probability in clean_stats.items():
                # Appliquer les remplacements
                ngram_tuple = replace_key(ngram_tuple)
                writer_clean.writerow([*ngram_tuple, probability])
                if not any (el in ngram_tuple for el in ['SPACE', 'RET', 'TAB']):
                    writer_no_space.writerow([*ngram_tuple, probability])

def clean_stats(folders, files):
    full_stats = load_stats(folders, files)
    for folder, dict_files in full_stats.items():
        for ngram, clean_stats in dict_files.items():
            writecsv(f"stats/{folder}/clean_{files[ngram]}", f"stats/{folder}/no_white_{files[ngram]}", clean_stats)

clean_stats(folders, files)

def load_no_white_stats():
    # Dictionnaire pour stocker les statistiques
    stats = {}
    # Parcourir chaque dossier
    for folder in folders:
        stats[folder] = {}
        # Parcourir chaque type de fichier dans le dossier
        for ngram in [3, 2, 1]:
            dict = {}
            stats[folder][ngram] = dict
            # Charger le fichier CSV
            with open(f"stats/{folder}/no_white_{files[ngram]}", newline='', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile)
                for row in spamreader:
                    if ngram == 1:
                        dict[row[0]] = float(row[-1])
                    else:
                        dict[tuple(row[:-1])] = float(row[-1])
    return stats

#stats = load_no_space_stats()
#print(stats)