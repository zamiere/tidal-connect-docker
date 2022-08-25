#!/bin/bash

AC_CONTROL_FILE="/opt/audiocontrol2/audiocontrol2.py"
DST_PLAYER_FILE=/opt/audiocontrol2/ac2/players/tidalcontrol.py
AC_UNIT_FILE="/etc/systemd/system/multi-user.target.wants/audiocontrol2.service"

rm -f "$DST_PLAYER_FILE"
ln -s "${PWD}/tidalcontrol.py" "$DST_PLAYER_FILE"

sed -i '/^from ac2\.players\.vollibrespot import MYNAME as SPOTIFYNAME$/a from ac2.players.tidalcontrol import TidalControl' "$AC_CONTROL_FILE"

PLACEHOLDER="$(sed -nE 's/^(.*)mpris\.register_nonmpris_player\(SPOTIFYNAME,vlrctl\)$/\1/p' "$AC_CONTROL_FILE")"
sed -i "/mpris.register_nonmpris_player(SPOTIFYNAME,vlrctl)/a \\\n${PLACEHOLDER}# TidalControl\n${PLACEHOLDER}tdctl = \
  TidalControl()\n${PLACEHOLDER}tdctl.start()\n${PLACEHOLDER}mpris.register_nonmpris_player(tdctl.playername,tdctl)" "$AC_CONTROL_FILE"

# Ensure that `audiocontrol2` is started after the TidalConnect container
sed -i 's/^After=.*$/After=sound.target dbus.service tidal.service/' "$AC_UNIT_FILE"
systemctl daemon-reload
systemctl restart audiocontrol2

echo "NOTE - THIS IS STILL WORK IN PROGRESS"
