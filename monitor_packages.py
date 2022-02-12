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
if os.path.exists(args.donefile):
    os.rename(args.donefile, 'tmpdone.txt')
    with open('tmpdone.txt', 'r') as f:
        done = f.read().splitlines()
    os.remove('tmpdone.txt')
    with open(args.removedfile, 'a+') as f:
        f.writelines("\n".join(done) + "\n")

print(f'original %d' % len(deps))

while(len(deps) > 0):
    print("in")
    todo = []
    oldtodo = []
    if os.path.exists(args.todofile):
        with open(args.todofile, 'r') as f:
            oldtodo = f.read().splitlines()
    newdeps = {}
    for pkg in deps.keys():
        for each in done:
            if each in deps[pkg]:
                deps[pkg].remove(each)
        if len(deps[pkg]) == 0:
            if pkg not in oldtodo:
                todo.append(pkg)
        else:
            newdeps[pkg] = deps[pkg]

    with open(args.inputjson, 'w') as f:
        f.writelines(json.dumps(newdeps, indent=4))
    if todo:
        roundcount += 1
        print(roundcount)
        print(f'len %d' % len(newdeps))
        with open(args.todofile, 'a+') as f:
            f.write("\n".join(todo) + "\n")
    while not os.path.exists(args.donefile):
        time.sleep(10)
    deps = newdeps
    done = []
    os.rename(args.donefile, 'tmpdone.txt')
    with open('tmpdone.txt', 'r') as f:
        done = f.read().splitlines()
    os.remove('tmpdone.txt')
    with open(args.removedfile, 'a+') as f:
        f.writelines("\n".join(done) + "\n")
    print("out")
