# HTTPOUT - Implementation.
# Author: Syed Emad
# Author: Vladimir Kutscher

"""
The HTTPOUT Module generates HTTP-Requests (GET/POST) over the network.
"""

################################################################################
## Imports
################################################################################
import os, sys
import json
import urllib.parse
import requests
curdir = os.path.abspath(os.path.dirname(__file__))
topdir = os.path.abspath(os.path.join(curdir, os.pardir, os.pardir))
if topdir not in sys.path:
	sys.path.insert(0, topdir)
from FUNCTIONALITY.configuration import config
from FUNCTIONALITY.module import module

def main():

    httpout = module('HTTPOUT', config)

    while True:
        try:
            """Requests from inside the Shell get analyzed and recombined
            to an HTTP-Request to an external Server. The Request to the Server
            is performed and the response of the external Server is translated
            back to internal Syntax and sended back to the shell-module
            which did the initial request.
            Any request has to contain the following
            REQUIRED-KEYs:
            'request' : 'GET or POST'
            'ip_address' : 'e.g. http://127.0.0.1:5001' <-Ext. Database
            'path' : '/database/availableAdds' <- GET request to ext. database

            Reminder!: The standard path for HTTPIN-API
            has the form: /<module_id>/<resource_id>

            Optional data can be included within a 'json_data'-Key for POST:
            'json_data' : {'key1':'value1', 'key2':'value2', ..., 'keyN':'valueN'}

            The custom data is  packed in the HTTP-Body and is not analyzed.
            """

            MESSAGE = httpout.receive()
            CORE = httpout.extract_core(MESSAGE)

            ## extracting the required-information
            request = CORE["request"]
            ip_address = CORE['ip_address']
            path = CORE['path']

            ## constructing of the url
            url = ip_address + path

            print('request '+request)
            if request == "GET":
                """GET-Requests have no content in the body, but just the url
                and the query. If an query is present, is will be extracted in
                a try-function.
                """
                try:
                    query = CORE['query']
                    ## Generating an query out of the transmitted data
                    # url = url + urllib.parse.urlencode({'address':address})
                except:
                    pass
                print('HTTPOUT - Making a GET-Request for: '+url)
                ## sending the request and catching the json-request in a
                ## variable
                response = requests.get(url).json()
                # response = json.dumps(response)
                RESPONSE = httpout.create_message(TO= MESSAGE,
                                                  CORE = {'response' : response })
                httpout.send(RESPONSE)

            elif request == "POST":
                """POST-Request contain a body. For that reason the data behind
                'json_data' is extracted from the MESSAGE-CORE.
                """
                try:
                    ## the date has to be encoded in json!
                    json_data = json.dumps(CORE['json_data'])
                except Exception as e:
                    print("POST request can't be encoded in JSON by HTTPOUT")
                print('HTTPOUT - Making a POST-Request for: '+url+' with the json_data: '+str(json_data))
                ## sendig a POST request to the url with json_data as payload
                response = requests.post(url, data=json_data)

                #json.dumps(response)


            else:
                ## main_api ist die URL des Servers, noch ohne jeglicher key=values
                ## aber schonmal mit dem Fragezeichen am Ende.
                main_api = request['main_api']

                address = request["address"]

                """Die url Variable wird zusammengebaut aus einer www-Adresse
                (main_api = z.B: http://maps.googleapis.com/maps/api/geocode/json?)
                und einer Anfrage (address   = z.B. Frankfurt)
                welche die angesprochene API genau in dieser Form kennt.

                urllib.parse.urlencode wandelt das JSON-Dictionary in
                "key1=val1&key2=val2" - Paare um. In diesem speziellen Fall wird
                aus dem Stadtnamen (z.B. Frankfurt) welche sich hinter der Variable
                address verbirgt und dem 'address' folgender Schlüssel
                zusammengestellt: address=Frankfurt. Die Wahl des Variablennamen
                address ist etwas unglücklich gewählt, da dieser nur für den
                speziellen Fall einer Anfrage an die Google Api sinn macht.
                Weiterhin sei angemerkt, dass request einen eingebaute Methode
                "params" zur Bildung von key=values-Paaren bietet,
                siehe request-Doku - Passing Parameters in URL."""

                url = main_api + urllib.parse.urlencode({'address':address})

                """Die GET Methode von requests wird verwendet, um die Antwort
                der url in JSON zu kodieren und der Variablen response zuzuordnen.
                Ohne explizite Angabe der Kodierung würde requests selbstständig
                kodieren (z.B. utf-8).
                Genau in dieser Zeile  findet die gesamte Komminikation zur
                Außenwelt statt"""
                response = requests.get(url).json()

                RESPONSE = httpout.create_message(TO= MESSAGE,
                                                  CORE = {'response' : response })
                httpout.send(RESPONSE)


        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
