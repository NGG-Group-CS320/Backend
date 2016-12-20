#!/usr/bin/python3
#
# Script to compute the health scores for each row in the database
#
import numpy as np
from health_score import *


# get a row of data to use to test the health score function
with make_connection() as conn:
	cur = conn.cursor()

	print("fetching list of unique systemid's")
	cur.execute("""
		SELECT systemid
		FROM hpnmb
		GROUP BY systemid;
		""")
	all_systemids = cur.fetchall() #length is currently 4519
	all_systemids = [x[0] for x in all_systemids]
	print(np.array(all_systemids))

	print(100.0*all_systemids.index(2262)/len(all_systemids),"% done")

	cur.close()

