from FFPoly import FFPoly, pol_to_string, string_to_pol, MODULATOR
import numpy as np
# import os
import json

def bitflip(msg, howmany=1, q=2):
    for i in range(howmany):
        flipwhere = np.random.randint(0, len(msg))
        bitflipped = (int(msg[flipwhere]) + 1) % 2
        msg = msg[:flipwhere:] + str(bitflipped) + msg[flipwhere+1::]

    return msg


class Coder:

    def __init__(self, m, q, polynoms_index):
        self._q = q
        self._m = m
        self._n = 2**m -1
        self._k = 2**m - m -1
        self.modulator = MODULATOR(self._n, self._q)
        with open('hammingpolynomials.json', 'r') as jsonfile:
            data = json.load(jsonfile)['data']
            for hamparam in data :
                if hamparam["q"] == q and hamparam["m"] == m:
                    # We found the right dict
                    self.generator = hamparam['pols'][polynoms_index]['generator']
                    self.checkpol = hamparam['pols'][polynoms_index]['checkpol']
                    self.generator = string_to_pol(self.generator, q)
                    self.checkpol = string_to_pol(self.checkpol, q)

                    break
        # now, let's build and record syndroms
        self.syndroms = self.buildsyndroms()
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

    def buildsyndroms(self):
        syndroms = []
        for i in range(self._n):
            epsilon = np.zeros((self._n))
            epsilon[i] = 1
            epsilon = FFPoly(epsilon, self._q)
            syndrom = epsilon * self.checkpol
            _, syndrom = syndrom / self.modulator
            tempsyn = (epsilon, syndrom)
            syndroms.append(tempsyn)

        return syndroms

    def checkiferror(self, msg_pol):
        syndrom = self.checkpol * msg_pol
        _, rem = syndrom / self.modulator
        if rem == FFPoly(np.array([0]), self._q):
            return False
        else :
            return True

    def cancorrect(self, msg_pol):
        syndrom = self.checkpol * msg_pol
        _, syndrom = syndrom / self.modulator
        for epsilon, syn in self.syndroms:
            if syn == syndrom:
                return True
        #If we arrive here, it means that no 1-bitflip syndrom correspond to ours
        #So there has been more than one bitflip, we cant decode it
        return False

    def decode(self, msg):
        assert len(msg) == self._n
        msg_pol = string_to_pol(msg, self._q)
        is_error = self.checkiferror(msg_pol)

        if is_error:
            # there is an error... let's see if we can correct it !
            can_correct = self.cancorrect(msg_pol)
            if can_correct:
                print("Error detected and corrected")
                syndrom = self.checkpol * msg_pol
                _, syndrom = syndrom / self.modulator
                for epsilon, syn in self.syndroms:
                    if syn == syndrom:
                        msg_pol = msg_pol + epsilon
            else:
                print("/!\ There has been more errors than allowed, can't correct")
                #cannot correct... let's just
        msg_pol, _ = msg_pol / self.generator
        decoded_word = pol_to_string(msg_pol, self._q)
        while len(decoded_word) < self._k:
            decoded_word += '0'
        return decoded_word


if __name__=='__main__':
    Hcode = Coder(3, 2, 0)
    print(str(Hcode.generator))
    to_code = ['1000', '1011', '0101', '1110', '0010', '0011']

    for word in to_code:
        coded = Hcode.encode(word)
        coded_witherror = bitflip(coded, howmany=3)
        decoded = Hcode.decode(coded_witherror)
        print(word +  " --> " + coded + " !bitflip! " + coded_witherror + " --> " + decoded + " | " + str(word==decoded))
    print('the end!')
