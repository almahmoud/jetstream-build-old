#!/bin/bash

mkdir -p lists
touch lists/todo

while [ -s lists/todo ]; do
    git config --local user.email "action@github.com"
	git config --local user.name "GitHub Action"
	git commit -m "Periodic commit" || true
    git add packages.json || true
    git add lists || true
	git push || true
	sleep 300
done

