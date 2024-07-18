# Tidal Connect Docker image for MoOde

Code based on https://github.com/TonyTromp/tidal-connect-docker.

# Installation

SSH into your Raspberry and clone/copy this repository onto /usr/local as root

```
# On moOde
sudo -s
cd /usr/local
git clone https://github.com/TonyTromp/tidal-connect-docker.git && \
cd tidal-connect-docker
./install
```

## Start/Stopping

You can either start or stop the TIDAL Service via command-line or with configured triggerhappy remote control.
If you would rather use command line, you might find these scripts handy.

You may also use the systemd scripts:
```
systemctl stop tidal.service
systemctl start tidal.service
```
