"""Elementos comuns da interface: cores, tipos de controlo e barra de navegação.

Tipos de controlo usados (identificadores invariantes do esquema pa.yaml v3.0).
Não se indica versão ("Control: Label" em vez de "Control: Label@x.y.z"): segundo a
documentação, sem versão o Studio usa a versão mais recente do controlo.
Os controlos clássicos que têm equivalente moderno usam o prefixo "Classic/".
"""
from .yaml_pa import Controlo

# Identificadores dos tipos de controlo (alterar aqui se o Studio exigir outro nome).
T_ETIQUETA = "Label"
T_BOTAO = "Classic/Button"
T_TEXTO = "Classic/TextInput"
T_LISTA = "Classic/DropDown"
T_GALERIA = "Gallery"
V_GALERIA = "BrowseLayout_Vertical_TwoTextOneImageVariant_ver5.0"
T_IMAGEM = "Image"
T_HTML = "HtmlViewer"
T_RETANGULO = "Rectangle"

# Paleta (contraste AA sobre branco)
COR_PRIMARIA = "RGBA(31, 78, 121, 1)"
COR_PRIMARIA_CLARA = "RGBA(222, 235, 247, 1)"
COR_FUNDO = "RGBA(244, 246, 249, 1)"
COR_PAINEL = "RGBA(255, 255, 255, 1)"
COR_TEXTO = "RGBA(33, 37, 41, 1)"
COR_SUAVE = "RGBA(90, 98, 106, 1)"
COR_LINHA = "RGBA(206, 212, 218, 1)"
COR_ERRO = "RGBA(176, 0, 32, 1)"
COR_SUCESSO = "RGBA(16, 124, 16, 1)"
FONTE = "Font.'Segoe UI'"

LARGURA = 1366
ALTURA = 768
ALTURA_CAB = 64

# Ecrãs da app, pela ordem da barra de navegação: (nome do ecrã, rótulo do botão, sufixo)
ECRAS = [
    ("scrDados", "Dados", "Dad"),
    ("scrDescritiva", "Descritiva", "Des"),
    ("scrFrequencias", "Frequências", "Fre"),
    ("scrRegressao", "Regressão", "Reg"),
    ("scrTestesT", "Testes t", "Tt"),
    ("scrAnova", "ANOVA", "Ano"),
    ("scrQuiQuadrado", "Qui-quadrado", "Qui"),
]


def pos(x, y, w, h):
    return {"X": str(x), "Y": str(y), "Width": str(w), "Height": str(h)}


def etiqueta(nome, texto, x, y, w, h, tamanho=12, negrito=False, cor=COR_TEXTO, extra=None):
    p = {"Text": texto, **pos(x, y, w, h), "Font": FONTE, "Size": str(tamanho), "Color": cor}
    if negrito:
        p["FontWeight"] = "FontWeight.Semibold"
    p.update(extra or {})
    return Controlo(nome, T_ETIQUETA, p)


def botao(nome, texto, onselect, x, y, w, h, primario=True, extra=None):
    p = {"Text": texto, "OnSelect": onselect, **pos(x, y, w, h), "Font": FONTE, "Size": "12",
         "RadiusTopLeft": "4", "RadiusTopRight": "4", "RadiusBottomLeft": "4", "RadiusBottomRight": "4"}
    if primario:
        p.update({"Fill": COR_PRIMARIA, "Color": "RGBA(255, 255, 255, 1)", "HoverFill": "RGBA(23, 58, 91, 1)",
                  "BorderColor": COR_PRIMARIA})
    else:
        p.update({"Fill": COR_PAINEL, "Color": COR_PRIMARIA, "HoverFill": COR_PRIMARIA_CLARA,
                  "HoverColor": COR_PRIMARIA, "BorderColor": COR_PRIMARIA, "BorderThickness": "1"})
    p.update(extra or {})
    return Controlo(nome, T_BOTAO, p)


def caixa_texto(nome, default, x, y, w, h, dica="", onchange=None, multilinha=False, extra=None):
    p = {"Default": default, **pos(x, y, w, h), "Font": FONTE, "Size": "12", "BorderColor": COR_LINHA}
    if dica:
        p["HintText"] = _t(dica)
    if onchange:
        p["OnChange"] = onchange
    if multilinha:
        p["Mode"] = "TextMode.MultiLine"
    p.update(extra or {})
    return Controlo(nome, T_TEXTO, p)


def lista(nome, itens, default, x, y, w, h, onchange=None, extra=None):
    p = {"Items": itens, **pos(x, y, w, h), "Font": FONTE, "Size": "12"}
    if default:
        p["Default"] = default
    if onchange:
        p["OnChange"] = onchange
    p.update(extra or {})
    return Controlo(nome, T_LISTA, p)


def retangulo(nome, x, y, w, h, cor=COR_PAINEL, extra=None):
    p = {"Fill": cor, **pos(x, y, w, h)}
    p.update(extra or {})
    return Controlo(nome, T_RETANGULO, p)


def html(nome, formula, x, y, w, h, extra=None):
    p = {"HtmlText": formula, **pos(x, y, w, h), "Font": FONTE, "Size": "12", "Color": COR_TEXTO}
    p.update(extra or {})
    return Controlo(nome, T_HTML, p)


def imagem(nome, formula, x, y, w, h, extra=None):
    p = {"Image": formula, **pos(x, y, w, h), "ImagePosition": "ImagePosition.Fit"}
    p.update(extra or {})
    return Controlo(nome, T_IMAGEM, p)


def galeria(nome, itens, x, y, w, h, altura_linha, filhos, extra=None):
    p = {"Items": itens, **pos(x, y, w, h), "TemplateSize": str(altura_linha), "TemplatePadding": "0",
         "ShowScrollbar": "true", "BorderColor": COR_LINHA, "BorderThickness": "1", "Fill": COR_PAINEL}
    p.update(extra or {})
    return Controlo(nome, T_GALERIA, p, variante=V_GALERIA, filhos=filhos)


def cabecalho(ecra_atual, titulo):
    """Barra superior com o título e os botões de navegação (nomes únicos por ecrã)."""
    suf = dict((e, s) for e, _, s in ECRAS)[ecra_atual]
    ctl = [
        retangulo(f"retCab{suf}", 0, 0, LARGURA, ALTURA_CAB, COR_PRIMARIA),
        etiqueta(f"lblCab{suf}", '"Estatística · " & ' + _t(titulo), 16, 0, 420, ALTURA_CAB, 18, True,
                 "RGBA(255, 255, 255, 1)"),
    ]
    x = 446
    for nome, rotulo, s in ECRAS:
        ativo = nome == ecra_atual
        w = 124 if rotulo == "Qui-quadrado" else 120 if rotulo == "Frequências" else 112
        p = {"Text": _t(rotulo), "OnSelect": f"Navigate({nome}, ScreenTransition.None)", **pos(x, 14, w, 36),
             "Font": FONTE, "Size": "11",
             "Fill": "RGBA(255, 255, 255, 1)" if ativo else COR_PRIMARIA,
             "Color": COR_PRIMARIA if ativo else "RGBA(255, 255, 255, 1)",
             "HoverFill": "RGBA(255, 255, 255, 1)" if ativo else "RGBA(23, 58, 91, 1)",
             "HoverColor": COR_PRIMARIA if ativo else "RGBA(255, 255, 255, 1)",
             "BorderColor": "RGBA(255, 255, 255, 1)", "BorderThickness": "1",
             "RadiusTopLeft": "4", "RadiusTopRight": "4", "RadiusBottomLeft": "4", "RadiusBottomRight": "4"}
        if ativo:
            p["FontWeight"] = "FontWeight.Semibold"
        ctl.append(Controlo(f"btnNav{suf}{s}", T_BOTAO, p))
        x += w + 6
    return ctl


def _t(s):
    return '"' + s.replace('"', '""') + '"'


def props_ecra(onvisible=None):
    p = {"Fill": COR_FUNDO}
    if onvisible:
        p["OnVisible"] = onvisible
    return p
