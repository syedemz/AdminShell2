# HTTPIN - Module.
# Author: Sebastian Mack
# Author: Vladimir Kutscher
# Autho: Syed Emad
"""
The HTTPIN is the API of the AAS.
"""

################################################################################
## Imports
################################################################################
from flask import Flask, jsonify, request, render_template_string
from os import path, chdir, pardir, getcwd
from werkzeug import SharedDataMiddleware
import json
from time import sleep
import sys
import importlib
curdir = path.abspath(path.dirname(__file__))
topdir = path.abspath(path.join(curdir, pardir, pardir))
if topdir not in sys.path:
	sys.path.insert(0, topdir)
import FUNCTIONALITY.configuration as configuration
from FUNCTIONALITY.module import module

##Instance of the Flask-Class with the name "app"
app = Flask(__name__)

global config
config = configuration.config
httpin = module(mod_name = 'HTTPIN', config = config)

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/static': path.join(path.dirname(__file__), pardir, pardir, 'FUNCTIONALITY', 'GUI', 'static', 'images')
    })

def zmq_request_httpin(api_name, api_data):
	"""A function which perform the zmq communication and reduces the
	amount of code. api_name is the name of the module, for example GUI
	and request_name ist the request the adressed api awaits, for example
	getAssetInfo. This function has to be in this script because the
	module is instantiated here.
	"""

	REQUEST = httpin.create_message(TO = api_name, CORE = api_data)
	httpin.send(REQUEST)

	## WAIT FOR THE ANSWER ##

	MESSAGE = httpin.poll(7000)
	CORE = httpin.extract_core(MESSAGE)
	response = CORE['response']
	return response

def request_wants_json():
	"""Function for handling of the mime-type of the request. application/json
	has higher quality an will be returned, if the client accepts it
	"""
	best = request.accept_mimetypes\
	.best_match(['application/json', 'text/html'])
	return best == 'application/json' and \
		request.accept_mimetypes[best] > \
		request.accept_mimetypes['text/html']

## Initialising of the asset installation -  Variable
## don't forget to restart the module_start, if you change the variable
assetInstalled = False

@app.route('/')
def newAsset():
    """Landing-page. Is different from the other URLs beause is shorter and not
    in the standard-form
    """

    if assetInstalled == False:
        """If no asset is installed, a request is sended to the GUI to call
        the installation process
        """

        ## Definition of the request
        api_data = {'request' : 'GET', 'module_version':'v1',
					'resource_id': 'newAsset'}
        ## predefined function to shorten the communication - defined above
        response = zmq_request_httpin('GUI', api_data)

        ## The Template(HTML) comes from the gui.py over the zeroMQ Socket
        ## as a string and is rendered here
        # print("Multithreading-Test. Waiting for 10 seconds till rendering the response...")
        # sleep(10)
        return render_template_string(response)

    elif assetInstalled == True:
        """If an asset is already installed, the user gets a message,
        that an asset is already installed
        """
        api_data = {'request' : 'GET', 'module_version':'v1','resource_id': 'assetAlreadyInstalled'}
        response = zmq_request_httpin('GUI', api_data)
        return render_template_string(response)

    else:
        pass

@app.route('/<module_id>/<resource_id>',
			methods=['GET','POST','PUT','DELETE'])
def distribute(module_id, resource_id):

	print("in HTTPIN...")
	global config
	## translating the module_id in upper-case
	module_id = module_id.upper()

	if (request.method == 'GET' or \
		request.method == 'POST' or \
		request.method == 'PUT' or \
		request.method == 'DELETE'):
		"""The HTTP-Method just has the information from the URL, which can
		be forwarded to the module.
		"""
		print('In first if-loop...')
		## the request method is also pased to the module and the module
		## decides how to react to the method
		api_data = {'request' : request.method, 'resource_id' : resource_id }

		if (request.method == 'POST' or \
			request.method == 'PUT' or \
			request.method == 'DELETE'):
			""" If the HTTP-Method has a body with json-content, it will be
			added here. get_json parses the request body for json content, if
			the application has the type: application/json.
			"""
			print("in second if-loop...")
			json_data = request.get_json(force=True)
			print("JSON_DATA: "+str(json_data))
			api_data['json_data'] = json_data

		else:
			pass

		if config.get(module_id, False):
                        
			"""Check, if the module is existing and sending the data to the
			module.
			"""
			response = zmq_request_httpin(module_id, api_data)

                        
			try:
				if request_wants_json():
					"""Returning an answer in json, if wanted
					"""
					return jsonify(response)
				else:
					return render_template_string(response)

			except TypeError:
				return jsonify({'response' : 'unknown type'})

		else:
			response = {'response' : 'unknown api'}
			return jsonify(response)

	else:
		response = {'response' : 'unknown HTTP-method'}
		return jsonify(response)

		if module_id == 'MODULE_INSTALLER':
			import FUNCTIONALITY.configuration as configuration

			configuration = importlib.reload(configuration)
			httpin.config = configuration.config

			config = configuration.config
			print (config)

@app.route('/GUI/adds/<add_name>/<add_template>')
def application(add_name, add_template):
    """ This function returns the add-html dependent on the asset_name
    and the add_name.
    """

    api_data = {'request' : 'getAddTemplate', 'resource_id' : 'resource_id',
                 'add_name' : add_name, 'add_template' : add_template }

    response = zmq_request_httpin('GUI', api_data)

    return render_template_string(response)

@app.route('/apis', methods=['GET','POST'])
def apis():
    if request.method == 'POST':
        if request.form:
            ## der Inhalt des Testeingabefeld der api_request.html
            ## mit dem Namen 'JSON' wird in der Variable 'postjson' gespeichert
            postjson = request.form['JSON']
            ## das JSON Objekt in String-Form (loadS) wird zu einer Python
            ##Dictionary decodiert
            postjson = json.loads(postjson)
            print("postjson-Variable in request.method =='POST' nach json.loads-Methode:"+str(postjson))
            try:
                ## Zuordnung des Inhalts zu entsprechenden Varibalen
                api_name = postjson['api_name']
                api_data = postjson['api_data']
            except KeyError:
                response = {'response' : 'wrong input try api_name and api_data'}
                ## jsonify von flask kodiert aenlich zu json.dumps die Daten in
                ## ein JSON Objekt, indem es die Daten zusaetzlich mit
                ## status=200 und mimetype='application/json' versieht.
                return jsonify(response)

            ## wenn die api_name in der config auftaucht
            if config.get(api_name, False):
                ## Anfrage an die api_name mit api_data als CORE
                try:
                    REQUEST = httpin.create_message(TO = api_name,
                                                    CORE = api_data)
                    httpin.send(REQUEST)
                    MESSAGE = httpin.receive()
                    test = jsonify(httpin.extract_core(MESSAGE))
                    print("Test: "+str(test))
                    return jsonify(httpin.extract_core(MESSAGE))
                except NameError:
                    response = {'response' : 'unknown input'}
                    return jsonify(response)
                except TypeError:
                    response = {'response' : 'unknown type'}
                    return jsonify(response)
                except KeyError:
                    response = {'response': 'wrong input, try api_name and api_data'}

            else:

                response = {'response' : 'unknown api'}

                return jsonify(response)



        if request.json:
            ## get_json parst die ankommenden JSON Daten und gibt sie aus.
            ## MIME-Typ muss dabei application/json sein, sonst gibt die Methode
            ## None aus. Dies wird mit flask.jsonify (jsonify()) erreicht.?
            postjson = request.get_json()
            # print("postjson-Variable in request.json nach get_json-Methode:"+postjson)
            api_name = postjson['api_name']
            api_data = postjson['api_data']
            print(api_name)

            if config.get(api_name, False):

                try:
                    REQUEST = httpin.create_message(TO = api_name,
                                                    CORE = api_data)
                    httpin.send(REQUEST)
                    MESSAGE = httpin.receive()

                    return jsonify(httpin.extract_core(MESSAGE))
                except NameError:
                    response = {'response' : 'unknown input'}
                    return jsonify(response)
                except TypeError:
                    response = {'response' : 'unknown type'}
                    return jsonify(response)

            else:

                response = {'response' : 'unknown api'}

                return jsonify(response)
    else:
        return render_template('api_request.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
