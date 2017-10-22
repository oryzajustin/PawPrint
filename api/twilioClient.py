#!/usr/bin/env python
import sys
import json
from twilio.rest import Client, TwilioRestClient
import requests
import urllib.parse

with open('config.json') as config_file:
	global data
	data = json.load(config_file)

class TwilioClient:
	def __init__(self):
		self.client = Client(data['TWILIO']['ACCOUNT_SID'], data['TWILIO']['AUTH_TOKEN'])
	
	def sendSms(self, message, number):
		self.client.messages.create(to = number, from_= data['TWILIO']['NUMBER'], body= message)

	def sendMediaSms(self, message, number, img_url):
		self.client.messages.create(to = number, from_= data['TWILIO']['NUMBER'], body= message, media_url = img_url)

	def validatePhone(self, phone):
		url = 'https://lookups.twilio.com/v1/PhoneNumbers/' + urllib.parse.quote_plus(phone)
		r = requests.get(url, auth=(data['TWILIO']['ACCOUNT_SID'], data['TWILIO']['AUTH_TOKEN']))
		return r.status_code == 200

