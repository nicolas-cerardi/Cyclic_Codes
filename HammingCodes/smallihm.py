# -*- coding: utf-8 -*-
"""
smallihm.py
Created on Fri Sep 14 20:25:51 2018

@author: 16Aghnar
"""
from Coder import Coder, bitflip

AUTO_SETUP = dict(m=3,
                  q=2,
                  polynoms_index=0)

STATES = ['INIT',
          'HAS_CONFIG'
          'HAS_WORD_TO_CODE',
          'HAS_CODED',
          'HAS_NOISED',
          'FINAL']

def is_batch(obj):
    if isinstance(obj, str):
        return False
    elif isinstance(obj, list):
        return True
    else:
        raise TypeError('obj should be string or list of string')
        
def tryencode(code, msg):
    if not is_batch(msg):
        return code.encode(msg)
    else:
        return [code.encode(elt) for elt in msg]
    
def trybitflip(code, msg, howmany=1):
    if not is_batch(msg):
        return bitflip(msg, howmany=howmany, q=code._q)
    else:
        return [bitflip(elt, howmany=howmany, q=code._q) for elt in msg]

def trydecode(code, msg):
    if not is_batch(msg):
        return code.decode(msg)
    else:
        return [code.decode(elt) for elt in msg]
    
def config():
    CONFIGURATION_METHOD = ["manual", "auto"]
    while True:
        configmethod = input("How do you want to configure this session? (manual/auto): ").lower()
        if not configmethod in CONFIGURATION_METHOD:
            print("Invalid Input !")
        else:
            break
    if configmethod == "auto":
        return Coder(AUTO_SETUP['m'],
                     AUTO_SETUP['q'],
                     AUTO_SETUP['polynoms_index'])
    else:
        m = int(input("Give the parameter m = n - k (m integer below 6):"))
        q = int(input("Give the parameter q, cardinal of the finitefield:"))
        polynoms_index = int(input("Give index of the generator polynomial you want to use (see list in the json file):"))
        return Coder(m,q,polynoms_index)

def get_word_to_code(code):
    do_batch = input("Perform operations on a batch of words (y/n)? ")
    if do_batch.lower() == "n":
        word = input("give word to manipulate (no spaces, no points) :")
        if len(word) != code._k :
                raise ValueError("please enter word of length {}".format(code._k))
        return word
    elif do_batch.lower() == "y":
        batch = []
        while True:
            word = input("Give word to manipulate (no spaces, no points) OR n to finish batch :")
            if word.lower() == "n":
                break
            if len(word) != code._k :
                raise ValueError("please enter word of length {}".format(code._k))
            batch.append(word)
        return batch
    else:
        raise ValueError("should not come here")
        
def end_session():
    YES_NO = ["y", "n"]
    while True:
        again = input("Do you wanna perform another session? (y/n): ").lower()
        if not again in YES_NO:
            print("Invalid Input !")
        else :
            break
    return again

def makeresume(words):
    result = ["FAILURE","SUCCESS"]
    arr = " --> "
    if isinstance(words[0], list):
        failnb = 0
        if words[2] is not None:
            print(" ----  Resumé of a batched session with bitflip(s)  ---- ")
            for i in range(len(words[0])):
                if not (words[0][i] == words[3][i]):
                    failnb += 1
                opline = words[0][i] + arr + words[1][i] + arr + words[2][i] + arr + words[3][i]
                print(opline + " | " + result[words[0][i] == words[3][i]])
            accuracy = "Accuracy : " + str((1 - failnb/len(words[0]))*100)
            print(str(failnb) + " failures for " + str(len(words[0])) + "words." + accuracy)
        else :
            print(" --  Resumé of a batched session without bitflip  -- ")
            for i in range(len(words[0])):
                if not (words[0][i] == words[3][i]):
                    failnb += 1
                opline = words[0][i] + arr + words[1][i] + arr + words[3][i]
                print(opline + " | " + result[words[0][i] == words[3][i]])
            accuracy = "Accuracy : " + str((1 - failnb/len(words[0]))*100)
            print(str(failnb) + " failures for " + str(len(words[0])) + " words." + accuracy)
    else :
        if words[2] is not None:
            print(" ----  Resumé of a simple session with bitflip(s)  ---- ")
            opline = words[0] + arr + words[1] + arr + words[2] + arr + words[3]
            print(opline + " | " + result[words[0] == words[3]])
        else :
            print(" --  Resumé of a simple session without bitflip  -- ")
            opline = words[0] + arr + words[1] + arr + words[3]
            print(opline + " | " + result[words[0] == words[3]])
    

def next_state(action, currentcode, words):
    if action.lower() == 'config':
        currentcode = config()
        words = [None, None, None, None]
        return 'HAS_CONFIG', currentcode, words
    if action.lower() == 'getword':
        data = get_word_to_code(currentcode)
        words = [data, None, None, None]
        return 'HAS_WORD_TO_CODE', currentcode, words
    if action.lower() == 'encode':
        words[1] = tryencode(currentcode, words[0])
        return 'HAS_CODED', currentcode, words
    if action.lower() == 'bitflip':
        howmany = int(input('Howmany stochastic bitflips ?'))
        words[2] = trybitflip(currentcode, words[1], howmany=howmany)
        return 'HAS_NOISED', currentcode, words
    if action.lower() == 'decode':
        if words[2] is not None:
            words[3] = trydecode(currentcode, words[2])
        else:
            words[3] = trydecode(currentcode, words[1])
        makeresume(words)
        return 'FINAL', currentcode, words
    if action.lower() == 'anothersess':
        return 'INIT', None, None
    if action.lower() == 'end':
        return None, None, None
    raise ValueError("Should not come here")
    
def next_action(state):
    if state == 'INIT':
        return 'config'
    if state == 'HAS_CONFIG':
        return 'getword'
    if state == 'HAS_WORD_TO_CODE':
        return 'encode'
    if state == 'HAS_CODED':
        action = input("select next action : bitflip or decode?")
        if not action in ['bitflip', 'decode']:
            raise ValueError("action not understood !")
        return action
    if state == 'HAS_NOISED':
        return 'decode'
    if state == 'FINAL':
        again = end_session()
        if again == 'y':
            return 'anothersess'
        else :
            return 'end'
    raise ValueError("Should not come here")
    
def mainloop():
    state = 'INIT'
    currentcode, words = None, None
    
    while True:
        action = next_action(state)
        state, currentcode, words = next_state(action, currentcode, words)
        if state is None:
            break

    print("Out of the main loop. Thanks for coming !")
    
    
if __name__=='__main__':
    ### MAIN LOOP ###
    mainloop()
    
    
    
