from math import isqrt


def strip(a, b, y, k):
    c = (a - 1) * (b - 1) // 2 + b
    return k * a * (y - 1) - k * c - a * b * k * (k - 1) // 2


class Astroid:
    def __init__(self, n):
        self.n = n
        self.m = n * n
        self.x_end = n - 1

    def outside(self, x, y):
        if y < 1:
            return False
        r = self.m - x * x - y * y
        if r < 0:
            return True
        return r * r * r < 27 * x * x * y * y * self.m

    def fits(self, x, y, a, b, k):
        return x + k * a <= self.x_end and self.outside(x + k * a, y - k * b)

    def lowest(self, x):
        lo, hi = 1, self.n
        while lo < hi:
            mid = (lo + hi) // 2
            if self.outside(x, mid):
                hi = mid
            else:
                lo = mid + 1
        return lo

    def max_copies(self, x, y, a, b):
        if not self.fits(x, y, a, b, 1):
            return 0
        lo = 1
        while self.fits(x, y, a, b, lo * 2):
            lo *= 2
        hi = lo * 2
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.fits(x, y, a, b, mid):
                lo = mid
            else:
                hi = mid
        return lo

    def first_fit(self, x, y, fa, fb, ga, gb):
        u = x + ga
        v = y - gb
        kmax = (self.x_end - u) // fa
        if fb:
            kmax = min(kmax, (v - 1) // fb)
        if kmax < 1:
            return 0
        s = fa * fa + fb * fb
        peak = isqrt(self.m * fa ** 6 * s) // (s * s)
        base = (peak - u) // fa
        found = None
        for k in sorted({min(max(base, 1), kmax), min(max(base + 1, 1), kmax)}):
            if self.outside(u + k * fa, v - k * fb):
                found = k
                break
        if found is None:
            return 0
        lo, hi = 1, found
        while lo < hi:
            mid = (lo + hi) // 2
            if self.outside(u + mid * fa, v - mid * fb):
                hi = mid
            else:
                lo = mid + 1
        return lo

    def tail_sum(self, stats=None):
        d = isqrt(self.m // 8)
        x = d + 1
        if x > self.x_end:
            return 0
        y = self.lowest(x)
        total = y - 1
        stack = [(1, 0), (1, 1)]
        while x < self.x_end:
            a, b = stack.pop()
            k = self.max_copies(x, y, a, b)
            if k:
                total += strip(a, b, y, k)
                x += k * a
                y -= k * b
                if stats is not None:
                    stats["edges"] += 1
            if x >= self.x_end:
                break
            ga, gb = a, b
            while True:
                a, b = stack.pop()
                if self.fits(x, y, a, b, 1):
                    break
                ga, gb = a, b
            fa, fb = a, b
            while True:
                if stats is not None:
                    stats["steps"] += 1
                k = self.first_fit(x, y, fa, fb, ga, gb)
                if k == 0:
                    break
                stack.append((fa, fb))
                ga += (k - 1) * fa
                gb += (k - 1) * fb
                fa += ga
                fb += gb
            stack.append((fa, fb))
        return total


def a216877(n, stats=None):
    if n == 0:
        return 1
    d = isqrt(n * n // 8)
    return 4 * (d * d + 2 * Astroid(n).tail_sum(stats)) + 4 * n + 1


def column_count(n, x):
    return Astroid(n).lowest(x) - 1


def by_columns(n):
    if n == 0:
        return 1
    ast = Astroid(n)
    return 4 * sum(ast.lowest(x) - 1 for x in range(1, n)) + 4 * n + 1
