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


def ctx_anova(caso):
    nome, fmt_, n1, fator, n2, n3 = caso
    return [{"nome": "varNomes", "expr": pfx_valor(NOMES_EXEMPLO)},
            {"nome": "colDados", "expr": pfx_valor(_col(n1, n2, None, fator, n3))},
            {"nome": "drpAnoFormato", "expr": controlo_lista(F.FORMATOS_ANOVA[fmt_ - 1])},
            {"nome": "drpAnoVar", "expr": controlo_lista(NOMES_EXEMPLO["N1"])},
            {"nome": "drpAnoFator", "expr": controlo_lista(NOMES_EXEMPLO["C2"])},
            {"nome": "drpAnoAlfa", "expr": controlo_lista("0,05")}]


def _ref_anova(caso):
    nome, fmt_, n1, fator, n2, n3 = caso
    if fmt_ == 1:
        niveis = sorted(set(g for g, x in zip(fator, n1) if g))
        grupos = [[x for x, g in zip(n1, fator) if g == nv and x is not None] for nv in niveis]
    else:
        grupos = [[x for x in col if x is not None] for col in (n1, n2, n3) if col]
    return R.anova(grupos)


def ctx_qui(caso):
    nome, tipo, orig, k1, k2, _, texto, esp, props, _ref = caso
    nomes = ["N1", "N2", "N3", "C1", "C2"]
    return [{"nome": "varNomes", "expr": pfx_valor(NOMES_EXEMPLO)},
            {"nome": "colDados", "expr": pfx_valor(_col([r[1] for r in D.DADOS_EXEMPLO], None,
                                                        [r[4] for r in D.DADOS_EXEMPLO], [r[5] for r in D.DADOS_EXEMPLO],
                                                        [r[3] for r in D.DADOS_EXEMPLO]))},
            {"nome": "drpQuiTipo", "expr": controlo_lista(F.TIPOS_QUI[tipo - 1])},
            {"nome": "drpQuiOrigem", "expr": controlo_lista(F.ORIGENS_QUI[orig - 1])},
            {"nome": "drpQuiVar1", "expr": controlo_lista(NOMES_EXEMPLO[nomes[k1 - 1]])},
            {"nome": "drpQuiVar2", "expr": controlo_lista(NOMES_EXEMPLO[nomes[k2 - 1]])},
            {"nome": "txtQuiTabela", "expr": controlo_texto(texto)},
            {"nome": "drpQuiEsperadas", "expr": controlo_lista(F.ESPERADAS_QUI[esp - 1])},
            {"nome": "txtQuiProporcoes", "expr": controlo_texto(props)},
            {"nome": "drpQuiAlfa", "expr": controlo_lista("0,05")}]


def tarefas():
    t = []
    for caso in D.QUI:
        vs = ctx_qui(caso)
        t.append({"id": f"f5.qui.{caso[0]}", "vars": vs, "expr": F.qui_quadrado()})
        t.append({"id": f"f5.quihtml.{caso[0]}", "vars": vs, "expr": F.html_qui()})
    for caso in D.ANOVA:
        vs = ctx_anova(caso)
        t.append({"id": f"f5.anova.{caso[0]}", "vars": vs, "expr": F.anova()})
        t.append({"id": f"f5.anovahtml.{caso[0]}", "vars": vs, "expr": F.html_anova()})
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
    for caso in D.QUI:
        nome, tipo = caso[0], caso[1]
        r = res[f"f5.qui.{nome}"]
        if not r["ok"]:
            out.append((f"qui-quadrado «{nome}»", False, r.get("erro")))
        else:
            v = r["valor"]
            refdef = caso[9]
            difs = []
            if refdef is None:
                # caso sem teste possível: o valor de p tem de ficar vazio, com motivo
                if v.get("p") is not None:
                    difs.append(f"esperava-se p vazio, Power Fx p={v.get('p')}")
                det = "teste não calculado: " + str(v.get("motivo"))
            else:
                obs, props = refdef
                if caso[2] == 1:
                    # origem = variáveis: contagens calculadas a partir dos dados de exemplo (não escritas à mão)
                    from collections import Counter
                    col = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
                    vals = lambda k: [r[col[k]] for r in D.DADOS_EXEMPLO]  # noqa: E731
                    a = vals(caso[3])
                    if tipo == 1:
                        cnt = Counter(a)
                        obs = [cnt[x] for x in sorted(cnt)]
                    else:
                        b = vals(caso[4])
                        la, lb = sorted(set(a)), sorted(set(b))
                        cnt = Counter(zip(a, b))
                        obs = [[cnt[(x, y)] for y in lb] for x in la]
                ref = R.qui_aderencia(obs, props) if tipo == 1 else R.qui_independencia(obs)
                esp_pfx = [c["E"] for c in sorted(v["Celulas"], key=lambda c: (c["i"], c["j"]))]
                esp_ref = ref["esperadas"] if tipo == 1 else [x for linha in ref["esperadas"] for x in linha]
                obs_pfx = [c["O"] for c in sorted(v["Celulas"], key=lambda c: (c["i"], c["j"]))]
                obs_ref = obs if tipo == 1 else [x for linha in obs for x in linha]
                if not iguais(obs_pfx, [float(x) for x in obs_ref]):
                    difs.append(f"observadas: Power Fx={obs_pfx} ref={obs_ref}")
                if not iguais(esp_pfx, esp_ref, 1e-9):
                    difs.append(f"esperadas: Power Fx={esp_pfx} ref={esp_ref}")
                for c in ["qui2", "gl", "baixas"]:
                    if not iguais(v.get(c), ref[c], 1e-9):
                        difs.append(f"{c}: Power Fx={v.get(c)} ref={ref[c]}")
                if v.get("p") is None or abs(v["p"] - ref["p"]) > 1e-6:
                    difs.append(f"p: Power Fx={v.get('p')} ref={ref['p']}")
                det = (f"χ²={v.get('qui2')}, gl={v.get('gl')}, p={v.get('p')} (scipy {ref['p']}), "
                       f"células com E<5: {v.get('baixas')}")
            out.append((f"qui-quadrado «{nome}»", not difs, det if not difs else "; ".join(difs)))
        h = res[f"f5.quihtml.{nome}"]
        out.append((f"relatório qui-quadrado «{nome}»", h["ok"] and "Hipóteses" in (h.get("valor") or ""),
                    h.get("erro") or "ok"))
    for caso in D.ANOVA:
        r = res[f"f5.anova.{caso[0]}"]
        ref = _ref_anova(caso)
        if not r["ok"]:
            out.append((f"ANOVA «{caso[0]}»", False, r.get("erro")))
        else:
            v = r["valor"]
            difs = [f"{c}: Power Fx={v.get(c)} ref={ref[c]}"
                    for c in ["k", "N", "SQE", "SQD", "SQT", "glE", "glD", "glT", "QME", "QMD", "F"]
                    if not iguais(v.get(c), ref[c], 1e-9)]
            if (v.get("p") is None) != (ref["p"] is None) or (ref["p"] is not None and abs(v["p"] - ref["p"]) > 1e-6):
                difs.append(f"p: Power Fx={v.get('p')} ref={ref['p']}")
            out.append((f"ANOVA «{caso[0]}»", not difs,
                        f"F={v.get('F')}, gl=({v.get('glE')}, {v.get('glD')}), p={v.get('p')} (scipy {ref['p']})"
                        if not difs else "; ".join(difs)))
        h = res[f"f5.anovahtml.{caso[0]}"]
        out.append((f"relatório ANOVA «{caso[0]}»", h["ok"] and "Tabela da ANOVA" in (h.get("valor") or ""),
                    h.get("erro") or "ok"))
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
