#!/bin/bash
# runs the scripts needed to give the bone internet

NAME=wlp0s20f3

./ipMasqueradeAI.sh $NAME
./firstsshAI.sh
