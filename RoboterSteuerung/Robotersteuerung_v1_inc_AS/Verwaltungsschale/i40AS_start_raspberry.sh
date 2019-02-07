#!/bin/sh


python3 /home/pi/Desktop/Robotersteuerung_v1_inc_AS/Verwaltungsschale/ROBOTERSTEUERUNG/Arduino_Schnittstelle/Arduino_schnittstelle.py &

cd /home/pi/Desktop/Robotersteuerung_v1_inc_AS/Verwaltungsschale/ROBOTERSTEUERUNG/XBox_Steuerung

python3 XBox_Steuerung_GUI.py &

cd /home/pi/Desktop/Robotersteuerung_v1_inc_AS/Verwaltungsschale/ROBOTERSTEUERUNG/Robotersteuerung

python3 hauptprogramm.py & 

cd ../..

python3 module_start.py & ###
python3 wsgi.py & ###

cd /home/pi/Desktop/Robotersteuerung_v1_inc_AS/Verwaltungsschale/ROBOT_SERVER

python3 robot_server.py & ###


cd /home/pi/Desktop/Robotersteuerung_v1_inc_AS/Verwaltungsschale/ROBOTERSTEUERUNG/Robotersteuerung_Schalenapp

python3 sec_main.py &

cd ../..

python3 control_start.py ###
