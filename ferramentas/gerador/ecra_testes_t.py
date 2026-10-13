"""Ecrã 5 — Testes t (uma amostra, duas amostras independentes, Welch, emparelhadas)."""
from .yaml_pa import Ecra
from .comum import (cabecalho, props_ecra, etiqueta, lista, caixa_texto, retangulo, html,
                    COR_SUAVE, COR_PAINEL, COR_LINHA)
from .f_comum import itens_numericas, itens_categoricas, default_numerica, default_categorica
from . import f_inferencia as F

NOME = "scrTestesT"


def construir():
    c = cabecalho(NOME, "Testes t")
    X, W = 16, 330
    tipo = "drpTtTipo.Selected.Value"
    indep = f'({tipo} = "{F.TIPOS_T[1]}" || {tipo} = "{F.TIPOS_T[2]}")'
    emparelhado = f'{tipo} = "{F.TIPOS_T[3]}"'
    por_grupo = f'{indep} && drpTtFormato.Selected.Value = "{F.FORMATOS_IND[0]}"'
    duas_colunas = f'{emparelhado} || ({indep} && drpTtFormato.Selected.Value = "{F.FORMATOS_IND[1]}")'
    c.append(retangulo("retTtPainel", X - 4, 72, W + 8, 684, COR_PAINEL,
                       extra={"BorderColor": COR_LINHA, "BorderThickness": "1"}))
    y = 78

    def campo(nome_lbl, rotulo, controlo, visivel="true"):
        nonlocal y
        c.append(etiqueta(nome_lbl, f'"{rotulo}"', X + 8, y, W - 16, 22, 10, True, extra={"Visible": visivel}))
        controlo.props["Visible"] = visivel
        controlo.props["X"], controlo.props["Y"] = str(X + 8), str(y + 22)
        controlo.props["Width"], controlo.props["Height"] = str(W - 16), "32"
        c.append(controlo)
        y += 60

    campo("lblTtTipo", "Teste", lista("drpTtTipo", "[" + ", ".join(f'"{t}"' for t in F.TIPOS_T) + "]",
                                       f'"{F.TIPOS_T[0]}"', 0, 0, 0, 0))
    campo("lblTtFormato", "Formato dos dados", lista("drpTtFormato", "[" + ", ".join(f'"{t}"' for t in F.FORMATOS_IND) + "]",
                                                     f'"{F.FORMATOS_IND[0]}"', 0, 0, 0, 0), indep)
    campo("lblTtVar", "Variável numérica (1.ª amostra / X)",
          lista("drpTtVar", itens_numericas(), default_numerica(1), 0, 0, 0, 0))
    campo("lblTtVar2", "2.ª variável numérica (2.ª amostra / Y)",
          lista("drpTtVar2", itens_numericas(), default_numerica(2), 0, 0, 0, 0), duas_colunas)
    campo("lblTtGrupoVar", "Variável de grupo", lista("drpTtGrupoVar", itens_categoricas(), default_categorica(1), 0, 0, 0, 0),
          por_grupo)
    niveis = F.niveis(F.indice_cat("drpTtGrupoVar"))
    campo("lblTtGrupoA", "Grupo da amostra 1", lista("drpTtGrupoA", niveis, f"First({niveis}).Value", 0, 0, 0, 0),
          por_grupo)
    campo("lblTtGrupoB", "Grupo da amostra 2",
          lista("drpTtGrupoB", niveis, f"With({{_n: {niveis}}}, If(CountRows(_n) >= 2, Index(_n, 2).Value, First(_n).Value))",
                0, 0, 0, 0), por_grupo)
    campo("lblTtMu0", "Valor sob H₀ (μ₀ ou diferença Δ₀)", caixa_texto("txtTtMu0", '"0"', 0, 0, 0, 0, dica="ex.: 170"))
    campo("lblTtAlternativa", "Hipótese alternativa H₁",
          lista("drpTtAlternativa", "[" + ", ".join(f'"{t}"' for t in F.ALTERNATIVAS) + "]", f'"{F.ALTERNATIVAS[0]}"',
                0, 0, 0, 0))
    campo("lblTtAlfa", "Nível de significância α",
          lista("drpTtAlfa", "[" + ", ".join(f'"{a}"' for a in F.ALFAS) + "]", '"0,05"', 0, 0, 0, 0))
    c.append(html("htmTtResultado", F.html_teste_t(), X + W + 20, 72, 1366 - (X + W + 20) - 16, 684,
                  extra={"Fill": COR_PAINEL, "PaddingTop": "6", "PaddingLeft": "10", "PaddingRight": "10"}))
    return Ecra(NOME, props_ecra(), c, "Testes t")
