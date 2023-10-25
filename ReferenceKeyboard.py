from Keyboard import *

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
    12: 'CAPS',
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
    'CAPS': 12,
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