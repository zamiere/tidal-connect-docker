'''
Copyright (c) 2020 Modul 9/HiFiBerry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import logging
from pickle import TRUE

import threading
from threading import Timer
import subprocess

from ac2.helpers import map_attributes
from ac2.players import PlayerControl
from ac2.constants import CMD_NEXT, CMD_PREV, CMD_PAUSE, CMD_PLAYPAUSE, CMD_STOP, CMD_PLAY, CMD_SEEK, \
    CMD_RANDOM, CMD_NORANDOM, CMD_REPEAT_ALL, CMD_REPEAT_NONE, \
    STATE_PAUSED, STATE_PLAYING, STATE_STOPPED, STATE_UNDEF
from ac2.metadata import Metadata
   
TIDAL_STATE_PLAY="PLAYING"
TIDAL_STATE_PAUSE="PAUSED"
TIDAL_STATE_STOPPED="IDLE"
TIDAL_STATE_BUFFERING="BUFFERING"

TIDAL_ATTRIBUTE_MAP={
    "artist": "artist",
    "title": "title",
    "albumartist": "albumArtist",
    "album": "albumTitle",
    "disc": "discNumber",
    "track": "tracknumber", 
    "duration": "duration",
    "time": "time",
    "file": "streamUrl" 
    }

STATE_MAP={
    TIDAL_STATE_PAUSE: STATE_PAUSED,
    TIDAL_STATE_PLAY: STATE_PLAYING,
    TIDAL_STATE_STOPPED: STATE_STOPPED
}

class Timer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            self.function(*self.args, **self.kwargs)

        self.finished.set()
    

class TidalControl(PlayerControl):
    
    def __init__(self, args={}):
        self.client=None
        self.state=None
        self.meta=None

        self.playername="Tidal"
        if "port" in args:
            self.port=args["port"]
        else:
            self.port=6700
            
        if "host" in args:
            self.host=args["host"]
        else:
            self.host="localhost"
            
        if " timeout" in args:
            self.timeout=args["timeout"]
        else:
            self.timeout=5
        self.timeout=10
        self._timer = Timer(1.0, self.tmux_scraper)
        self._timer.interval=4.0
        self._timer.start()
        #self.connect()

        
    def start(self):
        logging.info('tidalcontrol::start')
        # No threading implemented
        pass
    
    
    def connect(self):
        logging.info('tidalcontrol::connect')
        '''
        if self. is not None:
            return self.client
        
        self.client = MPDClient()
        self.client.timeout = self.timeout
        try:
            self.client.connect(self.host, self.port)
            logging.info("Connected to %s:%s",self.host, self.port)
        except:
            self.client=None
        '''
        self.client=TRUE
        return TRUE
        
        
    def disconnect(self):
        logging.info('tidalcontrol::disconnect')
        '''
        if self.client is None:
            return
        
        try:
            self.client.close()
            self.client.disconnect()
        except:
            pass
        
        self.client=None
        '''
        self.client=None
        return TRUE
        
    def get_supported_commands(self):
        logging.info('tidalcontrol::get_supported_commands')
        return [CMD_NEXT, CMD_PREV, CMD_PAUSE, CMD_PLAYPAUSE, CMD_STOP, CMD_PLAY, CMD_SEEK,
                CMD_RANDOM, CMD_NORANDOM, CMD_REPEAT_ALL, CMD_REPEAT_NONE]   

    def tmux_scraper(self):
        logging.info('tidalcontrol::tmux_scraper')
        cmd='docker exec -t tidal_connect /usr/bin/tmux capture-pane -pS -10'
        stdout = subprocess.check_output(cmd.split());
        WINDOW_SIZE=40
        WINDOW_COUNT=2
        VALUE_MAP = {}

        for line in stdout.decode('utf-8').splitlines():
            if line.startswith('PlaybackState::'):
                VALUE_MAP['state']=line.split('::')[1]
            # parse props
            if line.startswith('xx',WINDOW_SIZE-1):
                for window_cnt in range(WINDOW_COUNT):
                    str_keyvals = (line[(WINDOW_SIZE*window_cnt)+1:(WINDOW_SIZE*(window_cnt+1))-1].strip())

                    ar_props = str_keyvals.split(':')
                    if len(ar_props)>1:
                        key=(ar_props[0].replace(' ','_'));
                        value=''.join(ar_props[1:]).strip()
                        sess_state_prefix='SessionState'
                        if value.startswith(sess_state_prefix):
                            value=value[len(sess_state_prefix):]
                        VALUE_MAP[key]=value
            # parse volume
            if line.endswith('#k'):
                value = line.strip()
                VALUE_MAP["volume"]=value.count("#")
        self.state=VALUE_MAP["state"]


        md = Metadata()
        md.playerName = "Tidal"
        md.artist = VALUE_MAP['artists']
        md.title = VALUE_MAP['title']
        md.albumTitle = VALUE_MAP['album_name']
        md.duration = VALUE_MAP['duration']
        md.artUrl = None;
        md.externalArtUrl = None

        '''
        self.artist = artist
        self.title = title
        self.albumArtist = albumArtist
        self.albumTitle = albumTitle
        self.artUrl = artUrl
        self.externalArtUrl = None
        self.discNumber = discNumber
        self.tracknumber = trackNumber
        self.playerName = playerName
        self.playerState = playerState
        self.streamUrl = streamUrl
        self.playCount = None
        self.mbid = None
        self.artistmbid = None
        self.albummbid = None
        self.loved = None
        self.wiki = None
        self.loveSupported = Metadata.loveSupportedDefault
        self.tags = []
        self.skipped = False
        self.host_uuid = None
        self.releaseDate = None
        self.trackid = None
        self.hifiberry_cover_found=False
        self.duration=0
        self.time=0
        self.position=0 # poosition in seconds
        self.positionupdate=time() # last time position has been updated
        '''

        self.meta=md



    
    def get_state(self):
        logging.info('tidalcontrol::get_state')
        logging.info(self.state)

        #return STATE_STOPPED
        try:
            state = STATE_MAP[self.state]
        except:
            state = STATE_UNDEF

        return state
        '''
        if self.client is None:
            self.connect()

        if self.client is None:
            return {}
        
        try:
            status=self.client.status()
        except:
            # Connection to MPD might be broken
            self.disconnect()
            self.connect()
    
        
        try:
            state = STATE_MAP[status["state"]]
        except:
            state = STATE_UNDEF
            
        return state
        '''
    
        
    def get_meta(self):
        logging.info('tidalcontrol::get_meta')
        logging.info(self.client)
       
        if STATE_MAP[self.state] in [STATE_PLAYING,STATE_PAUSED]:
            #song=self.client.currentsong()
            song={
                "artist": "cd ",
                "title": "title",
                "albumartist": "albumArtist",
                "album": "albumTitle",
                "disc": "discNumber",
                "track": "tracknumber", 
                "duration": "duration",
                "time": "time",
                "file": "streamUrl" 
                } 
        return self.meta
    
    def send_command(self,command, parameters={}):
        logging.info('tidalcontrol::send_command')

        if command not in self.get_supported_commands():
            return False 
        
        if self.client is None:
            self.reconnect()

        if self.client is None:
            return False
        
        playstate=None
        if command in [CMD_PLAY, CMD_PLAYPAUSE]:
            playstate=self.get_state()
        
        if command == CMD_NEXT:
            self.client.next()
        elif command == CMD_PREV:
            self.client.previous()
        elif command == CMD_PAUSE:
            self.client.pause(1)
        elif command == CMD_STOP:
            self.client.stop()
        elif command == CMD_RANDOM:
            self.client.random(1)
        elif command == CMD_NORANDOM:
            self.client.random(0)
        elif command == CMD_REPEAT_ALL:
            self.client.repeat(1)
        elif command == CMD_REPEAT_NONE:
            self.client.repeat(0)
        elif command == CMD_REPEAT_ALL:
            self.client.repeat(1)
        elif command == CMD_PLAY:
            if playstate == STATE_PAUSED:
                self.client.pause(0)
            else:
                self.client.play(0)
        elif command == CMD_PLAYPAUSE:
            if playstate == STATE_PLAYING:
                self.client.pause(1)
            else:
                self.send_command(CMD_PLAY)
        else:
            logging.warning("command %s not implemented", command)
            
        
    """
    Checks if a player is active on the system and can result a 
    state. This does NOT mean this player is running
    """
    def is_active(self):
        return self.client is not None
    
