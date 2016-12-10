#!/usr/bin/python3
#
# Small script to show PostgreSQL and Pyscopg together
#
import sys
import psycopg2


# parses query results into variables to be used to compute health score
def parse_health_inputs_row(row):
	systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks = row[0], row[1], row[2:2+21], row[2+21:2+21+21], row[-3], row[-2], row[-1]
	writes = [float(x) for x in writes]
	reads = [float(x) for x in reads]
	return systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks


def get_test_health_inputs_row():
	try:
		import config
		connection_string = "host='{}' dbname='{}' user='{}' password='{}'".format(config.host, config.dbname, config.user, config.password)
		conn = psycopg2.connect(connection_string)
		cur = conn.cursor()

		# get health score inputs
		cur.execute("""
			SELECT systemid,"from",writes0_062msPct,writes0_125msPct,writes0_25msPct,writes0_5msPct,writes1msPct,writes2msPct,writes4msPct,writes8msPct,writes16msPct,writes32msPct,writes64msPct,writes128msPct,writes256msPct,writes512msPct,writes1024msPct,writes2048msPct,writes4096msPct,writes8192msPct,writes16384msPct,writes32768msPct,writes65536msPct,reads0_062msPct,reads0_125msPct,reads0_25msPct,reads0_5msPct,reads1msPct,reads2msPct,reads4msPct,reads8msPct,reads16msPct,reads32msPct,reads64msPct,reads128msPct,reads256msPct,reads512msPct,reads1024msPct,reads2048msPct,reads4096msPct,reads8192msPct,reads16384msPct,reads32768msPct,reads65536msPct,cpuLatestTotalAvgPct,portTotalBandwidthMBPS,delAcksPct
			FROM hp
			LIMIT 1
			""")

		rows = cur.fetchall()
		row = rows[0]

		cur.close()
		conn.close()

		return row
	except psycopg2.ProgrammingError as e:
		print(e)
		raise
	except:
		print("Error connecting to database: {}".format(sys.exc_info()[0]))
		raise


def main():
	try:
		# connect to the postgres database
		import config
		connection_string = "host='{}' dbname='{}' user='{}' password='{}'".format(config.host, config.dbname, config.user, config.password)
		conn = psycopg2.connect(connection_string)
		cur = conn.cursor()

		
		# run a test query
		# cur.execute("""
		# 	SELECT *
		# 	from hp
		# 	LIMIT 1
		# 	""")

		# get statistics
		# cur.execute("""
		# 	SELECT systemid, min(delackspct), max(delackspct), stddev(delackspct), avg(delackspct)
		# 	FROM hp
		# 	GROUP BY systemid
		# 	LIMIT 10
		# 	""")

		# get health score inputs
		cur.execute("""
			SELECT systemid,"from",writes0_062msPct,writes0_125msPct,writes0_25msPct,writes0_5msPct,writes1msPct,writes2msPct,writes4msPct,writes8msPct,writes16msPct,writes32msPct,writes64msPct,writes128msPct,writes256msPct,writes512msPct,writes1024msPct,writes2048msPct,writes4096msPct,writes8192msPct,writes16384msPct,writes32768msPct,writes65536msPct,reads0_062msPct,reads0_125msPct,reads0_25msPct,reads0_5msPct,reads1msPct,reads2msPct,reads4msPct,reads8msPct,reads16msPct,reads32msPct,reads64msPct,reads128msPct,reads256msPct,reads512msPct,reads1024msPct,reads2048msPct,reads4096msPct,reads8192msPct,reads16384msPct,reads32768msPct,reads65536msPct,cpuLatestTotalAvgPct,portTotalBandwidthMBPS,delAcksPct
			FROM hp
			LIMIT 1
			""")

		# print the results of the query	
		rows = cur.fetchall()
		# for row in rows:
		# 	print("   ", row)

		row = rows[0]
		# print(row)
		systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks = parse_health_inputs_row(row)
		print("systemid: {}\ntimestamp: {}\nwrites: {}\nreads: {}\ncpu: {}\nbandwidth: {}\ndelayedAcks: {}".format(systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks))


		cur.close()
		conn.close()
	except psycopg2.ProgrammingError as e:
		print(e)
	except:
		print("Error connecting to database: {}".format(sys.exc_info()[0]))

if __name__ == "__main__":
	main()
