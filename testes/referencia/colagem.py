"""Implementação de referência (Python) da leitura de dados colados do Excel.

Segue a especificação da app, de forma independente das fórmulas Power Fx:
  * linhas separadas por LF (CR é ignorado), colunas separadas por tabulação;
  * cada célula é limpa como o Trim do Power Fx (espaços nas pontas removidos e
    espaços repetidos reduzidos a um); o espaço inseparável conta como espaço;
  * linhas sem nenhuma célula preenchida são ignoradas;
  * número: retiram-se todos os espaços, troca-se ',' por '.', e lê-se o número.
"""
import re

_NUM = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")


def trim(s):
    return re.sub(" +", " ", s).strip(" ")


def numero(t):
    n = t.replace(" ", "").replace(" ", "").replace(" ", "").replace(",", ".")
    if n == "":
        return None, False
    pct = n.endswith("%")
    if pct:
        n = n[:-1]
    if not _NUM.match(n):
        return None, True
    v = float(n)
    return (v / 100 if pct else v), False


def linhas(texto):
    res = []
    for i, l in enumerate(texto.replace("\r", "").split("\n"), start=1):
        cel = [trim(c.replace(" ", " ")) for c in l.split("\t")]
        if any(c != "" for c in cel):
            res.append({"Linha": i, "Celulas": cel})
    return res


def colunas(lin):
    m = len(lin)
    k = max((len(r["Celulas"]) for r in lin), default=0)
    corpo = lin[1:] if m >= 2 else lin
    res = []
    for j in range(k):
        txt = [r["Celulas"][j] if j < len(r["Celulas"]) else "" for r in corpo]
        topo = lin[0]["Celulas"][j] if j < len(lin[0]["Celulas"]) else ""
        nv = sum(1 for t in txt if t != "")
        nn = sum(1 for t in txt if t != "" and numero(t)[0] is not None)
        res.append({"Col": j + 1, "Topo": topo, "TopoNumerico": numero(topo)[0] is not None,
                    "NNaoVazias": nv, "NNumeros": nn, "Numerica": nn > 0 and 2 * nn >= nv})
    return res


def importar(texto, modo_cab="Automático", nomes=None, mapa=None):
    """Devolve (linhas, invalidos, cabecalho, nomes, mapa) como a app.
    mapa: dict var -> n.º da coluna (0 = nenhuma); se None usa a sugestão automática."""
    lin = linhas(texto)
    cols = colunas(lin)
    if modo_cab == "Sim":
        cab = True
    elif modo_cab == "Não":
        cab = False
    else:
        cab = len(lin) >= 2 and any(c["Numerica"] and c["Topo"] != "" and not c["TopoNumerico"] for c in cols)
    if mapa is None:
        num_cols = [c["Col"] for c in cols if c["Numerica"]]
        cat_cols = [c["Col"] for c in cols if not c["Numerica"] and c["NNaoVazias"] > 0]
        mapa = {}
        for i, v in enumerate(["N1", "N2", "N3"]):
            mapa[v] = num_cols[i] if i < len(num_cols) else 0
        for i, v in enumerate(["C1", "C2"]):
            mapa[v] = cat_cols[i] if i < len(cat_cols) else 0
    corpo = lin[1:] if cab else lin

    def cel(r, j):
        return r["Celulas"][j - 1] if 1 <= j <= len(r["Celulas"]) else ""
    novos = dict(nomes or {})
    if cab:
        for v in ["N1", "N2", "N3", "C1", "C2"]:
            if mapa[v] > 0:
                novos[v] = cel(lin[0], mapa[v])
    regs, inval = [], []
    for i, r in enumerate(corpo, start=1):
        reg = {"Id": i}
        for v in ["N1", "N2", "N3"]:
            t = cel(r, mapa[v])
            val, inv = numero(t)
            reg[v] = val
            if inv:
                inval.append({"Linha": r["Linha"], "Variavel": novos.get(v, v), "Texto": t})
        for v in ["C1", "C2"]:
            reg[v] = cel(r, mapa[v])
        regs.append(reg)
    inval.sort(key=lambda d: d["Linha"])
    return {"Linhas": regs, "Invalidos": inval, "Cabecalho": cab, "Nomes": novos, "mapa": mapa, "colunas": cols}
