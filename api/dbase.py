#!/usr/bin/env python
import sys
import json
import mysql.connector

with open('config.json') as config_file:
	global data
	data = json.load(config_file)

print(data)

class DBase:
	db = None

	def __init__(self):
		self.db = mysql.connector.connect(
			host=data['DB']['SERVER'],
			user=data['DB']['USER'],
			password=data['DB']['PASSWORD'],
			database=data['DB']['SCHEMA']
		)
		self.cursor = self.db.cursor()

	def results(self, cursor):
		columns = cursor.description 
		result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
		return result

	def __enter__(self):
		return DBase()

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.db:
			self.db.close()

	def getOne(self, sql):
		self.cursor.execute(sql)
		return self.cursor.fetchone()

	def getAll(self, sql):
		self.cursor.execute(sql)
		return self.results(self.cursor)
		#JJ: make sure this works
		#columns = self.cursor.description 
		#result = [{columns[index][0]:column for index, column in enumerate(value)} for value in self.cursor.fetchall()]
		#return result
		#return self.cursor.fetchall()

	def rows(self):
		return self.cursor.rowcount

	def getAllCameras(self):
		sql = 'SELECT * FROM camera'
		return self.getAll(sql)

	def getCameraByUrl(self, url):
		sql = 'SELECT id FROM camera WHERE url=%s'
		self.cursor.execute(sql, (url,))
		result = self.cursor.fetchone()
		return result

	#JJ: getCamera(self, id)

	#JJ: def getFound(self, slug):

	#JJ: def saveRequest(self, request_data)

	#JJ: def findCameraWithinBounds(self, bound_north, bound_south, bound_east, bound_west):

	#JJ: def setFound(self, slug)

	def animalFound(self, camera_id, animal_type, image):
		sql = 'INSERT INTO foundanimal (camera_id, type, img) VALUES (%s, %s, %s)'
		result = self.cursor.execute(sql, (camera_id, animal_type, image,))
		self.db.commit()
		return result

	def findActiveRequests(self, camera_id, animal_type):
		sql = 'SELECT r.id, r.name, r.phone, r.animal_type FROM request r INNER JOIN requestCamera rc ON r.id=rc.request_id WHERE r.found=false AND r.animal_type=%s AND rc.camera_id=%s'
		self.cursor.execute(sql, (animal_type, camera_id,))
		return self.results(self.cursor)


