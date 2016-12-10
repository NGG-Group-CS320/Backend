#!/usr/bin/python3
#
# Script to compute health scores given storage system information
#
import numpy as np
from query_db import get_test_health_inputs_row, parse_health_inputs_row


write_weights = []
read_weights = []


def compute_health_score(ihs):
	pass


def compute_ihs(ws, res, cps, daPct):
	pass


def compute_cbs(cpuPct, bwPct):
	pass


def compute_rs(readScores):
	pass


def compute_ws(writeScores):
	pass


# main function for the purpose of testing
def main():
	row = get_test_health_inputs_row() #note: this function will have to be removed at some point
	systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks = parse_health_inputs_row(row)
	print("systemid: {}\ntimestamp: {}\nwrites: {}\nreads: {}\ncpu: {}\nbandwidth: {}\ndelayedAcks: {}".format(systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks))

if __name__ == "__main__":
	main()
