#!/bin/usr/python3
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("-w", "--worker-nodes", dest="workers",
                    help="""List of worker node names in format: -w '"node1","node2"')"""

args = parser.parse_args()

def create_build_job():
    print("yes")