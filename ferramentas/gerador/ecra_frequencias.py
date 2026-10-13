"""Ecrã 3 — Tabelas de frequências e gráficos (histograma / diagrama de barras)."""
from .yaml_pa import Ecra
from .comum import (cabecalho, props_ecra, etiqueta, lista, caixa_texto, retangulo, galeria, imagem,
                    COR_SUAVE, COR_PAINEL, COR_LINHA, COR_PRIMARIA, COR_ERRO)
from .f_comum import itens_todas, indice_todas, fmt, e_numerica, default_numerica
from . import f_frequencias as F
from . import f_graficos as G

NOME = "scrFrequencias"
COLS = [("Classe / valor", 170, "ThisItem.Classe", "Align.Left"),
        ("nᵢ", 50, 'Text(ThisItem.ni, "[$-en-US]0", "pt-PT")', "Align.Right"),
        ("fᵢ", 70, fmt("ThisItem.fi"), "Align.Right"),
        ("fᵢ (%)", 66, fmt("ThisItem.fi * 100", 2), "Align.Right"),
        ("Nᵢ", 50, 'Text(ThisItem.Ni, "[$-en-US]0", "pt-PT")', "Align.Right"),
        ("Fᵢ", 64, fmt("ThisItem.Fi"), "Align.Right")]


def construir():
    c = cabecalho(NOME, "Frequências e gráficos")
    X, W = 16, 300
    classes = f'{e_numerica(indice_todas("drpFreVar"))} && drpFreTipo.Selected.Value = "{F.TIPOS[1]}"'
    c.append(retangulo("retFrePainel", X - 4, 72, W + 8, 684, COR_PAINEL,
                       extra={"BorderColor": COR_LINHA, "BorderThickness": "1"}))
    c.append(etiqueta("lblFreVar", '"Variável"', X + 8, 80, W - 16, 26, 11, True))
    c.append(lista("drpFreVar", itens_todas(), default_numerica(1), X + 8, 108, W - 16, 36))
    c.append(etiqueta("lblFreTipo", '"Tipo de tabela"', X + 8, 154, W - 16, 26, 11, True))
    c.append(lista("drpFreTipo", "[" + ", ".join(f'"{t}"' for t in F.TIPOS) + "]", f'"{F.TIPOS[0]}"',
                   X + 8, 182, W - 16, 36,
                   extra={"DisplayMode": f'If({e_numerica(indice_todas("drpFreVar"))}, DisplayMode.Edit, DisplayMode.Disabled)'}))
    campos = [("K", "N.º de classes (vazio = regra de Sturges)", "ex.: 6"),
              ("Inicio", "Início da 1.ª classe (vazio = mínimo)", "ex.: 150"),
              ("Amplitude", "Amplitude das classes (vazio = automática)", "ex.: 5")]
    y = 228
    for suf, rot, dica in campos:
        c.append(etiqueta(f"lblFre{suf}", f'"{rot}"', X + 8, y, W - 16, 24, 10, extra={"Visible": classes}))
        c.append(caixa_texto(f"txtFre{suf}", '""', X + 8, y + 24, W - 16, 34, dica=dica,
                             extra={"Visible": classes}))
        y += 66
    c.append(etiqueta("lblFreResumo", f"With({{_F: {F.tabela()}}}, {F.resumo()})", X + 8, y + 4, W - 16, 150, 10,
                      extra={"VerticalAlign": "VerticalAlign.Top",
                             "Color": f'If(Find("⚠", Self.Text) > 0, {COR_ERRO}, RGBA(33, 37, 41, 1))'}))
    c.append(etiqueta("lblFreNotas",
                      '"nᵢ = frequência absoluta · fᵢ = nᵢ / n (relativa)" & Char(10) & '
                      '"Nᵢ e Fᵢ = frequências acumuladas (absoluta e relativa)" & Char(10) & '
                      '"Classes [Lᵢ ; Lᵢ₊₁[ fechadas à esquerda; a última é fechada dos dois lados."',
                      X + 8, 640, W - 16, 100, 10, cor=COR_SUAVE, extra={"VerticalAlign": "VerticalAlign.Top"}))

    # Tabela de frequências: cabeçalho + galeria
    XT = X + W + 16
    x = XT
    for i, (rot, w, _, al) in enumerate(COLS):
        c.append(etiqueta(f"lblFreCol{i + 1}", f'"{rot}"', x, 72, w, 34, 11, True, "RGBA(255, 255, 255, 1)",
                          extra={"Fill": COR_PRIMARIA, "Align": al, "PaddingLeft": "6", "PaddingRight": "6"}))
        x += w
    largura = x - XT
    filhos = []
    x = 0
    for i, (rot, w, f, al) in enumerate(COLS):
        filhos.append(etiqueta(f"lblFreGal{i + 1}", f, x, 0, w, 30, 11,
                               extra={"Align": al, "PaddingLeft": "6", "PaddingRight": "6"}))
        x += w
    c.append(galeria("galFrequencias", f"With({{_F: {F.tabela()}}}, _F.Linhas)", XT, 106, largura + 16, 650, 30,
                     filhos, extra={"TemplateFill": "If(Mod(ThisItem.Ordem, 2) = 1, RGBA(255, 255, 255, 1), "
                                                    "RGBA(243, 246, 250, 1))"}))

    # Gráfico
    XG = XT + largura + 32
    WG = 1366 - XG - 16
    grafico = (f"With({{_F: {F.tabela()}}},\n    If(_F.Tipo = 2,\n        "
               f"{G.histograma('_F', '\"Histograma — \" & drpFreVar.Selected.Value', 'drpFreVar.Selected.Value')},\n        "
               f"{G.barras('_F', '\"Diagrama de barras — \" & drpFreVar.Selected.Value', 'drpFreVar.Selected.Value')}))")
    c.append(imagem("imgFreGrafico", grafico, XG, 72, WG, round(WG * 400 / 640),
                    extra={"Fill": COR_PAINEL, "BorderColor": COR_LINHA, "BorderThickness": "1"}))
    return Ecra(NOME, props_ecra(), c, "Frequências e gráficos")
