#!/bin/bash

mkdir -p lists
touch lists/todo

git config --local user.email "action@github.com"
git config --local user.name "GitHub Action"

while true; do
    git commit -m "Periodic commit" || true
    git add packages.json || true
    git add lists || true
    git add manifests || true
    git push || true
    sleep 300
done

