import numpy as np
from FFPoly import FFPoly
import json

Mparam = 3
Qparam = 2
assert Mparam > 1

def int_to_pol(int, fieldcardinal):
    max_exp = 0
    scale = fieldcardinal**max_exp
    while scale <= int :
        max_exp += 1
        scale = fieldcardinal**max_exp

    coeffs = np.zeros((scale))
    intcopy = int
    while intcopy > 0:
        max_exp -= 1
        scale = fieldcardinal**max_exp
        coeffs[max_exp] = intcopy // scale
        intcopy -= (intcopy // scale) * scale
    return FFPoly(coeffs, fieldcardinal)

def find_hamming_gens(m = Mparam, q=Qparam):
    n, k = 2^m - 1, 2^m - m - 1
    modulator = np.zeros((n + 1))
    modulator[n+1] = 1
    modulator[0] = 1
    modulator = FFPoly(modulator, q)

    generators = []

if __name__=='__main__':
    print(str(int_to_pol(15,3)))
