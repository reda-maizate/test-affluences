import time
import sys
sys.path.append('..')

from detection_missing_data import *

n = 100

t0 = time.time()
for i in range(n):
    d = DetectMissingData("../data/data.csv", "../data/timetables.csv")
    d.detect()
t1 = time.time()

print("################################")
print(f"{round(t1-t0, 4)} seconds for {n} iterations.")
print(f"{round(((t1-t0)/n) * 1000, 4)} ms for 1 iteration.")
print("################################")
