"""Ecrã 7 — Testes do qui-quadrado (aderência e independência)."""
from .yaml_pa import Ecra
from .comum import (cabecalho, props_ecra, etiqueta, lista, caixa_texto, retangulo, html,
                    COR_SUAVE, COR_PAINEL, COR_LINHA)
from .f_comum import itens_todas
from . import f_inferencia as F

NOME = "scrQuiQuadrado"


def construir():
    c = cabecalho(NOME, "Testes do qui-quadrado")
    X, W = 16, 330
    ader = f'drpQuiTipo.Selected.Value = "{F.TIPOS_QUI[0]}"'
    indep = f'drpQuiTipo.Selected.Value = "{F.TIPOS_QUI[1]}"'
    vars_ = f'drpQuiOrigem.Selected.Value = "{F.ORIGENS_QUI[0]}"'
    colada = f'drpQuiOrigem.Selected.Value = "{F.ORIGENS_QUI[1]}"'
    indicadas = f'{ader} && drpQuiEsperadas.Selected.Value = "{F.ESPERADAS_QUI[1]}"'
    c.append(retangulo("retQuiPainel", X - 4, 72, W + 8, 684, COR_PAINEL,
                       extra={"BorderColor": COR_LINHA, "BorderThickness": "1"}))
    y = 78
    itens = lambda l: "[" + ", ".join(f'"{t}"' for t in l) + "]"  # noqa: E731

    def campo(sufixo, rotulo, ctl, visivel="true", altura=32):
        nonlocal y
        c.append(etiqueta("lbl" + sufixo, f'"{rotulo}"', X + 8, y, W - 16, 22, 10, True, extra={"Visible": visivel}))
        ctl.props.update({"X": str(X + 8), "Y": str(y + 22), "Width": str(W - 16), "Height": str(altura),
                          "Visible": visivel})
        c.append(ctl)
        y += 28 + altura

    campo("QuiTipo", "Teste", lista("drpQuiTipo", itens(F.TIPOS_QUI), f'"{F.TIPOS_QUI[0]}"', 0, 0, 0, 0))
    campo("QuiOrigem", "Origem das frequências", lista("drpQuiOrigem", itens(F.ORIGENS_QUI), f'"{F.ORIGENS_QUI[0]}"',
                                                       0, 0, 0, 0))
    y_var = y
    campo("QuiVar1", "Variável (linhas da tabela)", lista("drpQuiVar1", itens_todas(), "varNomes.C1", 0, 0, 0, 0), vars_)
    campo("QuiVar2", "Variável das colunas", lista("drpQuiVar2", itens_todas(), "varNomes.C2", 0, 0, 0, 0),
          f"{vars_} && {indep}")
    # a caixa da tabela colada ocupa o lugar das listas de variáveis
    y = y_var
    campo("QuiTabela", "Tabela de frequências (cole do Excel)",
          caixa_texto("txtQuiTabela", '""', 0, 0, 0, 0, dica="Cole a tabela (com ou sem nomes)", multilinha=True,
                      extra={"Size": "10"}), colada, altura=92)
    y = max(y, y_var + 2 * 60)
    campo("QuiEsperadas", "Frequências esperadas (aderência)",
          lista("drpQuiEsperadas", itens(F.ESPERADAS_QUI), f'"{F.ESPERADAS_QUI[0]}"', 0, 0, 0, 0), ader)
    campo("QuiProporcoes", "Proporções esperadas, pela ordem das categorias",
          caixa_texto("txtQuiProporcoes", '""', 0, 0, 0, 0, dica="ex.: 0,25; 0,5; 0,25 (ou uma por linha)",
                      multilinha=True, extra={"Size": "10"}), indicadas, altura=60)
    campo("QuiAlfa", "Nível de significância α",
          lista("drpQuiAlfa", "[" + ", ".join(f'"{a}"' for a in F.ALFAS) + "]", '"0,05"', 0, 0, 0, 0))
    c.append(etiqueta("lblQuiNotas",
                      '"As variáveis numéricas são tratadas como categorias (um valor = uma categoria). '
                      'Na tabela colada, a 1.ª linha e a 1.ª coluna podem ter os nomes das categorias. '
                      'Na aderência usa-se a 1.ª coluna de números. As proporções esperadas podem ser '
                      'proporções, percentagens ou pesos: são normalizadas para somar 1."',
                      X + 8, y + 4, W - 16, 756 - y - 12, 9, cor=COR_SUAVE, extra={"VerticalAlign": "VerticalAlign.Top"}))
    c.append(html("htmQuiResultado", F.html_qui(), X + W + 20, 72, 1366 - (X + W + 20) - 16, 684,
                  extra={"Fill": COR_PAINEL, "PaddingTop": "6", "PaddingLeft": "10", "PaddingRight": "10"}))
    return Ecra(NOME, props_ecra(), c, "Testes do qui-quadrado")
