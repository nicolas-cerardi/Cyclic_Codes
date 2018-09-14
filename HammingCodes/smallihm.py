# -*- coding: utf-8 -*-
"""
smallihm.py
Created on Fri Sep 14 20:25:51 2018

@author: 16Aghnar
"""
from Coder import Coder, bitflip

CONFIGURATION_METHOD = ["manual", "auto"]
YES_NO = ["y", "n"]

AUTO_SETUP = dict()

### MAIN LOOP ###
while True:
    while True:
        configmethod = input("How do you want to configure this session? (manual/auto): ").lower()
        if not configmethod in CONFIGURATION_METHOD:
            print("Invalid Input !")
        else:
            break
    
    while True:
        again = input("Do you wanna do another session? (y/n): ").lower()
        if not again in YES_NO:
            print("Invalid Input !")
        else :
            break
    if again == "n":
        break

print("Out of the main loop. Thanks for coming !")


