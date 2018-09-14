from FFPoly import FFPoly
from hcodebuilder import pol_to_string
import numpy as np
# import os
import json

def string_to_pol(polynom, q):
    rescoeffs = np.zeros((len(polynom)))
    i = 0
    for char in polynom:
        rescoeffs[i] = int(char)
        i += 1
    return FFPoly(rescoeffs, q)

class Coder:

    def __init__(self, m, q, polynoms_index):
        with open('hammingpolynomials.json', 'r') as jsonfile:
            data = json.load(jsonfile)['data']
            for hamparam in data :
                if hamparam["q"] == q and hamparam["m"] == m:
                    # We found the right dict
                    self.generator = hamparam['pols'][polynoms_index]['generator']
                    self.checkpol = hamparam['pols'][polynoms_index]['checkpol']
                    self.generator = string_to_pol(self.generator, q)
                    self.checkpol = string_to_pol(self.checkpol, q)
                    self._n = 2**m -1
                    self._k = 2**m - m -1
                    self._q = q
                    self._m = m
                    self.modulator = np.zeros((self._n + 1))
                    self.modulator[self._n] = 1
                    self.modulator[0] = 1
                    self.modulator = FFPoly(self.modulator, self._q)
                    self
                    break

        print("    ---    Coder Initialized    ---    ")
        print("  Code Parameters (n, k, q): ({}, {}, {})  ".format(self._n, self._k, self._q))

    def encode(self, msg):
        assert len(msg) == self._k

        to_code_pol = string_to_pol(msg, self._q)
        coded_pol = to_code_pol * self.generator
        quot, coded_pol = coded_pol / self.modulator
        coded_word = pol_to_string(coded_pol, self._q)
        while len(coded_word) < self._n :
            coded_word += '0'

        assert len(coded_word) == self._n
        return coded_word


if __name__=='__main__':
    Hcode = Coder(3, 2, 0)
    print(str(Hcode.generator))
    to_code = ['1000', '1011', '0101']
    for word in to_code:
        coded = Hcode.encode(word)
        print(word +  " --> " + coded)
    print('the end!')
