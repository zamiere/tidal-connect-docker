version: '2.2'
services:
  tidal-connect:
    container_name: tidal_connect
    env_file:
      - .env
    image: ${DOCKER_IMAGE}
    tty: true
    network_mode: host
    devices:
     - /dev/snd
    volumes:
      - ./entrypoint.sh:/entrypoint.sh
      - /var/run/dbus:/var/run/dbus
      - /etc/asound.conf:/etc/asound.conf
      - /etc/alsa:/etc/alsa
    restart: always
    dns:
      - ${DOCKER_DNS}
