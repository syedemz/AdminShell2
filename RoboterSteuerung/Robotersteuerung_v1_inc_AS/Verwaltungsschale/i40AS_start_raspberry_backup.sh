#!/bin/sh


python3 /home/pi/Desktop/Fernwartungsplattform/Verwaltungsschale/ROBOTERSTEUERUNG/Arduino_Schnittstelle/Arduino_schnittstelle.py &

cd /home/pi/Desktop/Fernwartungsplattform/Verwaltungsschale/ROBOTERSTEUERUNG/XBox_Steuerung

python3 XBox_Steuerung_GUI.py &

cd /home/pi/Desktop/Fernwartungsplattform/Verwaltungsschale/ROBOTERSTEUERUNG/Robotersteuerung

python3 hauptprogramm.py & 

cd ..
cd ..

python3 module_start.py &
python3 wsgi.py &
python3 /home/pi/Desktop/Fernwartungsplattform/Verwaltungsschale/ROBOT_SERVER/robot_server.py &

python3 control_start.py 