"""Lab 3 - Recursion and recurrence relations (reference solution)."""
import math, sys, random
sys.setrecursionlimit(20000)


class Counters:
    def __init__(self):
        self.calls = 0
        self.cmps = 0


def rsum(A, n, c):
    c.calls += 1
    if n == 0:
        return 0
    return rsum(A, n - 1, c) + A[n - 1]


def bsearch(A, x, lo, hi, c):
    c.calls += 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if A[mid] == x:
        return mid
    if A[mid] < x:
        return bsearch(A, x, mid + 1, hi, c)
    return bsearch(A, x, lo, mid - 1, c)


def merge(L, R, c):
    out, i, j = [], 0, 0
    while i < len(L) and j < len(R):
        c.cmps += 1
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
    return out + L[i:] + R[j:]


def merge_sort(A, c):
    c.calls += 1
    if len(A) <= 1:
        return A
    m = len(A) // 2
    L = merge_sort(A[:m], c)
    R = merge_sort(A[m:], c)
    return merge(L, R, c)


def t_n_minus_1_plus_n(n):
    """T(n) = T(n-1) + n, T(0) = 0  (not Master-Theorem form)."""
    return 0 if n == 0 else t_n_minus_1_plus_n(n - 1) + n


def experiment():
    rows = []
    rnd = random.Random(7)
    for k in range(4, 13):
        n = 2 ** k
        A = sorted(rnd.sample(range(10 * n), n))
        c1 = Counters(); rsum(A, n, c1)
        c2 = Counters(); bsearch(A, -1, 0, n - 1, c2)          # absent target = worst case
        B = A[:]; rnd.shuffle(B)
        c3 = Counters(); S = merge_sort(B, c3)
        assert S == sorted(B)
        rows.append(dict(n=n, rsum_calls=c1.calls, bs_calls=c2.calls, ms_calls=c3.calls,
                         ms_cmps=c3.cmps, nlogn=n * k, ratio=c3.cmps / (n * k)))
    return rows


def report():
    from display import banner, section, note, table, ci, figure, save, show_all
    banner("LAB 3 — Récursion et recurrences")
    section("1. Recurrences")
    table(["Algorithme", "Recurrence", "Solution"], [
        ["rsum", "T(n) = T(n-1) + c", "Θ(n)"], ["binary search", "T(n) = T(n/2) + c", "Θ(log n)"],
        ["merge sort", "T(n) = 2T(n/2) + cn", "Θ(n log n)  (Master, cas 2)"],
        ["T(n) = T(n-1) + n", "(machi forme Master)", "Θ(n²)  (expansion: n(n+1)/2)"]])
    section("2. Mesures (permutations aléatoires, n = 2^k)")
    rows = experiment()
    table(["n", "rsum appels", "bsearch appels", "merge appels", "merge comparaisons", "n·log2 n", "ratio cmp/(n·log2 n)"],
          [[ci(r["n"]), ci(r["rsum_calls"]), r["bs_calls"], ci(r["ms_calls"]), ci(r["ms_cmps"]), ci(r["nlogn"]), f"{r['ratio']:.3f}"] for r in rows])
    note("rsum: n+1 appels. bsearch: log2 n + 1 appels. merge sort: 2n-1 appels (Θ(n)) lakin comparaisons ≈ n·log2 n — 3lach? l'coût l'kol appel machi constant (l'merge).")
    fig, ax = figure(1, 2, figsize=(11, 4))
    if fig:
        ns = [r["n"] for r in rows]
        ax[0].plot(ns, [r["rsum_calls"] for r in rows], "o-", label="rsum appels (n+1)")
        ax[0].plot(ns, [r["ms_calls"] for r in rows], "s-", label="merge_sort appels (2n-1)")
        ax[0].plot(ns, [r["bs_calls"] for r in rows], "^-", label="bsearch appels (log2 n + 1)")
        ax[0].set_xscale("log", base=2); ax[0].set_yscale("log"); ax[0].set_xlabel("n"); ax[0].set_ylabel("nombre d'appels"); ax[0].set_title("Nombre d'appels récursifs"); ax[0].legend()
        ax[1].plot(ns, [r["ms_cmps"] for r in rows], "o-", label="comparaisons merge sort")
        ax[1].plot(ns, [r["nlogn"] for r in rows], "k--", label="n·log2 n")
        ax[1].plot(ns, [r["nlogn"] / 2 for r in rows], "g:", label="(n/2)·log2 n")
        ax[1].set_xscale("log", base=2); ax[1].set_yscale("log"); ax[1].set_xlabel("n"); ax[1].set_ylabel("comparaisons"); ax[1].set_title("Merge sort: Θ(n log n)"); ax[1].legend()
        save(fig, "lab03_recurrences")
    show_all()


if __name__ == "__main__":
    report()
