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
c = np.arange(21,0,-1)
c = c / np.linalg.norm(c)
write_weights = c
read_weights = c


def compute_health_score(writes, reads, cpu, bandwidth, delayedAcks):
	readScore = compute_rs(reads)
	writeScore = compute_ws(writes)
	cbs = compute_cbs(cpu, bandwidth)
	ihs = compute_ihs(writeScore, readScore, cbs, delayedAcks)
	return 800*ihs


def compute_ihs(ws, res, cps, daPct):
	return np.dot([ws,res, cps, 1-daPct], weights)


def compute_cbs(cpuPct, bwPct):
	return np.sqrt(((1-cpuPct)**2+bwPct**2)/2)


def compute_rs(readScores):
	readScores = np.array(readScores) / 100
	return np.dot(readScores, write_weights)


def compute_ws(writeScores):
	writeScores = np.array(writeScores) / 100
	return np.dot(writeScores, read_weights)


# main function for the purpose of testing
def main():
	row = get_test_health_inputs_row() #note: this function will have to be removed at some point
	systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks = parse_health_inputs_row(row)
	print("systemid: {}\ntimestamp: {}\nwrites: {}\nreads: {}\ncpu: {}\nbandwidth: {}\ndelayedAcks: {}".format(systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks))
	score = compute_health_score(writes, reads, cpu, bandwidth, delayedAcks)
	print("this system has a health score of {}/800 (higher is healthier)".format(score))

if __name__ == "__main__":
	main()
