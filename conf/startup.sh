#!/bin/bash

/usr/local/bin/docker-compose -f /home/swx_pi/docker-compose.yml down

docker login -u gitlab+deploy-token-130024 -p 8Awi7iV68Wy-hhBf2S7t registry.gitlab.com/swxadmin/clockwerx-ws

docker pull registry.gitlab.com/swxadmin/clockwerx-ws:native

docker logout

docker login -u gitlab+deploy-token-130012 -p C-TX_Z9_UUFMKsaZq9va registry.gitlab.com/swxadmin/clockwerx-web

docker pull registry.gitlab.com/swxadmin/clockwerx-web:native

docker logout

docker image prune -f

/usr/local/bin/docker-compose -f /home/swx_pi/docker-compose.yml up -d
