import json
import urllib.parse
import requests

from structure.configuration import config
from structure.module import module



def main():

    httpout = module('HTTPOUT', config)


    while True:
        try:

            MESSAGE = httpout.receive()
            CORE = httpout.extract_core(MESSAGE)


            request = CORE["request"]
            main_api = request['main_api']
            address = request["address"]
            url = main_api + urllib.parse.urlencode({'address':address})
            response = requests.get(url).json()
            


            RESPONSE = httpout.create_message(TO= MESSAGE, CORE = response)
            httpout.send(RESPONSE)


        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    main()
