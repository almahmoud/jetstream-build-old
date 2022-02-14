#!/bin/bash

bash -c "bash dispatch_loop.sh -n $NAMESPACE -c $PVC &
sleep 5 && bash monitor_pods.sh -n $NAMESPACE &
sleep 30 && bash cleanup_loop.sh -n $NAMESPACE -c $PVC &
sleep 60 && bash commit.sh &
sleep 60 && bash update_lists.sh"