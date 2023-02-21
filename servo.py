#!/usr/bin/env python3

import os
import time

servo_pwm_chip='0'
servo_pwm_pin='0'

path = '/sys/class/pwm/pwmchip' + servo_pwm_chip + '/pwm' + servo_pwm_pin + '/'
print(path)

duty_min = 500000
duty_max = 2500000 
duty_range = duty_max - duty_min

def init_pwm():
    enable_cmd = "echo 1 > " +  path + 'enable'
    print(enable_cmd)
    os.system(enable_cmd)

    period_cmd = "echo 20000000 > " + path + 'period'
    print(period_cmd)
    os.system(period_cmd)

def set_duty(duty):
    print(duty)
    os.system("echo " + duty + ' > ' +  path + 'duty_cycle')

def set_angle(angle):
    print(angle)
    duty_cycle = duty_min + (duty_range * angle / 180)
    duty_cycle = int(duty_cycle)
    set_duty(str(duty_cycle))

init_pwm()
while True:
    for i in [0, 45, 90, 135, 180]:
        set_angle(i)
        time.sleep(1)
