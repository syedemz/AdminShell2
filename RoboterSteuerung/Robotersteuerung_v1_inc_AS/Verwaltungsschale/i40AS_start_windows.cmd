@echo off
del "%cd%\log\*.log"

start /b python "%cd%\control_start.py"
start /b python "%cd%\module_start.py"
start /b python "%cd%\wsgi.py"
start /b python "%cd%\ROBOT_SERVER\robot_server.py"
start /b python "%cd%\ROBOTERSTEUERUNG\Robotersteuerung\hauptprogramm.py"
start /b python "%cd%\ROBOTERSTEUERUNG\Arduino_Schnittstelle\Arduino_schnittstelle.py"
