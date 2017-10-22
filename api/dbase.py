#!/usr/bin/env python
import sys
import json
import mysql.connector

with open('config.json') as config_file:
	global data
	data = json.load(config_file)

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

	def addRequest(self, phone, camera_ids, animal_type, name):
		sql = 'INSERT INTO request (name, phone, animal_type) VALUES (%s, %s, %s)'
		self.cursor.execute(sql, (name, phone, animal_type))
		self.db.commit()
		request_id = self.cursor.lastrowid
		
		for camera_id in camera_ids:
			sql = 'INSERT INTO requestCamera (request_id, camera_id) VALUES (%s, %s)'
			self.cursor.execute(sql, (request_id, camera_id))
			self.db.commit()
		return True

	def setFound(self, phone):
		sql = 'UPDATE request SET found=1 WHERE phone=%s'
		self.cursor.execute(sql, (phone,))
		self.db.commit()
		return True

	def animalFound(self, camera_id, animal_type, image):
		sql = 'INSERT INTO foundanimal (camera_id, type, img) VALUES (%s, %s, %s)'
		result = self.cursor.execute(sql, (camera_id, animal_type, image,))
		self.db.commit()
		return result

	def findActiveRequests(self, camera_id, animal_type):
		if animal_type is 'both':
			sql = 'SELECT r.id as id, r.name as name, r.phone as phone, r.animal_type as animal_type FROM request r INNER JOIN requestCamera rc ON r.id=rc.request_id WHERE r.found=false AND rc.camera_id=%s'
			self.cursor.execute(sql, (camera_id,))
		else:
			sql = 'SELECT r.id as id, r.name as name, r.phone as phone, r.animal_type as animal_type FROM request r INNER JOIN requestCamera rc ON r.id=rc.request_id WHERE r.found=false AND (r.animal_type="both" OR r.animal_type=%s) AND rc.camera_id=%s'
			self.cursor.execute(sql, (animal_type, camera_id,))

		return self.results(self.cursor)


