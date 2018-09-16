# -*- coding: utf-8 -*-
"""
util.py
Created on Sun Sep 16 14:36:41 2018
16Aghnar
"""
from FFPoly import pol_to_string
from hcodebuilder import int_to_pol

def int_to_FF(I, length, q):
    res = pol_to_string(int_to_pol(I, q), q)
    while len(res) < length:
        res += "0"
    return res

def FF_to_int(word, q):
    res = 0
    scale = 1
    for i in range(len(word)):
        res += scale*int(word[i])
        scale *= q
    return res

if __name__=="__main__":
    initial = 26
    q = 3
    print(initial)
    msg = int_to_FF(initial,10,q)
    print(msg)
    re_int = FF_to_int(msg, q)
    print(re_int)