#!/bin/bash

while true; do
	python update_lists.py -j packages.json -t lists/todo -d lists/done -r lists/removed -f lists/failed -s lists/skipped
	sleep 15;
done

