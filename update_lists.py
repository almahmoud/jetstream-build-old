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
                    help="File listing packages already built and removed")
parser.add_argument("-f", "--failed-file", dest="failedfile",
                    help="File listing packages that failed building")
parser.add_argument("-s", "--skipped-file", dest="skippedfile",
                    help="File listing packages skipped due to dependencies failing")


args = parser.parse_args()

roundcount = 0


with open(args.inputjson, 'r') as f:
    deps = json.load(f)
done = []
failed = []
skipped = []
if os.path.exists(args.donefile):
    os.rename(args.donefile, 'tmpdone.txt')
    with open('tmpdone.txt', 'r') as f:
        done = f.read().splitlines()
    os.remove('tmpdone.txt')
    with open(args.removedfile, 'a+') as f:
        f.writelines("\n".join(done) + "\n")

if os.path.exists(args.failedfile):
    os.rename(args.failedfile, 'tmpfailed.txt')
    with open('tmpfailed.txt', 'r') as f:
        failed = f.read().splitlines()
    os.remove('tmpfailed.txt')
    with open(args.removedfile, 'a+') as f:
        f.writelines("\n".join(failed) + "\n")

if os.path.exists(args.skippedfile):
    os.rename(args.skippedfile, 'tmpskipped.txt')
    with open('tmpskipped.txt', 'r') as f:
        skipped = f.read().splitlines()
    os.remove('tmpskipped.txt')
    with open(args.removedfile, 'a+') as f:
        f.writelines("\n".join(skipped) + "\n")

print(f'original %d' % len(deps))

todo = []
oldtodo = []
skipped = []
newskipped = []

if os.path.exists(args.todofile):
    with open(args.todofile, 'r') as f:
        oldtodo = f.read().splitlines()
newdeps = {}
for pkg in deps.keys():
    for each in done:
        if each in oldtodo:
            oldtodo.remove(each)
        if each in deps[pkg]:
            deps[pkg].remove(each)
    if len(deps[pkg]) == 0:
        if pkg not in oldtodo:
            todo.append(pkg)
    else:
        skip = False
        for each in failed + skipped:
            if each in oldtodo:
                oldtodo.remove(each)
            if each in deps[pkg]:
                newskipped.append(pkg)
                skip = True
        if not skip:
            newdeps[pkg] = deps[pkg]

while newskipped:
    with open(args.removedfile, 'a+') as f:
        f.writelines("\n".join(newskipped) + "\n")
    deps = newdeps
    newdeps = {}
    skipped = newskipped
    newskipped = []
    for pkg in deps.keys():
        for each in skipped:
            if each in oldtodo:
                oldtodo.remove(each)
            if each in deps[pkg]:
                newskipped.append(pkg)
                skip = True
        if not skip:
            newdeps[pkg] = deps[pkg]

with open(args.inputjson, 'w') as f:
    f.writelines(json.dumps(newdeps, indent=4))
if todo:
    print(f'len %d' % len(newdeps))
    with open(args.todofile, 'w') as f:
        f.write("\n".join(oldtodo+todo) + "\n")

