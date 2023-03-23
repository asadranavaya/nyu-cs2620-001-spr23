sudo yum install git
yes
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
sudo pip3 install requests
sudo pip3 install pythonping
sudo pip3 install wget
cwd=$(pwd)
sudo chmod -R 777 cwd
sudo mkdir ~/test
sudo cp -f test.txt ~/test/test.txt
sudo apt-get install nginx -y
sudo cp -f nginx.conf /etc/nginx/nginx.conf
sudo /usr/sbin/nginx -s reload