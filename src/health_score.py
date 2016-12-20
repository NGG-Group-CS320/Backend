#!/usr/bin/python3
#
# Script to compute health scores given storage system information
#
import numpy as np
from query_db import make_connection

"""
Let c be a 21-dimensional vector defined as <21/21, 20/21, 19/21, 18/21, ..., 3/21, 2/21, 1/21>.
Create a 21-dimensional vector w from the fields of the form writes*msPct ordered from smallest to greatest time.
Create a 21-dimensional vector r from the fields of the form reads*msPct ordered from smallest to greatest time.
Let ws=wc and rs=rc. We call ws and rs the write score and read score respectively.
Compute cbs=dist((cpu, nbw), (1, 0))/sqrt(2)=sqrt((1-cpu)^2+nbw^2)/2) where cpu corresponds to cpuLatestTotalAvgPct and nbw corresponds to portTotalBandwidthMBPS normalized by the maximum value of portTotalBandwidthMBPS seen for the particular system at hand. We call this the CPU-bandwidth score. If nbw would be undefined, we use nbw=1 in computing cbs.
Compute the interim health score ihs=<ws, rs, cbs, 1-da><0.45, 0.25, 0.2, 0.1> on the range [0, 1] where da is the delAckPct.
The resulting health score is floor(800*ihs) yielding a value on the range [0, 800].
"""
weights = [0.45, 0.25, 0.2, 0.1]
c = np.arange(21, 0, -1) / 21
write_weights = c
read_weights = c


# return the color associated with each given score range
def score_to_color(score):
	color = "#000000"
	if 0 <= score <= 99:
		color = "#c0392b"
	elif 100 <= score <= 199:
		color = "#e74c3c"
	elif 200 <= score <= 299:
		color = "#d35400"
	elif 300 <= score <= 399:
		color = "#e67e22"
	elif 400 <= score <= 499:
		color = "#f39c12"
	elif 500 <= score <= 599:
		color = "#f1c40f"
	elif 600 <= score <= 699:
		color = "#2ecc71"
	elif 700 <= score <= 799:
		color = "#27ae60"
	return color


def compute_health_score(writes, reads, cpu, bandwidth, delayedAcks):
	# calculate all scores
	readScore = compute_rs(reads)
	print("Read score: {:.4}".format(readScore))

	writeScore = compute_ws(writes)
	print("Write score: {:.4}".format(writeScore))

	cbs = compute_cbs(cpu, bandwidth)
	print("CPU-Bandwidth score: {:.4}".format(cbs))

	print("Delayed Acks: {:.4}".format(delayedAcks))

	ihs = compute_ihs(writeScore, readScore, cbs, delayedAcks)
	print("Interim Health score: {:.4}".format(ihs))

	return int(800*ihs)


# calculate Interim Health score
def compute_ihs(ws, res, cps, daPct):
	return np.dot([ws, res, cps, 1 - daPct], weights)


# calculate CPU-Bandwidth score
def compute_cbs(cpuPct, bwPct):
	return np.sqrt(((1 - cpuPct) ** 2 + bwPct ** 2) / 2)


# calculate Read score
def compute_rs(readScores):
	return np.dot(readScores, read_weights)


# calculate Write score
def compute_ws(writeScores):
	return np.dot(writeScores, write_weights)


# get a row of data to use to test the health score function
def get_test_health_inputs_row():
	with make_connection() as conn:
		cur = conn.cursor()
		# get health score inputs
		cur.execute("""
			SELECT writes0_062msPct,writes0_125msPct,writes0_25msPct,writes0_5msPct,writes1msPct,writes2msPct,writes4msPct,writes8msPct,writes16msPct,writes32msPct,writes64msPct,writes128msPct,writes256msPct,writes512msPct,writes1024msPct,writes2048msPct,writes4096msPct,writes8192msPct,writes16384msPct,writes32768msPct,writes65536msPct,reads0_062msPct,reads0_125msPct,reads0_25msPct,reads0_5msPct,reads1msPct,reads2msPct,reads4msPct,reads8msPct,reads16msPct,reads32msPct,reads64msPct,reads128msPct,reads256msPct,reads512msPct,reads1024msPct,reads2048msPct,reads4096msPct,reads8192msPct,reads16384msPct,reads32768msPct,reads65536msPct,systemid,"from","to",cpuLatestTotalAvgPct,portTotalBandwidthMBPS,delAcksPct
			FROM hp
			LIMIT 1
			""")

		rows = cur.fetchall()
		cur.close()
		row = rows[0]
		return row


# parses query results into variables to be used to compute health score
def parse_health_inputs_row(row):
	# extract the fields from the row
	writes, reads, systemid, from_time, to_time, cpu, bandwidth, delayedAcks = row[0:21], row[21:21+21], row[-6], row[-5], row[-4], row[-3], row[-2], row[-1]
	writes = [float(x) for x in writes]
	reads = [float(x) for x in reads]
	cpu, bandwidth, delayedAcks = float(cpu), float(bandwidth), float(delayedAcks)

	# change the percentages to be in the range [0,1] instead of [0,100]
	reads = np.array(reads) / 100
	writes = np.array(writes) / 100
	cpu, bandwidth, delayedAcks = cpu/100, bandwidth/100, delayedAcks/100

	return systemid, from_time, to_time, writes, reads, cpu, bandwidth, delayedAcks



# returns all the rows containing the ID's in IDlist
# columns are from, to, health_score
def get_health_scores(IDlist):
	with make_connection() as conn:
		cur = conn.cursor()
		import time
		def to_unix_time(from_time):
			return str(int(time.mktime(from_time.timetuple())))

		def get_system_rows(systemID):
			cur.execute("""
				SELECT "from",health_score
				FROM health_scores
				WHERE systemid={};
				""".format(systemID))
			systems_info = cur.fetchall()
			systems_info = [{"time":to_unix_time(x[0]),"score":str(x[1])} for x in systems_info]
			return systems_info


		systems_info = [{"id":systemID,"name":"System {}".format(systemID),"data":get_system_rows(systemID)} for systemID in IDlist]
		
		cur.close()
		return systems_info



# main function for the purpose of testing
def main():
	row = get_test_health_inputs_row() #note: this function will have to be removed at some point
	systemid, from_time, to_time, writes, reads, cpu, bandwidth, delayedAcks = parse_health_inputs_row(row)
	
	print(type(from_time))
	print(from_time)
	unixtime = time.mktime(d.timetuple())

	# print("systemid: {}\nfrom_time: {}\nto_time: {}\nwrites: {}\nreads: {}\ncpu: {}\nbandwidth: {}\ndelayedAcks".format(systemid, from_time, to_time, writes, reads, cpu, bandwidth, delayedAcks))
	# print("systemid: {}\nfrom_time: {}\nto_time: {}\nwrites: {}\nreads: {}\ncpu: {}\nbandwidth: {}\ndelayedAcks".format(systemid, from_time, to_time, np.sum(writes), np.sum(reads), cpu, bandwidth, delayedAcks))

	# score = compute_health_score(writes, reads, cpu, bandwidth, delayedAcks)
	# print("This system has a health score of {}/800 (higher is healthier)".format(score))

if __name__ == "__main__":
	main()
