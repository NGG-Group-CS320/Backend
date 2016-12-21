#!/usr/bin/python3
#
# Script to compute health scores given storage system information
#
from time import time
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
c = np.arange(21, 0, -1) / 20
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


# parses query results into variables to be used to compute health score
def parse_health_inputs_row(row):
	# extract the fields from the row
	writes, reads, systemid, from_time, to_time, cpu, bandwidth, delayedAcks = row[0:21], row[21:21+21], row[-6], row[-5], row[-4], row[-3], row[-2], row[-1]
	if bandwidth is None:
		bandwidth = 0
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
def get_line_graph_json(IDlist):
	#set up a connection
	with make_connection() as conn:
		cur = conn.cursor()

		#convert the verbose timestamp to unix time
		import time
		def to_unix_time(from_time):
			return str(int(time.mktime(from_time.timetuple())))

		#function for getting from_time and health_score given a system ID
		def get_system_rows(systemID):
			cur.execute("""
				SELECT "from",health_score
				FROM health_scores
				WHERE systemid={};
				""".format(systemID))
			systems_info = cur.fetchall()
			#format into dictionary
			systems_info = [{"time":to_unix_time(x[0]),"score":str(x[1])} for x in systems_info]
			return systems_info

		#format into better dictionary
		systems_info = [{"id":systemID,"name":"System {}".format(systemID),"data":get_system_rows(systemID)} for systemID in IDlist]
		
		cur.close()
		return systems_info


# returns all the rows containing the ID's in IDlist
# columns are from, to, health_score
def get_wheel_graph_json(IDlist):
	#set up a connection
	with make_connection() as conn:
		cur = conn.cursor()

		cur.execute("""
			SELECT hs.*
			FROM
				(SELECT systemid, max("from") AS maxDate
				FROM health_scores
				GROUP BY systemid) m, health_scores hs
			WHERE m.systemid=hs.systemid AND m.maxDate=hs."from" AND ({})
			ORDER BY health_score ASC;
			""".format(" OR ".join(["hs.systemid={}".format(x) for x in IDlist])))

		systems_info = cur.fetchall()

		#format into dictionary
		def make_row_tuple(row):
			systemid, from_time, to_time, health_score, write_score, read_score, cpu_bandwidth_score, del_ack_score = row

			return {
						"id": systemid,
						"name": "System {}".format(systemid),
						"color": "#{}".format(score_to_color(health_score)),
						"score": str(health_score),
						"writeScore": write_score,
						"readScore": read_score,
						"cbScore": cpu_bandwidth_score,
						"delAckPct": del_ack_score
					}

		systems_info = [make_row_tuple(row) for row in systems_info]

		bin1 = [system for system in systems_info if   0 <= int(system["score"]) <= 199]
		bin2 = [system for system in systems_info if 200 <= int(system["score"]) <= 399]
		bin3 = [system for system in systems_info if 400 <= int(system["score"]) <= 599]
		bin4 = [system for system in systems_info if 600 <= int(system["score"]) <= 800]

		results = [
			{"name":"0-400","children":
				[
					{"name":"0-200","children":bin1},
					{"name":"200-400","children":bin2}
				]
			},
			{"name":"400-800","children":
				[
					{"name":"400-600","children":bin3},
					{"name":"600-800","children":bin4}
				]
			}
		]

		cur.close()
		return results


# main function for the purpose of testing
def main():
	print("insert test functions here")

if __name__ == "__main__":
	main()
