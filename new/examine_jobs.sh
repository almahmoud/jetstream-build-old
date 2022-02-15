#!/bin/bash
while getopts "n:b:f:" flag
do
    case "${flag}" in
        n) namespace=${OPTARG};;
        b) built=${OPTARG};;
        f) failed=${OPTARG};;
    esac
done


if [ -z "$namespace" ];
    then echo "Needed: -n myinitials-mynamespace";
    exit;
fi

if [ -z "$built" ];
    then echo "Needed: -b built.list";
    exit;
fi


if [ -z "$failed" ];
    then echo "Needed: -f failed.list";
    exit;
fi

kubectl get jobs -n $namespace --no-headers | grep 1/1 | awk '{print \$1}' |\
    xargs kubectl get -n $namespace --no-headers -o custom-columns=':spec.template.spec.containers[0].args' job |\
    awk -F'\"' '{print \$2}' > $built &&\
    kubectl get jobs -n $namespace --no-headers | grep 1/1 | awk '{print \$1}' |\
    xargs kubectl delete -n $namespace job;

kubectl get jobs -n $namespace -o custom-columns=':metadata.name,:status.conditions[0].type' | grep Failed | awk '{print $1}' |\
    xargs kubectl get -n $namespace --no-headers -o custom-columns=':spec.template.spec.containers[0].args' job |\
    awk -F'\"' '{print \$2}' >> $failed &&\
    kubectl get jobs -n $namespace -o custom-columns=':metadata.name,:status.conditions[0].type' | grep Failed | awk '{print $1}' |\
    xargs kubectl delete -n $namespace job;
