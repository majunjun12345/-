#!/usr/bin/env bash


source_root='/root/极验证'


sudo apt-get update
sudo apt-get install -y git python3 python3-pip
sudo apt-get install -y nginx mongodb supervisor
sudo pip3 install jinja2 flask gunicorn pymongo gevent


sudo rm -f /etc/nginx/sites-enabled/*
sudo rm -f /etc/nginx/sites-available/*


sudo ln -s -f ${source_root}/web21.conf /etc/supervisor/conf.d/web21.conf

sudo ln -s -f ${source_root}/web21.nginx /etc/nginx/sites-enabled/web21


sudo chmod o+xr /root
sudo chmod -R o+xr ${source_root}

sudo service supervisor restart
sudo service nginx restart

echo "setup development environemtn success"