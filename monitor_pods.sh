#!/bin/bash

while [ -s lists/todo ]; do
	echo "$(date) successful jobs running: $(($(kubectl get pods -n testbuild | grep "build" | grep -i completed | wc -l)))"
	echo "$(date) successful jobs waiting cleanup: $(($(kubectl get pods -n testbuild | grep "build" | grep -i completed | wc -l)))"
	echo "$(date) failing jobs: $(($(kubectl get pods -n testbuild | grep "build" | grep -i crash | wc -l)+$(kubectl get pods -n testbuild | grep "build" | grep -i error | wc -l)))"
	sleep 5;
done