import random
import re

from datasets import load_dataset


def load_problems(n=100, seed=42, level5_only=True):
    ds = load_dataset("HuggingFaceH4/MATH-500", split="test")
    problems = []
    for i, row in enumerate(ds):
        if level5_only and not str(row["level"]).strip().endswith("5"):
            continue
        problems.append({
            "id": f"MATH500/{i}",
            "problem": row["problem"],
            "answer": row["answer"],
            "subject": row["subject"],
            "level": row["level"],
        })
    random.Random(seed).shuffle(problems)
    return problems[:n]


def build_prompt(problem):
    return (
        "Solve the following math problem. Reason step by step, then give "
        "your final answer as \\boxed{...} in simplest exact form "
        "(for example \\frac{3}{4}, not 0.75).\n\n" + problem["problem"]
    )


def last_boxed(text):
    start = text.rfind("\\boxed{")
    if start == -1:
        return None
    i = start + len("\\boxed{")
    depth = 1
    out = []
    while i < len(text):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return "".join(out)
        out.append(ch)
        i += 1
    return None


def normalize(s):
    if s is None:
        return None
    s = s.strip()
    s = s.replace("$", "")
    s = s.replace("\\!", "").replace("\\,", "").replace("\\;", "")
    s = s.replace("\\left", "").replace("\\right", "")
    s = s.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")
    s = s.replace("^\\circ", "").replace("^{\\circ}", "")
    s = s.replace("\u00b0", "")
    s = s.replace("\\%", "").replace("%", "")
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = s.replace(" ", "")
    s = s.rstrip(".")
    if s.count("=") == 1:
        lhs, rhs = s.split("=")
        if len(lhs) <= 2:
            s = rhs
    m = re.fullmatch(r"(-?\d+)/(\d+)", s)
    if m:
        s = "\\frac{" + m.group(1) + "}{" + m.group(2) + "}"
    return s


def is_correct(text, gold):
    pred = normalize(last_boxed(text))
    ref = normalize(gold)
    if pred is None:
        return False
    if pred == ref:
        return True
    try:
        return abs(float(pred) - float(ref)) < 1e-9
    except ValueError:
        return False


if __name__ == "__main__":
    print("level-5 problems available:", len(load_problems(n=10**6)))
    probs = load_problems(n=3)
    for p in probs:
        print(p["id"], p["subject"], "| level:", repr(p["level"]),
              "| answer:", p["answer"])
    print()
    print(build_prompt(probs[0]))
    print()
    assert last_boxed("so \\boxed{\\frac{1}{2}} done") == "\\frac{1}{2}"
    assert is_correct("\\boxed{\\dfrac{3}{4}}", "\\frac{3}{4}")
    assert is_correct("\\boxed{x = 5}", "5")
    assert is_correct("\\boxed{0.5}", "0.5")
    assert not is_correct("\\boxed{6}", "5")
    assert not is_correct("no answer here", "5")
    print("self-test passed")