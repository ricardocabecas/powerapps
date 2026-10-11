"""Ecrã 2 — Estatística descritiva."""
from .yaml_pa import Ecra
from .comum import cabecalho, props_ecra, etiqueta, lista, html, retangulo, COR_SUAVE, COR_PAINEL, COR_LINHA
from .f_comum import itens_numericas
from . import f_descritiva as F

NOME = "scrDescritiva"


def construir():
    c = cabecalho(NOME, "Estatística descritiva")
    X, W = 16, 330
    c.append(retangulo("retDesPainel", X - 4, 72, W + 8, 684, COR_PAINEL,
                       extra={"BorderColor": COR_LINHA, "BorderThickness": "1"}))
    c.append(etiqueta("lblDesVar", '"Variável numérica"', X + 8, 80, W - 16, 26, 11, True))
    c.append(lista("drpDesVar", itens_numericas(), "", X + 8, 108, W - 16, 36))
    c.append(etiqueta("lblDesGrupo", '"Agrupar por (opcional)"', X + 8, 154, W - 16, 26, 11, True))
    c.append(lista("drpDesGrupo", f'["{F.SEM_GRUPOS}", varNomes.C1, varNomes.C2]', f'"{F.SEM_GRUPOS}"',
                   X + 8, 182, W - 16, 36))
    c.append(etiqueta("lblDesQuartis", '"Método de cálculo dos quartis"', X + 8, 228, W - 16, 26, 11, True))
    c.append(lista("drpDesQuartis", "[" + ", ".join(f'"{m}"' for m in F.METODOS_QUARTIS) + "]",
                   f'"{F.METODOS_QUARTIS[0]}"', X + 8, 256, W - 16, 36))
    c.append(etiqueta("lblDesAjuda",
                      '"Notas" & Char(10) & Char(10) & '
                      '"• Amostral (divisor n − 1): estima a variância da população a partir de uma amostra. '
                      'É a que se usa na inferência." & Char(10) & Char(10) & '
                      '"• Populacional (divisor n): quando os dados são a população inteira." & Char(10) & Char(10) & '
                      '"• Quartis: há várias definições. QUARTIL.INC usa a posição (n − 1)p + 1; QUARTIL.EXC e o '
                      'SPSS usam (n + 1)p; muitos manuais usam a mediana de cada metade (sem o valor central '
                      'quando n é ímpar). A mediana é igual nos três métodos." & Char(10) & Char(10) & '
                      '"• CV = s / |x̄| × 100 (com o desvio padrão amostral)."',
                      X + 8, 304, W - 16, 440, 10, cor=COR_SUAVE,
                      extra={"VerticalAlign": "VerticalAlign.Top"}))
    c.append(html("htmDescritiva", F.html(), X + W + 20, 72, 1366 - (X + W + 20) - 16, 684,
                  extra={"Fill": COR_PAINEL, "PaddingTop": "8", "PaddingLeft": "8", "PaddingRight": "8"}))
    return Ecra(NOME, props_ecra(), c, "Estatística descritiva")
