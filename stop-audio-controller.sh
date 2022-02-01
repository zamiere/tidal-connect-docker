#!/bin/bash

echo "Stopping Speaker Controller Application..."
docker exec -ti tidal_connect /usr/bin/tmux kill-session -t speaker_controller_application

