FROM ubuntu:18.04

Run apt-get update -y

Run apt-get install lirc -y

Run apt-get install python-pip -y

Run pip install flask

Run apt-get -y install openssh-client

Run apt-get -y install sshpass

Run apt-get install apache2 -y

Run apt-get install libapache2-mod-wsgi -y

WORKDIR /etc/apache2

Run a2enmod headers

COPY conf/apache2.conf .

COPY conf/ports.conf .

WORKDIR /etc/apache2/sites-available

COPY conf/clockwerxWS.conf .

WORKDIR /var/www

Run mkdir -p clockwerxWS

WORKDIR /var/www/clockwerxWS

COPY app app

COPY conf/clockwerxWS.wsgi .

Run mkdir -p conf

COPY conf/clockDefs.json conf/

run mkdir -p logs

Run chmod 777 logs

WORKDIR  /etc/apache2/sites-available

Run a2dissite 000-default

Run a2ensite clockwerxWS.conf

Run apt-get install supervisor -y 

Run mkdir -p /var/log/supervisor

Run mkdir -p /etc/supervisor/conf.d

COPY conf/supervisor.conf /etc/conf.d/supervisor.conf

WORKDIR /

CMD ["supervisord", "-c", "/etc/conf.d/supervisor.conf"]
