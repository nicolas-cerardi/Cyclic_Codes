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

def mkstats1_1(lambdas, errfunc=dist_h, paramcoder=(3,2)):
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

def mkstats1_2():
    res_dh_m3 = mkstats1_1(lambdas)
    res_ts_m3 = mkstats1_1(lambdas, errfunc=transmission_score)
    res_dh_m3 = res_dh_m3 / np.max(res_dh_m3)
    res_ts_m3 = res_ts_m3 / np.max(res_ts_m3)
    
    res_dh_m4 = mkstats1_1(lambdas, paramcoder=(4,2))
    res_ts_m4 = mkstats1_1(lambdas, errfunc=transmission_score, paramcoder=(4,2))
    res_dh_m4 = res_dh_m4 / np.max(res_dh_m4)
    res_ts_m4 = res_ts_m4 / np.max(res_ts_m4)
    
    res_dh_m5 = mkstats1_1(lambdas, paramcoder=(5,2))
    res_ts_m5 = mkstats1_1(lambdas, errfunc=transmission_score, paramcoder=(5,2))
    res_dh_m5 = res_dh_m5 / np.max(res_dh_m5)
    res_ts_m5 = res_ts_m5 / np.max(res_ts_m5)
    
    fig, axarr = plt.subplots(1,3)

    axarr[0].plot(lambdas, res_dh_m3, 'b')
    axarr[0].plot(lambdas, res_ts_m3, 'r')
    axarr[0].grid(linestyle='--')
    
    axarr[1].plot(lambdas, res_dh_m4, 'b')
    axarr[1].plot(lambdas, res_ts_m4, 'r')
    axarr[1].grid(linestyle='--')
    
    axarr[2].plot(lambdas, res_dh_m5, 'b')
    axarr[2].plot(lambdas, res_ts_m5, 'r')
    axarr[2].grid(linestyle='--')
    
    #plt.plot(hyplambdas, mkstats(hyplambdas), 'r')
    plt.show()
    
def mkstats2(paramcoders=[(3,2), (4,2), (5,2), (6,2), (7,2), (8,2) ], NB_TIMES=10):
    res = np.zeros((len(paramcoders)))
    for i, parcod in enumerate(paramcoders):
          
        crt_code = Coder(parcod[0], parcod[1], 0)
        
        inittime = time()
        for j in range(NB_TIMES):
            crt_dh = DataHandler(testtext, crt_code, lenbinarychar = 7)
            crt_dh.downgradelevel()
            crt_dh.downgradelevel()
            crt_dh.ATTACK(param=0.99)
            crt_dh.upgradelevel()
            crt_dh.upgradelevel()
            
        res[i] = (time() - inittime) / NB_TIMES
        
    plt.plot(res)
    plt.show()
    return res

        
    
    

if __name__ == '__main__' :
    mkstats2()
    
    