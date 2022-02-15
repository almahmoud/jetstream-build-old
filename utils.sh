#cleanup all jobs

kubectl get jobs -n newbuild --no-headers -o custom-columns=":metadata.name" | xargs kubectl delete -n newbuild job

# cleanup completed
kubectl get jobs -n newbuild --no-headers | grep 1/1 | awk '{print $1}' | xargs kubectl delete -n newbuild job


# All done PACKAGE NAMES
kubectl get jobs -n newbuild --no-headers | grep 1/1 | awk '{print $1}' | xargs kubectl get -n newbuild --no-headers -o custom-columns=":spec.template.spec.containers[0].args" job | awk -F'"' '{print $2}' > lists/done