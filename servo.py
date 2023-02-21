#!/usr/bin/env python3

import os
import time

servo_pwm_chip=0
servo_pwm_pin=0

path = '/sys/class/pwm/pwmchip' + servo_pwm_chip + '/pwm' + servo_pwm_pin + '/'

def init_pwm():
    os.system("echo 1 > " +  path + 'enable')
    
    os.system("echo 2500 > " +  path + 'period')

def set_duty(duty):
    os.system("echo " + duty + ' > ' +  path + 'duty_cycle')

init_pwm()
set_duty(75)
