#!/bin/bash

# init
# start
# download

if [ $ARGUMENT ]; then
    BASENAME=$(basename "$ARGUMENT")
    echo "$ACTION" >> "/home/stephen/stephenskywatcher/hook.log"
    echo "$BASENAME" >> "/home/stephen/stephenskywatcher/hook.log"
    # if [[ $ARGUMENT =~ .+\.[jpg|JPG] ]]
fi
