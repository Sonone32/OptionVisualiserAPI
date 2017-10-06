#!/bin/bash
# Put this in crontab with trigger @reboot
SESSION_NAME=$1
REDISPATH=$2 # Path to the folder containing Redis, assuming config file is in that folder directly
VIRTUALENV_ACTIVATE=$3
PYTHON_APP=$4
tmux new -d -s redis && \
    tmux send-keys -t redis "$REDISPATH/src/redis-server $REDISPATH/redis.conf" C-m && \
    tmux new -d -s $SESSION_NAME && \
    tmux send-keys -t $SESSION_NAME ". $VIRTUALENV_ACTIVATE && python3 $PYTHON_APP" C-m
