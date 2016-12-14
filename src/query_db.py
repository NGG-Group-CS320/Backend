#!/usr/bin/python3
#
# Script to facilitate querying the data
#
import sys
import psycopg2

class make_connection():
	def __enter__(self):
		try:
			import config
			connection_string = "host='{}' dbname='{}' user='{}' password='{}'".format(config.host, config.dbname, config.user, config.password)
			self.conn = psycopg2.connect(connection_string)
			return self.conn
		except psycopg2.ProgrammingError as e:
			print(e)
			raise
		except:
			print("Error connecting to database: {}".format(sys.exc_info()[0]))
			raise
	def __exit__(self, type, value, traceback):
		self.conn.close()
