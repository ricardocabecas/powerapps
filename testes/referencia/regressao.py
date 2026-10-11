"""Referência da correlação e regressão (scipy.stats.linregress / pearsonr)."""
import numpy as np
from scipy import stats


def regressao(xs, ys, x0=None):
    p = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(p)
    r = {"n": n}
    if n == 0:
        return {**r, **{k: None for k in ["mediaX", "mediaY", "Sxx", "Syy", "Sxy", "sx", "sy", "cov", "r", "r2",
                                          "b", "a", "previsao"]}}
    x = np.array([a for a, _ in p], float)
    y = np.array([b for _, b in p], float)
    mx, my = x.mean(), y.mean()
    Sxx, Syy, Sxy = ((x - mx) ** 2).sum(), ((y - my) ** 2).sum(), ((x - mx) * (y - my)).sum()
    r.update({"mediaX": mx, "mediaY": my, "Sxx": Sxx, "Syy": Syy, "Sxy": Sxy,
              "sx": float(np.std(x, ddof=1)) if n >= 2 else None, "sy": float(np.std(y, ddof=1)) if n >= 2 else None,
              "cov": float(np.cov(x, y, ddof=1)[0, 1]) if n >= 2 else None})
    if n >= 2 and Sxx > 0:
        lr = stats.linregress(x, y)
        r["b"], r["a"] = float(lr.slope), float(lr.intercept)
        r["previsao"] = (r["a"] + r["b"] * x0) if x0 is not None else None
    else:
        r["b"] = r["a"] = r["previsao"] = None
    if n >= 2 and Sxx > 0 and Syy > 0:
        r["r"] = float(stats.pearsonr(x, y).statistic) if n >= 2 else None
        r["r2"] = r["r"] ** 2
    else:
        r["r"] = r["r2"] = None
    return r
