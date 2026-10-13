"""Fase 2 — Estatística descritiva."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ferramentas"))
from gerador import f_descritiva as F  # noqa: E402
from gerador.f_comum import NOMES_EXEMPLO  # noqa: E402
from motor import pfx_valor, controlo_lista, iguais  # noqa: E402
from referencia import descritiva as R  # noqa: E402
import dados_teste as D  # noqa: E402
from modelo import vars_dados, nome as nome_var  # noqa: E402

NOME = "Fase 2 — Estatística descritiva"
CAMPOS = ["n", "soma", "media", "mediana", "moda", "minimo", "maximo", "amplitude", "q1", "q3", "varA", "varP",
          "dpA", "dpP", "cv"]


def contexto(vals, grupos, metodo):
    return vars_dados([vals, None, None, grupos]) + [
        {"nome": "drpDesVar", "expr": controlo_lista(nome_var(1))},
        {"nome": "drpDesGrupo", "expr": controlo_lista(nome_var(4) if grupos is not None else F.SEM_GRUPOS)},
        {"nome": "drpDesQuartis", "expr": controlo_lista(F.METODOS_QUARTIS[metodo - 1])}]


def tarefas():
    t = []
    for nome, (vals, grupos) in D.DESCRITIVA.items():
        for metodo in (1, 2, 3):
            vs = contexto(vals, grupos, metodo)
            t.append({"id": f"f2.{nome}.{metodo}", "vars": vs, "expr": F.colunas()})
            if metodo == 1:
                t.append({"id": f"f2.html.{nome}", "vars": vs, "expr": F.html()})
    return t


def verificar(res):
    out = []
    for nome, (vals, grupos) in D.DESCRITIVA.items():
        for metodo in (1, 2, 3):
            r = res[f"f2.{nome}.{metodo}"]
            if not r["ok"]:
                out.append((f"{nome} (quartis {metodo})", False, r.get("erro")))
                continue
            cols = r["valor"]
            refs = [("Total", R.descritiva(vals, metodo))]
            if grupos is not None:
                niveis = sorted(set(g for g, v in zip(grupos, vals) if g and v is not None))
                for g in niveis:
                    refs.append((g, R.descritiva([v for v, gg in zip(vals, grupos) if gg == g], metodo)))
            ok = len(cols) == len(refs)
            difs = []
            for col, (g, ref) in zip(cols, refs):
                if col["Grupo"] != g:
                    ok = False
                    difs.append(f"grupo {col['Grupo']}≠{g}")
                for c in CAMPOS:
                    if not iguais(col.get(c), ref[c], 1e-9):
                        ok = False
                        difs.append(f"{g}.{c}: Power Fx={col.get(c)} ref={ref[c]}")
            tot = cols[0] if cols else {}
            det = (f"n={tot.get('n')}, média={tot.get('media')}, Q1={tot.get('q1')}, Q3={tot.get('q3')}, "
                   f"s²={tot.get('varA')}, moda={tot.get('moda')}")
            out.append((f"{nome} (quartis {metodo})" + (" por grupo" if grupos else ""), ok,
                        det if ok else "; ".join(difs)))
        h = res[f"f2.html.{nome}"]
        out.append((f"{nome}: tabela HTML", h["ok"] and "<table" in (h.get("valor") or ""),
                    h.get("erro") or f"{len(h.get('valor') or '')} caracteres"))
    return out
