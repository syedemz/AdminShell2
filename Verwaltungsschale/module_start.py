#!/bin/sh

from multiprocessing import Process
import xml.dom.minidom as dom
import importlib
from os import path, pardir, system

from DATABASE import info
from TRANSMISSION.HTTPOUT import http_requests
from INTERFACE import asset
from FUNCTIONALITY.GUI import gui
from FUNCTIONALITY.RESTART import restart
from FUNCTIONALITY.module_installer import module_installer
from FUNCTIONALITY.asset_installer import asset_installer


def main(DATABASE=True, HTTPOUT=True, INTERFACE=True, gui_on=True, RESTART=True,
        MODULE_INSTALLER=True, ASSET_INSTALLER=True):
    """Starting all mudules. Mudules which can't be installed/deinstalled are
    hard - coded here and all the other modules (from FUNCTIONALITY) are started
    by a function.
    The boolean-Parameter which are delivered to the main(boolean-Parameter=True)
    are just boolenan "Switches" for the if-loop inside and have nothing to to
    with the module itself. They can also be named completely different
    (e.g. gui_on).
    ATTENTION!: Some of the modules (e.g. GUI - database_parser) work with
    the os.getcwd() function. This function deliver the path where the code
    is initially started from and this is from here (Verwaltungsschale - level)
    in this case.
    """

    if DATABASE:
        Process(target=info.main,).start()

    if HTTPOUT:
        Process(target=http_requests.main,).start()

    if INTERFACE:
        Process(target=asset.main,).start()

    if gui_on:
        Process(target=gui.main,).start()

    if RESTART:
        Process(target=restart.main,).start()

    if MODULE_INSTALLER:
        Process(target=module_installer.main,).start()

    if ASSET_INSTALLER:
        Process(target=asset_installer.main,).start()

    """Starting all modules from installed_adds.xml"""
    ## getting the path to the dir of this script
    curdir=path.abspath(path.dirname(__file__))
    installed_adds_path = path.join(curdir, 'DATABASE', 'installed_adds.xml')
    add_config = dom.parse(installed_adds_path)
    add_list = add_config.getElementsByTagName("add")
    if add_list:
        for add in add_list:
            module_id = add.getAttribute("id")
            if module_id == 'remote_maintenance':
                """The remote_maintenance module has to be handled separately, because
                its a flask - app and don't has an main() - method. The module
                has to be started from an own terminal or it will block all
                further modules.
                """
                print("The remote_maintenance - module has to be started separately at the moment!")
                # path_to_robot_server = path.join(curdir, 'FUNCTIONALITY',
                #                                 'robot_server', 'robot_server.py')
                # system("python3 "+path_to_robot_server)
            else:
                """All the other modules with a main() - method
                """
                main_module = add.getElementsByTagName("main")[0].firstChild.data
                add_module = "FUNCTIONALITY." + module_id + "." + main_module
                add_module = importlib.import_module(add_module)
                Process(target=add_module.main,).start()



if __name__ == '__main__':
    main()
