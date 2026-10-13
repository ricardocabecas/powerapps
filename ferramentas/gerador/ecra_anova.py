"""Ecrã 6 — ANOVA a um fator."""
from .yaml_pa import Ecra
from .comum import cabecalho, props_ecra, etiqueta, lista, retangulo, html, COR_SUAVE, COR_PAINEL, COR_LINHA
from .f_comum import itens_numericas, itens_categoricas, default_numerica, default_categorica
from . import f_inferencia as F

NOME = "scrAnova"


def construir():
    c = cabecalho(NOME, "ANOVA a um fator")
    X, W = 16, 330
    por_fator = f'drpAnoFormato.Selected.Value = "{F.FORMATOS_ANOVA[0]}"'
    c.append(retangulo("retAnoPainel", X - 4, 72, W + 8, 684, COR_PAINEL,
                       extra={"BorderColor": COR_LINHA, "BorderThickness": "1"}))
    campos = [
        ("Formato dos dados", "drpAnoFormato", "[" + ", ".join(f'"{t}"' for t in F.FORMATOS_ANOVA) + "]",
         f'"{F.FORMATOS_ANOVA[0]}"', "true"),
        ("Variável numérica (resposta)", "drpAnoVar", itens_numericas(), default_numerica(1), por_fator),
        ("Fator (variável de grupo)", "drpAnoFator", itens_categoricas(), default_categorica(2), por_fator),
        ("Nível de significância α", "drpAnoAlfa", "[" + ", ".join(f'"{a}"' for a in F.ALFAS) + "]", '"0,05"', "true"),
    ]
    y = 78
    for rot, nome, itens, defeito, vis in campos:
        c.append(etiqueta("lbl" + nome[3:], f'"{rot}"', X + 8, y, W - 16, 22, 10, True, extra={"Visible": vis}))
        c.append(lista(nome, itens, defeito, X + 8, y + 22, W - 16, 32, extra={"Visible": vis}))
        y += 60
    c.append(etiqueta("lblAnoNotas",
                      '"Notas" & Char(10) & Char(10) & '
                      '"• Formato «variável + fator»: cada linha da tabela de dados é uma observação; o fator diz a '
                      'que grupo pertence." & Char(10) & Char(10) & '
                      '"• Formato «colunas como grupos»: cada variável numérica (" & '
                      'Concat(Filter(varVariaveis, numerica), nome, ", ") & ") é um grupo." & Char(10) & Char(10) & '
                      '"• Com 2 grupos, a ANOVA dá o mesmo valor de p do teste t com variâncias iguais (F = t²)."',
                      X + 8, y + 8, W - 16, 300, 10, cor=COR_SUAVE, extra={"VerticalAlign": "VerticalAlign.Top"}))
    c.append(html("htmAnoResultado", F.html_anova(), X + W + 20, 72, 1366 - (X + W + 20) - 16, 684,
                  extra={"Fill": COR_PAINEL, "PaddingTop": "6", "PaddingLeft": "10", "PaddingRight": "10"}))
    return Ecra(NOME, props_ecra(), c, "ANOVA a um fator")
