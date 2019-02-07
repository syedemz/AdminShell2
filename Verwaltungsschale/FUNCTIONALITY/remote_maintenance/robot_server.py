    # -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:17:20 2017

@author: Denis

THIS IS THE SERVER WHICH IS NECESSARY TO RUN THE REMOTE MAINTENANCE PLATFORM
THIS PYTHON SCRIPT IS DIVDED INTO 5 MAIN PARTS


1) IMPORT LIBRARIES
2) ACCOUNT DATA
3) WEBPAGE BUILD
4) WEBPAGES STILL WORK IN PROGRESS
5) DEFINING PORT

you can use the search function to jump directly to the required chapter

"""


#######################################################################################################
""""""""""""""""""" 3) CORS DECORATOR """""""""""""""""""""""""""""""""""""""
#######################################################################################################




from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper




try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

#######################################################################################################
""""""""""""""""""" 1) IMPORT LIBRARIES """""""""""""""""""""""""""""""""""""""
#######################################################################################################



#from flask import Flask, request
from flask import Flask, render_template, jsonify  #, url_for
import json, io, os
#from flask_cors import CORS, cross_origin

#from structure import config, module

#COM_module = module.entity('HTML_APP', config.data)


try:
    to_unicode = unicode
except NameError:
    to_unicode = str




#######################################################################################################
""""""""""""""""""" 3) WEBPAGE BUILD """""""""""""""""""""""""""""""""""""""
#######################################################################################################
import sys

curdir = os.path.abspath(os.path.dirname(__file__))
topdir = os.path.abspath(os.path.join(curdir, os.pardir))
if topdir not in sys.path:
	sys.path.insert(0, topdir)

from robot_control import robot_control
from configuration import config
from module import module

# use flask module

app = Flask(__name__)
robotserver = module('REMOTE_MAINTENANCE', config)

""" Login homepage """
@app.route('/')
@crossdomain(origin='*')
def login_robot():
    return render_template('Login.html')


#### important for robot remote control: get requests are processed here
@app.route('/bosch2.html/query', methods=['GET'])
@crossdomain(origin='*')
def bosch2_query():
    with open(os.getcwd()+'/data/data.json') as data_file:
        json_data = json.load(data_file)
        a0 = request.args.get('a0_1000', False, type=int)/1000
        a1 = request.args.get('a1_1000', False, type=int)/1000
        a2 = request.args.get('a2_1000', False, type=int)/1000
        b0 = request.args.get('b0_1000', False, type=int)/1000
        c0 = request.args.get('c0_1000', False, type=int)/1000
        grab_close_ratio =( request.args.get('slider_ratio_1000', False, type=int)/1000)
        json_data['a0']=a0
        json_data['a1']=a1
        json_data['a2']=a2
        json_data['b0']=b0
        json_data['c0']=c0
        json_data['grab_close_ratio']=grab_close_ratio
        with io.open('data/data.json', 'w', encoding='utf8') as outfile:
            outfile.write(to_unicode(json.dumps(json_data)))
            #return(robot_control(2,b0,a0,a1,a2,c0,grab_close_ratio))
            #return("hi")
            return(jsonify(json_data))

global a0
global a1
global a2
global b0
global c0
global grab_close_ratio
global view
global json_data

@app.route('/control', methods=['GET'])
@crossdomain(origin='*')
def control():
    with open(os.getcwd()+'/data/data.json') as data_file:
        json_data = json.load(data_file)
        view = 0;
        view = request.args.get('view', False, type=int)
        if view ==1:
            a0 = request.args.get('a0_1000', False, type=int)/1000
            a1 = request.args.get('a1_1000', False, type=int)/1000
            a2 = request.args.get('a2_1000', False, type=int)/1000
            json_data['a0']=a0
            json_data['a1']=a1
            json_data['a2']=a2
        elif view ==2:
            b0 = request.args.get('b0_1000', False, type=int)/1000
            json_data['b0']=b0
        elif view ==3:
            c0 = request.args.get('c0_1000', False, type=int)/1000
            grab_close_ratio = request.args.get('slider_ratio', False, type=int)/1000
            json_data['c0']=c0
            json_data['grab_close_ratio']=grab_close_ratio
        with io.open('data/data.json', 'w', encoding='utf8') as outfile:
            outfile.write(to_unicode(json.dumps(json_data)))
            a0=json_data['a0']
            a1=json_data['a1']
            a2=json_data['a2']
            b0=json_data['b0']
            c0=json_data['c0']
            grab_close_ratio=json_data['grab_close_ratio']
            a = robot_control(2,b0,a0,a1,a2,c0,grab_close_ratio)
            REQUEST = robotserver.create_message(TO = 'API_ROBOTARM', CORE = a)
            robotserver.send(REQUEST)
#            MESSAGE = robotserver.receive()
            #print(robot_control(2,b0,a0,a1,a2,c0,grab_close_ratio))
            #return(robot_control(2,b0,a0,a1,a2,c0,grab_close_ratio))
            #return("hi")
            return(jsonify(json_data))

@app.route('/testfunction', methods=['GET'])
def testfunction():
    REQUEST = robotserver.create_message(TO = 'API_ROBOTARM', CORE = {"request":"current position"})
    robotserver.send(REQUEST)
    MESSAGE = robotserver.receive()
    return jsonify(robotserver.extract_core(MESSAGE))


@app.route('/current_position', methods=['GET'])
@crossdomain(origin='*')
def current_position():

    with open(os.getcwd()+'/data/data.json') as data_file:
        json_data = json.load(data_file)
        return(jsonify(json_data))

@app.route('/control_start', methods=['GET'])
@crossdomain(origin='*')
def control_start():
    with open(os.getcwd()+'/data/data.json') as data_file:
        json_data = json.load(data_file)
        with open(os.getcwd()+'/data/position.json') as data_file:
            position = json.load(data_file)
            json_data['a0']=position['a0']
            json_data['a1']=position['a1']
            json_data['a2']=position['a2']
            json_data['b0']=position['b0']
            json_data['c0']=position['c0']
            json_data['grab_close_ratio']=position['grab_close_ratio']
            with io.open('data/data.json', 'w', encoding='utf8') as outfile:
                outfile.write(to_unicode(json.dumps(json_data)))
                return (jsonify(json_data))
                #return(robot_control(1,0,0,0,0,0,0))

@app.route('/control_start_command', methods=['GET'])
@crossdomain(origin='*')
def control_start_command():

    REQUEST = robotserver.create_message(TO = 'API_ROBOTARM', CORE = '20')
    robotserver.send(REQUEST)
    MESSAGE = robotserver.receive()

    a = robot_control(1,0,0,0,0,0,0)
#    REQUEST = robotserver.create_message(TO = 'ROBO_GUI', CORE = {"request":a})
    REQUEST = robotserver.create_message(TO = 'API_ROBOTARM', CORE = a)
    robotserver.send(REQUEST)
#    MESSAGE = robotserver.receive()
    #print(robot_control(1,0,0,0,0,0,0))
    return(robot_control(1,0,0,0,0,0,0))


@app.route('/control_stop', methods=['GET'])
@crossdomain(origin='*')
def control_stop():
    a = robot_control(3,0,0,0,0,0,0)
    REQUEST = robotserver.create_message(TO = 'API_ROBOTARM', CORE = a)
    robotserver.send(REQUEST)
#    MESSAGE = robotserver.receive()
    #print(robot_control(3,0,0,0,0,0,0))
    return(robot_control(3,0,0,0,0,0,0))

global username
global password

username=["admin"]
password=["123"]


@app.route('/robot_login.html', methods=['POST'])
@crossdomain(origin='*')
def robot_login_data():
    global input_username
    global input_password
    input_username=request.form['username']
    input_password=request.form['password']
    try:
        global a
        a=int(username.index(input_username))
        if input_password==password[a]:
                    global login_check
                    login_check=True
                    return render_template('bosch4.html')
    except ValueError:
        return render_template('wrong_Login.html', username="Wrong username and/or password")


""" bosch 2  """
@app.route('/bosch4.html', methods=['GET','POST'])
@crossdomain(origin='*')
def bosch4():
    if login_check==True:
        return render_template('bosch4.html')


@app.route('/bosch4_top.html', methods=['GET','POST'])
@crossdomain(origin='*')
def bosch4_top():
    if login_check==True:
        return render_template('bosch4_top.html')

@app.route('/bosch4_grab.html', methods=['GET','POST'])
@crossdomain(origin='*')
def bosch4_grab():
    if login_check==True:
        return render_template('bosch4_grab.html')

@app.route('/position',  methods=['GET'])
@crossdomain(origin='*')
def position():
    with open(os.getcwd()+'/data/position.json') as position_file:
        position = json.load(position_file)
        return (jsonify(position))



@app.route('/get_sensor_data',  methods=['GET'])
@crossdomain(origin='*')
def get_sensor_data():
    results=[]
    filename = request.args.get('filename', False, type=str)
    with open(os.getcwd()+'/data/'+filename+'.txt','r') as data_file:
        for line in data_file:
            current_line = line.split(',')
            current_line = list(map(float, current_line))
            results.append(current_line)
    string_sensor_data=str(results)
    return (string_sensor_data)
    #return ("hi")



#######################################################################################################
""""""""""""""""""" 5) DEFINING PORT """""""""""""""""""""""""""""""""""""""
#######################################################################################################

# Run the app :)
if __name__=="__main__":
    app.run("", port=40000)
