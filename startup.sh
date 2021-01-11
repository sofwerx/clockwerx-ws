#!/bin/bash

grep -Fxq "swx_pi	ALL=(ALL) NOPASSWD: /sbin/reboot, /sbin/poweroff, /sbin/shutdown" /etc/sudoers || echo 'swx_pi	ALL=(ALL) NOPASSWD: /sbin/reboot, /sbin/poweroff, /sbin/shutdown' >> /etc/sudoers

/usr/local/bin/docker-compose -f /home/swx_pi/docker-compose.yml down

docker login -u gitlab+deploy-token-1300241 -p <GITLAB PASSWORD> registry.gitlab.com/swxadmin/clockwerx-ws

docker pull registry.gitlab.com/swxadmin/clockwerx-ws:native

docker logout

docker login -u gitlab+deploy-token-1300121 -p <GITLAB PASSWORD> registry.gitlab.com/swxadmin/clockwerx-web

docker pull registry.gitlab.com/swxadmin/clockwerx-web:native


docker logout

docker image prune -f

/usr/local/bin/docker-compose -f /home/swx_pi/docker-compose.yml up -d
