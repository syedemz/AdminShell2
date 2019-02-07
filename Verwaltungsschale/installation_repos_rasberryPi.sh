# Mit diesem Skript kann man alle für die i40AS notwendigen Pakete
# auf dem Raspbery intallieren. Die Grundlage ist debei ein  frisches
# Raspbian Lite. Die Lite Version ist sehr schmal und hat entsprechend fast
# keine Programme.

#Sollten Fehler oder Fehlendes vorhanden sein, gerne verbessern/erweitern

##### Grundeinstellungen auf dem RPI #####

# in raspi-config stellt man nach dem ersten Start des RPI folgenden ein:
# - Tastaturlayout
# - SSH/VNC eraluben
# - Filesystem erweitern

##### Update/Upgrade ######

sudo apt-get update
sudo apt-get upgrade -y #mit -y werden alle unkritischen Fragen automatisch mit Ja benatwortet
sudo apt-get dist-upgrade

##### PIXEL-GUI installieren #####

sudo apt-get install --no-install-recommends xserver-xorg -y #Display-Server
sudo apt-get install --no-install-recommends xinit -y #Desktop Environment
sudo apt-get install raspberrypi-ui-mods -y #Window Manageer
sudo apt-get install lightdm -y #Login Manager

##### Browser installieren (Web/Epiphany) #####

sudo apt-get install epiphany-browser -y

##### Git intallieren (GitHub kann direkt durch "git clone <url>" kopiert werden) #####

sudo apt-get install git -y

##### Python3 (aktuell die 3.4 für Raspbian) #####

sudo apt-get intall python3 -y
sudo apt-get install python3-pip -y #Pip install Python - Paketverwaltung für Python3
#sudo apt-get install python3-dev -y #dev müsste schon bei pip dabei gegewesen sein

##### Python 3.5.2 installieren (nur solange nicht default) ######

sudo wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz #Datei laden
sudo tar -zxvf Python-3.5.2.tgz #Entpacken
cd Python-3.5.2/
sudo ./configure
sudo make -j4 #4-fach paralleles bauen
sudo make install

###### Server ######

sudo apt-get install nginx -y #Engine X -  Webserver

##### Alle sonstigen Pakete, die für die i40AS benötigt werden #####

sudo apt-get install build-essential -y
sudo apt-get install libncurses5-dev -y
sudo apt-get install libreadline6-dev -y
sudo apt-get install libncursesw5-dev -y
sudo apt-get install libssl-dev -y
sudo apt-get install libgdbm-dev -y
sudo apt-get install libc6-dev -y
sudo apt-get install libsqlite3-dev -y
sudo apt-get install tk-dev -y
sudo apt-get install libbz2-dev -y
sudo apt-get install libdb5.3-dev -y
sudo apt-get install libexpat1-dev -y

sudo apt-get install liblzma-dev -y
sudo apt-get install zlib1g-dev -y

sudo pip3 install zmq
sudo pip3 install flask
sudo pip3 install uwsgi
sudo pip3 install requests

sudo apt-get clean # Installationsdeteien werden wieder gelöscht, wenn nicht bereits passiert
