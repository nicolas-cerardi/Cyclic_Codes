# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:46:33 2018

@author: Sony
"""

import numpy as np
from Coder import Coder, DataHandler
import matplotlib.pyplot as plt
from util import transmission_score, dist_h
from time import time

NB_TEST = 20
NB_LAMBDA = 50
testtext = "Non mais moi, ces histoires de nord et de sud, j'aime pas trop ! Selon comment on est tournés, ça change tout !"

def hypscale(arr, a=1.04, b=-1/20, c=-0.1):
    arrcop = np.reshape(arr, (-1, 1))
    res = np.zeros(arr.shape)
    for i, val in enumerate(arrcop):
        
        res[i] = a + b / (val - c)
    #print(res)
    
    return res

paramcoder = [(3,2)]
lambdas = np.linspace(0,1,NB_LAMBDA)
hyplambdas = hypscale(lambdas)
lambdas = np.linspace(0.5, 0.999, NB_LAMBDA)

def mkstats(lambdas, errfunc=dist_h):
    inittime = time()  
    crt_code = Coder(paramcoder[0][0], paramcoder[0][1], 0)
    res = np.zeros((NB_LAMBDA))
    for i in range(NB_LAMBDA):  
        crt_res = 0
        print("\r{}/{}".format(i, NB_LAMBDA), end=" ", flush=True)
        
        for j in range(NB_TEST):
            crt_dh = DataHandler(testtext, crt_code, lenbinarychar = 7)
            crt_dh.downgradelevel()
            crt_dh.downgradelevel()
            crt_dh.ATTACK(param=lambdas[i])
            crt_dh.upgradelevel()
            crt_dh.upgradelevel()
            crt_res += errfunc(testtext, crt_dh.data)
        crt_res /= NB_TEST
        res[i] = crt_res
    print('Time : {} s'.format(time() - inittime))
    return res

if __name__ == '__main__' :
    fig, axarr = plt.subplots(2,1)

    axarr[0].plot(lambdas, mkstats(lambdas), 'b')
    axarr[1].plot(lambdas, mkstats(lambdas, errfunc=transmission_score), 'r')
    axarr[0].grid(linestyle='--')
    axarr[1].grid(linestyle='--')
    #plt.plot(hyplambdas, mkstats(hyplambdas), 'r')
    plt.show()