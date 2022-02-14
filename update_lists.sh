#!/bin/bash
while getopts "n:c:" flag
do
    case "${flag}" in
        n) namespace=${OPTARG};;
        c) claim=${OPTARG};;
    esac
done


if [ -z "$namespace" ];
    then echo "A namespace must be specific with eg: -n myinitials-mynamespace";
    exit;
fi


if [ -z "$claim" ];
    then echo "A persistent volume claim for persisting R libraries must be specific with eg: -c bioconductor-pvc";
    exit;
fi

while [ -s lists/todo ]; do
    python check_job_status.py -p $pkg -n $namespace -s manifests/$pkg/status -l manifests/$pkg/log
done

