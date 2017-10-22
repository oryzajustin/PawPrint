#!/usr/bin/env python
import sys
import json
from twilio.rest import Client, TwilioRestClient
from credentials import account_sid, auth_token, my_number, twilio_number

class TwilioClient:
	def __init__(self):
		self.client = Client(account_sid, auth_token)
	
	def sendSms(self, message, number):
		self.client.messages.create(to = number, from_= twilio_number, body= message)

	def sendMediaSms(self, message, number, img_url):
		self.client.messages.create(to = number, from_= twilio_number, body= message, media_url = img_url)
