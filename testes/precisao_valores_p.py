"""Mede o erro dos valores de p calculados em Power Fx (integração numérica) face ao scipy,
numa grelha alargada de estatísticas e graus de liberdade. Resultado: docs/precisao-valores-p.md"""
import itertools
import os
import sys

import numpy as np
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "ferramentas"))
from gerador import f_inferencia as F  # noqa: E402
from motor import correr  # noqa: E402

T_GL = [1, 1.05, 1.3, 1.5, 1.8, 2, 2.5, 3, 4, 5, 7, 10, 15, 20, 30, 50, 100, 300, 1000, 10000, 100000]
T_VAL = [0, 0.01, 0.1, 0.5, 1, 1.5, 1.96, 2, 2.5, 3, 4, 5, 8, 12, 30, 100]
F_D1 = [1, 2, 3, 4, 5, 8, 10, 20, 40]
F_D2 = [1, 2, 3, 5, 8, 10, 20, 30, 60, 120, 500, 5000]
F_VAL = [0.01, 0.1, 0.5, 1, 1.5, 2, 3, 4, 6, 10, 30, 100, 1000]
Q_K = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 50, 100, 200, 500, 1000]
Q_VAL = [0.001, 0.01, 0.1, 0.5, 1, 2, 3, 3.84, 5, 7, 10, 15, 20, 30, 50, 80, 120, 200, 300, 600, 1200]


def casos():
    c = []
    for gl, t in itertools.product(T_GL, T_VAL):
        c.append(("t", (t, gl), F.p_t_bilateral(repr(float(t)), repr(float(gl))), 2 * stats.t.sf(t, gl)))
    for d1, d2, f in itertools.product(F_D1, F_D2, F_VAL):
        c.append(("F", (f, d1, d2), F.p_f(repr(float(f)), str(d1), str(d2)), stats.f.sf(f, d1, d2)))
    for k, x in itertools.product(Q_K, Q_VAL):
        c.append(("χ²", (x, k), F.p_qui(repr(float(x)), str(k)), stats.chi2.sf(x, k)))
    return c


def main():
    cs = casos()
    res = correr([{"id": f"p{i}", "expr": e} for i, (_, _, e, _) in enumerate(cs)])
    fam = {}
    falhas = []
    for i, (f, args, _, ref) in enumerate(cs):
        r = res[f"p{i}"]
        if not r["ok"]:
            falhas.append((f, args, r.get("erro")))
            continue
        err = abs(r["valor"] - ref)
        d = fam.setdefault(f, {"n": 0, "max": 0.0, "arg": None, "acima": 0, "dec4": 0})
        d["n"] += 1
        if err > d["max"]:
            d["max"], d["arg"] = err, (args, r["valor"], ref)
        if err >= 5e-5:
            d["acima"] += 1
        # mesma apresentação com 4 casas decimais (ou ambos «< 0,0001»)?
        a = "<" if r["valor"] < 1e-4 else f"{r['valor']:.4f}"
        b = "<" if ref < 1e-4 else f"{ref:.4f}"
        if a != b:
            d["dec4"] += 1
    return fam, falhas


if __name__ == "__main__":
    fam, falhas = main()
    for f, d in fam.items():
        print(f, d)
    print("falhas:", falhas[:5], len(falhas))
