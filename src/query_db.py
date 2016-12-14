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


# parses query results into variables to be used to compute health score
def parse_health_inputs_row(row):
	systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks = row[0], row[1], row[2:2+21], row[2+21:2+21+21], row[-3], row[-2], row[-1]
	writes = [float(x) for x in writes]
	reads = [float(x) for x in reads]
	cpu, bandwidth, delayedAcks = float(cpu), float(bandwidth), float(delayedAcks)
	return systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks


# get a row of data to use to test the health score function
def get_test_health_inputs_row():
	with make_connection() as conn:
		cur = conn.cursor()
		# get health score inputs
		cur.execute("""
			SELECT systemid,"from",writes0_062msPct,writes0_125msPct,writes0_25msPct,writes0_5msPct,writes1msPct,writes2msPct,writes4msPct,writes8msPct,writes16msPct,writes32msPct,writes64msPct,writes128msPct,writes256msPct,writes512msPct,writes1024msPct,writes2048msPct,writes4096msPct,writes8192msPct,writes16384msPct,writes32768msPct,writes65536msPct,reads0_062msPct,reads0_125msPct,reads0_25msPct,reads0_5msPct,reads1msPct,reads2msPct,reads4msPct,reads8msPct,reads16msPct,reads32msPct,reads64msPct,reads128msPct,reads256msPct,reads512msPct,reads1024msPct,reads2048msPct,reads4096msPct,reads8192msPct,reads16384msPct,reads32768msPct,reads65536msPct,cpuLatestTotalAvgPct,portTotalBandwidthMBPS,delAcksPct
			FROM hp
			LIMIT 1
			""")

		rows = cur.fetchall()
		row = rows[0]
		return row


# print(get_test_health_inputs_row())
