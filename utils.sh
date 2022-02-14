#cleanup all jobs

kubectl get jobs -n testbuild --no-headers -o custom-columns=":metadata.name" | xargs kubectl delete -n testbuild job