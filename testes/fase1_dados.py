"""Fase 1 — Entrada de dados: leitura de texto colado, conversão de números e formatação."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ferramentas"))
from gerador import f_dados as F  # noqa: E402
from gerador.f_comum import num, invalido, fmt, NOMES_EXEMPLO, VARS  # noqa: E402
from motor import pfx_valor, controlo_lista, controlo_texto, iguais  # noqa: E402
from referencia import colagem as R  # noqa: E402
import dados_teste as D  # noqa: E402

NOME = "Fase 1 — Entrada de dados"


def _vars_colagem(texto, modo="Automático"):
    v = [{"nome": "varNomes", "expr": pfx_valor(NOMES_EXEMPLO)},
         {"nome": "drpCabecalho", "expr": controlo_lista(modo)},
         {"nome": "txtColar", "expr": controlo_texto(texto)},
         {"nome": "colColagem", "expr": F.linhas("txtColar.Text")},
         {"nome": "colColunas", "expr": F.colunas()}]
    for var in VARS:
        v.append({"nome": f"drpMap{var}", "expr": "{Selected: {Value: " + F.default_mapa(var) + "}}"})
    return v


def tarefas():
    t = []
    for nome, texto in D.COLAGENS.items():
        for modo in (["Automático", "Sim", "Não"] if nome == "virgula_com_cabecalho" else ["Automático"]):
            vs = _vars_colagem(texto, modo)
            t.append({"id": f"f1.colagem.{nome}.{modo}", "vars": vs, "expr": F.importar("0")})
            t.append({"id": f"f1.diagnostico.{nome}.{modo}", "vars": vs, "expr": F.texto_diagnostico()})
            t.append({"id": f"f1.colunas.{nome}.{modo}", "vars": vs, "expr": "colColunas"})
    for i, s in enumerate(D.NUMEROS):
        t.append({"id": f"f1.num.{i}", "expr": num(pfx_valor(s))})
        t.append({"id": f"f1.invalido.{i}", "expr": invalido(pfx_valor(s))})
    for i, x in enumerate(D.FORMATOS):
        t.append({"id": f"f1.fmt.{i}", "expr": fmt(pfx_valor(x))})
    return t


def _fmt_ref(x, sep):
    v = 0.0 if abs(x) < 0.00005 else x
    s = f"{v:,.4f}"
    return s.replace(",", "§").replace(".", ",").replace("§", sep)


def verificar(res):
    out = []
    for nome, texto in D.COLAGENS.items():
        for modo in (["Automático", "Sim", "Não"] if nome == "virgula_com_cabecalho" else ["Automático"]):
            ref = R.importar(texto, modo, NOMES_EXEMPLO)
            r = res[f"f1.colagem.{nome}.{modo}"]
            if not r["ok"]:
                out.append((f"colagem «{nome}» ({modo})", False, r.get("erro")))
                continue
            v = r["valor"]
            inv_pfx = sorted([(d["Linha"], d["Variavel"], d["Texto"]) for d in v["Invalidos"]])
            inv_ref = sorted([(d["Linha"], d["Variavel"], d["Texto"]) for d in ref["Invalidos"]])
            ok = (iguais(v["Linhas"], ref["Linhas"]) and inv_pfx == inv_ref and v["Cabecalho"] == ref["Cabecalho"]
                  and v["Nomes"] == ref["Nomes"])
            det = (f"{len(v['Linhas'])} linhas, cabeçalho={v['Cabecalho']}, {len(inv_pfx)} inválidos, "
                   f"mapa={ref['mapa']}")
            if not ok:
                det += f" | Power Fx={v} | referência={ref}"
            out.append((f"colagem «{nome}» ({modo})", ok, det))
            d = res[f"f1.diagnostico.{nome}.{modo}"]
            out.append((f"diagnóstico «{nome}» ({modo})", d["ok"] and isinstance(d.get("valor"), str),
                        (d.get("valor") or d.get("erro") or "").replace("\n", " ⏎ ")))
    for i, s in enumerate(D.NUMEROS):
        val, inv = R.numero(s)
        r1, r2 = res[f"f1.num.{i}"], res[f"f1.invalido.{i}"]
        ok = r1["ok"] and r2["ok"] and iguais(r1.get("valor"), val) and r2.get("valor") == inv
        out.append((f"número «{s}»", ok, f"Power Fx={r1.get('valor')} inválido={r2.get('valor')} | "
                                         f"referência={val} inválido={inv}"))
    seps = set()
    for i, x in enumerate(D.FORMATOS):
        r = res[f"f1.fmt.{i}"]
        txt = r.get("valor") or ""
        sep = next((c for c in txt if c in "\u00a0\u202f "), " ")
        seps.add(sep)
        esp = _fmt_ref(x, sep)
        out.append((f"formatação {x!r}", r["ok"] and txt == esp, f"Power Fx=«{txt}» esperado=«{esp}»"))
    return out
