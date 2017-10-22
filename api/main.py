#!/usr/bin/env python

import os, time
import sys
from flask import Flask, request, Response
import json
from dbase import DBase

app = Flask(__name__)


#def validate_found(data):
#	if not data.has_key(''):

# CORS
@app.before_request
def option_autoreply():
	""" Always reply 200 on OPTIONS request """
	if request.method == 'OPTIONS':
		resp = app.make_default_options_response()

		headers = None
		if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
			headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

		h = resp.headers

		h['Access-Control-Allow-Origin'] = request.headers['Origin']
		h['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS"
		h['Access-Control-Max-Age'] = "10000"

		if headers is not None:
			h['Access-Control-Allow-Headers'] = headers

		return resp

@app.after_request
def set_allow_origin(resp):
	h = resp.headers
	if request.method != 'OPTIONS' and 'Origin' in request.headers:
		h['Access-Control-Allow-Origin'] = request.headers['Origin']

	return resp

def errorResponse(code, msg):
	return msg, code

@app.route("/")
def index():
	return "why u here?"

@app.route("/cameras")
def cameras():
	with DBase() as db:
		data = db.getAllCameras()
		result = json.dumps(data)
		return Response(result, mimetype='text/json')

#{'isDogFound': dog_found, 'isCatFound': cat_found, 'url': url, 'image': file_name}
@app.route('/found', methods = ['POST'])
def found():
	data = request.get_json()
	with DBase() as db:
		camera_id = db.getCameraByUrl(data['url'])
		if camera_id is None:
			return errorResponse(400, "camera url is not valid")
		camera_id = camera_id[0] # tuple to int

		animal_type = 'cat'
		if data['isDogFound']:
			animal_type = 'dog'
		image_url = data['image']

		result = db.animalFound(camera_id, animal_type, image_url)

		print(json.dumps(result))
		if result == False:
			return errorResponse(500, "ERROR PROCESSING REQUEST 1000")
	
		animal_requests = db.findActiveRequests(camera_id, animal_type)

		#for animal_request in animal_requests:
			#JJ: TODO: twilio
		return json.dumps(animal_requests)



print("starting program...")

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
