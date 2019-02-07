# DATABASE - Module.
# Author: Vladimir Kutscher
# Author: Syed Emad

"""
The info.py handles the information transfer to and from the DATABASE.
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
from DATABASE.database_parser import findBlockId, tagIterator, saveDataXml

def main():

    database = module('DATABASE', config)

    while True:
        """The ZeroMQ - Socket is listening for incoming messages in loop.
        Incoming requests get processed and a response is sended back.
        """

        try:

            MESSAGE = database.receive()
            CORE = database.extract_core(MESSAGE)
            request = CORE["request"]

            ### REQUEST TO asset_list ###
            if request == "getAssetInfo":

                response = tagIterator(xml_file = 'asset_list.xml')

            ### REQUEST TO data.xml - particular block ###
            elif request == "getDataLeftView":

                ## generierung der Antwort mithilfe der findBlockId-Funktion
                response = findBlockId(xml_file = 'data.xml',
                                       searchId = 'viewImage')

            ### REQUEST TO data.xml - all blocks ###
            elif request == "getBlockData":

                response = tagIterator(xml_file = 'data.xml')

            ### REQUEST TO installed_adds.xml ###
            elif request == "getAddInfo":

                response = tagIterator(xml_file = 'installed_adds.xml')

            elif request == "saveDataXml":
                """ A function to save the data.xml coming from the gui
                in the DATABASE"""
                ## extracting of the data from dict
                data_xml = CORE['data_xml']
                response = saveDataXml(data_xml)

            else:
                print("Unknown request in info.py")
                response = {'response' : 'unknown request'}

            RESPONSE = database.create_message(TO = MESSAGE,
                                               CORE = {'response' : response })
            database.send(RESPONSE)


        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
