"""Referência das tabelas de frequências (aritmética exata com Fraction para as classes)."""
import math
from collections import Counter
from fractions import Fraction

from .descritiva import fmt_livre


def fmt_curto(v):
    r = round(v + 0.0, 4)
    if r == int(r):
        return str(int(r))
    return f"{r:.4f}".rstrip("0").rstrip(".").replace(".", ",")


def _acumular(base):
    n = sum(b["ni"] for b in base)
    out, acum = [], 0
    for i, b in enumerate(base, start=1):
        acum += b["ni"]
        out.append({**b, "Ordem": i, "fi": b["ni"] / n, "Ni": acum, "Fi": acum / n})
    return out


def discreta(valores):
    v = [x for x in valores if x is not None and x != ""]
    c = Counter(v)
    base = []
    for x in sorted(c):
        if isinstance(x, str):
            base.append({"Classe": x, "Centro": None, "Li": None, "Ls": None, "ni": c[x]})
        else:
            base.append({"Classe": fmt_livre(x), "Centro": x, "Li": None, "Ls": None, "ni": c[x]})
    return _acumular(base) if base else []


def classes(valores, k=None, a=None, h=None):
    v = [x for x in valores if x is not None]
    n = len(v)
    kS = math.ceil(1 + math.log2(n) - 1e-9) if n > 0 else 0
    k = min(int(k), 50) if k else max(kS, 1)
    mn, mx = (min(v), max(v)) if v else (None, None)
    a = mn if a is None else a
    fa = Fraction(str(a))
    if not h:
        # amplitude automática exata: (máximo − início) / k
        fh = (Fraction(str(mx)) - fa) / k if mx > a else Fraction(1)
        h = float(fh)
    else:
        fh = Fraction(str(h))
    # atribuição exata de cada valor à classe [a+(i-1)h ; a+ih[ (última fechada)
    cont = Counter()
    fora = 0
    for x in v:
        z = (Fraction(str(x)) - fa) / fh
        if z < 0:
            fora += 1
            continue
        i = math.floor(z) + 1
        if i == k + 1 and z == k:
            i = k
        if i > k:
            fora += 1
            continue
        cont[i] += 1
    base = []
    for i in range(1, k + 1):
        li, ls = a + (i - 1) * h, a + i * h
        base.append({"Classe": f"[{fmt_curto(li)} ; {fmt_curto(ls)}{']' if i == k else '['}",
                     "Centro": a + (i - 0.5) * h, "Li": li, "Ls": ls, "ni": cont[i]})
    return {"Linhas": _acumular(base) if n else [], "k": k, "kSturges": kS, "a": a, "h": h, "Fora": fora, "n": n}
