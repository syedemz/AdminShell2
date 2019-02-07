@echo off
start cmd /k "activate qt35 && timeout /T 1 && python "%cd%\..\Arduino_Schnittstelle\Arduino_schnittstelle.py""
start cmd /k "activate qt35 && timeout /T 1 && python "%cd%\..\Robotersteuerung_Schalenapp\main.py""
start cmd /k "activate qt35 && timeout /T 1 && python "%cd%\hauptprogramm.py""