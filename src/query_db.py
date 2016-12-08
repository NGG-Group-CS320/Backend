#!/usr/bin/python3
#
# Small script to show PostgreSQL and Pyscopg together
#

import psycopg2



def main():
	try:
		import config
		connection_string = "host='{}' dbname='{}' user='{}' password='{}'".format(config.host, config.dbname, config.user, config.password)
		conn = psycopg2.connect(connection_string)
		cur = conn.cursor()

		
		# run a test query
		# cur.execute("""SELECT * from hp LIMIT 10""")

		# get statistics
		cur.execute("""SELECT systemid, min(delackspct), max(delackspct), stddev(delackspct), avg(delackspct) FROM hp GROUP BY systemid LIMIT 10""")
		
		rows = cur.fetchall()
		# print(rows)
		print("\nShow me the databases:\n")
		for row in rows:
			print("   ", row)

		# print(rows[0])

	except:
		print("Unable to connect to the database")

if __name__ == "__main__":
	main()
