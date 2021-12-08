[Unit]
Description=Tidal Connect Docker Service
After=docker.service network-online.target
Requires=docker.service network-online.target

[Service]
#WorkingDirectory=/data/tidal-connect-docker/Docker/
WorkingDirectory=${PWD}/Docker/
Type=oneshot
RemainAfterExit=yes

#ExecStartPre=/bin/docker-compose pull --quiet
ExecStart=/bin/docker-compose up -d

ExecStop=/bin/docker-compose down

#ExecReload=/bin/docker-compose pull --quiet
ExecReload=/bin/docker-compose up -d

[Install]
WantedBy=multi-user.target

