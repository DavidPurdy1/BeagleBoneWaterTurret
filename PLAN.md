# Plan

1. Get stepper motor working first, have it rotate the plate. (We need some kind of connector for it) Stepper motor isn't going to follow the person at all, just kinda go on it's own 

Chip 1, line 89 for P8_13
Chip 1, line 75 for P8_14
Chip 1, line 61 for P8_15
Chip 1, line 62 for P8_16

set the pin P8_13 high using `gpioset 1 89=1`

2. Servo next, get that setup 
3. Relay, test using led, we don't water yet.
4. Write camera data to the servo arm.
5. Housing once we are getting some data. Get that setup. Might cut acryllic not for sure yet. 
6. Make sure that we can ssh into bone so we can start the script remotely. 
7. Water time. 
