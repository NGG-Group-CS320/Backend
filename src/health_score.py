#!/usr/bin/python3
#
# Script to compute health scores given storage system information
#
import numpy as np
from query_db import get_test_health_inputs_row, parse_health_inputs_row

"""
Let c be a 21-dimensional vector defined as <2121, 2021, 1921, 1821, ... 321, 221, 121>.
Create a 21-dimensional vector w from the fields of the form writes*msPct ordered from smallest to greatest time.
Create a 21-dimensional vector r from the fields of the form reads*msPct ordered from smallest to greatest time.
Let ws=wc and rs=rc. We call ws and rs the write score and read score respectively.
Compute cbs=dist((cpu, nbw), (1, 0))/sqrt(2)=sqrt((1-cpu)^2+nbw^2)/2) where cpu corresponds to cpuLatestTotalAvgPct and nbw corresponds to portTotalBandwidthMBPS normalized by the maximum value of portTotalBandwidthMBPS seen for the particular system at hand. We call this the CPU-bandwidth score. If nbw would be undefined, we use nbw=1 in computing cbs.
Compute the interim health score ihs=<ws, rs, cbs, 1-da><0.45, 0.25, 0.2, 0.1> on the range [0, 1] where da is the delAckPct.
The resulting health score is floor(800*ihs) yielding a value on the range [0, 800].
"""
weights = [0.45,0.25,0.2,0.1]
c = [21/21, 20/21, 19/21, 18/21. 17/21, 16/21, 15/21, 14/21, 13/21, 12/21, 11/21, 10/21, 9/21, 8/21, 7/21, 6/21, 5/21, 4/21, 3/21, 2/21, 1/21]
write_weights = []
read_weights = []


def compute_health_score(ihs):
	readScore = compute_rs(read_weights)
	writeScore = compute_ws(write_weights)
	cbs = compute_cbs(cpu, bw)
	ihs = (writeScore, readScore, cbs, daPct)
	return 800*ihs


def compute_ihs(ws, res, cps, daPct):
	return numpy.dot([ws,res, cps, 1-daPct], weights)


def compute_cbs(cpuPct, bwPct):
	return numpy.sqrt(((1-cpuPct)**2+bwPct**2)/2)


def compute_rs(readScores):
	return numpy.dot(readScores, c)


def compute_ws(writeScores):
	return numpy.dot(writeScores, c)


# main function for the purpose of testing
def main():
	row = get_test_health_inputs_row() #note: this function will have to be removed at some point
	systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks = parse_health_inputs_row(row)
	print("systemid: {}\ntimestamp: {}\nwrites: {}\nreads: {}\ncpu: {}\nbandwidth: {}\ndelayedAcks: {}".format(systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks))

if __name__ == "__main__":
	main()
