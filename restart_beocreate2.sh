#!/bin/bash

echo "Stopping Beocreate 2 Server"
systemctl stop beocreate2
echo "Starting Beocreate 2 Server"
systemctl start beocreate2
echo "Finished restarting Beocreate 2 Server."
