from flask import Flask, jsonify, request
from health_score import *
app = Flask(__name__)


@app.route('/line/<IDs>', methods=['GET'])
def line(IDs):
	IDlist = IDs.split(",")

	systems_info = get_health_scores(IDlist)

	return jsonify(systems_info)



if __name__ == "__main__":
    app.run()