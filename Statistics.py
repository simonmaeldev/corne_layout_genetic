import os
import csv
from collections import Counter
from multiprocessing import Pool

def calculate_statistics(text):
    total_chars = len(text)
    char_counts = Counter(text)
    digram_counts = count_ngrams(text, 2)
    trigram_counts = count_ngrams(text, 3)
    return total_chars, char_counts, digram_counts, trigram_counts

def count_ngrams(text, n):
    ngrams = [text[i:i + n] for i in range(len(text) - n + 1)]
    return Counter(ngrams)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().lower()  # Convert text to lowercase for case insensitivity

    # Appeler la fonction pour calculer les statistiques pour ce fichier
    return calculate_statistics(text)

def main(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_list = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)

    with Pool(processes=12) as pool:  # Vous pouvez ajuster le nombre de processus
        results = pool.map(process_file, file_list)

    # Rassembler les statistiques pour les monogrammes, digrammes et trigrammes
    total = 0
    monogram_stats = Counter()
    digram_stats = Counter()
    trigram_stats = Counter()

    for result in results:
        # Mettre en commun les statistiques pour chaque fichier
        # Utiliser les résultats pour mettre à jour les compteurs monogram, digram et trigram
        count, mono, digram, trigram = result
        total += count
        monogram_stats.update(mono)
        digram_stats.update(digram)
        trigram_stats.update(trigram)

    # Écrire les statistiques dans des fichiers CSV dédiés
    monogram_output_path = os.path.join(output_folder, "monogram_statistics.csv")
    with open(monogram_output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item, frequency in monogram_stats.items():
            writer.writerow([item, frequency])

    digram_output_path = os.path.join(output_folder, "digram_statistics.csv")
    with open(digram_output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item, frequency in digram_stats.items():
            writer.writerow([item, frequency])

    trigram_output_path = os.path.join(output_folder, "trigram_statistics.csv")
    with open(trigram_output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item, frequency in trigram_stats.items():
            writer.writerow([item, frequency])

if __name__ == "__main__":
    input_folder = "/chemin/vers/votre/dossier/d_entree"
    output_folder = "/chemin/vers/votre/dossier/de_sortie"
    main(input_folder, output_folder)
