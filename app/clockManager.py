import json
import os
import sys
from flask import jsonify

def getConfigurations():

	with open("/var/www/clockwerxWS/conf/clockDefs.json", 'r') as json_file:
		data = json.load(json_file)
		return jsonify( data)

