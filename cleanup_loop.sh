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
    if [ -f "manifests/$pkg/$pkg.yaml" ]
    then
        echo "Checking pkg: $pkg"
        python check_job_status.py -p $pkg -n $namespace -s manifests/$pkg/status -l manifests/$pkg/log
        grep -ir "built" manifests/$pkg | awk -F'/' '{print $2}' >> lists/done;
        grep -ir "failedbuild" manifests/$pkg | awk -F'/' '{print $2}' >> lists/failed;
    fi
}

#Rscript deps_json.R packages.json
mkdir -p lists
touch lists/todo
touch lists/done
touch lists/removed
touch lists/failed
touch lists/skipped


while (( $(kubectl get jobs -n testbuild | grep 'build' | wc -l) > 0 )); do
    grep -v "^$" lists/todo > lists/tmpclnlptodocleanup
    while IFS= read -r pkg; do
        dispatch_job
    done < lists/tmpclnlptodocleanup
    rm lists/tmpclnlptodocleanup
done
