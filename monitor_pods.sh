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
	echo "$(date) jobs running: $(($(kubectl get pods -n $namespace | grep "build" | grep -i running | wc -l)))"
	echo "$(date) jobs completed: $(($(kubectl get pods -n $namespace | grep "build" | grep -i completed | wc -l)))"
	echo "$(date) jobs failing: $(($(kubectl get pods -n $namespace | grep "build" | grep -i crash | wc -l)+$(kubectl get pods -n $namespace | grep "build" | grep -i error | wc -l)))"
	echo "$(date) jobs pending: $(($(kubectl get pods -n $namespace | grep "build" | grep -i pending | wc -l)))"
	sleep 5;
done