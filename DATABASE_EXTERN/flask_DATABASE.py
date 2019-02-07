from flask import Flask, jsonify
from external_database_functions import tagIterator_extern, get_add_data, get_asset_data

app_DB = Flask(__name__)
# app_DB.config['DEBUG']=True

@app_DB.route('/', methods = ['GET'])
def welcome():
    return 'Welcome to the External-Database.'

@app_DB.route('/database/availableAdds', methods = ['GET'])
def getAvailableAdds():
    response = tagIterator_extern(xml_file = 'add_directory.xml',
                                  asset_name = None)
    return jsonify(response)

@app_DB.route('/database/assets/<asset_id>', methods = ['GET'])
def getAssetData(asset_id):
    response = get_asset_data(asset_id)
    return jsonify(response)

@app_DB.route('/database/adds/<add_id>', methods = ['GET'])
def getAddData(add_id):
    response = get_add_data(add_id)
    return jsonify(response)

if __name__ == "__main__":
	app_DB.run(host='0.0.0.0', port=5001)
