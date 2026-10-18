import os
import re
import subprocess
import sys
import tempfile


def extract_code(response_text):
    """Pull the first code block out of a model response."""
    blocks = re.findall(r"```(?:python)?\n(.*?)```", response_text, re.DOTALL)
    return blocks[0] if blocks else response_text


def run_program(program, timeout=10):
    """Run a Python program in a subprocess. True only if it exits cleanly."""
    env = {k: v for k, v in os.environ.items() if "KEY" not in k.upper()}
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "prog.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(program)
        try:
            result = subprocess.run(
                [sys.executable, path],
                cwd=tmp, env=env, capture_output=True, timeout=timeout,
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False


if __name__ == "__main__":
    from src.problems import load_problems, build_test_program

    p = load_problems(n=1)[0]
    good = p["prompt"] + p["canonical_solution"]
    bad = p["prompt"] + "    pass\n"
    print("canonical (expect True):", run_program(build_test_program(p, good)))
    print("stub (expect False):", run_program(build_test_program(p, bad)))