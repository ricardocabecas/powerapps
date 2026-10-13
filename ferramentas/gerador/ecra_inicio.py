"""Ecrã 0 — Início: apresentação da app, estado dos dados e atalhos para cada secção.
O OnVisible deste ecrã (o primeiro da app) cria os dados de exemplo e os nomes das variáveis."""
from .yaml_pa import Ecra, Controlo
from .comum import (cabecalho, props_ecra, etiqueta, retangulo, pos, T_BOTAO, FONTE,
                    COR_PRIMARIA, COR_PRIMARIA_CLARA, COR_PAINEL, COR_LINHA, COR_SUAVE)
from . import f_dados as FD

NOME = "scrInicio"

# (ecrã, título do cartão, descrição, sufixo do nome dos controlos)
CARTOES = [
    ("scrDados", "1. Dados",
     "Escrever ou colar dados do Excel (vírgula ou ponto decimal) e dar nome às variáveis.", "Dad"),
    ("scrDescritiva", "2. Estatística descritiva",
     "Média, mediana, moda, quartis, variância e desvio padrão (amostral e populacional), CV.", "Des"),
    ("scrFrequencias", "3. Frequências e gráficos",
     "Tabelas de frequências (valores ou classes), histograma e diagrama de barras.", "Fre"),
    ("scrRegressao", "4. Correlação e regressão",
     "Coeficiente de Pearson, R², reta dos mínimos quadrados, previsão e diagrama de dispersão.", "Reg"),
    ("scrTestesT", "5. Testes t",
     "Uma amostra, duas amostras independentes (variâncias iguais ou Welch) e emparelhadas.", "Tt"),
    ("scrAnova", "6. ANOVA",
     "Análise de variância a um fator com a tabela completa (SQ, gl, QM, F e valor de p).", "Ano"),
    ("scrQuiQuadrado", "7. Qui-quadrado",
     "Testes de aderência e de independência, com frequências esperadas.", "Qui"),
]


def construir():
    c = cabecalho(NOME, "Início")
    X0, Y0 = 40, 84
    c.append(etiqueta("lblIniTitulo", '"Estatística — aulas práticas"', X0, Y0, 900, 48, 26, True, COR_PRIMARIA))
    c.append(etiqueta("lblIniSubtitulo",
                      '"Escolha uma secção. Comece pelos Dados: a app traz um exemplo com 20 estudantes fictícios, '
                      'que pode substituir pelos seus dados (escritos à mão ou colados do Excel)."',
                      X0, Y0 + 50, 1286, 44, 13, cor=COR_SUAVE))
    # Estado atual dos dados
    c.append(retangulo("retIniEstado", X0, Y0 + 104, 1286, 56, COR_PRIMARIA_CLARA,
                       extra={"BorderColor": COR_LINHA, "BorderThickness": "1"}))
    c.append(etiqueta("lblIniEstado",
                      '"Dados atuais: " & CountRows(colDados) & " linhas   ·   Variáveis numéricas: " & '
                      'Coalesce(Concat(Filter(varVariaveis, numerica), nome, ", "), "nenhuma") & '
                      '"   ·   Categóricas: " & '
                      'Coalesce(Concat(Filter(varVariaveis, !numerica && n > 0), nome, ", "), "nenhuma")',
                      X0 + 16, Y0 + 104, 1254, 56, 12, extra={"PaddingLeft": "4"}))
    # Cartões: 4 na 1.ª fila e 3 na 2.ª
    W, H, GAP = 304, 196, 22
    for i, (ecra, titulo, desc, s) in enumerate(CARTOES):
        lin, col = divmod(i, 4)
        x = X0 + col * (W + GAP) + (0 if lin == 0 else (W + GAP) // 2)
        y = Y0 + 184 + lin * (H + GAP)
        c.append(retangulo(f"retIniCartao{s}", x, y, W, H, COR_PAINEL,
                           extra={"BorderColor": COR_LINHA, "BorderThickness": "1"}))
        c.append(etiqueta(f"lblIniDesc{s}", '"' + desc + '"', x + 16, y + 72, W - 32, 70, 11, cor=COR_SUAVE,
                          extra={"VerticalAlign": "VerticalAlign.Top"}))
        c.append(Controlo(f"btnIniAbrir{s}", T_BOTAO, {
            "Text": '"' + titulo + '"', "OnSelect": f"Navigate({ecra}, ScreenTransition.Fade)",
            **pos(x + 16, y + 16, W - 32, 48), "Font": FONTE, "Size": "13", "FontWeight": "FontWeight.Semibold",
            "Fill": COR_PRIMARIA, "Color": "RGBA(255, 255, 255, 1)", "HoverFill": "RGBA(23, 58, 91, 1)",
            "HoverColor": "RGBA(255, 255, 255, 1)", "BorderColor": COR_PRIMARIA,
            "RadiusTopLeft": "4", "RadiusTopRight": "4", "RadiusBottomLeft": "4", "RadiusBottomRight": "4"}))
        c.append(etiqueta(f"lblIniIr{s}", '"Abrir →"', x + 16, y + H - 42, W - 32, 30, 11, True, COR_PRIMARIA,
                          extra={"Align": "Align.Right", "OnSelect": f"Navigate({ecra}, ScreenTransition.Fade)"}))
    c.append(etiqueta("lblIniRodape",
                      '"Números com vírgula decimal (pt-PT). Em todos os testes: rejeita-se H₀ quando p ≤ α. '
                      'As fórmulas estão explicadas no documento «Fórmulas da app de Estatística»."',
                      X0, 720, 1286, 36, 10, cor=COR_SUAVE))
    return Ecra(NOME, props_ecra(FD.iniciar()), c, "Início")
