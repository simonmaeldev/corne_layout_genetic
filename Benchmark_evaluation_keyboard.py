from Keyboard import *
from Dataset import *

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

qwerty_key_to_char = {
    0: 'TAB',
    1: 'Q',
    2: 'W',
    3: 'E',
    4: 'R',
    5: 'T',
    6: 'Y',
    7: 'U',
    8: 'I',
    9: 'O',
    10: 'P',
    11: 'BSPC',
    12: 'CAPSLOCK',
    13: 'A',
    14: 'S',
    15: 'D',
    16: 'F',
    17: 'G',
    18: 'H',
    19: 'J',
    20: 'K',
    21: 'L',
    22: ';',
    23: 'SQT',
    24: 'SHIFT',
    25: 'Z',
    26: 'X',
    27: 'C',
    28: 'V',
    29: 'B',
    30: 'N',
    31: 'M',
    32: ',',
    33: '.',
    34: '/',
    35: 'SHIFT',
    36: 'CTRL',
    37: 'ALT',
    38: 'SPACE',
    39: 'ALTGR',
    40: 'MENU',
    41: 'CTRLRIGHT',
}

qwerty_char_to_key = {
    'TAB': 0,
    'Q': 1,
    'W': 2,
    'E': 3,
    'R': 4,
    'T': 5,
    'Y': 6,
    'U': 7,
    'I': 8,
    'O': 9,
    'P': 10,
    'BSPC': 11,
    'CAPSLOCK': 12,
    'A': 13,
    'S': 14,
    'D': 15,
    'F': 16,
    'G': 17,
    'H': 18,
    'J': 19,
    'K': 20,
    'L': 21,
    ';': 22,
    'SQT': 23,
    'SHIFT': 24,
    'Z': 25,
    'X': 26,
    'C': 27,
    'V': 28,
    'B': 29,
    'N': 30,
    'M': 31,
    ',': 32,
    '.': 33,
    '/': 34,
    'LSHIFT': 35,
    'LCTRL': 36,
    'SPACE': 37,
    'LALT': 38,
    'RET': 39,
    'LGUI': 40,
    'RALT': 41,
}

qwerty_keyboard = Keyboard(rand=False, key_to_char=qwerty_key_to_char, char_to_key=qwerty_char_to_key)
char_to_hf = qwerty_keyboard.finilize()

def same_hand(hf1, hf2):
    return hf1[0] == hf2[0]

def doigts_voisins(hf1: [Doigts], hf2: [Doigts]):
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