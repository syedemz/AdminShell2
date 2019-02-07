import os



config_windows = {
'HTTPIN': {'identity': b'httpin','url':'tcp://127.0.0.1:5555'},
'HTTPOUT': {'identity': b'httpout','url': 'tcp://127.0.0.1:5556'},
'DATABASE': {'identity': b'database','url': 'tcp://127.0.0.1:5557'},
'SYSTEM': {'identity': b'system','url': 'tcp://127.0.0.1:5558'},
'INTERFACE': {'identity': b'interface','url': 'tcp://127.0.0.1:5559'},
'API_MAINTENANCE': {'identity': b'api_maintenance','url': 'tcp://127.0.0.1:6000'},
'ROBOTER_SERVER': {'identity': b'robotserver','url': 'tcp://127.0.0.1:6001'},
'ROBOTER_GUI': {'identity': b'robo-gui','url': 'tcp://127.0.0.1:6002'},
'ROBOTER_GUI_SHADOW': {'identity': b'robo-gui-shadow','url': 'tcp://127.0.0.1:6003'},
'X_BOX': {'identity': b'x-box','url': 'tcp://127.0.0.1:6004'},



}

config_linux = {
'HTTPIN': {'identity': b'httpin','url':'tcp://127.0.0.1:5555'},
'HTTPOUT': {'identity': b'httpout','url': 'tcp://127.0.0.1:5556'},
'DATABASE': {'identity': b'database','url': 'tcp://127.0.0.1:5557'},
'SYSTEM': {'identity': b'system','url': 'tcp://127.0.0.1:5558'},
'INTERFACE': {'identity': b'interface','url': 'tcp://127.0.0.1:5559'},
'API_MAINTENANCE': {'identity': b'api_maintenance','url': 'tcp://127.0.0.1:6000'},
'ROBOTER_SERVER': {'identity': b'robotserver','url': 'tcp://127.0.0.1:6001'},
'ROBOTER_GUI': {'identity': b'robo-gui','url': 'tcp://127.0.0.1:6002'},
'ROBOTER_GUI_SHADOW': {'identity': b'robo-gui-shadow','url': 'tcp://127.0.0.1:6003'},
'X_BOX': {'identity': b'x-box','url': 'tcp://127.0.0.1:6004'},
}

config = {}

if os.name == 'nt':
    config=config_windows
else:
    config=config_linux
