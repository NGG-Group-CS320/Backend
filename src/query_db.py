#!/usr/bin/python3
#
# Small script to show PostgreSQL and Pyscopg together
#
import psycopg2


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
		# 	LIMIT 10
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
			SELECT writesGt32msPct,writesGt64msPct,writesGt128msPct,writesGt256msPct,writesGt512msPct,writesGt1024msPct,writesGt2048msPct,writesGt4096msPct,writes0_062msPct,writes0_125msPct,writes0_25msPct,writes0_5msPct,writes1msPct,writes2msPct,writes4msPct,writes8msPct,writes16msPct,writes32msPct,writes64msPct,writes128msPct,writes256msPct,writes512msPct,writes1024msPct,writes2048msPct,writes4096msPct,writes8192msPct,writes16384msPct,writes32768msPct,writes65536msPct,reads0_062msPct,reads0_125msPct,reads0_25msPct,reads0_5msPct,reads1msPct,reads2msPct,reads4msPct,reads8msPct,reads16msPct,reads32msPct,reads64msPct,reads128msPct,reads256msPct,reads512msPct,reads1024msPct,reads2048msPct,reads4096msPct,reads8192msPct,reads16384msPct,reads32768msPct,reads65536msPct,cpuLatestTotalAvgPct,portTotalBandwidthMBPS,delAcksPct
			FROM hp
			WHERE systemid = 4
			LIMIT 10
			""")

		# print the results of the query	
		rows = cur.fetchall()
		for row in rows:
			print("   ", row)



		cur.close()
		conn.close()
	except:
		print("Unable to connect to the database")

if __name__ == "__main__":
	main()
