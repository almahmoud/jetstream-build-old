#!/bin/bash

bash dispatch_loop.sh -n $NAMESPACE -c $PVC &
sleep 5 && bash monitor_pods.sh -n $NAMESPACE &
sleep 60 && bash update_lists.sh &
sleep 60 && bash commit.sh &
sleep 30 && bash cleanup_loop.sh -n $NAMESPACE -c $PVC