# Tidal Connect Docker image for HifiBerry

![hifiberry_sources](https://github.com/TonyTromp/tidal-connect-docker/blob/master/img/hifiberry_listsources.png?raw=true)


Image based on https://github.com/shawaj/ifi-tidal-release and https://github.com/seniorgod/ifi-tidal-release. 
Please visit https://www.raspberrypi.org/forums/viewtopic.php?t=297771 for full information on the backround of this project.

# Why this Docker Port

I have been hapilly using HifiberryOS but beeing an extremely slim OS (based on Buildroot) has its pitfalls, that there is no easy way of extending its current features. Thankfully the Hifiberry Team have blessed us by providing Docker and Docker-Compose within OS.
As I didnt want to add yet another system for Tidal integration (e.g. Bluesound, Volumio), i stumbled upon this https://support.hifiberry.com/hc/en-us/community/posts/360013667717-Tidal-Connect-, and i decided to do something about it. 

This port does much more than just providing the docker image with TIDAL Connect and volume control, as for HifiBerry users it will also install additional sources meny as displayed above.
Volume controls are reflected in the UI.

# Installation

1. SSH into your Raspberry and clone/copy this repository onto your system. 
```
# On HifiberryOS 
git clone https://github.com/TonyTromp/tidal-connect-docker.git
cd tidal-connect-docker
```

2. Install and run

```
./install.sh
```

ENJOY ! ;)

This will download the Docker image from github and install and start TIDAL Connect as a service.
In addition it will also add a new UI Source to HifiBerry called TIDAL Connect which you can use to start/stop the service

3. Start/Stopping

You can either start or stop the TIDAL Service via the HifiBerry Sources menu or via command-line.
If you rather use command line, you might find these scripts handy.

![hifiberry_startstop](https://github.com/TonyTromp/tidal-connect-docker/blob/master/img/hifiberry_tidalcontrol.png?raw=true)

```
./start-tidal-service.sh
./stop-tidal-service.sh
```

4. Trouble shooting

* NO VOLUME *
Please check your volume setting on your device and use your device to increase the volume. 
If setup/dac is recognized it you will see volume changes also updating in the HifiBerry Audio Controls.

* DAC NOT RECOGNIZED / NOT PLAYING *
There are known issues whereas playback is not working, as the DAC is not recognized.
You can check the logs from the Docker image by running:
```
docker logs docker_tidal-connect_1
```
This will list some debug information usefull for trouble shooting.
You can explicitly set the DAC playback device in the Docker/entrypoint.sh file.

For 'HifiBerry Digi+ Pro', if it doesnt work out-of-the-box, you will need to edit the Docker/entrypoint.sh and use
 "snd_rpi_hifiberry_digi: HiFiBerry Digi+ Pro HiFi wm8804-spdif-0 (hw:0,0)" as default playback device (like below).
```
/app/ifi-tidal-release/bin/tidal_connect_application \
   --tc-certificate-path "/app/ifi-tidal-release/id_certificate/IfiAudio_ZenStream.dat" \
   -f "HiFiBerry" \
   --playback-device "snd_rpi_hifiberry_digi: HiFiBerry Digi+ Pro HiFi wm8804-spdif-0 (hw:0,0)" \
   --codec-mpegh true \
   --codec-mqa false \
   --model-name "HiFiBerry" \
   --disable-app-security false \
   --disable-web-security false \
   --enable-mqa-passthrough false \
   --log-level 3 \
   --enable-websocket-log "0" \
```

Note you can list/print your device/DAC name by running the following command
```
docker run -ti \
--device /dev/snd \
-v /var/run/dbus:/var/run/dbus \
-v /var/run/avahi-daemon/socket:/var/run/avahi-daemon/socket \
--entrypoint /app/ifi-tidal-release/bin/ifi-pa-devs-get edgecrush3r/tidal-connect
```

Edit the entryfile.sh and set the playback-device accordingly should solve your issue.

# *** Other Stuff *** #

Build the docker image (OPTIONAL!):

NOTE: I have already uploaded a pre-build docker image to Docker Hub for you.
This means you can skip this time consuming step to build the image manually, and use the pre-build image unless you need to add something to the base image.
However for those who like to thinker, you can add other things to the docker image if you would like to.
```
# Go to the <tidal-connect-docker>/Docker path
cd tidal-connect-docker-master/Docker

# Build the image
./build_docker.sh
```


List Devices
```
docker run -ti \
--device /dev/snd \
-v /var/run/dbus:/var/run/dbus \
-v /var/run/avahi-daemon/socket:/var/run/avahi-daemon/socket \
--entrypoint /app/ifi-tidal-release/bin/ifi-pa-devs-get edgecrush3r/tidal-connect
```

# Tweaking and tuning configuration
If you need to alter any parameters, just change the entrypoint.sh to contain whatever settinsgs you need
The entrypoint.sh file/command is executed upon start of the container and mounted via docker-compose.

