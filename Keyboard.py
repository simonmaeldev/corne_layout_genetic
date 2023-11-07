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
        self.stats = None

        if rand:
            self.disp = list(range(36))
            random.shuffle(self.disp)
            self._set_random_letters()
            self._set_custom_stack()
            self.finilize()

    def _set_thumb(self):
        if (self.key_to_char == None):
            self.key_to_char = {}
        self.key_to_char[36] = "LALT"
        self.key_to_char[37] = "DEL"
        self.key_to_char[38] = "SPACE"
        self.key_to_char[39] = "RET"
        self.key_to_char[40] = "BSPC"
        self.key_to_char[41] = "ESC"

        if (self.char_to_key == None):
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
    
    def set_stats(self, stats):
        self.stats = stats
    
    def get_stats(self):
        return self.stats

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

    def all_in_keyboard(self, seq):
        return all(char in self.char_to_key for char in seq)

    def is_same_hand(self, hf1, hf2):
        return hf1[0] == hf2[0]

    def is_sfb(self, hf1, hf2):
        return hf1 == hf2

    def record_rolls(self, keyboard_stats, roll_seq, roll_hf, proba_by_char):
        ro = False
        if roll_seq:
            roll_str = ""
            if roll_seq.count(roll_seq[0]) == len(roll_seq):
                # c'est tout le temps le meme roll dans ma liste
                roll = roll_seq[0]
                if roll == Roll.IN:
                    roll_str = "roll_in"
                else :
                    roll_str = "roll_out"
                    ro = True
            else :
                # si il y a plusieurs rolls différents c'est que c'est un redirect
                roll_str = "redirect"
                ro = True
            for hf in roll_hf:
                keyboard_stats[roll_str][hf] += proba_by_char
        return ro
                

    def get_stats_grams(self, dict):
        # init
        keyboard_stats = {
            "sfb" : {}, # doit utiliser le même doigt pour taper sur 2 touches différentes à la suite. On en veut pas
            "row_jump": {}, # doit sauter la ligne du milieu entre 2 utilisations de la même main (même si l'autre main a été utilisée entre temps). On en veut pas
            "repet" : {}, # probabilité de répéter la même touche
            "roll_in": {}, # deux touches ou plus qui utilisent de facon consécutive des doigts de la même main, vers l'index. ex : sd, ast
            "roll_out": {}, # même chose, mais vers le petit doigt. On en veut pas
            "redirect": {}, # commence un roll dans un sens puis va dans l'autre sens. ex : sfd. On en veut pas
            "ligne_diff": {}, # deux doigts voisins qui sont pas sur la même ligne
            "saut_doigt": {}, # dans un roll, les doigts utilisés ne sont pas tous voisins. Ex : sf
            "alternate" : {}, # on alterne entre les deux mains
        }
        not_present = {}
        weakness = {}
        for empty_dict in keyboard_stats.values():
            for main in Main:
                for doigt in Doigts:
                    empty_dict[(main, doigt)] = 0
        # calcul
        for seq, proba in dict.items():
            if self.all_in_keyboard(seq):
                prev = seq[0]
                last = {Main.GAUCHE : None, Main.DROITE : None}
                roll_seq = []
                roll_hf = []
                last_hf = None
                current_hf = None
                rj = False
                ro = False
                ld = False
                for next in seq[1:]:
                    last_hf = self.char_to_hand_finger[prev]
                    last[last_hf[0]] = self.char_to_key[prev]
                    current_hf = self.char_to_hand_finger[next]
                    roll_hf.append(last_hf)
                    # section 2 appuis consécutifs
                    if self.is_same_hand(last_hf, current_hf):
                        if prev == next :
                            keyboard_stats["repet"][last_hf] += proba
                        elif self.is_sfb(last_hf, current_hf):
                                keyboard_stats["sfb"][last_hf] += proba
                        else :
                            # meme main, pas meme lettre et pas sfb : c'est un roll
                            current_roll = None
                            if last_hf[1].value < current_hf[1].value:
                                current_roll = Roll.OUT
                            else:
                                current_roll = Roll.IN
                            roll_seq.append(current_roll)
                            if not self.doigts_voisins(last_hf, current_hf):
                                keyboard_stats["saut_doigt"][last_hf] += proba
                                keyboard_stats["saut_doigt"][current_hf] += proba
                    else : 
                        keyboard_stats["alternate"][last_hf] += proba
                        keyboard_stats["alternate"][current_hf] += proba
                        # enregistre les rolls si il y en a
                        ro = self.record_rolls(keyboard_stats, roll_seq, roll_hf, proba / len(seq)) or ro
                        roll_seq = []
                        roll_hf = []
                    # section comparaison avec le dernier de la même main
                    if last[current_hf[0]] != None:
                        last_row = keypos_row[last[current_hf[0]]]
                        next_key = self.char_to_key[next]
                        current_row = keypos_row[next_key]
                        reconstructed = (current_hf[0], keypos_finger[last[current_hf[0]]])
                        if last_row != Ligne.POUCE and current_row != Ligne.POUCE:
                            if last_row != current_row and self.doigts_voisins(reconstructed, current_hf):
                                keyboard_stats["ligne_diff"][reconstructed] += proba
                                keyboard_stats["ligne_diff"][current_hf] += proba
                                ld = True
                        if abs(last_row.value - current_row.value) > 1:
                                keyboard_stats["row_jump"][reconstructed] += proba
                                keyboard_stats["row_jump"][current_hf] += proba
                                rj = True
                    prev = next
                ro = self.record_rolls(keyboard_stats, roll_seq, roll_hf, proba / len(seq)) or ro
                if rj or (ro and ld) : #proba > 0.2 and (
                    weakness[seq] = proba
            else :
                not_present[seq] = proba
        return keyboard_stats, not_present, weakness

    # pour les monograms uniquement
    def weight_proba(self, dict):
        weight_by_finger = {}
        not_present = {}
        total_weight = 0
        for main in Main:
            for doigt in Doigts:
                weight_by_finger[(main, doigt)] = 0
        for char, prob in dict.items():
            if char in self.char_to_key:
                weight_by_finger[self.char_to_hand_finger[char]] += prob
                total_weight += prob * weight_map[self.char_to_key[char]]
            else:
                not_present[char] = prob
        return weight_by_finger, not_present, total_weight


    def merge_dict(self, dict1, dict2, weight=1):
        merged_dict = dict1.copy()  # Crée une copie de dict1 pour ne pas modifier l'original
        for key, value in dict2.items():
            if key in merged_dict:
                merged_dict[key] += value * weight
            else:
                merged_dict[key] = value * weight
        return merged_dict

    def evaluate(self):
        # full detailled stats
        detailled_stats = {}
        res_stats = {
            # convergence
            "total_weight": 0,
            "total_weighted_weakness": 0,
            "total_sfb": 0,
            "left_min": 0,
            "left_max": 0,
            "right_min": 0,
            "right_max": 0,
            "total_left": 0,
            "total_right": 0,
            "sfb_left_max": 0,
            "sfb_left_min": 0,
            "sfb_right_max": 0,
            "sfb_right_min": 0,
            "jump_auri": 0,
            "diff_annu": 0,
            "sfb_auri": 0,
            "sfb_annu": 0,
            "total_alternate": 0,
            "total_saut_doigt": 0,
            "total_ligne_diff": 0,
            "total_row_jump": 0,
            "total_roll_in": 0,
            "total_roll_out": 0,
            "total_redirect": 0,
        }
        sum_hf = {}
        sfb_hf = {}
        roll_in_hf = {}
        roll_out_hf = {}
        row_jump_hf = {}
        repet_hf = {}
        ligne_diff_hf = {}
        total_alternate = 0
        total_saut_doigt = 0
        total_ligne_diff = 0
        total_row_jump = 0
        total_roll_in = 0
        total_roll_out = 0
        total_redirect = 0
        for language, dict in stats.items():
            # detailled stats
            keyboard_stats3, not_present3, weakness3 = self.get_stats_grams(dict[3])
            keyboard_stats2, not_present2, weakness2 = self.get_stats_grams(dict[2])
            weight_by_finger, not_present1, total_weight = self.weight_proba(dict[1])
            not_present = self.merge_dict(not_present1, self.merge_dict(not_present2, not_present3))
            weakness = self.merge_dict(weakness2, weakness3)
            keyboard_stats = {}
            for key in keyboard_stats2:
                keyboard_stats[key] = self.merge_dict(keyboard_stats2[key], keyboard_stats3[key])
            detailled_stats[language] = {
                "weight_by_finger": weight_by_finger,
                "keyboard_detailled_stats": keyboard_stats,
                "not_present": not_present,
                "weakness": weakness,
                "total_weight" : total_weight,
            }
            # res stats
            weight_l = weights[language]
            res_stats["total_weight"] += weight_l * total_weight
            res_stats["total_weighted_weakness"] += weight_l * sum(weight_map[self.char_to_key[char]] * value/len(seq) for seq, value in weakness.items() for char in seq)
            res_stats["total_sfb"] += weight_l * sum(keyboard_stats["sfb"].values())
            sum_hf = self.merge_dict(sum_hf, weight_by_finger, weight_l)
            sfb_hf = self.merge_dict(sfb_hf, keyboard_stats["sfb"], weight_l)
            roll_in_hf = self.merge_dict(roll_in_hf, keyboard_stats["roll_in"], weight_l)
            roll_out_hf = self.merge_dict(roll_out_hf, keyboard_stats["roll_out"], weight_l)
            row_jump_hf = self.merge_dict(row_jump_hf, keyboard_stats["row_jump"], weight_l)
            repet_hf = self.merge_dict(repet_hf, keyboard_stats["repet"], weight_l)
            ligne_diff_hf = self.merge_dict(ligne_diff_hf, keyboard_stats["ligne_diff"], weight_l)
            total_alternate += weight_l * sum(keyboard_stats["alternate"].values()) / 2
            total_saut_doigt += weight_l * sum(keyboard_stats["saut_doigt"].values()) / 2
            total_ligne_diff += weight_l * sum(keyboard_stats["ligne_diff"].values()) / 2
            total_row_jump += weight_l * sum(keyboard_stats["row_jump"].values()) / 2
            total_roll_in += weight_l * sum(keyboard_stats["roll_in"].values())
            total_roll_out += weight_l * sum(keyboard_stats["roll_out"].values())
            total_redirect += weight_l * sum(keyboard_stats["redirect"].values())

        res_stats["left_min"] = min(sum_hf[(Main.GAUCHE, Doigts.INDEX)], sum_hf[(Main.GAUCHE, Doigts.MAJEUR)])
        res_stats["left_max"] = max(sum_hf[(Main.GAUCHE, Doigts.AURICULAIRE)], sum_hf[(Main.GAUCHE, Doigts.ANNULAIRE)])
        res_stats["right_min"] = min(sum_hf[(Main.DROITE, Doigts.INDEX)], sum_hf[(Main.DROITE, Doigts.MAJEUR)])
        res_stats["right_max"] = max(sum_hf[(Main.DROITE, Doigts.AURICULAIRE)], sum_hf[(Main.DROITE, Doigts.ANNULAIRE)])
        res_stats["sfb_left_min"] = min(sfb_hf[(Main.GAUCHE, Doigts.INDEX)], sfb_hf[(Main.GAUCHE, Doigts.MAJEUR)])
        res_stats["sfb_left_max"] = max(sfb_hf[(Main.GAUCHE, Doigts.AURICULAIRE)], sfb_hf[(Main.GAUCHE, Doigts.ANNULAIRE)])
        res_stats["sfb_right_min"] = min(sfb_hf[(Main.DROITE, Doigts.INDEX)], sfb_hf[(Main.DROITE, Doigts.MAJEUR)])
        res_stats["sfb_right_max"] = max(sfb_hf[(Main.DROITE, Doigts.AURICULAIRE)], sfb_hf[(Main.DROITE, Doigts.ANNULAIRE)])
        res_stats["total_left"] = sum(value for hf, value in sum_hf.items() if hf[0] == Main.GAUCHE)
        res_stats["total_right"] = sum(value for hf, value in sum_hf.items() if hf[0] == Main.DROITE)
        res_stats["jump_auri"] = keyboard_stats["row_jump"][(Main.GAUCHE, Doigts.AURICULAIRE)] + keyboard_stats["row_jump"][(Main.DROITE, Doigts.AURICULAIRE)]
        res_stats["diff_annu"] = keyboard_stats["ligne_diff"][(Main.GAUCHE, Doigts.ANNULAIRE)] + keyboard_stats["ligne_diff"][(Main.DROITE, Doigts.ANNULAIRE)]
        res_stats["sfb_auri"] = keyboard_stats["sfb"][(Main.GAUCHE, Doigts.AURICULAIRE)] + keyboard_stats["sfb"][(Main.DROITE, Doigts.AURICULAIRE)]
        res_stats["sfb_annu"] = keyboard_stats["sfb"][(Main.GAUCHE, Doigts.ANNULAIRE)] + keyboard_stats["sfb"][(Main.DROITE, Doigts.ANNULAIRE)]
        res_stats["sfb_maj"] = keyboard_stats["sfb"][(Main.GAUCHE, Doigts.MAJEUR)] + keyboard_stats["sfb"][(Main.DROITE, Doigts.MAJEUR)]
        res_stats["sfb_ind"] = keyboard_stats["sfb"][(Main.GAUCHE, Doigts.INDEX)] + keyboard_stats["sfb"][(Main.DROITE, Doigts.INDEX)]
        res_stats["missing"] = "; ".join(str(k) for k in not_present.keys())
        res_stats["weakness"] = "; ".join(str(k) for k in weakness.keys())

        res_stats["total_alternate"] = total_alternate
        res_stats["total_saut_doigt"] = total_saut_doigt
        res_stats["total_ligne_diff"] = total_ligne_diff
        res_stats["total_row_jump"] = total_row_jump
        res_stats["total_roll_in"] = total_roll_in
        res_stats["total_roll_out"] = total_roll_out
        res_stats["ratio_roll"] = total_roll_out / total_roll_in
        res_stats["total_redirect"] = total_redirect

        for hf in sum_hf:
            if hf[1] != Doigts.POUCE:
                res_stats[hf[0].name[0] + "_" + hf[1].name] = sum_hf[hf]
                res_stats["sfb_" + hf[0].name[0] + "_" + hf[1].name] = sfb_hf[hf]
                res_stats["roll_in_" + hf[0].name[0] + "_" + hf[1].name] = roll_in_hf[hf]
                res_stats["roll_out_" + hf[0].name[0] + "_" + hf[1].name] = roll_out_hf[hf]
                res_stats["row_jump_" + hf[0].name[0] + "_" + hf[1].name] = row_jump_hf[hf]
                res_stats["repet_" + hf[0].name[0] + "_" + hf[1].name] = repet_hf[hf]
                res_stats["ligne_diff_" + hf[0].name[0] + "_" + hf[1].name] = ligne_diff_hf[hf]

        self.full_stats = detailled_stats
        self.set_stats(res_stats)
        return res_stats
    
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

class Roll(Enum):
    IN = 0
    OUT = 1
    REDIRECT = 2

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
index_keys = [4, 5, 6, 7, 16, 17, 18, 19, 28, 29, 30, 31]

weight_map = {
     0: 5,    1: 4,    2: 1.5,    3: 1,    4: 1,    5: 1.5,  6: 1.5,  7: 1,    8: 1,    9: 1.5, 10: 4,   11: 5,  
    12: 4,   13: 2,   14: 1,     15: 0.5, 16: 0.5, 17: 1,   18: 1,   19: 0.5, 20: 0.5, 21: 1,   22: 2,   23: 4,
    24: 5,   25: 4,   26: 1.5,   27: 1,   28: 1,   29: 1.5, 30: 1.5, 31: 1,   32: 1,   33: 1.5, 34: 4,   35: 5,  
                               36: 1.5, 37: 0.5, 38: 1,   39: 1,   40: 0.5, 41: 1.5,
}


weights = {
    'fr' : 0.7,
    'en' : 0.3,
    'java' : 0,
    'python' : 0,
    'md' : 0
}


stats = load_no_white_stats()