import os
import pandas as pd


# Dossiers à analyser
folders = ["fr", "en", "java", "python", "md"]

# dictionnaire du ngram vers le nom du fichier
files = {
    1: "monogram_statistics.csv",
    2: "digram_statistics.csv",
    3: "trigram_statistics.csv",
}

def load_stats(folders, files, threshold = 0.01, limit = 1000):
    # Dictionnaire pour stocker les statistiques
    stats = {}
    # Parcourir chaque dossier
    for folder in folders:
        stats[folder] = {}
        
        # Parcourir chaque type de fichier dans le dossier
        for ngram in [1, 2, 3]:
            # Charger le fichier CSV
            df = pd.read_csv(f"stats/{folder}/{files[ngram]}")
            
            # Prendre les n premières colonnes et la dernière colonne
            df = df.iloc[:, list(range(ngram)) + [-1]]
            
            # Filtrer les lignes en fonction du seuil
            df = df[df.iloc[:, -1] > threshold]
            
            # Limiter à limit lignes
            df = df.head(limit)

            # Replace \n by RET, \s by SPACE and \t by TAB
            df.replace({r'\n': 'RET', r'\s': 'SPACE', r'\t': 'TAB'}, regex=True, inplace=True)

            # Stocker les statistiques dans le dictionnaire
            if ngram == 1 :
                stats[folder][ngram] = {row[0]: row[-1] for row in df.values}
            else :
                stats[folder][ngram] = {tuple(row[:-1]): row[-1] for row in df.values}
    return stats

stats = load_stats(folders, files)