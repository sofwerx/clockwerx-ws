#!/bin/bash
sudo rm -rf /var/www/clockwerxWS/app
sudo mkdir /var/www/clockwerxWS/app
sudo cp -r ../app/* /var/www/clockwerxWS/app/.
sudo rm -rf /var/www/clockwerxWS/conf
sudo mkdir /var/www/clockwerxWS/conf
sudo cp -r ../conf/clockDefs.json /var/www/clockwerxWS/conf/.
sudo service apache2 restart

