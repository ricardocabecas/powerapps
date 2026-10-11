"""Fase 5 — Inferência: testes t, ANOVA e qui-quadrado (valores de p por integração numérica)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ferramentas"))
from gerador import f_inferencia as F  # noqa: E402
from gerador.f_comum import NOMES_EXEMPLO  # noqa: E402
from motor import pfx_valor, controlo_lista, controlo_texto, iguais  # noqa: E402
from referencia import inferencia as R  # noqa: E402
from referencia.colagem import numero  # noqa: E402
import dados_teste as D  # noqa: E402

NOME = "Fase 5 — Inferência"


def _col(n1, n2=None, c1=None, c2=None, n3=None):
    m = max(len(x) for x in [n1, n2 or [], c1 or [], c2 or [], n3 or []])
    def g(l, i, vazio):
        return l[i] if l is not None and i < len(l) and l[i] is not None else vazio
    return [{"Id": i + 1, "N1": g(n1, i, None), "N2": g(n2, i, None), "N3": g(n3, i, None),
             "C1": g(c1, i, ""), "C2": g(c2, i, "")} for i in range(m)]


def ctx_t(caso):
    nome, tipo, fmt_, v1, v2, grupos, gA, gB, d0, alt = caso
    return [{"nome": "varNomes", "expr": pfx_valor(NOMES_EXEMPLO)},
            {"nome": "colDados", "expr": pfx_valor(_col(v1, v2, grupos))},
            {"nome": "drpTtTipo", "expr": controlo_lista(F.TIPOS_T[tipo - 1])},
            {"nome": "drpTtFormato", "expr": controlo_lista(F.FORMATOS_IND[fmt_ - 1])},
            {"nome": "drpTtVar", "expr": controlo_lista(NOMES_EXEMPLO["N1"])},
            {"nome": "drpTtVar2", "expr": controlo_lista(NOMES_EXEMPLO["N2"])},
            {"nome": "drpTtGrupoVar", "expr": controlo_lista(NOMES_EXEMPLO["C1"])},
            {"nome": "drpTtGrupoA", "expr": controlo_lista(gA)},
            {"nome": "drpTtGrupoB", "expr": controlo_lista(gB)},
            {"nome": "txtTtMu0", "expr": controlo_texto(d0)},
            {"nome": "drpTtAlternativa", "expr": controlo_lista(F.ALTERNATIVAS[alt - 1])},
            {"nome": "drpTtAlfa", "expr": controlo_lista("0,05")}]


def tarefas():
    t = []
    for caso in D.TESTES_T:
        vs = ctx_t(caso)
        t.append({"id": f"f5.t.{caso[0]}", "vars": vs, "expr": F.teste_t()})
        t.append({"id": f"f5.thtml.{caso[0]}", "vars": vs, "expr": F.html_teste_t()})
    return t


def _ref_t(caso):
    nome, tipo, fmt_, v1, v2, grupos, gA, gB, d0, alt = caso
    d0 = numero(d0)[0] or 0.0
    if tipo in (2, 3) and fmt_ == 1:
        a = [x for x, g in zip(v1, grupos) if g == gA and x is not None]
        b = [x for x, g in zip(v1, grupos) if g == gB and x is not None]
        return R.teste_t(tipo, a, b, d0, alt)
    return R.teste_t(tipo, v1, v2, d0, alt)


def verificar(res):
    out = []
    for caso in D.TESTES_T:
        r = res[f"f5.t.{caso[0]}"]
        ref = _ref_t(caso)
        if not r["ok"]:
            out.append((f"teste t «{caso[0]}»", False, r.get("erro")))
        else:
            v = r["valor"]
            difs = []
            for c in ["n1", "n2", "m1", "m2", "s1", "s2", "t", "gl"]:
                if c in ref and not iguais(v.get(c), ref[c], 1e-9):
                    difs.append(f"{c}: Power Fx={v.get(c)} ref={ref[c]}")
            # valor de p: integração numérica, tolerância absoluta 1e-6 (a app mostra 4 casas)
            if (v.get("p") is None) != (ref["p"] is None) or (ref["p"] is not None and abs(v["p"] - ref["p"]) > 1e-6):
                difs.append(f"p: Power Fx={v.get('p')} ref={ref['p']}")
            det = (f"t={v.get('t')}, gl={v.get('gl')}, p={v.get('p')} (scipy {ref['p']})" if not difs
                   else "; ".join(difs))
            out.append((f"teste t «{caso[0]}»", not difs, det))
        h = res[f"f5.thtml.{caso[0]}"]
        out.append((f"relatório t «{caso[0]}»", h["ok"] and "Hipóteses" in (h.get("valor") or ""),
                    h.get("erro") or "ok"))
    return out
