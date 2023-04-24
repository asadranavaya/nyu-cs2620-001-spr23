#!/bin/bash
sudo yum update
sudo yum install python -y
sudo yum install -y python3-pip
sudo /etc/init.d/apache2 stop
sudo pip3 install requests
sudo pip3 install pythonping
sudo pip3 install wget
sudo mkdir ~/test
sudo cp -f test.txt ~/test/test.txt
sudo yum install nginx -y
sudo systemctl start nginx.service
sudo cp -f nginx_aws.conf /etc/nginx/nginx.conf
sudo /usr/sbin/nginx -s reload