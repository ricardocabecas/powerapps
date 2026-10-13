"""Construção dos dados de teste no formato da app: colDados com Tk (texto) e Xk (número) por variável,
varNomes e varVariaveis (calculada com a mesma fórmula da app)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ferramentas"))
from gerador import f_comum as FC  # noqa: E402
from motor import pfx_valor  # noqa: E402
from referencia.colagem import numero  # noqa: E402


def registos(colunas):
    """colunas: lista de listas (valores de V1, V2, …); None = célula vazia; texto ou número."""
    m = max((len(c) for c in colunas if c), default=0)
    regs = []
    for i in range(m):
        r = {"Id": i + 1}
        for k in range(1, FC.NV + 1):
            col = colunas[k - 1] if k - 1 < len(colunas) and colunas[k - 1] else []
            v = col[i] if i < len(col) else None
            t = FC.texto_pt(v)
            r[f"T{k}"] = t
            r[f"X{k}"] = numero(t)[0]
        regs.append(r)
    return regs


def vars_dados(colunas, nomes=None):
    """Variáveis de contexto: varNomes, colDados e varVariaveis."""
    nomes = nomes or FC.NOMES_EXEMPLO
    return [{"nome": "varNomes", "expr": pfx_valor(nomes)},
            {"nome": "colDados", "expr": pfx_valor(registos(colunas))},
            {"nome": "varVariaveis", "expr": FC.variaveis()}]


def nome(k):
    return FC.NOMES_EXEMPLO[f"V{k}"]
