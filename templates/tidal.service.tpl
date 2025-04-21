[Unit]
Description=Tidal Connect Docker Service
After=docker.service network-online.target
Requires=docker.service network-online.target

[Service]
WorkingDirectory=${PWD}/
Type=oneshot
RemainAfterExit=yes

#ExecStartPre=/bin/docker-compose pull --quiet
ExecStart=/bin/docker-compose up -d --no-recreate

ExecStop=/bin/docker-compose stop

ExecReload=/bin/docker-compose up -d --no-recreate

[Install]
WantedBy=multi-user.target

