from FFPoly import FFPoly, pol_to_string, string_to_pol, MODULATOR
import numpy as np
# import os
import json
from util import FF_to_int, int_to_FF

def bitflip(msg, howmany=1, q=2):
    for i in range(howmany):
        flipwhere = np.random.randint(0, len(msg))
        bitflipped = (int(msg[flipwhere]) + 1) % 2
        msg = msg[:flipwhere:] + str(bitflipped) + msg[flipwhere+1::]

    return msg


class Coder:

    def __init__(self, m, q, polynoms_index, verbose=0):
        self._q = q
        self._m = m
        self._n = 2**m -1
        self._k = 2**m - m -1
        self.modulator = MODULATOR(self._n, self._q)
        self.verbose = verbose
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
        """
        decode method
        Args:
            self : the coder used to decode
            msg : a string, which chars are in the finitefield of card self._q
                  and of length self._n
                  
        Returns :
            decoded_word : a string of length self._k, always the finite field of card self.q
        """
        assert len(msg) == self._n
        msg_pol = string_to_pol(msg, self._q)
        is_error = self.checkiferror(msg_pol)

        if is_error:
            # there is an error... let's see if we can correct it !
            can_correct = self.cancorrect(msg_pol)
            if can_correct:
                if self.verbose > 0:
                    print("Error detected and corrected")
                syndrom = self.checkpol * msg_pol
                _, syndrom = syndrom / self.modulator
                for epsilon, syn in self.syndroms:
                    if syn == syndrom:
                        msg_pol = msg_pol + epsilon
            else:
                if self.verbose > 0:
                    print("/!\ There has been more errors than allowed, can't correct")
                #cannot correct... let's just divide by generator
        msg_pol, _ = msg_pol / self.generator
        decoded_word = pol_to_string(msg_pol, self._q)
        while len(decoded_word) < self._k:
            decoded_word += '0'
        return decoded_word


class DataHandler:
    
    def __init__(self, data, coder):
        """
        Attributes :
            self.data is ... the data itself. can be in three different states :
                - text in latin alphabet
                - text in alphabet of q letters
                - text in alphabet of q letters, encoded
            self.level represent the data state (2=latin, 1=binary, 0=list, -1=unconvenient format)
            self.q is the cardinal of the finitefield
            self.k is the length of elementary words
        """
        self.coder = coder
        self._q = coder._q
        self._k = coder._k
        self.data = data
        self.level = self.whichlevel()
        if self.level == -1:
            raise ValueError("Wrong data format of input data")
        if self.level == 2:
            self.wordlen = len(self.data)
        elif self.level == 1:
            self.wordlen = len(self.data) // 16
        elif self.level == 0:
            self.wordlen = ((len(self.data) // self._n) * self._k) // 16
        
    def whichlevel(self):    
        if isinstance(self.data, str):
            possibchar = [str(i) for i in range(self._q)]
            for char in self.data:
                if char not in possibchar:
                    return 2
            return 1
        return -1
    
    def upgradelevel(self):
        if self.level == 0:
            res = []
            N = self.coder._n
            nbchar = len(self.data) // N
            # assert not len(self.data) % N
            for i in range(nbchar):
                res.append(self.data[N*i:N*i + N:])
            for i, word in enumerate(res):
                res[i] = self.coder.decode(word)
            self.data = ''.join(res)
            self.level += 1
        elif self.level == 1:
            nbchar = len(self.data) // 16
            # assert not len(self.data) % 16
            self.data = ''.join(chr(FF_to_int(self.data[16*i:16*i + 16:], self._q)) for i in range(nbchar))
            self.data = self.data[:self.wordlen + 1]
            self.level += 1
        else:
            raise ValueError("level not understood : " + str(self.level) )

    def downgradelevel(self):
        if self.level == 2:
            self.data = ''.join(int_to_FF(ord(x), 16, self._q) for x in self.data)
            self.level -= 1
        elif self.level == 1: 
            res = []
            if not len(self.data) % self._k:
                nbchar = len(self.data) // self._k
            else :
                nbchar = len(self.data) // self._k + 1
                nbadditional = self._k - (len(self.data) % self._k)
                self.data += ''.join('0' for i in range(nbadditional))
            # assert not len(self.data) % self._k
            for i in range(nbchar):
                res.append(self.data[self._k*i:self._k*i + self._k:])
            for i, word in enumerate(res):
                res[i] = self.coder.encode(word)
            self.data = self.data = ''.join(res)
            self.level -= 1

    def ATTACK(self, law='bernoulli', param=0.97):
        assert law in ['bernoulli', 'poisson']
        if self.level == 0:
            if law == 'bernoulli':
                for i, char in enumerate(self.data):
                    if np.random.random() >= param:
                        chgdbit = str((int(char) + 1) % self._q)
                        if i < len(self.data) - 1 :
                            self.data = self.data[:i] + chgdbit + self.data[i+1:]
                        else :
                            self.data = self.data[:i] + chgdbit
            elif law == 'poisson':
                pass
    
    def can_upgrade(self):
        return self.level < 2
    
    def can_downgrade(self):
        return self.level > 0
            
    

if __name__=='__main__':
    Hcode = Coder(4, 2, 0, verbose=1)
    """
    print(str(Hcode.generator))
    to_code = ['1000', '1011', '0101', '1110', '0010', '0011']

    for word in to_code:
        coded = Hcode.encode(word)
        coded_witherror = bitflip(coded, howmany=1)
        decoded = Hcode.decode(coded_witherror)
        print(word +  " --> " + coded + " !bitflip! " + coded_witherror + " --> " + decoded + " | " + str(word==decoded))
    print('the end!')
    """
    mystring = "Hello world!"
    datahandler = DataHandler(mystring, Hcode)
    print(datahandler.data)
    datahandler.downgradelevel()
    # print(datahandler.data)
    datahandler.downgradelevel()
    # print(datahandler.data)
    datahandler.ATTACK()
    # print(datahandler.data)
    datahandler.upgradelevel()
    # print(datahandler.data)
    datahandler.upgradelevel()
    print(datahandler.data)
    
