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


function dispatch_job {
    if [ ! -f "manifests/$pkg/$pkg.yaml" ]
    then
        mkdir -p "manifests/$pkg"
        python dispatch_build_job.py -p $pkg -n $namespace -c $claim -m "manifests/$pkg" -w "$(kubectl get nodes | grep $(kubectl get nodes | grep etcd | awk '{print $1}')- | awk '{print "\""$1"\""}' | paste -sd, -)"
        echo "Dispatched pkg: $pkg"
    fi
}

#Rscript deps_json.R packages.json
mkdir -p lists
touch lists/todo
touch lists/done
touch lists/removed
touch lists/failed
touch lists/skipped

python update_lists.py -j packages.json -t lists/todo -d lists/done -r lists/removed -f lists/failed -s lists/skipped

while true; do
    grep -v "^$" lists/todo > lists/tmpdsplooptodo;
    while IFS= read -r pkg; do
        dispatch_job
    done < lists/tmpdsplooptodo

    rm lists/tmpdsplooptodo
done
