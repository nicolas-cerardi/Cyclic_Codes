# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 13:35:23 2017

@author: Sony
"""

#CYCLIC CODE
import random

class Polynome:
    def __init__(self, coeff):
        self.coeff = [int(v) for v in coeff] + [0 for i in range(40-len(coeff))]
        
    def add(c1, c2):
        c3 = Polynome('0')
        c3.coeff = [(v+w)%2 for v,w in zip(c1.coeff, c2.coeff)]
        return c3
    
    def multcons(pol, cons):
        c = Polynome('0')
        c.coeff = [ (cons*v)%2 for v in pol.coeff]
        return c
        
    def ordup(c1, deg):
        c2 = Polynome('0')
        c2.coeff = [0 for i in range(deg)] + c1.coeff[:41-deg]
        return c2
    
    def multpol(c1, c2):
        c3 = Polynome('0')
        for i,v in enumerate(c2.coeff):
            if v!=0:
                c3 = Polynome.add(c3, Polynome.multcons(Polynome.ordup(c1, i), v))
        c3.coeff = [v%2 for v in c3.coeff]
        return c3
    
    def get_deg(self):
        deg = -1
        for i,v in enumerate(self.coeff):
            if v == 1:
                deg = i
        return deg
    
    def divpol(c1, c2):
        pol1 = c1
        pol2 = c2
        Q = Polynome('0')
        while pol1.get_deg() >= pol2.get_deg():
            a, b = pol2.coeff[pol2.get_deg()], pol1.coeff[pol1.get_deg()]
            difdeg = pol1.get_deg()-pol2.get_deg()
            Piv = Polynome('0')
            Piv.coeff[difdeg] = a/b
            Q = Polynome.add(Q, Piv)
            c3 = Polynome.multpol(pol2, Piv)
            c3.coeff = [-v for v in c3.coeff]
            pol1 = Polynome.add(pol1, c3)
            
        return Q, pol1

class CyclicCode:
    
    def encode(self, msg):
        polmsg = Polynome(msg)
        codedmsg = Polynome.multpol(polmsg, self.generator)
        return codedmsg
    
    def decode(self, msg):
        polmsg = Polynome(msg)
        q, r = Polynome.divpol(polmsg, self.generator)
        return q, r
    
    def correct(self,  msg):
        if self.is_correct(msg):
            return msg
        polmsg = Polynome(msg)
        q1, r1 = Polynome.divpol(polmsg, self.generator)
        for i in range(len(msg)):
            epsilon = ''
            for j in range(len(msg)):
                if j == i : epsilon += '1'
                else : epsilon += '0'
            poleps = Polynome(epsilon)
            q2, r2 = Polynome.divpol(poleps, self.generator)
            if r2.coeff == r1.coeff:
                return Polynome.add(polmsg, poleps)
        print('coeff de r1 :', r1.coeff)
        print('oups bug...')
        return
    
    def is_correct(self, msg):
        polmsg = Polynome(msg)
        P1 = Polynome.multpol(polmsg, self.check)
        q, r = Polynome.divpol(P1, self.modulo)
        if r.coeff == Polynome('0').coeff:
            return True
        return False

    def put_error(self, msg):
        k = random.random()*7
        i=0
        msgcorrupt = ''
        for i in range(len(msg)):
            if (i <= k) and (k < i+1):
                msgcorrupt += str((int(msg[i])+1)%2)
            else :
                msgcorrupt += msg[i]
        return msgcorrupt
    
    def pol_into_msg(self, pol):
        msg = ''
        for val in pol.coeff:
            msg += str(int(val))
        return msg[:2**self.M-1]
    
    def __init__(self, msg):
        self.key = len(msg)
        
        Mfound = False
        self.M = 0
        while(not(Mfound)):
            self.M += 1
            if len(msg) == (2**self.M)-self.M-1:
                Mfound = True
            elif self.M>100 :
                print('boucle infinie')
                raise Exception
        
        modulopoly = '1'
        for i in range((2**self.M)-2):
            modulopoly += '0'
        modulopoly += '1'
        self.modulo = Polynome(modulopoly)
        
        if len(msg) == 4:
            self.generator = Polynome('1101')
        elif len(msg) == 11:
            self.generator = Polynome('11001')
        elif len(msg == 26):
            self.generator = Polynome('101001')
            
        Qt, Rs = Polynome.divpol(self.modulo, self.generator)
        
        if not(1 in Rs.coeff):
            print("ça roule")
        self.check = Qt
        
        '''
        GenFound = False
        count = 0
        while not(GenFound):
            count += 1
            countbis = count
            q = -1 
            res = '' 
            while q != 0: 
                q = countbis // 2 
                r = countbis % 2 
                res = res + str(r)
                countbis = q
            while len(res) != self.M:
                res += '0'
            res += '1'
                
            testpol = Polynome(res)
            q1, r1 = Polynome.divpol(self.modulo, testpol)
            q2, r2 = Polynome.divpol(Polynome(msg), testpol)
            
            if (not(1 in r1.coeff) and not(1 in r2.coeff)):
                print( '\ncount :', count, '| res :', res)
                GenFound = True
                self.generator = testpol
                self.check = q1
       ''' 
        
        
if __name__ == '__main__':
    
    can_begin = False
    while(not(can_begin)):
        entry =  input('Enter some binary message of length 4, 11 or 26 : ')
        if len(entry) in [4, 11, 26]:
            can_begin = True
        else: print('Try again...')
    
    Hamming = CyclicCode(entry)
    
    '''
    print(Hamming.generator.coeff)
    print(Hamming.check.coeff)
    print(Hamming.modulo.coeff)
    '''
    
    codedpol = Hamming.encode(entry)
    codedmsg = Hamming.pol_into_msg(codedpol)
    print('Coded message : ' + codedmsg )
    
    msgcorrupt = Hamming.put_error(codedmsg)
    print('Corrupted message : ' + msgcorrupt)
    
    correctedpol = Hamming.correct(msgcorrupt)
    correctedmsg = Hamming.pol_into_msg(correctedpol)
    print('Corrected message : ' + correctedmsg )
    
    decodedpol, r = Hamming.decode(correctedmsg)
    decodedmsg = Hamming.pol_into_msg(decodedpol)[:(2**Hamming.M)-1-Hamming.M]
    print('Decoded message :' + decodedmsg)
    print('We found the right message :', decodedmsg == entry)
    
