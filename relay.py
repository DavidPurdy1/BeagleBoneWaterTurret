#!/usr/bin/env python3

import os
import time

# Test script for relay to work
relay_pin = '59'

relay_fire_cmd = 'gpioset 1 ' + relay_pin + '=1'
relay_stop_fire_cmd = 'gpioset 1 ' + relay_pin + '=0'

print("starting firing...")
os.system(relay_fire_cmd)

time.sleep(3)

print("stopping firing...")
os.system(relay_stop_fire_cmd)

