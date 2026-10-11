"""Ecrã 1 — Entrada de dados: tabela editável, nomes das variáveis e colagem do Excel."""
from .yaml_pa import Ecra, Controlo
from .comum import (cabecalho, props_ecra, etiqueta, botao, caixa_texto, lista, retangulo, galeria, pos,
                    T_TEXTO, T_BOTAO, T_ETIQUETA, FONTE, COR_PAINEL, COR_LINHA, COR_ERRO, COR_SUAVE, COR_PRIMARIA,
                    COR_PRIMARIA_CLARA)
from .f_comum import VARS, VARS_NUM, VARS_CAT, num, invalido, fmt_livre, registo_nomes, tabela_dados, \
    DADOS_EXEMPLO, NOMES_EXEMPLO
from . import f_dados as F

NOME = "scrDados"
X0 = 16          # margem esquerda
XCOL = 64        # início da 1.ª coluna de dados
WCOL = 112       # largura de cada coluna
PASSO = 116      # largura + intervalo
NOMES_PADRAO = {"N1": "Variável 1", "N2": "Variável 2", "N3": "Variável 3", "C1": "Grupo 1", "C2": "Grupo 2"}


def construir():
    c = cabecalho(NOME, "Entrada de dados")

    # ---------- Tabela de dados (lado esquerdo) ----------
    c.append(etiqueta("lblDadosTitulo", '"Tabela de dados"', X0, 72, 300, 30, 14, True))
    c.append(etiqueta("lblDadosResumo",
                      '"Linhas: " & CountRows(colDados) & "   ·   Células numéricas vazias: " & '
                      '(CountRows(Filter(colDados, IsBlank(N1))) + CountRows(Filter(colDados, IsBlank(N2))) + '
                      'CountRows(Filter(colDados, IsBlank(N3))))',
                      330, 72, 380, 30, 11, cor=COR_SUAVE, extra={"Align": "Align.Right"}))
    c.append(etiqueta("lblDadosColN", '"N.º"', X0, 106, 44, 34, 11, True, extra={"Align": "Align.Center"}))
    for i, v in enumerate(VARS):
        x = XCOL + i * PASSO
        c.append(caixa_texto(
            f"txtNome{v}", f"varNomes.{v}", x, 106, WCOL, 34, dica="Nome da variável",
            onchange=(f'// Muda o nome da variável (um nome vazio repõe o nome por omissão)\n'
                      f'Set(varNomes, Patch(varNomes, {{{v}: If(Len(Trim(Self.Text)) = 0, "{NOMES_PADRAO[v]}", '
                      f'Trim(Self.Text))}}))'),
            extra={"FontWeight": "FontWeight.Semibold", "Fill": COR_PRIMARIA_CLARA, "Size": "11"}))
        c.append(etiqueta(f"lblTipo{v}", '"numérica"' if v in VARS_NUM else '"categórica (grupo)"',
                          x, 140, WCOL, 22, 9, cor=COR_SUAVE, extra={"Align": "Align.Center"}))

    # Linha da galeria: n.º, 3 numéricas, 2 categóricas e botão apagar
    filhos = [etiqueta("lblGalId", "ThisItem.Id", 0, 4, 44, 32, 11, cor=COR_SUAVE,
                       extra={"Align": "Align.Center"})]
    for i, v in enumerate(VARS):
        x = XCOL - X0 + i * PASSO
        if v in VARS_NUM:
            filhos.append(Controlo(f"txtGal{v}", T_TEXTO, {
                "Default": fmt_livre(f"ThisItem.{v}"),
                "OnChange": F.onchange_numero(v),
                **pos(x, 4, WCOL, 32), "Font": FONTE, "Size": "11", "Align": "Align.Right",
                "BorderColor": f"If({invalido('Self.Text')}, {COR_ERRO}, {COR_LINHA})",
                "HintText": '"vazio"'}))
        else:
            filhos.append(Controlo(f"txtGal{v}", T_TEXTO, {
                "Default": f"ThisItem.{v}",
                "OnChange": f"Patch(colDados, LookUp(colDados, Id = ThisItem.Id), {{{v}: Trim(Self.Text)}})",
                **pos(x, 4, WCOL, 32), "Font": FONTE, "Size": "11", "BorderColor": COR_LINHA,
                "HintText": '"vazio"'}))
    filhos.append(Controlo("btnGalApagar", T_BOTAO, {
        "Text": '"✕"',
        "OnSelect": "// Apaga a linha e volta a numerar 1..n\nRemoveIf(colDados, Id = ThisItem.Id);\n" + F.renumerar(),
        **pos(XCOL - X0 + 5 * PASSO, 6, 32, 28), "Font": FONTE, "Size": "11",
        "Fill": COR_PAINEL, "Color": COR_ERRO, "BorderColor": COR_LINHA, "BorderThickness": "1",
        "HoverFill": "RGBA(253, 236, 238, 1)", "HoverColor": COR_ERRO, "Tooltip": '"Apagar esta linha"'}))
    c.append(galeria("galDados", "colDados", X0, 166, 700, 500, 40, filhos, extra={
        "TemplateFill": "If(Mod(ThisItem.Id, 2) = 0, RGBA(248, 249, 250, 1), RGBA(255, 255, 255, 1))"}))

    c.append(botao("btnAdicionarLinha", '"+ Adicionar linha"',
                   "// Nova linha vazia no fim da tabela\n"
                   "Collect(colDados, {Id: Coalesce(Max(colDados, Id), 0) + 1, N1: Blank(), N2: Blank(), "
                   'N3: Blank(), C1: "", C2: ""})',
                   X0, 676, 170, 36))
    c.append(botao("btnDadosExemplo", '"Repor dados de exemplo"',
                   f"Set(varNomes, {registo_nomes(NOMES_EXEMPLO)});\n"
                   f"ClearCollect(colDados, {tabela_dados(DADOS_EXEMPLO)});\n"
                   f"Set(varConfirmarApagar, false)",
                   X0 + 180, 676, 200, 36, primario=False))
    c.append(botao("btnApagarTudo",
                   'If(varConfirmarApagar, "Clique de novo para confirmar", "Apagar todos os dados")',
                   "// Pede confirmação: o 1.º clique arma, o 2.º apaga\n"
                   "If(varConfirmarApagar,\n    Clear(colDados);\n    Set(varConfirmarApagar, false),\n"
                   "    Set(varConfirmarApagar, true)\n)",
                   X0 + 390, 676, 250, 36, primario=False,
                   extra={"Color": COR_ERRO, "BorderColor": COR_ERRO, "HoverColor": COR_ERRO,
                          "HoverFill": "RGBA(253, 236, 238, 1)"}))
    c.append(etiqueta("lblAvisoNomes",
                      'If(CountRows(Distinct([varNomes.N1, varNomes.N2, varNomes.N3, varNomes.C1, varNomes.C2], '
                      'Value)) < 5, "⚠ Há variáveis com o mesmo nome. Dê nomes diferentes para as poder escolher '
                      'nos outros ecrãs.", "Dica: clique no cabeçalho de uma coluna para mudar o nome da variável. '
                      'Pode usar vírgula ou ponto decimal.")',
                      X0, 718, 700, 40, 10,
                      cor=f'If(CountRows(Distinct([varNomes.N1, varNomes.N2, varNomes.N3, varNomes.C1, '
                          f'varNomes.C2], Value)) < 5, {COR_ERRO}, {COR_SUAVE})'))

    # ---------- Colagem a partir do Excel (lado direito) ----------
    XP, WP = 732, 618
    c.append(retangulo("retPainelColar", XP - 8, 72, WP + 16, 688, COR_PAINEL,
                       extra={"BorderColor": COR_LINHA, "BorderThickness": "1"}))
    c.append(etiqueta("lblColarTitulo", '"Colar dados do Excel"', XP, 78, 400, 30, 14, True))
    c.append(etiqueta("lblColarAjuda",
                      '"Selecione uma ou várias colunas no Excel, copie (Ctrl+C) e cole aqui (Ctrl+V). '
                      'A 1.ª linha pode ter os nomes das variáveis. Aceita vírgula ou ponto decimal."',
                      XP, 106, WP, 44, 10, cor=COR_SUAVE))
    c.append(caixa_texto("txtColar", '""', XP, 152, WP, 160, dica="Cole aqui os dados (Ctrl+V)",
                         multilinha=True, extra={"Size": "10"}))
    c.append(etiqueta("lblCabecalho", '"A 1.ª linha é cabeçalho?"', XP, 320, 170, 34, 11))
    c.append(lista("drpCabecalho", '["Automático", "Sim", "Não"]', '"Automático"', XP + 172, 320, 130, 34))
    c.append(botao("btnAnalisar", '"Analisar"',
                   "// Parte o texto em linhas e colunas e caracteriza cada coluna\n"
                   f"ClearCollect(colColagem, {F.linhas('txtColar.Text')});\n"
                   f"ClearCollect(colColunas, {F.colunas()})",
                   XP + 314, 320, 140, 34))
    c.append(botao("btnLimparColagem", '"Limpar"',
                   "Reset(txtColar);\nClear(colColagem);\nClear(colColunas)",
                   XP + 464, 320, WP - 464, 34, primario=False))
    c.append(etiqueta("lblDiagnostico", F.texto_diagnostico(), XP, 362, WP, 150, 10,
                      extra={"VerticalAlign": "VerticalAlign.Top", "Fill": "RGBA(248, 249, 250, 1)",
                             "PaddingLeft": "8", "PaddingTop": "6",
                             "Color": "If(CountRows(colColagem) > 0 && Find(\"⚠\", Self.Text) > 0, "
                                      f"{COR_ERRO}, RGBA(33, 37, 41, 1))"}))
    c.append(etiqueta("lblMapaTitulo", '"Coluna de origem de cada variável (— = nenhuma)"', XP, 518, WP, 26, 11,
                      True))
    for i, v in enumerate(VARS):
        col, lin = (0, i) if v in VARS_NUM else (1, i - 3)
        x = XP + col * 312
        y = 548 + lin * 40
        c.append(etiqueta(f"lblMapa{v}", f"varNomes.{v}", x, y, 140, 34, 10))
        c.append(lista(f"drpMap{v}", F.itens_mapa(), F.default_mapa(v), x + 142, y, 156, 34))
    c.append(botao("btnImportarSubstituir", '"Importar (substituir dados)"', F.importar_substituir(),
                   XP, 676, 300, 40, extra={"DisplayMode":
                                            "If(CountRows(colColagem) > 0, DisplayMode.Edit, DisplayMode.Disabled)"}))
    c.append(botao("btnImportarAcrescentar", '"Importar (acrescentar)"', F.importar_acrescentar(),
                   XP + 312, 676, WP - 312, 40, primario=False,
                   extra={"DisplayMode": "If(CountRows(colColagem) > 0, DisplayMode.Edit, DisplayMode.Disabled)"}))

    return Ecra(NOME, props_ecra(F.iniciar()), c, "Entrada de dados")
