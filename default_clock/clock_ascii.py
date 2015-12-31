a1_, a2_, b_, c_, d1_, d2_, e_, f_, g1_, g2_, h_, j_, k_, l_, m_, n_ = range(16)

h20_h2f = [
    [],  # 0x20 space
    [],  # 0x21 exclam
    [],  # 0x22 double quote
    [],  # 0x23 pound sign
    [],  # 0x24 dollar
    [],  # 0x25 percent
    [],  # 0x26 ampersand
    [],  # 0x27 single quote
    [],  # 0x28 o parenth
    [],  # 0x29 c parenth
    [],  # 0x2a asterisk
    [],  # 0x2b plus
    [],  # 0x2c comma
    [],  # 0x2d hyphen
    [],  # 0x2e period
    [],  # 0x2f slash
]

h30_h39 = [
    [a1_, a2_, b_, c_, d1_, d2_, e_, f_, k_, n_],       # 0x30 0
    [b_, c_, k_],                                       # 0x31 1
    [a1_, a2_, b_, d1_, d2_, e_, g1_, g2_],             # 0x32 2
    [a1_, a2_, b_, c_, d1_, d2_, g2_],                  # 0x33 3
    [b_, c_, f_, g1_, g2_],                             # 0x34 4
    [a1_, a2_, c_, d1_, d2_, f_, g1_, g2_],             # 0x35 5
    [a1_, c_, d1_, d2_, e_, f_, g1_, g2_],              # 0x36 6
    [a1_, a2_, b_, c_],                                 # 0x37 7
    [a1_, a2_, b_, c_, d1_, d2_, e_, f_, g1_, g2_],     # 0x38 8
    [a1_, a2_, b_, c_, d2_, f_, g1_, g2_],              # 0x39 9
]

h3a_h40 = [
    [],  # 0x3a colon
    [],  # 0x3b semicolon
    [],  # 0x3c less than
    [],  # 0x3d equals
    [],  # 0x3e greater than
    [],  # 0x3f question mark
    [],  # 0x40 at symbol
]

h5b_h60 = [
    [],  # 0x5b o bracket
    [],  # 0x5c backslash
    [],  # 0x5d c bracket
    [],  # 0x5e caret
    [],  # 0x5f underscore
    [],  # 0x60 grave
]

hb0_hb9 = [
    [a2_, b_, g2_, j_],  # 0xb0 degree
    [],  # 0xb1 plus-minus
    [],  # 0xb2 super 2
    [],  # 0xb3 super 3
    [],  # 0xb4 acute accent
    [],  # 0xb5 micro
    [],  # 0xb6 pilcrow
    [],  # 0xb7 middle dot
    [],  # 0xb8 spacing cedilla
    [],  # 0xb9 super 1
]

alphabet = [
    [a1_, a2_, b_, c_, e_, f_, g1_, g2_],       # A
    [a1_, a2_, b_, c_, d1_, d2_, g1_, g2_, j_, m_],   # B
    [a1_, a2_, d1_, d2_, e_, f_],               # C
    [a1_, a2_, b_, c_, d1_, d2_, j_, m_],       # D
    [a1_, a2_, d1_, d2_, e_, f_, g1_],           # E
    [a1_, a2_, e_, f_, g1_],               # F
    [a1_, a2_, c_, d1_, d2_, e_, f_, g2_],       # G
    [b_, c_, e_, f_, g1_, g2_],           # H
    [a1_, a2_, d1_, d2_, j_, m_],                       # I
    [b_, c_, d1_, d2_, e_],               # J
    [e_, f_, g1_, k_, l_],           # K
    [d1_, d2_, e_, f_],                   # L
    [b_, c_, e_, f_, h_, k_],                   # M
    [b_, c_, e_, f_, h_, l_],                   # N
    [a1_, a2_, b_, c_, d1_, d2_, e_, f_],       # O
    [a1_, a2_, b_, e_, f_, g1_, g2_],           # P
    [a1_, a2_, b_, c_, d1_, d2_, e_, f_, l_],           # Q
    [a1_, a2_, b_, e_, f_, g1_, g2_, l_],                       # R
    [a1_, a2_, c_, d1_, d2_, f_, g1_, g2_],           # S
    [a1_, a2_, j_, m_],               # T
    [b_, c_, d1_, d2_, e_, f_],           # U
    [e_, f_, n_, k_],                   # V
    [b_, c_, e_, f_, n_, l_],                   # W
    [h_, k_, l_, n_],           # X
    [b_, f_, g1_, g2_, m_],           # Y
    [a1_, a2_, d1_, d2_, k_, n_],           # Z
]


def char_segs(char):
    char = ord(char)

    if 0x00 <= char < 0x20:
        return []
    if 0x20 <= char < 0x30:
        return h20_h2f[char-0x20]
    if 0x30 <= char < 0x3a:
        return h30_h39[char-0x30]
    if 0x3a <= char < 0x41:
        return h3a_h40[char-0x3a]
    if 0x41 <= char < 0x5b:
        return alphabet[char-0x41]
    if 0x5b <= char < 0x61:
        return h5b_h60[char-0x5b]
    if 0x61 <= char < 0x7b:
        return alphabet[char-0x61]
    if 0x7b <= char < 0xb0:
        return []
    if 0xb0 <= char < 0xba:
        return hb0_hb9[char-0xb0]
    if 0xba <= char <= 0xff:
        return []
