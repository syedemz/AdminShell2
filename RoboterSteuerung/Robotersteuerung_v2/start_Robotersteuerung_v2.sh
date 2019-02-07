#!/bin/sh

## Start Arduino Schnittstelle
python3 /home/pi/Desktop/Robotersteuerung_v2/Arduino_Schnittstelle/Arduino_schnittstelle.py &

## Start X-BOX-Steuerung
#cd /home/pi/Desktop/Robotersteuerung_v2/XBox_Steuerung
#python3 XBox_Steuerung_GUI.py &

## Start Robotersteuerung
cd /home/pi/Desktop/Robotersteuerung_v2/Robotersteuerung/ 
python3 hauptprogramm.py 


