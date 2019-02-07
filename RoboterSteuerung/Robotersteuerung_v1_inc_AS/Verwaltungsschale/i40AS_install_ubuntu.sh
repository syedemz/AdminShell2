#!/bin/sh
apt-get update  # To get the latest package lists
apt-get install python3-pip python3-dev nginx -y


pip3 install virtualenv
virtualenv -p python3 projectenv
source projectenv/bin/activate
pip install -r install/requirements_ubuntu.txt
deactivate


sed -i -e "s@DIR@$PWD@g" install/control.service
sed -i -e "s@USR@$SUDO_USER@g" install/control.service

sed -i -e "s@DIR@$PWD@g" install/wsgi.service
sed -i -e "s@USR@$SUDO_USER@g" install/wsgi.service

sed -i -e "s@DIR@$PWD@g" install/module.service
sed -i -e "s@USR@$SUDO_USER@g" install/module.service

sed -i -e "s@DIR@$PWD@g" install/nginx
ADDRESS=`ifconfig eth0 2>/dev/null|awk '/inet addr:/ {print $2}'|sed 's/addr://'`
sed -i -e "s@ADD@$ADDRESS@g" install/nginx


cp install/control.service /etc/systemd/system
cp install/wsgi.service /etc/systemd/system
cp install/module.service /etc/systemd/system
cp install/nginx /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/nginx /etc/nginx/sites-enabled


systemctl start control
systemctl enable control

systemctl start wsgi
systemctl enable wsgi

systemctl start module
systemctl enable module

systemctl daemon-reload
systemctl restart nginx
