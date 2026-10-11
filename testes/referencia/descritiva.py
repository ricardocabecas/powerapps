"""Referência da estatística descritiva (numpy/scipy), independente das fórmulas Power Fx."""
from collections import Counter

import numpy as np
from scipy import stats


def fmt_livre(v):
    if float(v).is_integer():
        return str(int(v))
    s = f"{v:.10f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def _metades(s, qual):
    n = len(s)
    m = n // 2
    if m == 0:
        return s[0]
    bloco = s[:m] if qual == 1 else s[n - m:]
    return float(np.median(bloco))


def quartil(s, qual, metodo):
    p = {1: 0.25, 3: 0.75}[qual]
    if metodo == 1:
        return float(np.quantile(s, p, method="linear"))       # tipo 7 (Hyndman & Fan)
    if metodo == 2:
        return float(np.quantile(s, p, method="weibull"))      # tipo 6 (Hyndman & Fan)
    return _metades(s, qual)


def moda_texto(s):
    n = len(s)
    if n == 0:
        return "n.d."
    c = Counter(s)
    fmax = max(c.values())
    modas = sorted(v for v, f in c.items() if f == fmax)
    if n > 1 and len(modas) == len(c):
        return "não existe (amodal)"
    t = "; ".join(fmt_livre(v) for v in modas[:5]) + ("; …" if len(modas) > 5 else "")
    t += " (bimodal)" if len(modas) == 2 else (" (multimodal)" if len(modas) > 2 else "")
    return t + f" — freq. {fmax}"


def descritiva(valores, metodo=1):
    s = sorted(v for v in valores if v is not None)
    n = len(s)
    r = {"n": n, "moda": moda_texto(s)}
    if n == 0:
        r.update({k: None for k in ["soma", "media", "mediana", "minimo", "maximo", "amplitude", "q1", "q3",
                                    "varA", "varP", "dpA", "dpP", "cv"]})
        return r
    a = np.array(s, dtype=float)
    media = float(np.mean(a))
    r.update({
        "soma": float(np.sum(a)), "media": media, "mediana": float(np.median(a)),
        "minimo": float(a.min()), "maximo": float(a.max()), "amplitude": float(np.ptp(a)),
        "q1": quartil(s, 1, metodo), "q3": quartil(s, 3, metodo),
        "varA": float(np.var(a, ddof=1)) if n >= 2 else None,
        "varP": float(np.var(a, ddof=0)),
        "dpA": float(np.std(a, ddof=1)) if n >= 2 else None,
        "dpP": float(np.std(a, ddof=0)),
    })
    # scipy.stats.variation usa o desvio padrão populacional por omissão; com ddof=1 dá o amostral
    r["cv"] = (float(abs(stats.variation(a, ddof=1))) * 100) if n >= 2 and media != 0 else None
    return r
