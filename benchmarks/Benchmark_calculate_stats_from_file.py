"""
This script benchmarks two methods of calculating text statistics: an old method and a new method.

The script does the following:
1. Defines two functions for calculating text statistics:
   - calculate_statistics_old: Uses list comprehensions and Counter objects
   - calculate_statistics_new: Uses a single pass through the text with manual counting
2. Generates texts of various sizes (from 10^4 to 10^8 characters)
3. Measures the execution time of both methods for each text size
4. Plots the results on a log-log scale graph

The benchmark compares the performance of these methods in terms of:
- Counting total characters
- Counting individual characters
- Counting digrams (2-character sequences)
- Counting trigrams (3-character sequences)

The results are visualized using matplotlib, showing how execution time scales with text size for both methods.
"""

import timeit
import random
import string
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

def calculate_statistics_old(text):
    total_chars = len(text)
    char_counts = Counter(text)
    digram_counts = count_ngrams(text, 2)
    trigram_counts = count_ngrams(text, 3)
    return total_chars, char_counts, digram_counts, trigram_counts

def count_ngrams(text, n):
    ngrams = [text[i:i + n] for i in range(len(text) - n + 1)]
    return Counter(ngrams)

def calculate_statistics_new(text):
    total_chars = len(text)
    char_counts = Counter()
    digram_counts = Counter()
    trigram_counts = Counter()

    for i in range(total_chars):
        char_counts[text[i]] += 1
        if i < total_chars - 1:
            digram_counts[text[i:i+2]] += 1
        if i < total_chars - 2:
            trigram_counts[text[i:i+3]] += 1

    return total_chars, char_counts, digram_counts, trigram_counts


# Générer une gamme de tailles de texte à tester
sizes = np.logspace(4, 8, num=10, dtype=int)

old_times = []
new_times = []

for size in sizes:
    print("start generating text.")
    text = "".join(random.choices(string.ascii_letters + string.digits + " .\n", k=size))
    print("text generated.")

    start_time = timeit.default_timer()
    calculate_statistics_old(text)
    old_times.append(timeit.default_timer() - start_time)

    start_time = timeit.default_timer()
    calculate_statistics_new(text)
    new_times.append(timeit.default_timer() - start_time)

# Tracer les résultats
plt.figure(figsize=(10, 6))
plt.plot(sizes, old_times, label='Ancienne méthode')
plt.plot(sizes, new_times, label='Nouvelle méthode')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Taille du texte')
plt.ylabel('Temps (secondes)')
plt.legend()
plt.grid(True)
plt.title('Performance des méthodes de calcul des statistiques de texte')
plt.show()
