# -*- coding: utf-8 -*-
"""
util.py
Created on Sun Sep 16 14:36:41 2018
16Aghnar
"""
from FFPoly import pol_to_string
from hcodebuilder import int_to_pol
import numpy as np

def int_to_FF(I, length, q):
    """
    int_to_FF function
    Args : a number in base 10
    Returns : the same number written in base q
    """
    res = pol_to_string(int_to_pol(I, q), q)
    while len(res) < length:
        res += "0"
    return res

def FF_to_int(word, q):
    """
    FF_to_int function
    Args : a number in base q
    Returns : the same number written in base 10
    """
    res = 0
    scale = 1
    for i in range(len(word)):
        res += scale*int(word[i])
        scale *= q
    return res

def dist_h(x, y):
    assert len(x) == len(y)
    res = 0
    for i in range(len(x)):
        if x[i] != y[i]:
            res += 1
    return res


def transmission_score(e,s):
    """
    transmission_score function
    Args : 
        e, entry string to be coded
        s, output string decoded
    returns :
        score, a real number representing dissimilarity between e and s
    """
    words = e.split(' ')
    
    nb_w = len(words)
    nb_w += (nb_w - 1)
    w_ers = []
    len_saw = 0
    # print(words, nb_w)
    for i in range(nb_w):
        # print(len_saw)
        if i % 2 == 0:
            #a non-space word.
            w_ind = i//2
            e_w = words[w_ind]
            if len(e_w)>0:
                e_s = s[len_saw:len_saw + len(e_w)]
                w_score = dist_h(e_w, e_s) / len(e_w)
                if len(e_w) == 1 :
                    w_score *= 0.3
                len_saw += len(e_w)
            else:
                #it's an empty word !
                pass
        else:
            #a space word
            e_w = ' '
            e_s = s[len_saw]
            w_score = dist_h(e_w, e_s) / 1
            len_saw += 1
        w_ers.append(w_score)
    score = sum(w_ers) / nb_w
    return np.exp(2 * score) - 1

if __name__=="__main__":
    """
    initial = 26
    q = 3
    print(initial)
    msg = int_to_FF(initial,10,q)
    print(msg)
    re_int = FF_to_int(msg, q)
    print(re_int)
    """

    seq1 = "Hello world !"
    seq2 = "Hellà world !"
    seq3 = "Heluo worldm."
    print(dist_h(seq1, seq1))
    print(transmission_score(seq1,seq1))
    print(transmission_score(seq1,seq2))
    print(transmission_score(seq1,seq3))