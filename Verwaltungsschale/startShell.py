#!/bin/sh
import subprocess
import shlex
import platform
from os import path
import sys

curdir = path.abspath(path.dirname(__file__))

operating_system = platform.system()

# Linux
if operating_system == 'Linux':
    proc1=subprocess.Popen(shlex.split("gnome-terminal -e 'bash -c \" cd CONTROL; python3.6 control_start.py; exec bash\"'"))
    proc1.communicate()
    proc2=subprocess.Popen(shlex.split("gnome-terminal -e 'bash -c \" cd TRANSMISSION/HTTPIN; python3.6 flask_server.py; exec bash\"'"))
    proc2.communicate()
    proc3=subprocess.Popen(shlex.split("gnome-terminal -e 'bash -c \" python3.6 module_start.py; exec bash\"'"))
    proc3.communicate()
    proc4 = subprocess.Popen(shlex.split("gnome-terminal -e 'bash -c \" python3.6 ../DATABASE_EXTERN/flask_DATABASE.py; exec bash\"'"))
    proc4.communicate()

else:
    print ("system not recognized.")
    ##### need to add code for windows systems
