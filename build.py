"""Cloudflare Pages build step.

Generates the first 10,000,000 decimal digits of pi (after the "3.") with the
Chudnovsky algorithm and writes the deployable site to ./dist:

    dist/index.html
    dist/_headers
    dist/pi-10m.txt

Build command:  pip install gmpy2 && python3 build.py
Output dir:     dist
"""
import os
import shutil
import sys
import time

import gmpy2
from gmpy2 import mpz

N = 10_000_000
GUARD = 50


def bs(a, b):
    if b - a == 1:
        if a == 0:
            pab = qab = mpz(1)
        else:
            pab = mpz((6 * a - 5) * (2 * a - 1) * (6 * a - 1))
            qab = mpz(a * a * a * 10939058860032000)
        tab = pab * (13591409 + 545140134 * a)
        if a & 1:
            tab = -tab
        return pab, qab, tab
    m = (a + b) // 2
    pam, qam, tam = bs(a, m)
    pmb, qmb, tmb = bs(m, b)
    return pam * pmb, qam * qmb, qmb * tam + pam * tmb


def main():
    sys.setrecursionlimit(10000)
    t0 = time.time()
    digits = N + GUARD
    terms = int(digits / 14.181647462725477) + 2
    _, q, t = bs(0, terms)
    one = mpz(10) ** digits
    sqrt_c = gmpy2.isqrt(mpz(10005) * one * one)
    s = str((q * 426880 * sqrt_c) // t)
    body = s[1 : 1 + N]  # digits after the decimal point

    # sanity checks against well-known landmarks
    assert s.startswith("31415926535897932384626433832795"), "leading digits wrong"
    assert len(body) == N and body.isdigit(), "bad length"
    assert body[999990:1000000] == "5779458151", "digits 999,991-1,000,000 wrong"
    assert body.find("999999") + 1 == 762, "Feynman point wrong"

    os.makedirs("dist", exist_ok=True)
    with open("dist/pi-10m.txt", "w") as f:
        f.write(body)
    for name in ("index.html", "_headers"):
        shutil.copy(name, os.path.join("dist", name))
    print(f"built {N:,} digits in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
