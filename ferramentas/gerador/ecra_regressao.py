"""Ecrã 4 — Correlação e regressão linear simples."""
from .yaml_pa import Ecra
from .comum import (cabecalho, props_ecra, etiqueta, lista, caixa_texto, retangulo, html, imagem,
                    COR_SUAVE, COR_PAINEL, COR_LINHA)
from .f_comum import itens_numericas, indice_num
from . import f_regressao as F

NOME = "scrRegressao"


def grafico():
    return (f"With({{_R: {F.resultados()}, _P: {F.pares(indice_num('drpRegX'), indice_num('drpRegY'))}}},\n"
            f"    {F.dispersao('_R', '_P', '\"Dispersão — \" & drpRegY.Selected.Value & \" vs \" & drpRegX.Selected.Value', 'drpRegX.Selected.Value', 'drpRegY.Selected.Value')})")


def construir():
    c = cabecalho(NOME, "Correlação e regressão")
    X, W = 16, 300
    c.append(retangulo("retRegPainel", X - 4, 72, W + 8, 684, COR_PAINEL,
                       extra={"BorderColor": COR_LINHA, "BorderThickness": "1"}))
    c.append(etiqueta("lblRegX", '"Variável explicativa (x)"', X + 8, 80, W - 16, 26, 11, True))
    c.append(lista("drpRegX", itens_numericas(), "varNomes.N1", X + 8, 108, W - 16, 36))
    c.append(etiqueta("lblRegY", '"Variável resposta (y)"', X + 8, 154, W - 16, 26, 11, True))
    c.append(lista("drpRegY", itens_numericas(), "varNomes.N2", X + 8, 182, W - 16, 36))
    c.append(etiqueta("lblRegX0", '"Previsão: valor de x"', X + 8, 228, W - 16, 26, 11, True))
    c.append(caixa_texto("txtRegX0", '""', X + 8, 256, W - 16, 36, dica="ex.: 172,5"))
    c.append(etiqueta("lblRegNotas",
                      '"Notas" & Char(10) & Char(10) & '
                      '"• Só entram os pares com x e y preenchidos." & Char(10) & Char(10) & '
                      '"• r mede a intensidade da relação LINEAR (−1 ≤ r ≤ 1); r = 0 não exclui outras relações." '
                      '& Char(10) & Char(10) & '
                      '"• R² é a proporção da variabilidade de y explicada pela reta." & Char(10) & Char(10) & '
                      '"• A reta dos mínimos quadrados minimiza Σ(yᵢ − ŷᵢ)². Previsões fora do intervalo dos x '
                      'observados (extrapolação) são pouco fiáveis." & Char(10) & Char(10) & '
                      '"• Correlação não implica causalidade."',
                      X + 8, 304, W - 16, 440, 10, cor=COR_SUAVE, extra={"VerticalAlign": "VerticalAlign.Top"}))
    XH = X + W + 16
    WH = 430
    c.append(html("htmRegressao", F.html(), XH, 72, WH, 684,
                  extra={"Fill": COR_PAINEL, "PaddingTop": "8", "PaddingLeft": "8", "PaddingRight": "8"}))
    XG = XH + WH + 16
    WG = 1366 - XG - 16
    c.append(imagem("imgRegDispersao", grafico(), XG, 72, WG, round(WG * 400 / 640),
                    extra={"Fill": COR_PAINEL, "BorderColor": COR_LINHA, "BorderThickness": "1"}))
    return Ecra(NOME, props_ecra(), c, "Correlação e regressão")
