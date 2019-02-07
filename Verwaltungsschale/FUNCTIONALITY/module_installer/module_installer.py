.# Author: Vladimir Kutscher
# Author: Syed Emad

import os, sys
curdir = os.path.abspath(os.path.dirname(__file__))
topdir = os.path.abspath(os.path.join(curdir, os.pardir, os.pardir))
if topdir not in sys.path:
	sys.path.insert(0, topdir)
from FUNCTIONALITY.configuration import config
from FUNCTIONALITY.module import module
from FUNCTIONALITY.module_installer.addInstallation import add_install, add_deinstall

def main():
    """The Module Installer is handling the communication, while the
    installation-procedure is in the addInstallation.py
    """

    module_installer = module('MODULE_INSTALLER', config)

    def zmq_request_installer(api_name, api_data):
        """A function which perform the zmq communication
        """

        REQUEST = module_installer.create_message(TO = api_name, CORE = api_data)
        module_installer.send(REQUEST)
        ## WAIT FOR THE ANSWER ##
        MESSAGE = module_installer.receive()
        CORE = module_installer.extract_core(MESSAGE)

        response = CORE['response']

        return response

    while True:
        """Die while True Loop is needed, because the zmq-Socket should wait
        for requests all the time and not just once.
        """

        try:
            ## Waiting for any request
            MESSAGE = module_installer.receive()
            CORE = module_installer.extract_core(MESSAGE)
            method = CORE["request"]

            ## resource_id = install would be redundant an the moment
            resource_id = CORE['resource_id']
            json_data = CORE['json_data']
            ## getting the module_id which schould be installed
            module_id = json_data['module_id']

            ### ADD INSTALLATION ###
            if method == 'PUT' and resource_id == 'install':
                """With the PUT-Method new Modules can be installed here
                """

                """FIRST STEP: Collecting the required addData through
                a call to the HTTPOUT, because the data comes from
                outside the shell
                """

                api_data = {'request' : 'GET',
                            'ip_address' : 'http://127.0.0.1:5001',
                            'path' : '/database/adds/'+module_id}

                response_2 = zmq_request_installer("HTTPOUT", api_data)

                """SECOND STEP: Placing the configuration data
                and code data to the respective files (installed_adds.xml
                Python-Script and HTML - Script). Collected in an separate
                addInstallation - script.
                """

                add_config = add_install(add_name = module_id, addData = response_2)

                """THIRD STEP: Send message to Restart to register Module in Broker and
                Start the Add """

                add_config[module_id]['identity'] = add_config[module_id]['identity'].decode()
                config_info = {'Anweisung' : 'NEU', 'DATA' : add_config}
                install_message = module_installer.create_message(TO = "RESTART", CORE = config_info)
                module_installer.send(install_message)

                ## response that the asset is installed
                response = "addSuccessfullyInstalled"


            ### REMOVE ADD ###
            elif method == "DELETE" and resource_id == 'remove':
                """ If a DELETE - request comes from flask_server, the add will
                be removed.
                """

                add_deinstall(add_name = module_id)

                remove_info = {'Anweisung':'LÖSCHE', 'DATA': {"module" :module_id}}
                remove_message = module_installer.create_message(TO='RESTART', CORE=remove_info)
                module_installer.send(remove_message)

                ## response that the asset is removed
                response = "addSuccessfullyRemoved"

            else:
                pass

            ## sending back the request
            RESPONSE = module_installer.create_message(TO = MESSAGE,
                                             CORE = {'response' : response})
            module_installer.send(RESPONSE)

        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
