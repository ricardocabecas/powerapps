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


def importar(texto, modo_cab="Automático", nomes=None, nv=6):
    """Devolve o registo de importação como a app: a coluna j vai para a variável Vj (j = 1..nv);
    inválidos = textos não numéricos em colunas numéricas; nomes da 1.ª linha se for cabeçalho."""
    lin = linhas(texto)
    cols = colunas(lin)
    if modo_cab == "Sim":
        cab = True
    elif modo_cab == "Não":
        cab = False
    else:
        cab = len(lin) >= 2 and any(c["Numerica"] and c["Topo"] != "" and not c["TopoNumerico"] for c in cols)
    corpo = lin[1:] if cab else lin
    numcol = {c["Col"]: c["Numerica"] for c in cols}

    def cel(r, j):
        return r["Celulas"][j - 1] if 1 <= j <= len(r["Celulas"]) else ""
    novos = {}
    for j in range(1, nv + 1):
        h = cel(lin[0], j) if (cab and lin) else ""
        novos[f"V{j}"] = h if h != "" else f"Variável {j}"
    regs, inval = [], []
    for i, r in enumerate(corpo, start=1):
        reg = {"Id": i}
        for j in range(1, nv + 1):
            t = cel(r, j)
            val, inv = numero(t)
            reg[f"T{j}"], reg[f"X{j}"] = t, val
            if inv and numcol.get(j, False):
                inval.append({"Linha": r["Linha"], "Variavel": novos[f"V{j}"], "Texto": t})
        regs.append(reg)
    inval.sort(key=lambda d: d["Linha"])
    return {"Linhas": regs, "Invalidos": inval, "Cabecalho": cab, "Nomes": novos, "colunas": cols}
