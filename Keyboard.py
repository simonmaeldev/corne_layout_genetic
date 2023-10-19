from enum import Enum
from Data import *
import random
import numpy as np


class Keyboard():
    def __init__(self,empty= False, key_to_char = {}, char_to_key = {}):
        self.key_to_char = key_to_char
        self.char_to_key = char_to_key
        self.disp = []
        self._set_thumb()

        if not empty:
            self.disp = random.shuffle(range(36))
            self._set_random_letters()
            self._set_custom_stack()

    def _set_thumb(self):
        self.key_to_char[36] = "LALT"
        self.key_to_char[37] = "DEL"
        self.key_to_char[38] = "SPACE"
        self.key_to_char[39] = "ENTER"
        self.key_to_char[40] = "BSPC"
        self.key_to_char[41] = "ESC"

        self.char_to_key["LALT"] = 36
        self.char_to_key["DEL"] = 37
        self.char_to_key["SPACE"] = 38
        self.char_to_key["ENTER"] = 39
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
    
    def get_key_to_char(self):
        return self.key_to_char

    def get_char_to_key(self):
        return self.char_to_key
    
    def get_char(self, key):
        return self.char_to_key[key]
    
    def get_key(self, char):
        return self.key_to_char[char]
    
    def set_key_char(self, key, char):
        self.key_to_char[key] = char
        self.char_to_key[char] = key

    def mate_with(self, other):
        # mate with method in this paper http://azariaa.com/content/publications/keyboard.pdf
        # modified to generate 2 childs
        not_done = random.shuffle(char_to_set.copy())
        parent1, parent2 = self, other
        child1, child2 = Keyboard(empty=True), Keyboard(empty=True)
        while not_done:
            # get parents
            if np.random.random() < 0.5:
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
        return child1, child2
    
    def __eq__(self, other):
        if isinstance(other, Keyboard):
            return self.key_to_char == other.key_to_char and self.char_to_key == other.char_to_key
        return False

    def _evaluate(self, x, out, *args, **kwargs):
        n_a, n_b = 0, 0
        keyboard = x[0]


        out["F"] = np.array([- n_a, - n_b], dtype=float)



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