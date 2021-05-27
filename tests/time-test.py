import time
import sys
sys.path.append('..')

from detection_missing_data import *

n = 1

t0 = time.time()
for i in range(n): DetectMissingData("../data/data.csv", "../data/timetables.csv")
t1 = time.time()

print(f"{t1-t0} secondes")
