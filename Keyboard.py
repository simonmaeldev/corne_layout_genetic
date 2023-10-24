from enum import Enum
from Data import *
import random
import numpy as np
from Dataset import *


class Keyboard():
    def __init__(self, rand= True, key_to_char = None, char_to_key = None):
        self.key_to_char = key_to_char
        self.char_to_key = char_to_key
        self.disp = None
        self.char_to_hand_finger = None
        self._set_thumb()
        self.full_stats = None

        if rand:
            self.disp = list(range(36))
            random.shuffle(self.disp)
            self._set_random_letters()
            self._set_custom_stack()
            self.finilize()

    def _set_thumb(self):
        self.key_to_char = {}
        self.key_to_char[36] = "LALT"
        self.key_to_char[37] = "DEL"
        self.key_to_char[38] = "SPACE"
        self.key_to_char[39] = "RET"
        self.key_to_char[40] = "BSPC"
        self.key_to_char[41] = "ESC"

        self.char_to_key = {}
        self.char_to_key["LALT"] = 36
        self.char_to_key["DEL"] = 37
        self.char_to_key["SPACE"] = 38
        self.char_to_key["RET"] = 39
        self.char_to_key["BSPC"] = 40
        self.char_to_key["ESC"] = 41

    def _set_random_letters(self):
        for char in not_stackable:
            char = char.upper()
            idx = self.disp.pop()
            self.key_to_char[idx] = char
            self.char_to_key[char] = idx
    
    def _set_custom_stack(self):
        for pair in custom_stack:
            lower = pair[0]
            #upper = pair[1]
            idx = self.disp.pop()
            #self.key_to_char[idx] = [lower, upper]
            self.key_to_char[idx] = lower
            self.char_to_key[lower] = idx
            #self.char_to_key[upper] = idx
    
    def finilize(self):
        self.add_custom_stack()
        return self.calculate_char_to_hand_finger()

    def calculate_char_to_hand_finger(self):
        self.char_to_hand_finger = {}
        for char, key in self.char_to_key.items():
            hand = keypos_hand.get(key)
            finger = keypos_finger.get(key)
            if hand is not None and finger is not None:
                self.char_to_hand_finger[char] = (hand, finger)
        return self.char_to_hand_finger
    
    def add_custom_stack(self):
        for stack in custom_stack:
            if (stack[0] in self.char_to_key):
                self.char_to_key[stack[1]] = self.char_to_key[stack[0]]

    def get_key_to_char(self):
        return self.key_to_char

    def get_char_to_key(self):
        return self.char_to_key
    
    def get_char(self, key):
        return self.key_to_char[key]
    
    def get_key(self, char):
        return self.char_to_key[char]
    
    def set_key_char(self, key, char):
        self.key_to_char[key] = char
        self.char_to_key[char] = key

    def mate_with(self, other):
        # mate with method in this paper http://azariaa.com/content/publications/keyboard.pdf
        # modified to generate 2 childs
        not_done = char_to_set.copy()
        random.shuffle(not_done)
        parent1, parent2 = self, other
        child1, child2 = Keyboard(rand=False), Keyboard(rand=False)
        while not_done:
            # get parents
            r = np.random.random()
            if r < 0.5:
                parent1, parent2 = self, other
            else:
                parent1, parent2 = other, self
            char = not_done[0]
            original = char
            cycle_finished = False
            while not cycle_finished:
                not_done.remove(char)
                key1 = parent1.get_key(char)
                key2 = parent2.get_key(char)
                child1.set_key_char(key1, char)
                child2.set_key_char(key2, char)
                char = parent1.get_char(key2)
                cycle_finished = original == char
        child1.finilize()
        child2.finilize()
        return child1, child2
    
    def __eq__(self, other):
        if isinstance(other, Keyboard):
            return self.key_to_char == other.key_to_char and self.char_to_key == other.char_to_key
        return False

    def same_hand(self, hf1, hf2):
        return hf1[0] == hf2[0]

    def doigts_voisins(self, hf1, hf2):
        return hf1[1].value == hf2[1].value -1 or hf1[1].value == hf2[1].value +1

    # pour les digrams et trigrams
    def get_nb_sfb_jump(self, dict):
        # nombre de lettres différentes qui sont tapées par le même doigt à la suite
        prob_sfb = 0
        # si doit utiliser le meme doigt, éviter de sauter une ligne
        prob_row_jump = 0
        # repetition de la meme lettre
        prob_repet = 0
        # annulaire sur rangée différente du voisin
        annulaire = 0
        # roll in / roll out
        roll_in, roll_out = 0, 0
        # voisins pas meme ligne / saute doigt
        voisins_ligne_diff, saut_doigt = 0, 0

        # annulaire sur rangée différente du majeur ou du petit doigt
        for seq, proba in dict.items():
            prev = seq[0]
            for next in seq[1:]:
                if prev in self.char_to_key and next in self.char_to_key:
                    # meme caractere 
                    if prev == next :
                        if Doigts.MAJEUR == keypos_finger[self.char_to_key[prev]]:
                            prob_repet += proba /2
                        else :
                            prob_repet += proba
                    else : 
                        hf_prev = self.char_to_hand_finger[prev]
                        hf_next = self.char_to_hand_finger[next]
                        row_prev = keypos_row[self.char_to_key[prev]]
                        row_next = keypos_row[self.char_to_key[next]]
                        # meme doigt et meme main
                        if ( hf_prev == hf_next):
                            prob_sfb += proba
                            # on saute la ligne centrale
                            if (row_prev == Ligne.BAS and row_next == Ligne.HAUT) or (row_prev == Ligne.HAUT and row_next == Ligne.BAS):
                                prob_row_jump += proba
                        else :
                            if self.same_hand(hf_prev, hf_next):
                                voisins = self.doigts_voisins(hf_prev, hf_next)
                                if (hf_prev[1].value < hf_next[1].value) :
                                    roll_out += proba
                                else : 
                                    roll_in += proba
                                
                                if row_prev != row_next:
                                    if voisins:
                                        voisins_ligne_diff += proba
                                        # on utilise l'annulaire et un autre doigt voisin et ils sont pas sur la meme ligne
                                        if (hf_prev[1] == Doigts.ANNULAIRE or hf_next[1] == Doigts.ANNULAIRE):
                                            annulaire += proba
                                    else:
                                        saut_doigt += proba
                prev = next

        ratio_roll = 0
        ratio_voisin_saut = 0

        if roll_out != 0:
            if roll_in == 0:
                ratio_roll = float('inf')
            else:
                ratio_roll = roll_out / roll_in
        if voisins_ligne_diff != 0:
            if saut_doigt == 0:
                ratio_voisin_saut = float('inf')
            else:
                ratio_voisin_saut = voisins_ligne_diff / saut_doigt
        return prob_sfb, prob_row_jump, prob_repet, annulaire, ratio_roll, ratio_voisin_saut

    # pour les monograms uniquement
    def weight_proba(self, dict):
        total = 0
        index = 0
        for char, prob in dict.items():
            if char in self.char_to_key:
                key = self.char_to_key[char]
                weight = weight_map[key] * prob
                total += weight
                if key in index_keys:
                    index += weight
        return total, index
    
    def evaluate(self):
        res = {}
        for language, dict in stats.items():
            res2 = self.get_nb_sfb_jump(dict[2])
            res3 = self.get_nb_sfb_jump(dict[3])
            sum_23 = list(map(lambda x, y: x + y, res2, res3))
            res[language] = list(self.weight_proba(dict[1])) + sum_23
        self.full_stats = res
        return res
    
    def __str__(self):
        sorted_keys = sorted(self.key_to_char.keys())
        return "|" + "|".join([self.key_to_char[key].center(5) + ('|\n' if i % 12 == 11 else '') + (' ' * 18 if i == 35 else '') for i, key in enumerate(sorted_keys)]) + "|"

class Ligne(Enum):
    MILIEU = 0
    HAUT = 1
    BAS = 2
    POUCE = 3

class Doigts(Enum):
    POUCE = 0
    INDEX = 1
    MAJEUR = 2
    ANNULAIRE = 3
    AURICULAIRE = 4

class Main(Enum):
    GAUCHE = 0
    DROITE = 1

# mis en dur pour un soucis d'optimisation comme on va souvent y avoir accès
keypos_hand = {
    0: Main.GAUCHE,
    1: Main.GAUCHE,
    2: Main.GAUCHE,
    3: Main.GAUCHE,
    4: Main.GAUCHE,
    5: Main.GAUCHE,
    6: Main.DROITE,
    7: Main.DROITE,
    8: Main.DROITE,
    9: Main.DROITE,
    10: Main.DROITE,
    11: Main.DROITE,
    12: Main.GAUCHE,
    13: Main.GAUCHE,
    14: Main.GAUCHE,
    15: Main.GAUCHE,
    16: Main.GAUCHE,
    17: Main.GAUCHE,
    18: Main.DROITE,
    19: Main.DROITE,
    20: Main.DROITE,
    21: Main.DROITE,
    22: Main.DROITE,
    23: Main.DROITE,
    24: Main.GAUCHE,
    25: Main.GAUCHE,
    26: Main.GAUCHE,
    27: Main.GAUCHE,
    28: Main.GAUCHE,
    29: Main.GAUCHE,
    30: Main.DROITE,
    31: Main.DROITE,
    32: Main.DROITE,
    33: Main.DROITE,
    34: Main.DROITE,
    35: Main.DROITE,
    36: Main.GAUCHE,
    37: Main.GAUCHE,
    38: Main.GAUCHE,
    39: Main.DROITE,
    40: Main.DROITE,
    41: Main.DROITE
}

keypos_finger = {
    0: Doigts.AURICULAIRE,
    1: Doigts.AURICULAIRE,
    2: Doigts.ANNULAIRE,
    3: Doigts.MAJEUR,
    4: Doigts.INDEX,
    5: Doigts.INDEX,
    6: Doigts.INDEX,
    7: Doigts.INDEX,
    8: Doigts.MAJEUR,
    9: Doigts.ANNULAIRE,
    10: Doigts.AURICULAIRE,
    11: Doigts.AURICULAIRE,
    12: Doigts.AURICULAIRE,
    13: Doigts.AURICULAIRE,
    14: Doigts.ANNULAIRE,
    15: Doigts.MAJEUR,
    16: Doigts.INDEX,
    17: Doigts.INDEX,
    18: Doigts.INDEX,
    19: Doigts.INDEX,
    20: Doigts.MAJEUR,
    21: Doigts.ANNULAIRE,
    22: Doigts.AURICULAIRE,
    23: Doigts.AURICULAIRE,
    24: Doigts.AURICULAIRE,
    25: Doigts.AURICULAIRE,
    26: Doigts.ANNULAIRE,
    27: Doigts.MAJEUR,
    28: Doigts.INDEX,
    29: Doigts.INDEX,
    30: Doigts.INDEX,
    31: Doigts.INDEX,
    32: Doigts.MAJEUR,
    33: Doigts.ANNULAIRE,
    34: Doigts.AURICULAIRE,
    35: Doigts.AURICULAIRE,
    36: Doigts.POUCE,
    37: Doigts.POUCE,
    38: Doigts.POUCE,
    39: Doigts.POUCE,
    40: Doigts.POUCE,
    41: Doigts.POUCE
}

keypos_row = {
    0: Ligne.HAUT,
    1: Ligne.HAUT,
    2: Ligne.HAUT,
    3: Ligne.HAUT,
    4: Ligne.HAUT,
    5: Ligne.HAUT,
    6: Ligne.HAUT,
    7: Ligne.HAUT,
    8: Ligne.HAUT,
    9: Ligne.HAUT,
    10: Ligne.HAUT,
    11: Ligne.HAUT,
    12: Ligne.MILIEU,
    13: Ligne.MILIEU,
    14: Ligne.MILIEU,
    15: Ligne.MILIEU,
    16: Ligne.MILIEU,
    17: Ligne.MILIEU,
    18: Ligne.MILIEU,
    19: Ligne.MILIEU,
    20: Ligne.MILIEU,
    21: Ligne.MILIEU,
    22: Ligne.MILIEU,
    23: Ligne.MILIEU,
    24: Ligne.BAS,
    25: Ligne.BAS,
    26: Ligne.BAS,
    27: Ligne.BAS,
    28: Ligne.BAS,
    29: Ligne.BAS,
    30: Ligne.BAS,
    31: Ligne.BAS,
    32: Ligne.BAS,
    33: Ligne.BAS,
    34: Ligne.BAS,
    35: Ligne.BAS,
    36: Ligne.POUCE,
    37: Ligne.POUCE,
    38: Ligne.POUCE,
    39: Ligne.POUCE,
    40: Ligne.POUCE,
    41: Ligne.POUCE
}

comfort_pos = [2, 3, 4, 7, 8, 9, 13, 14, 15, 16, 19, 20, 21, 22, 26, 27, 28, 31, 32, 33]
home_row = [13, 14, 15, 16, 19, 20, 21, 22]
voisins_annulaire = [Doigts.AURICULAIRE, Doigts.MAJEUR]
index_keys = [4, 5, 6, 716, 17, 18, 19, 28, 29, 30, 31]

weight_map = {
    0: 2,
    1: 1.5,
    2: 1,
    3: 1,
    4: 1,
    5: 1.5,
    6: 1.5,
    7: 1,
    8: 1,
    9: 1,
    10: 1.5,
    11: 2,
    12: 1.5,
    13: 1,
    14: 0.5,
    15: 0.5,
    16: 0.5,
    17: 1,
    18: 1,
    19: 0.5,
    20: 0.5,
    21: 0.5,
    22: 1,
    23: 1.5,
    24: 2,
    25: 1.5,
    26: 1,
    27: 1,
    28: 1,
    29: 1.5,
    30: 1.5,
    31: 1,
    32: 1,
    33: 1,
    34: 1.5,
    35: 2,
    36: 1.5,
    37: 0.5,
    38: 1,
    39: 1,
    40: 0.5,
    41: 1.5,
}
