#!/usr/bin/python3
#
# Script to compute the health scores for each row in the database
#
import numpy as np
from health_score import *
from math import floor
from time import time

# current_milli_time = lambda: int(round(time() * 1000))


# get a row of data to use to test the health score function
with make_connection() as conn:
	cur = conn.cursor()

	# start_time = current_milli_time()
	print("fetching list of unique systemid's")
	cur.execute("""
		SELECT systemid
		FROM hp
		GROUP BY systemid;
		""")
		# WHERE systemid=251
	all_systemids = cur.fetchall() #length is currently 4519
	all_systemids = [x[0] for x in all_systemids]
	print(np.array(all_systemids))
	# end_time = current_milli_time()

	# print(end_time-start_time, "ms to run")

	# exit(0)

	for systemid in all_systemids:

		# get health score inputs
		print("fetching all rows for systemid {}".format(systemid))
		cur.execute("""
			SELECT writes0_062msPct,writes0_125msPct,writes0_25msPct,writes0_5msPct,writes1msPct,writes2msPct,writes4msPct,writes8msPct,writes16msPct,writes32msPct,writes64msPct,writes128msPct,writes256msPct,writes512msPct,writes1024msPct,writes2048msPct,writes4096msPct,writes8192msPct,writes16384msPct,writes32768msPct,writes65536msPct,reads0_062msPct,reads0_125msPct,reads0_25msPct,reads0_5msPct,reads1msPct,reads2msPct,reads4msPct,reads8msPct,reads16msPct,reads32msPct,reads64msPct,reads128msPct,reads256msPct,reads512msPct,reads1024msPct,reads2048msPct,reads4096msPct,reads8192msPct,reads16384msPct,reads32768msPct,reads65536msPct,systemid,"from","to",cpuLatestTotalAvgPct,normalizedBandwidth,delAcksPct
			FROM hpnmb
			WHERE systemid = %s;
			""",(systemid,))

		rows = cur.fetchall()
		print("  calculating & inserting health scores for systemid {}".format(systemid))

		from tqdm import tqdm
		for row in tqdm(rows):
			systemid, from_time, to_time, writes, reads, cpu, bandwidth, delayedAcks = parse_health_inputs_row(row)

			# calculate all scores
			readScore = compute_rs(reads)
			writeScore = compute_ws(writes)
			cbs = compute_cbs(cpu, bandwidth)
			ihs = compute_ihs(writeScore, readScore, cbs, delayedAcks)

			def scale(x):
				return floor(x*800)

			health_score = scale(ihs)


			cur.execute("""
				INSERT INTO health_scores (systemid, "from", "to", health_score, write_score, read_score, cpu_bandwidth_score, del_ack_score)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
				(systemid, from_time, to_time, health_score, scale(writeScore), scale(readScore), scale(cbs), scale(delayedAcks)))
			# cur.execute("""
			# 	UPDATE health_scores
			# 	SET systemid=%s, "from"=%s, "to"=%s, health_score=%s, write_score=%s, read_score=%s, cpu_bandwidth_score=%s, del_ack_score=%s""",
			# 	(systemid, from_time, to_time, health_score, scale(writeScore), scale(readScore), scale(cbs), scale(delayedAcks)))

		conn.commit()
	
	cur.close()

