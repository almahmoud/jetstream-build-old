#!/bin/bash
while getopts "n:" flag
do
    case "${flag}" in
        n) namespace=${OPTARG};;
    esac
done


if [ -z "$namespace" ];
    then echo "A namespace must be specific with eg: -n myinitials-mynamespace";
    exit;
fi

while [ -s lists/todo ]; do
	echo "$(date) successful jobs running: $(($(kubectl get pods -n $namespace | grep "build" | grep -i running | wc -l)))"
	echo "$(date) successful jobs waiting cleanup: $(($(kubectl get pods -n $namespace | grep "build" | grep -i completed | wc -l)))"
	echo "$(date) failing jobs: $(($(kubectl get pods -n $namespace | grep "build" | grep -i crash | wc -l)+$(kubectl get pods -n $namespace | grep "build" | grep -i error | wc -l)))"
	sleep 5;
done