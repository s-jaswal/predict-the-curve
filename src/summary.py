import json
import os
from collections import Counter

from src.config import DATA_DIR

res = json.load(open(os.path.join(DATA_DIR, "results.json"), encoding="utf-8"))
fracs = {pid: v["c"] / v["n"] for pid, v in res.items()}
n = len(fracs)
print("run:", DATA_DIR)
print("problems graded:", n)
print("samples per problem:", Counter(v["n"] for v in res.values()))
print("mean pass@1:", round(sum(fracs.values()) / n, 3))

buckets = Counter()
for f in fracs.values():
    if f == 1.0:
        buckets["100%"] += 1
    elif f >= 0.8:
        buckets["80-99%"] += 1
    elif f >= 0.4:
        buckets["40-79%"] += 1
    elif f > 0:
        buckets["1-39%"] += 1
    else:
        buckets["0%"] += 1
for k in ["100%", "80-99%", "40-79%", "1-39%", "0%"]:
    print(f"{k:>7}: {buckets[k]}")

print()
print("problems with any failure:")
for pid, f in sorted(fracs.items(), key=lambda kv: kv[1]):
    if f < 1.0:
        print(" ", pid, f'{res[pid]["c"]}/{res[pid]["n"]}')