#!/bin/bash
BONE=${1:-192.168.6.2}
USER=debian
./setDNSAI.sh $BONE
# ./setDate.sh $BONE
ssh -X $USER@$BONE
