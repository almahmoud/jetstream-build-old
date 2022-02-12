#!/bin/usr/python3

from argparse import ArgumentParser
import json
import os
import time

parser = ArgumentParser()
parser.add_argument("-j", "--json-file", dest="inputjson",
                    help="Input JSON file")
parser.add_argument("-t", "--todo-file", dest="todofile",
                    help="File listing packages to build")
parser.add_argument("-d", "--done-file", dest="donefile",
                    help="File listing packages already built")
parser.add_argument("-r", "--removed-file", dest="removedfile",
                    help="File listing packages already built")


args = parser.parse_args()

roundcount = 0


with open(args.inputjson, 'r') as f:
    deps = json.load(f)
done = []
if os.path.exists(args.removedfile):
    with open(args.removedfile, 'r') as f:
        done = f.read().splitlines()
print(f'original %d' % len(deps))
ncount = 0 
count = 0
for each in deps.keys():
    if each not in done:
        print(each)
        ncount += 1
for each in done:
    if each not in deps.keys():
        print(each)
        count += 1
print(ncount)
print(count)