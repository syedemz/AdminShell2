# DATABASE - Module.
# Author: Vladimir Kutscher
# Author: Syed Emad

import os, sys
curdir = os.path.abspath(os.path.dirname(__file__))
topdir = os.path.abspath(os.path.join(curdir, os.pardir, os.pardir))
if topdir not in sys.path:
	sys.path.insert(0, topdir)
from FUNCTIONALITY.configuration import config
from FUNCTIONALITY.module import module
from FUNCTIONALITY.asset_installer.assetInstallation import save_gui_data

def main():
    """The Asset Installer is handling the communication, while the
    installation-procedure is in the assetInstallation.py
    """

    asset_installer = module('ASSET_INSTALLER', config)

    def zmq_request_installer(api_name, api_data):
        """A function which perform the zmq communication
        """

        REQUEST = asset_installer.create_message(TO = api_name, CORE = api_data)
        asset_installer.send(REQUEST)
        ## WAIT FOR THE ANSWER ##
        MESSAGE = asset_installer.receive()
        CORE = asset_installer.extract_core(MESSAGE)

        response = CORE['response']

        return response

    while True:
        """Die while True Loop is needed, because the zmq-Socket should wait
        for requests all the time and not just once.
        """

        try:

            ## Waiting for any request
            MESSAGE = asset_installer.receive()
            CORE = asset_installer.extract_core(MESSAGE)
            request = CORE["request"]
            resource_id = CORE['resource_id']
            json_data = CORE['json_data']
            ## getting the asset_id which schould be istalled
            asset_id = json_data['asset_id']

            ### ASSET INSTALLATION ###
            if  (request == "PUT" and \
                resource_id == "install"):
                """ If a request with the HTTP-Method PUT comes
                from flask_server, the asset will be installed.
                The asset installation has three steps (A, B, C) at the moment
                """

                """STEP A: Collecting the asset data (data.xml, templates)
                from an external database """
                api_data = {'request' : 'GET',
                            'ip_address' : 'http://127.0.0.1:5001',
                            'path' : '/database/assets/'+asset_id,
                            }

                response_2 = zmq_request_installer("HTTPOUT", api_data)

                """STEP B: Passing the data.xml to the DATABASE"""
                ## extracting the data_xml from the response_2
                dataXmlData = response_2.get('data_xml')
                ## wrapping of the message to the DATABASE
                api_data = {'request' : 'saveDataXml', 'data_xml': dataXmlData}
                ## send the request to the DATABASE -
                ## the response ("dataXml saved") is not checked yet
                response_3 = zmq_request_installer("DATABASE", api_data)

                """STEP C: Pasting of the templates into the gui"""

                templates_data = response_2.get('templates_data')
                ## the installation process is defined in an extern script
                save_gui_data(asset_name = asset_id, templates_data = templates_data)

                ## response that the asset is installed
                response = "assetSuccessfullyInstalled"

            else:
                pass

            ## sending back the request
            RESPONSE = asset_installer.create_message(TO = MESSAGE,
                                             CORE = {'response' : response})
            asset_installer.send(RESPONSE)


        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
