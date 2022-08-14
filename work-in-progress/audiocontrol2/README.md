
* Note! This modification is work-in-progress 
And requires manual editting of the HifiBerryOS files.
If you are not comfortable with editting in Linux environment, wrongly modifying these files can lead to a non-working HifiBerryOS system. Therefore: ALWAYS make a backup of files that you are about to change. You do this modication at your own risk.

* CURRENT ISSUES *

Right now the solution ONLY works when running the AudioControl2 process in the foreground.
This might has something todo with the Threading i am polling the information in Python.
The result is that, if you start this service as background job (e.g. systemctl start audiocontrol2) it will not work.


* Installation

You can either run the ./install.sh script or add the following modifications manually

   ```
1. Create symbolic link to add TidalController to AudioControl2 daemon
   ln -s ${PWD}/tidalcontrol.py /opt/audiocontrol2/ac2/players/tidalcontrol.py
   ```
2. go and edit the file and initialize the player
   ```
   nano /opt/audiocontrol2/audiocontrol2.py
   ```

3. Look for the following section and import the TidalControl class
   ```
   from ac2.players.vollibrespot import VollibspotifyControl
   from ac2.players.vollibrespot import MYNAME as SPOTIFYNAME
   ```

   and add the following line so it looks like
   ```
   from ac2.players.vollibrespot import VollibspotifyControl
   from ac2.players.vollibrespot import MYNAME as SPOTIFYNAME
   from ac2.players.tidalcontrol import TidalControl
   ```

4. Look for the following section and add code to add and initialize the TidalController
   ```
   # Vollibrespot
   vlrctl = VollibspotifyControl()
   vlrctl.start()
   mpris.register_nonmpris_player(SPOTIFYNAME,vlrctl)
   ```

   into
   ```
   # Vollibrespot
   vlrctl = VollibspotifyControl()
   vlrctl.start()
   mpris.register_nonmpris_player(SPOTIFYNAME,vlrctl)

   # TidalControl (ADD THIS PART)
   tdctl = TidalControl()
   tdctl.start()
   mpris.register_nonmpris_player(tdctl.playername,tdctl)
   ```

5. Testing
   ```
   # Stop AudioControl2 Daemon
   systemctl restart audiocontrol2
   ```

6. Done!!!... Now open your HifiBerryOS webpage and start a song... you should see track metadata in the player. (controls from WEBUI still needs to be implemted. Controls work via Phone.)

* Audio Controll Api Reference
https://github.com/hifiberry/audiocontrol2/blob/master/doc/api.md

** NOTE TO SELF: I will make a daemon which will scrape and keep track of state, independendly from the AudioController (this because Threading doesnt seem to play nicely and scraping from docker using TMUX is too slow). The daemon will scrape state in seperate thread and then update ENV vars that can be accessed globally. 
The audiocontrol2 will simply only read the ENV vars.
