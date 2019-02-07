#!/bin/sh

#install python3.5.2 on raspberry pi if necessary

#sudo apt-get install build-essential
#sudo apt-get install libncurses5-dev
#sudo apt-get libreadline6-dev
#sudo apt-get libncursesw5-dev
#sudo apt-get libssl-dev
#sudo apt-get libgdbm-dev
#sudo apt-get install libc6-dev
#sudo apt-get libsqlite3-dev
#sudo apt-get tk-dev
#sudo apt-get libbz2-dev
#sudo apt-get install libdb5.3-dev
#sudo apt-get install libexpat1-dev
#sudo apt-get liblzma-dev
#sudo apt-get zlib1g-dev

#cd $HOME
#wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
#tar -zxvf Python-3.5.2.tgz

#cd Python-3.5.2
#./configure       # 3 min 13 s

#make -j4          # 8 min 29 s
#sudo make install # ~ 4 min

#sudo pip3 install -U pip
#sudo pip3 install -U setuptools

###########################################################################


apt-get update
apt-get install python3-pip python3-dev nginx -y


pip3 install virtualenv
virtualenv -p python3 projectenv
source projectenv/bin/activate
pip install -r install/requirements_raspberryPI.txt
deactivate


sed -i -e "s@DIR@$PWD@g" install/wsgi.service
sed -i -e "s@USR@$SUDO_USER@g" install/wsgi.service

sed -i -e "s@DIR@$PWD@g" install/nginx
ADDRESS=`ifconfig wlan0 2>/dev/null|awk '/inet addr:/ {print $2}'|sed 's/addr://'`
sed -i -e "s@ADD@$ADDRESS@g" install/nginx


cp install/wsgi.service /etc/systemd/system
cp install/nginx /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/nginx /etc/nginx/sites-enabled


systemctl start wsgi
systemctl enable wsgi

systemctl daemon-reload
systemctl restart nginx


#install pandas manually (long process)
#sudo ~/i40AS/projectenv/bin/pip install pandas
