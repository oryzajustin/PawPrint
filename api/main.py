#!/usr/bin/env python

import os, time
import sys
from flask import Flask, request, Response
import json
from dbase import DBase

app = Flask(__name__)


#def validate_found(data):
#	if not data.has_key(''):


@app.route("/")
def index():
	return "Hello World!"

@app.route("/cameras")
def cameras():
	with DBase() as db:
		data = db.getAllCameras()
		result = json.dumps(data)
		return Response(result, mimetype='text/json')

@app.route('/found', methods = ['POST'])
def found():
	data = request.get_json()
	
	# Validation
	validate_found(data)
	#print(data)
	return "Post World!" + str(data)

print("starting program...")

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
