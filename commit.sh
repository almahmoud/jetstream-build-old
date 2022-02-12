#!/bin/bash
set -e

mkdir -p lists
touch lists/todo

while [ -s lists/todo ]; do
	git config --local user.email "action@github.com"
	git config --local user.name "GitHub Action"
	git add .
	git commit -m "Periodic commit"
	git push
	sleep 300
done

