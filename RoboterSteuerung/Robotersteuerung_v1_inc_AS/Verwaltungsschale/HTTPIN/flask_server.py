from flask import Flask, jsonify, request, render_template
import json

from structure.configuration import config
from structure.module import module


app = Flask(__name__)
httpin = module('HTTPIN', config)



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/apis', methods=['GET','POST'])
def apis():
    if request.method == 'POST':
        if request.form:
            postjson = request.form['JSON']
            postjson = json.loads(postjson)
            api_name = postjson['api_name']
            api_data = postjson['api_data']

            if config.get(api_name, False):
                try:
                    REQUEST = httpin.create_message(TO = api_name, CORE = api_data)
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



        if request.json:
            postjson = request.get_json()
            api_name = postjson['api_name']
            api_data = postjson['api_data']

            if config.get(api_name, False):

                try:
                    REQUEST = httpin.create_message(TO = api_name, CORE = api_data)
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
    app.run(host='0.0.0.0')
