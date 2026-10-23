import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUNS = {
    "HumanEval, Haiku 5.5 (n=164)": "data/haiku-5-5/results.json",
    "HumanEval, Haiku 4.5 (n=164)": "data/haiku-4-5/results.json",
    "MATH-500 Level 5, Haiku 4.5 (n=100)": "data/math-haiku-4-5/results.json",
}

width = 0.27
plt.figure(figsize=(8, 4.8))
for i, (label, path) in enumerate(RUNS.items()):
    res = json.load(open(path, encoding="utf-8"))
    n = len(res)
    counts = [0] * 6
    for v in res.values():
        counts[v["c"]] += 1
    print(label, counts)
    full = 100 * counts[5] / n
    pct = [100 * counts[j] / n for j in range(5)]
    xs = [j + (i - 1) * width for j in range(5)]
    plt.bar(xs, pct, width=width, label=f"{label}: {full:.0f}% at 5/5")

plt.xticks(range(5), [f"{j}/5" for j in range(5)])
plt.xlabel("samples correct (out of 5)")
plt.ylabel("% of problems")
plt.title("Problems that were not solved on every sample")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
os.makedirs("plots", exist_ok=True)
plt.savefig("plots/pass_distribution.png", dpi=150)
print("saved plots/pass_distribution.png")