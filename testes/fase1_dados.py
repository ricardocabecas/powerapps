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
    return v


def _vars_pos_importacao(texto):
    """Contexto depois de carregar em Importar (substituir): colDados, varNomes e varVariaveis."""
    from gerador import f_comum as FC
    imp = F.importar("0")
    return _vars_colagem(texto) + [
        {"nome": "varImportacao", "expr": imp},
        {"nome": "colDados", "expr": "varImportacao.Linhas"},
        {"nome": "varNomes", "expr": "varImportacao.Nomes"},
        {"nome": "varVariaveis", "expr": FC.variaveis()}]


def tarefas():
    from gerador import f_comum as FC, f_descritiva as FD
    t = []
    vs = _vars_pos_importacao(D.COLAGENS["bovinos_excel"])
    t.append({"id": "f1.bovinos.numericas", "vars": vs, "expr": FC.itens_numericas()})
    t.append({"id": "f1.bovinos.todas", "vars": vs, "expr": FC.itens_todas()})
    t.append({"id": "f1.bovinos.descritiva", "vars": vs + [
        {"nome": "drpDesVar", "expr": controlo_lista("Prod. Leite")},
        {"nome": "drpDesGrupo", "expr": controlo_lista("Raça")},
        {"nome": "drpDesQuartis", "expr": controlo_lista(FD.METODOS_QUARTIS[0])}], "expr": FD.colunas()})
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
    # Caso real: Peso e Prod. Leite (contínuas) têm de aparecer nas listas de variáveis numéricas
    r1, r2, r3 = res["f1.bovinos.numericas"], res["f1.bovinos.todas"], res["f1.bovinos.descritiva"]
    num = [x["Value"] for x in r1.get("valor") or []]
    todas = [x["Value"] for x in r2.get("valor") or []]
    out.append(("caso real (bovinos): lista de variáveis numéricas", num == ["Numero", "Idade", "Peso", "Prod. Leite"],
                f"{num}"))
    out.append(("caso real (bovinos): lista de variáveis de grupo", todas == ["Numero", "Raça", "Idade", "Peso", "Prod. Leite"],
                f"{todas}"))
    leite = [166.1, 176.3, 137.2, 209.9, 147.7, 167.1, 191.1]
    racas = ["BBB", "Charolesa", "Cruzada", "Charolesa", "Charolesa", "Charolesa", "BBB"]
    ok3, det3 = r3["ok"], r3.get("erro", "")
    if ok3:
        cols = {c["Grupo"]: c for c in r3["valor"]}
        esperado = {"Total": leite, **{g: [x for x, rr in zip(leite, racas) if rr == g] for g in set(racas)}}
        ok3 = set(cols) == set(esperado) and all(
            iguais(cols[g]["media"], sum(v) / len(v)) and cols[g]["n"] == len(v) for g, v in esperado.items())
        det3 = ", ".join(f"{g}: n={c['n']}, média={c['media']:.4f}" for g, c in cols.items())
    out.append(("caso real (bovinos): descritiva de Prod. Leite por Raça", ok3, det3))
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
            tipos = ", ".join(f"{c['Col']}:{'num' if c['Numerica'] else 'cat'}" for c in ref["colunas"])
            det = (f"{len(v['Linhas'])} linhas, cabeçalho={v['Cabecalho']}, {len(inv_pfx)} inválidos, "
                   f"tipos das colunas = {tipos}")
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
