from math import comb


def pass_at_k(n, c, k):
    """Unbiased estimate of P(at least 1 of k samples is correct),
    given n samples of which c were correct."""
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)


if __name__ == "__main__":
    print(pass_at_k(10, 0, 1))    # expect 0.0
    print(pass_at_k(10, 10, 1))   # expect 1.0
    print(pass_at_k(10, 5, 1))    # expect 0.5