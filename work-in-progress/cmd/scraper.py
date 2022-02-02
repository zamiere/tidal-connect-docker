#!/bin/python

import os
import subprocess

cmd='docker exec -ti tidal_connect /usr/bin/tmux capture-pane -pS -10'

stdout = subprocess.check_output(cmd.split());

WINDOW_SIZE=40
WINDOW_COUNT=2

VALUE_MAP = {}


for line in stdout.decode('utf-8').splitlines():
  #print(line+'|')
  # parse status
  if line.startswith('PlaybackState::'):
     VALUE_MAP['playback_state']=line.split('::')[1]
  # parse props
  if line.startswith('xx',WINDOW_SIZE-1):
    for window_cnt in range(WINDOW_COUNT):
      str_keyvals = (line[(WINDOW_SIZE*window_cnt)+1:(WINDOW_SIZE*(window_cnt+1))-1].strip())
      #print(str_keyvals)

      ar_props = str_keyvals.split(':')
      if len(ar_props)>1:
        key=(ar_props[0].replace(' ','_'));
        value=''.join(ar_props[1:]).strip()
        sess_state_prefix='SessionState'
        if value.startswith(sess_state_prefix):
           value = value[len(sess_state_prefix):] 
        VALUE_MAP[key]=value
  # parse volume
  if line.endswith('#k'):
    value = line.strip()
    VALUE_MAP["volume"]=value.count("#")
print(VALUE_MAP)
