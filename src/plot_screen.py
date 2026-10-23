import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.metrics import pass_at_k

RUNS = {
    "HumanEval, Haiku 5.5 (n=164)": "data/haiku-5-5/results.json",
    "HumanEval, Haiku 4.5 (n=164)": "data/haiku-4-5/results.json",
    "MATH-500 Level 5, Haiku 4.5 (n=100)": "data/math-haiku-4-5/results.json",
}

plt.figure(figsize=(7, 4.5))
for label, path in RUNS.items():
    if not os.path.exists(path):
        print("missing:", path)
        continue
    res = json.load(open(path, encoding="utf-8"))
    ks = list(range(1, 6))
    ys = []
    for k in ks:
        vals = [pass_at_k(v["n"], v["c"], k) for v in res.values()]
        ys.append(sum(vals) / len(vals))
    print(label, [round(y, 3) for y in ys])
    plt.plot(ks, ys, marker="o", label=label)

plt.xlabel("k (samples per problem)")
plt.ylabel("average pass@k (coverage)")
plt.title("Coverage vs. samples, 5-sample screens")
plt.xticks(range(1, 6))
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
os.makedirs("plots", exist_ok=True)
plt.savefig("plots/screen_coverage.png", dpi=150)
print("saved plots/screen_coverage.png")