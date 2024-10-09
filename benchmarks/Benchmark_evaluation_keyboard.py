from models.Keyboard import Ligne, Doigts, keypos_finger, keypos_row, index_keys, weight_map, stats
from models.ReferenceKeyboard import qwerty_char_to_key, char_to_hf
from typing import List

keyboard_keys = [
    'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'BSPC',
    'CapsLock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'',
    'Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift',
    'Ctrl', 'Alt', 'Space', 'AltGr', 'Menu', 'CtrlRight'
]

def list_to_dict(lst):
    return {k: v.upper() for k, v in enumerate(lst)}
keyboard_dict = list_to_dict(keyboard_keys)

# Afficher le dictionnaire
for key, value in keyboard_dict.items():
    print(f"'{value}': {key},")



def same_hand(hf1, hf2):
    return hf1[0] == hf2[0]

def doigts_voisins(hf1: List[Doigts], hf2: List[Doigts]):
    return hf1[1].value == hf2[1].value -1 or hf1[1].value == hf2[1].value +1

# pour les digrams et trigrams
def get_nb_sfb_jump(dict):
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
            if prev in qwerty_char_to_key and next in qwerty_char_to_key:
                # meme caractere 
                if prev == next :
                    if Doigts.MAJEUR == keypos_finger[qwerty_char_to_key[prev]]:
                        prob_repet += proba /2
                    else :
                        prob_repet += proba
                else : 
                    hf_prev = char_to_hf[prev]
                    hf_next = char_to_hf[next]
                    row_prev = keypos_row[qwerty_char_to_key[prev]]
                    row_next = keypos_row[qwerty_char_to_key[next]]
                    # meme doigt et meme main
                    if ( hf_prev == hf_next):
                        prob_sfb += proba
                        # on saute la ligne centrale
                        if (row_prev == Ligne.BAS and row_next == Ligne.HAUT) or (row_prev == Ligne.HAUT and row_next == Ligne.BAS):
                            prob_row_jump += proba
                    else :
                        if same_hand(hf_prev, hf_next):
                            voisins = doigts_voisins(hf_prev, hf_next)
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
def weight_proba(dict):
    total = 0
    index = 0
    for char, prob in dict.items():
        if char in qwerty_char_to_key:
            key = qwerty_char_to_key[char]
            weight = weight_map[key] * prob
            total += weight
            if key in index_keys:
                index += weight
    return total, index

def evaluate():
    res = {}
    for language, dict in stats.items():
        res[language] = list(weight_proba(dict[1])) + list(get_nb_sfb_jump(dict[2])) + list(get_nb_sfb_jump(dict[3]))
    return res

print(evaluate())