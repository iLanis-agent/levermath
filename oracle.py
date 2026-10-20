#!/usr/bin/env python3
# Lever Math oracle - mirrors engine.js with Fractions: each side's pull is the exact product of its mass and distance, the balancing distance and the pivot point are the exact ratios of the entered numbers, rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

MASS = "each mass must be from 0.1 to 1000 kg with at most one decimal place"
DIST = "each distance must be from 0.01 to 20 m with at most two decimal places"
BEAM = "the beam must be from 0.1 to 20 m with at most one decimal place"
def dec(t, err, intd, places, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,%d}(\.[0-9]{1,%d})?" % (intd, places), t) or not F(lo) <= F(t) <= F(hi): raise ValueError(err)
    return F(t)
def mass(t): return dec(t, MASS, 4, 1, "0.1", "1000")
def dist(t): return dec(t, DIST, 2, 2, "0.01", "20")
def txt(fr, places):
    v = int((Decimal(fr.numerator) / Decimal(fr.denominator) * (10 ** places)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    ip, fp = divmod(v, 10 ** places); fs = str(fp).zfill(places).rstrip("0")
    return f"{ip}.{fs}" if fs else str(ip)
def kg(m): return f"{txt(m,1)} kg"
def m_(d): return f"{txt(d,2)} m"
def tq(m, d): return f"{txt(m * d,2)} kg·m"

def balance(m1, d1, m2, d2):
    a, x, b, y = mass(m1), dist(d1), mass(m2), dist(d2)
    t1, t2 = a * x, b * y
    s = f"Side one is {kg(a)} at {m_(x)}, making {tq(a,x)}. Side two is {kg(b)} at {m_(y)}, making {tq(b,y)}. "
    if t1 == t2: return s + "They balance."
    big = "Side one" if t1 > t2 else "Side two"
    return s + f"{big} is heavier by {txt(abs(t1 - t2),2)} kg·m."
def match(m1, d1, m2):
    a, x, b = mass(m1), dist(d1), mass(m2)
    return f"To balance {kg(a)} at {m_(x)} with {kg(b)} on the other side, put the {kg(b)} at {m_(a * x / b)} from the pivot."
def fulcrum(m1, m2, beam):
    a, b = mass(m1), mass(m2); L = dec(beam, BEAM, 3, 1, "0.1", "20")
    x1 = b * L / (a + b); x2 = a * L / (a + b)
    return f"With {kg(a)} at one end of a {txt(L,1)} m beam and {kg(b)} at the other, the pivot goes {m_(x1)} from the {kg(a)} end and {m_(x2)} from the {kg(b)} end."

FNS = {"balanceTruth": balance, "matchTruth": match, "fulcrumTruth": fulcrum}
def cases():
    c = []
    masses = ["0.1", "8", "20", "100.5", "1000"]; dists = ["0.01", "0.6", "1.5", "10", "20"]
    for a in masses:
        for d in dists:
            c.append(("balanceTruth", [a, d, "20", "0.6"]))
            c.append(("matchTruth", [a, d, "20"]))
    for a, d, b, y in [("8", "1.5", "20", "0.6"), ("8", "1.5", "20", "0.7"), ("1", "0.01", "1000", "20"), ("1000", "20", "0.1", "0.01"), ("5", "2", "10", "1"), ("0.1", "20", "0.1", "20")]:
        c.append(("balanceTruth", [a, d, b, y]))
    for a in ["0.1", "8", "1000"]:
        for b in ["0.1", "20", "1000"]:
            for L in ["0.1", "3", "20"]:
                c.append(("fulcrumTruth", [a, b, L]))
    for t in [(" 8 ", " 1.5 ", " 20 ", " 0.6 "), ("8.0", "1.50", "20.0", "0.60")]:
        c += [("balanceTruth", list(t)), ("matchTruth", list(t[:3])), ("fulcrumTruth", [t[0], t[2], " 3 "])]
    bad = ["", "x", "0", "0.0", "0.001", "1.234", "-1", ".5", "5.", "1e2", "10000", "99999"]
    for v in bad:
        c += [("balanceTruth", [v, "1.5", "20", "0.6"]), ("balanceTruth", ["8", v, "20", "0.6"]), ("balanceTruth", ["8", "1.5", v, "0.6"]), ("balanceTruth", ["8", "1.5", "20", v]),
              ("matchTruth", ["8", "1.5", v]), ("fulcrumTruth", [v, "20", "3"]), ("fulcrumTruth", ["8", v, "3"]), ("fulcrumTruth", ["8", "20", v])]
    for t in [("1000.1", "1.5", "20", "0.6"), ("8", "20.01", "20", "0.6"), ("8", "0.001", "20", "0.6"), ("8", "1.5", "0.05", "0.6")]:
        c.append(("balanceTruth", t))
    for t in [("8", "20", "20.1"), ("8", "20", "0.09")]: c.append(("fulcrumTruth", t))
    r = random.Random(717)
    for _ in range(10):
        a = f"{r.randint(0, 999)}.{r.randint(0, 9)}"; a = "0.1" if a == "0.0" else a
        b = f"{r.randint(0, 999)}.{r.randint(0, 9)}"; b = "0.1" if b == "0.0" else b
        x = f"{r.randint(0, 19)}.{r.randint(0, 99):02d}"; x = "0.01" if float(x) < 0.01 else x
        y = f"{r.randint(0, 19)}.{r.randint(0, 99):02d}"; y = "0.01" if float(y) < 0.01 else y
        L = f"{r.randint(0, 19)}.{r.randint(0, 9)}"; L = "0.1" if L == "0.0" else L
        c += [("balanceTruth", [a, x, b, y]), ("matchTruth", [a, x, b]), ("fulcrumTruth", [a, b, L])]
    return c
out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":"), ensure_ascii=False) for o in out) + "\n]\n")
print(len(out), "cases written")
