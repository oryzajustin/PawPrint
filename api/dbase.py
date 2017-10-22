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

	def __enter__(self):
		return DBase()

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.db:
			self.db.close()

	def getOne(self,sql):
		self.cursor.execute(sql)
		return self.cursor.fetchone()

	def getAll(self, sql):
		self.cursor.execute(sql)
		columns = self.cursor.description 
		result = [{columns[index][0]:column for index, column in enumerate(value)} for value in self.cursor.fetchall()]
		return result
		#return self.cursor.fetchall()

	def rows(self):
		return self.cursor.rowcount

	def getAllCameras(self):
		sql = 'SELECT * FROM camera'
		return self.getAll(sql)

