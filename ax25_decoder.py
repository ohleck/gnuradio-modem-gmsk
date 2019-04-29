#!/usr/bin/python2.7
import socket, argparse, datetime, sys

# Purpose: decodes an AX.25 packet from an input of hexa values (ascii encoded) from the standard input. 
# Suitable for using piped from other modules output. Ex: source.bin | ax25_decoder.py  or  echo "FEAABB" | ax25_decoder.py 


import sys
import time


while True:
    inBuffer1 = sys.stdin.read(1)
    inBuffer2 = sys.stdin.read(1)


byte 

    print "Just read:", inBuffer
