@echo off
del "%cd%\log\*.log"

start /b python "%cd%\CONTROL\control_start.py"
start /b python "%cd%\module_start.py"
start /b python "%cd%\TRANSMISSION\HTTPIN\flask_server.py"
