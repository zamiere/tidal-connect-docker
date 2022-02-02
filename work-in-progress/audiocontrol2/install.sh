#!/bin/bash

DST_PLAYER_FILE=/opt/audiocontrol2/ac2/players/tidalcontrol.py

rm ${DST_PLAYER_FILE}
ln -s ${PWD}/tidalcontrol.py ${DST_PLAYER_FILE}

echo "NOTE - THIS IS STILL WORK IN PROGRESS"
echo ""
echo "You will need to manually setup /opt/audiocontrol2/audiocontrol2.py"
