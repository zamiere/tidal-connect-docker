FROM raspbian/stretch

RUN echo 'deb http://archive.raspberrypi.org/debian/ stretch main' > /etc/apt/sources.list && \
    echo 'deb http://legacy.raspbian.org/raspbian stretch main contrib non-free rpi firmware' >> /etc/apt/sources.list && \
    echo 'deb-src http://legacy.raspbian.org/raspbian stretch main contrib non-free rpi firmware' >> /etc/apt/sources.list

# Add [trusted=yes] to disable the GPG check temporarily for snapshot repositories
RUN sed -i 's/^deb /deb [trusted=yes] /' /etc/apt/sources.list
RUN sed -i 's/^deb-src /deb-src [trusted=yes] /' /etc/apt/sources.list

RUN apt-get -o Acquire::Check-Valid-Until=false update -y -q
RUN apt-get upgrade -y -q --allow-unauthenticated

#RUN apt-get update -y -q && apt-get upgrade -y -q --allow-unauthentcated
RUN apt install --fix-missing --fix-broken -y -q multiarch-support git  libavformat57 libportaudio2* libflac++6v5* libavahi-common3 libavahi-client3 alsa-utils curl portaudio19-dev neovim zsh

#libcurl3 -y 
RUN mkdir -p /app/ifi-tidal-release
WORKDIR /app/ifi-tidal-release

RUN curl -k -O -L https://snapshot.debian.org/archive/debian-security/20190925T215334Z/pool/updates/main/o/openssl/libssl1.0.0_1.0.1t-1%2Bdeb8u12_armhf.deb 
RUN apt install -y ./libssl1.0.0_1.0.1t-1%2Bdeb8u12_armhf.deb
RUN rm ./libssl1.0.0_1.0.1t-1%2Bdeb8u12_armhf.deb 

RUN curl -k -O -L https://snapshot.debian.org/archive/debian-security/20190913T112238Z/pool/updates/main/c/curl/libcurl3_7.38.0-4%2Bdeb8u16_armhf.deb
RUN apt install -y ./libcurl3_7.38.0-4%2Bdeb8u16_armhf.deb --allow-downgrades
RUN rm ./libcurl3_7.38.0-4%2Bdeb8u16_armhf.deb
RUN apt install -y -q tmux

COPY Docker/src/bin/ bin
COPY Docker/src/pa_devs/ .
COPY Docker/src/play .
COPY Docker/src/id_certificate id_certificate
COPY Docker/src/licenses licenses
RUN chmod a+x bin/* 

ENV PA_ALSA_PLUGHW=1

COPY Docker/entrypoint.sh /
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

