@echo off
start cmd /k "activate qt4 && timeout /T 1 && python "%cd%\..\Arduino_Schnittstelle\Arduino_schnittstelle.py""
start cmd /k "activate qt4 && timeout /T 1 && python "%cd%\hauptprogramm.py""