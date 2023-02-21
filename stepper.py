#!/usr/bin/env python3 

# Pins are P8_13, P8_14, P8_15, P8_16

import os
import time

A1_PIN = '89'
A2_PIN = '75'
B1_PIN = '61'
B2_PIN = '62'

seq = [[1,0,0,1], [1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0],[0,0,1,1], [0,0,0,1]]

delay = 0.01
steps = 100
step_count = 0

while step_count < steps:
    for i in range(8):
        os.system("gpioset 1 " + A1_PIN + "=" + str(seq[i][0]))
        os.system("gpioset 1 " + A2_PIN + "=" + str(seq[i][1]))
        os.system("gpioset 1 " + B1_PIN + "=" + str(seq[i][2]))
        os.system("gpioset 1 " + B2_PIN + "=" + str(seq[i][3]))
        time.sleep(delay)
    step_count += 1

# Turn off
os.system("gpioset 1 " + A1_PIN + "=0" )
os.system("gpioset 1 " + A2_PIN + "=0" )
os.system("gpioset 1 " + B1_PIN + "=0" )
os.system("gpioset 1 " + B2_PIN + "=0" )
