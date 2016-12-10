#!/usr/bin/python3
#
# Script to compute health scores given storage system information
#
import numpy as np
from query_db import get_test_health_inputs_row, parse_health_inputs_row


write_weights = []
read_weights = []


def compute_health_score(ihs):
	row = get_test_health_inputs_row()
	systemid, timestamp, writes, reads, cpu, bandwidth, delayedAcks = parse_health_inputs_row(row)
	pass


def compute_ihs(ws, res, cps, daPct):
	pass


def compute_cbs(cpuPct, bwPct):
	pass


def compute_rs(readScores):
	pass


def compute_ws(writeScores):
	pass

