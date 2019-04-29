#!/usr/bin/python2.7
import socket, argparse, datetime, sys

# Purpose: decodes an AX.25 packet from an input of hexa values (ascii encoded) from the standard input. 
# Suitable for using piped from other modules output. Ex: source.bin | ax25_decoder.py  or  echo "FEAABB" | ax25_decoder.py 


import sys
import time


while True:
    inBuffer = sys.stdin.read(2)

    print "Just read:", inBuffer
    