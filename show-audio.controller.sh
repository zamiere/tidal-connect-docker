#!/bin/bash

echo "Shows Audio Controller UI started within a running Tidal Container"
docker exec -ti tidal_connect /usr/bin/tmux a -t speaker_controller_application
