# Need to test if health score functions properly.
# (See health_score.py)

# Elements needed for health score are:
# write speed, read speed, cpu, bandwidth, delayed Acks

# So come up with values for those that produce perfect results and worst results
# Print out what those values are and what the test of the health score should return as a result

# Run the health score and print out it's result.

#Check if what the health score should be and what it outputted are equivalent

# ...?
# Profit.

# step one: what values make a perfect health score?
# step two: what values make a pessimal health score?

from health_score import *
import numpy as np

y = 0

print(" OPTIMAL TEST")
x = compute_health_score(np.array([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), np.array([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), 0.0, 1.0, 0.0)
print("\n   Optimal score should be >=799.\n   With optimal health score factor values, health score function should return a score >= 799.")
print("   Health score with optimal values: %d" % (x))
print("   Optimal health score test: ")
if x >= 799:
	print(" PASS")
	y += 1
else:
	print(" FAIL")


print("\n PESSIMAL TEST")
z = compute_health_score(np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]), np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]), 1.0, 0.0, 1.0)
print("\n   Pessimal score should be 26.\n   With pessimal health score factor values, health score function should return a score of 26.")
print("   Health score with pessimal values: %d" % (z))
print("   Pessimal health score test: ")
if z == 26:
	print(" PASS")
	y += 1
else:
	print(" FAIL")


print("\n COMPARE HEALTH SCORES TEST")
print("   Health score with optimal values: %d" % (x))
print("   Health score with pessimal values: %d" % (z))
print("   Optimal health score should be ranked higher than pessimal health score.")
if z > x:
	print("   Higher rank is: %d" % (z))
	print(" FAIL")
if z <= x:
	print("   Higher rank is: %d" % (x))
	print(" PASS")
	y += 1


if y == 3:
	print("\nALL TESTS PASS")
else:
	print("\nTEST FAILURE")


