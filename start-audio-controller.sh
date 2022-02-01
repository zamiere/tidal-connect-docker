#!/bin/bash

# Stop if already running
if pgrep -f ^/app/ifi-tidal-release/bin/speaker_controller_application >/dev/null 2>&1
then
  ./stop-audio-controller.sh
fi


echo "Starting Speaker Controller Application..."
docker exec -ti tidal_connect /usr/bin/tmux new-session -d -s speaker_controller_application '/app/ifi-tidal-release/bin/speaker_controller_application'

