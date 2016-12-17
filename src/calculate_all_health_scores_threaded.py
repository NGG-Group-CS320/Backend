#!/usr/bin/python3
#
# Script to compute the health scores for each row in the database
#
from threading import Thread
import numpy as np
from health_score import *

'''
NOTE: This script seg faulted after 4 inserts when I ran it.
Fixes should be done before running again.
'''

# get a row of data to use to test the health score function
with make_connection() as conn:
	cur = conn.cursor()

	# fix bug
	cur.execute("SET CLIENT_ENCODING TO 'LATIN1';")

	print("[SELECT] list of all unique systemid's")
	cur.execute("""
		SELECT systemid
		FROM hp
		GROUP BY systemid
		LIMIT 10;
		""")
	all_systemids = cur.fetchall() #length is currently 4519
	all_systemids = [x[0] for x in all_systemids]
	print(np.array(all_systemids))

	def calc_all_health_scores_for_systemid(systemid):
		# print(type(systemid))
		# print(systemid)
		# print(str(systemid))
		# exit(0)

		# get all rows for systemid
		print("[SELECT] rows for systemid {}".format(systemid))
		cur.execute("""
			SELECT writes0_062msPct,writes0_125msPct,writes0_25msPct,writes0_5msPct,writes1msPct,writes2msPct,writes4msPct,writes8msPct,writes16msPct,writes32msPct,writes64msPct,writes128msPct,writes256msPct,writes512msPct,writes1024msPct,writes2048msPct,writes4096msPct,writes8192msPct,writes16384msPct,writes32768msPct,writes65536msPct,reads0_062msPct,reads0_125msPct,reads0_25msPct,reads0_5msPct,reads1msPct,reads2msPct,reads4msPct,reads8msPct,reads16msPct,reads32msPct,reads64msPct,reads128msPct,reads256msPct,reads512msPct,reads1024msPct,reads2048msPct,reads4096msPct,reads8192msPct,reads16384msPct,reads32768msPct,reads65536msPct,systemid,"from","to",cpuLatestTotalAvgPct,portTotalBandwidthMBPS,delAcksPct
			FROM hp
			WHERE systemid = %s;
			""",(str(systemid),))
		rows = cur.fetchall()

		print("[INSERT] health scores for systemid {}".format(systemid))
		for row in rows:
			systemid, from_time, to_time, writes, reads, cpu, bandwidth, delayedAcks = parse_health_inputs_row(row)

			# calculate all scores
			readScore = compute_rs(reads)
			writeScore = compute_ws(writes)
			cbs = compute_cbs(cpu, bandwidth)
			ihs = compute_ihs(writeScore, readScore, cbs, delayedAcks)
			health_score = int(800*ihs)

			cur.execute("""
				INSERT INTO health_scores (systemid, "from", "to", health_score, write_score, read_score, cpu_bandwidth_score, del_ack_score)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",(systemid, from_time, to_time, health_score, writeScore, readScore, cbs, delayedAcks))

		# commit all the inserts
		conn.commit()

	# make all the threads
	threads = [Thread(target = calc_all_health_scores_for_systemid, args = (systemid, )) for systemid in all_systemids]

	# start all the threads
	for thread in threads:
		thread.start()

	# wait for all the threads to finish
	for thread in threads:
		thread.join()
	
	cur.close()

