#cleanup all jobs

kubectl get jobs -n testbuild --no-headers -o custom-columns=":metadata.name" | xargs kubectl delete -n testbuild job

# cleanup completed
kubectl get jobs -n testbuild --no-headers | grep 1/1 | awk '{print $1}' | xargs kubectl delete -n testbuild job