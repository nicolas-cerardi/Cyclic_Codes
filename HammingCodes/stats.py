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
NB_LAMBDA = 20
testtext = "Non mais moi, ces histoires de nord et de sud, j'aime pas trop ! Selon comment on est tournés, ça change tout !"

def hypscale(arr, a=1.04, b=-1/20, c=-0.1):
    arrcop = np.reshape(arr, (-1, 1))
    res = np.zeros(arr.shape)
    for i, val in enumerate(arrcop):
        
        res[i] = a + b / (val - c)
    #print(res)
    
    return res

lambdas = np.linspace(0,1,NB_LAMBDA)
hyplambdas = hypscale(lambdas)
lambdas = np.linspace(0.5, 0.999, NB_LAMBDA)

def mkstats(lambdas, errfunc=dist_h, paramcoder=(3,2)):
    inittime = time()  
    crt_code = Coder(paramcoder[0], paramcoder[1], 0)
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
    res_dh_m3 = mkstats(lambdas)
    res_ts_m3 = mkstats(lambdas, errfunc=transmission_score)
    res_dh_m3 = res_dh_m3 / np.max(res_dh_m3)
    res_ts_m3 = res_ts_m3 / np.max(res_ts_m3)
    
    res_dh_m4 = mkstats(lambdas, paramcoder=(4,2))
    res_ts_m4 = mkstats(lambdas, errfunc=transmission_score, paramcoder=(4,2))
    res_dh_m4 = res_dh_m4 / np.max(res_dh_m4)
    res_ts_m4 = res_ts_m4 / np.max(res_ts_m4)
    
    fig, axarr = plt.subplots(1,2)

    axarr[0].plot(lambdas, res_dh_m3, 'b')
    axarr[0].plot(lambdas, res_ts_m3, 'r')
    axarr[0].grid(linestyle='--')
    
    axarr[1].plot(lambdas, res_dh_m4, 'b')
    axarr[1].plot(lambdas, res_ts_m4, 'r')
    axarr[1].grid(linestyle='--')
    
    #plt.plot(hyplambdas, mkstats(hyplambdas), 'r')
    plt.show()