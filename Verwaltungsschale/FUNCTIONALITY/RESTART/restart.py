# Author: Syed Emad

from os import chdir, system, getcwd, path, pardir
from time import sleep
import sys
import subprocess
import xml.dom.minidom as dom

curdir = path.abspath(path.dirname(__file__))
topdir = path.abspath(path.join(curdir, pardir))
if topdir not in sys.path:
	sys.path.insert(0, topdir)

from module import module
from configuration import config


def main():

    restart = module(mod_name = 'RESTART', config = config)

    while True:

        MESSAGE = restart.receive()
        CORE = restart.extract_core(MESSAGE)
        if CORE['Anweisung'] == 'NEU':
            data = dom.parse("DATABASE/installed_adds.xml") #Get the Data for the New App
            adds = data.getElementsByTagName("add")

            add_name = next( iter(CORE["DATA"].keys()))
            add_identity = CORE["DATA"][add_name]["identity"] #Lookup the identity

            for add in adds:
                if add.getAttribute("id") == add_identity:
                    main = add.getElementsByTagName("main")[0].firstChild.data #get the name of the main Module
                    path = "FUNCTIONALITY/" + add_name +"/" + main + ".py" #path to the main script
                    command = "python " + path
                    exec('sub' + add_name +  '= subprocess.Popen(command, cwd = getcwd())') # Start the mainscript in a Subprocess

        elif CORE['Anweisung'] == 'LÖSCHE':
            add_name = CORE['DATA']['module']
            try:
                exec('sub' + add_name + '.kill()')
                pass
            except NameError:
                exec(add_name + '.kill')
            except Exception as e:
                print('Exception while killing module socket occurs: '+str(e))
                continue
            restart.sysout('Prozess beendet', meta = add_name)
            answer = {'answer': 'gelöscht'}

if __name__ == '__main__':
	main()
