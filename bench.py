import time

from astroid import Astroid, a216877, by_columns


def timed(f, *args):
    t = time.perf_counter()
    v = f(*args)
    return time.perf_counter() - t, v


def by_pairs(n):
    ast = Astroid(n)
    count = 4 * n + 1
    for x in range(1, n):
        for y in range(1, n):
            if not ast.outside(x, y):
                count += 4
    return count


def bench_pairs():
    print("table 1: pair enumeration O(n^2) against the walk")
    print("n, pairs, walk")
    for n in (100, 200, 400, 800):
        tp, vp = timed(by_pairs, n)
        tw, vw = timed(a216877, n)
        assert vp == vw
        print(n, "%.4f" % tp, "%.6f" % tw)


def bench_main():
    print("table 2: a(n) by columns O(n log n) and by the walk")
    print("n, columns, walk, edges, steps, steps/n^(2/3), a(n), a(n)/n^2")
    for e in range(2, 11):
        n = 10**e
        stats = {"edges": 0, "steps": 0}
        tw, vw = timed(a216877, n, stats)
        if e <= 6:
            tc, vc = timed(by_columns, n)
            assert vc == vw
            col = "%.4f" % tc
        else:
            col = "---"
        print(n, col, "%.4f" % tw, stats["edges"], stats["steps"], "%.3f" % (stats["steps"] / n ** (2 / 3)), vw, "%.7f" % (vw / n**2), flush=True)


if __name__ == "__main__":
    bench_pairs()
    bench_main()
