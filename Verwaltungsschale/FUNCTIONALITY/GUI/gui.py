# GUI - Module.
# Author: Syed Emad


"""
The GUI is the HMI of the AAS.
"""

################################################################################
## Imports
################################################################################
import os, sys
curdir = os.path.abspath(os.path.dirname(__file__))
topdir = os.path.abspath(os.path.join(curdir, os.pardir, os.pardir))
if topdir not in sys.path:
	sys.path.insert(0, topdir)
from FUNCTIONALITY.configuration import config
from FUNCTIONALITY.module import module
from FUNCTIONALITY.GUI.template_creation import create_template

def main():

    gui = module('GUI', config)

    def zmq_request_GUI(api_name, api_data):
        """A function which perform the zmq communication and reduces the
        amount of code. api_name is the name of the module, for example DATABASE
        and request_name ist the request the adressed api awaits, for example
        getDataLeftView. This function has to be in this script because the
        module is instantiated here.
        ATTENTION!!!! With the timeout-function of the poll-method,
        the following scenario is possible: you send a REQUEST for someting
        and dont receive an 'response' within the timeout. The soket restarts
        and the gui is in the receive-mode. If the other module
        is responsing after that, the message comes to the regular-recieve,
        which is not intended and dont even has the 'request'-key.
        """

        REQUEST = gui.create_message(TO = api_name, CORE = api_data)
        gui.send(REQUEST)
        ## WAIT FOR THE ANSWER ##
        MESSAGE = gui.poll(10000)
        print('MESSAGE: '+str(MESSAGE))
        CORE = gui.extract_core(MESSAGE)
        response = CORE['response']

        return response

    while True:
        """Die while True Loop is needed, because the zmq-Socket should wait
        for requests all the time.
        """

        try:
            """Receiving, processing and sending back of requests from HTTPIN
            """

            ## Waiting for any request
            MESSAGE = gui.receive()
            CORE = gui.extract_core(MESSAGE)
            request = CORE['request']
            template_id = CORE['resource_id']

            if request == 'GET':
                """A request to GET some html - data.
                """
                ## Initialising an empty data-dictionary
                template_data = {}

                if template_id == "newAsset":
                    """Landing-page, if no asset is installed
                    """
                    ## defining the request for data to the DATABASE
                    api_data = {'request' : 'getAssetInfo'}
                    ## getting the data from the DATABASE
                    template_data = zmq_request_GUI("DATABASE", api_data)

                elif template_id == "index":
                    api_data = {'request' : 'getDataLeftView'}
                    template_data = zmq_request_GUI('DATABASE', api_data)

                elif template_id == 'data':
                    api_data = {'request' : 'getBlockData'}
                    template_data = zmq_request_GUI('DATABASE', api_data)

                elif template_id == 'adds':
                    api_data = {'request' : 'getAddInfo'}
                    template_data = zmq_request_GUI('DATABASE', api_data)

                elif template_id == 'newAdd':
                    ## defining the request for an external database, which
                    ## runs on an separate flask server but on the same system
                    api_data = {'request' : 'GET',
                                'ip_address' : 'http://127.0.0.1:5001',
                                'path' : '/database/availableAdds'}
                    template_data = zmq_request_GUI('HTTPOUT', api_data)

                elif template_id == 'assetAlreadyInstalled':
                    """Nothing is happening here untill now.
                    """
                    pass

                ## using the create_template function
                ## from the template_creation module
                response = create_template('GUI/templates/'+template_id+'.html',
                                            variables=template_data)


            ### ADD - TEMPLATES ###
            elif request == "getAddTemplate":
                """The Add - Templates are in the corresponding add - folder
                and has to be gathered from there"""

                ## getting the add_name, whose template should be rendered
                add_name = CORE['add_name']
                add_template = CORE['add_template']

                response = create_template(add_name+'/templates/'+add_template,
                                            variables = None)

            else:
                response = create_template('GUI/templates/unknownRequest.html',
                                            variables = None)

            ## sending back the request
            RESPONSE = gui.create_message(TO = MESSAGE,
                                             CORE = {'response' : response})
            gui.send(RESPONSE)

        except KeyboardInterrupt:
            break

        except KeyError as e:
            print('KeyError: '+str(e)+' in the GUI.')

# if __name__ == "__main__":
#     main()
