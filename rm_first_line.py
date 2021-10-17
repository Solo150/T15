#!/bin/python3
import sys

with open(sys.argv[1] + '_domens.txt', 'r') as domens:
	domens = domens.readlines()

with open(sys.argv[1] + '_domens.txt', 'w') as domens_w:
	domens_w.writelines(domens[1:])
