#!/usr/bin/env python

import os, time
import sys
from flask import Flask, request, Response
import json
from dbase import DBase
from twilioClient import TwilioClient
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
twilio_client = TwilioClient()

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

@app.route("/request", methods = ['POST'])
def requestTrack():
	data = request.get_json()
	camera_ids = data['cameraids']
	name = data['name']
	phone = "+1" + data['phone']
	animal_type = data['pet']
	
	# Phone number verification
	if not twilio_client.validatePhone(phone):
		return errorResponse(400, "Phone is not valid. Please have it in the format of '1234567890'")

	with DBase() as db:
		result = db.addRequest(phone, camera_ids, animal_type, name)
		return json.dumps({'success': result})

@app.route('/sms', methods = ['POST'])
def sms():
	response = MessagingResponse()
	body = request.values.get('Body', None)

	if(body.lower() == 'stop' or body.lower() == 's'):
		with DBase() as db:
			phone = request.values.get('From', None) #FIXED: not working
			if db.setFound(phone):
				response.message("Okay. Bye")
	else:
		response.message("Please enter 'Stop' if you want to stop receiving messages.")

	return str(response)

@app.route('/found', methods = ['POST'])
def found():
	data = request.get_json()
	with DBase() as db:
		camera_id = db.getCameraByUrl(data['url'])
		if camera_id is None:
			return errorResponse(400, "camera url is not valid")
		camera_id = camera_id[0] # tuple to int

		animal_type = None
		if data['isDogFound'] and data['isCatFound']:
			animal_type = 'both'
		elif data['isDogFound']:
			animal_type = 'dog'
		elif data['isCatFound']:
			animal_type = 'cat'
		else:
			return errorResponse(400, "no animal found yo")

		image_url = data['image']

		result = db.animalFound(camera_id, animal_type, image_url)

		if result == False:
			return errorResponse(500, "ERROR PROCESSING REQUEST 1000")

		animal_requests = db.findActiveRequests(camera_id, animal_type)

		for animal_request in animal_requests:
			message = 'found yo animal bro.'
			#JJ: TODO animal_request['name'], animal_request['animal_type']
			global twilio_client
			twilio_client.sendMediaSms(message, animal_request['phone'], image_url)
			db.setFound(animal_request['phone']) #FIXME: Don't set animal to found here....
		return json.dumps(animal_requests)

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
