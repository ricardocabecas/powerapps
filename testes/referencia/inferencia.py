"""Referência dos testes de hipóteses (scipy.stats)."""
import numpy as np
from scipy import stats

ALT = {1: "two-sided", 2: "less", 3: "greater"}


def teste_t(tipo, a, b=None, d0=0.0, alt=1):
    """tipo 1 uma amostra; 2 independentes (variâncias iguais); 3 Welch; 4 emparelhadas (a = x, b = y)."""
    if tipo == 4:
        pares = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
        a = [x - y for x, y in pares]
        b = None
    a = np.array([x for x in a if x is not None], float)
    if tipo in (1, 4):
        if len(a) < 2:
            return {"n1": len(a), "t": None, "gl": None, "p": None}
        if np.std(a, ddof=1) == 0:   # variância nula: gl definidos, t não
            return {"n1": len(a), "t": None, "gl": len(a) - 1, "p": None}
        r = stats.ttest_1samp(a, d0, alternative=ALT[alt])
        return {"n1": len(a), "m1": a.mean(), "s1": np.std(a, ddof=1), "t": float(r.statistic),
                "gl": float(r.df), "p": float(r.pvalue)}
    b = np.array([x for x in b if x is not None], float)
    if len(a) < 2 or len(b) < 2:
        return {"n1": len(a), "n2": len(b), "t": None, "gl": None, "p": None}
    if np.var(a, ddof=1) + np.var(b, ddof=1) == 0:
        return {"n1": len(a), "n2": len(b), "t": None, "gl": (len(a) + len(b) - 2) if tipo == 2 else None, "p": None}
    r = stats.ttest_ind(a - d0, b, equal_var=(tipo == 2), alternative=ALT[alt])
    return {"n1": len(a), "n2": len(b), "m1": a.mean(), "m2": b.mean(), "s1": np.std(a, ddof=1),
            "s2": np.std(b, ddof=1), "t": float(r.statistic), "gl": float(r.df), "p": float(r.pvalue)}


def anova(grupos):
    """grupos: lista de listas de valores (só grupos com n ≥ 1)."""
    g = [np.array(x, float) for x in grupos if len(x) > 0]
    N, k = sum(len(x) for x in g), len(g)
    mg = np.concatenate(g).mean()
    sqe = sum(len(x) * (x.mean() - mg) ** 2 for x in g)
    sqd = sum(((x - x.mean()) ** 2).sum() for x in g)
    r = {"k": k, "N": N, "SQE": sqe, "SQD": sqd, "SQT": ((np.concatenate(g) - mg) ** 2).sum(),
         "glE": k - 1, "glD": N - k, "glT": N - 1}
    r["QME"] = sqe / (k - 1) if k >= 2 else None
    r["QMD"] = sqd / (N - k) if N > k else None
    if k >= 2 and N > k and sqd > 0:
        f = stats.f_oneway(*g)
        r["F"], r["p"] = float(f.statistic), float(f.pvalue)
    else:
        r["F"] = r["p"] = None
    return r


def qui_aderencia(obs, props=None):
    obs = np.array(obs, float)
    n = obs.sum()
    p = np.ones(len(obs)) / len(obs) if props is None else np.array(props, float) / np.sum(props)
    esp = n * p
    r = stats.chisquare(obs, esp)
    return {"esperadas": list(esp), "qui2": float(r.statistic), "gl": len(obs) - 1, "p": float(r.pvalue),
            "baixas": int((esp < 5).sum())}


def qui_independencia(tab):
    tab = np.array(tab, float)
    r = stats.chi2_contingency(tab, correction=False)
    return {"esperadas": r.expected_freq.tolist(), "qui2": float(r.statistic), "gl": int(r.dof),
            "p": float(r.pvalue), "baixas": int((r.expected_freq < 5).sum())}
