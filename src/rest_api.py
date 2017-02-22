from flask import Flask, jsonify, request
from flask.ext.cors import CORS, cross_origin
from health_score import *
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#send a GET request here
#<IDs> is a comma separated list of system ID's as integers
@app.route('/line/<IDs>', methods=['GET'])
@cross_origin()
def line(IDs):
	#split system ID's into an array
	IDlist = IDs.split(",")
	# pass the array to get the formatted health scores
	systems_info = get_line_graph_json(IDlist)
	# return as in JSON format
	return jsonify(systems_info)


#send a GET request here
#<IDs> is a comma separated list of system ID's as integers
@app.route('/wheel/<IDs>', methods=['GET'])
@cross_origin()
def wheel(IDs):
	#split system ID's into an array
	IDlist = IDs.split(",")
	# pass the array to get the formatted health scores
	systems_info = get_wheel_graph_json(IDlist)
	# return as in JSON format
	return jsonify(systems_info)



if __name__ == "__main__":
    app.run()
