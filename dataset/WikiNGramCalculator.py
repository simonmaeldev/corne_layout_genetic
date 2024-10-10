"""
WikiNGramCalculator.py

This script is designed to process text data extracted from Wikipedia using WikiExtractor
and calculate n-gram statistics. It is the first step in creating a dataset for further
analysis or machine learning tasks.

Key concepts:
1. Monograms (or unigrams): Single characters in the text.
2. Digrams: Sequences of two consecutive characters in the text.
3. Trigrams: Sequences of three consecutive characters in the text.

The script does the following:
1. Reads text files from a specified input folder (containing WikiExtractor output).
2. Processes each file to calculate monogram, digram, and trigram frequencies.
3. Aggregates statistics across all processed files.
4. Outputs the results as CSV files in a specified output folder.

The n-gram calculations are case-insensitive (all text is converted to lowercase).
The script uses multiprocessing to improve performance when processing multiple files.

Output:
- monogram_statistics.csv: Contains single character frequencies.
- digram_statistics.csv: Contains two-character sequence frequencies.
- trigram_statistics.csv: Contains three-character sequence frequencies.

Each output file includes the n-gram, its frequency count, and its percentage of total n-grams.
"""

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
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
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

    results = []
    with Pool(processes=8) as pool:  # Vous pouvez ajuster le nombre de processus
        for i, result in enumerate(pool.imap(process_file, file_list), 1):
            print(f"{i}/{len(file_list)} done.")
            results.append(result)

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
        writer = csv.writer(csvfile, escapechar='\\')
        for item, frequency in monogram_stats.items():
            writer.writerow([item, frequency, frequency * 100 / total])

    digram_output_path = os.path.join(output_folder, "digram_statistics.csv")
    with open(digram_output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, escapechar='\\')
        for item, frequency in digram_stats.items():
            writer.writerow([item[0], item[1], frequency, frequency * 100 / total])

    trigram_output_path = os.path.join(output_folder, "trigram_statistics.csv")
    with open(trigram_output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, escapechar='\\')
        for item, frequency in trigram_stats.items():
            writer.writerow([item[0], item[1], item[2], frequency, frequency * 100 / total])

if __name__ == "__main__":
    input_folder = "/home/move/Documents/perso/WikiExtractor/files-en"
    output_folder = "/home/move/Documents/perso/stats/en"
    #input_folder = "/home/move/Documents/perso/raw_data_perso/md"
    #output_folder = "/home/move/Documents/perso/stats/md"

    main(input_folder, output_folder)
