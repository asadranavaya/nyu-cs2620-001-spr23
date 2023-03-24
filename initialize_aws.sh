#!/bin/bash
sudo yum update
sudo yum install -y python3-pip
sudo /etc/init.d/apache2 stop
sudo pip3 install requests
sudo pip3 install pythonping
sudo pip3 install wget
sudo mkdir ~/test
sudo cp -f test.txt ~/test/test.txt
sudo amazon-linux-extras install nginx1
sudo cp -f nginx.conf /etc/nginx/nginx.conf
sudo /usr/sbin/nginx -s reload