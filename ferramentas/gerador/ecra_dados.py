"""Ecrã 1 — Entrada de dados: tabela editável, nomes das variáveis e colagem do Excel."""
from .yaml_pa import Ecra, Controlo
from .comum import (cabecalho, props_ecra, etiqueta, botao, caixa_texto, lista, retangulo, galeria, pos,
                    T_TEXTO, T_BOTAO, FONTE, COR_PAINEL, COR_LINHA, COR_ERRO, COR_SUAVE, COR_PRIMARIA_CLARA)
from .f_comum import (VARS, NV, NOMES_EXEMPLO, NOMES_PADRAO, invalido, fmt_livre, registo_nomes, tabela_dados,
                      atualizar_variaveis, DADOS_EXEMPLO)
from . import f_dados as F

NOME = "scrDados"
X0 = 16          # margem esquerda
XCOL = 62        # início da 1.ª coluna de variáveis
WCOL = 96        # largura de cada coluna
PASSO = 100      # largura + intervalo


def _var(j):
    return f"LookUp(varVariaveis, k = {j})"


def construir():
    c = cabecalho(NOME, "Entrada de dados")

    # ---------- Tabela de dados (lado esquerdo) ----------
    c.append(etiqueta("lblDadosTitulo", '"Tabela de dados"', X0, 72, 300, 30, 14, True))
    c.append(etiqueta("lblDadosResumo",
                      '"Linhas: " & CountRows(colDados) & "   ·   Numéricas: " & '
                      'CountRows(Filter(varVariaveis, numerica)) & "   ·   Categóricas: " & '
                      'CountRows(Filter(varVariaveis, !numerica && n > 0)) & '
                      'With({_inv: Sum(varVariaveis, nInv)}, If(_inv > 0, "   ·   ⚠ Não numéricos: " & _inv, ""))',
                      300, 72, 416, 30, 11, cor=COR_SUAVE, extra={"Align": "Align.Right"}))
    c.append(etiqueta("lblDadosColN", '"N.º"', X0, 106, 44, 34, 11, True, extra={"Align": "Align.Center"}))
    for j, v in enumerate(VARS, start=1):
        x = XCOL + (j - 1) * PASSO
        c.append(caixa_texto(
            f"txtNome{v}", f"varNomes.{v}", x, 106, WCOL, 34, dica="Nome da variável",
            onchange=(f'// Muda o nome da variável (um nome vazio repõe o nome por omissão)\n'
                      f'Set(varNomes, Patch(varNomes, {{{v}: If(Len(Trim(Self.Text)) = 0, "{NOMES_PADRAO[v]}", '
                      f'Trim(Self.Text))}}));\n{atualizar_variaveis()}'),
            extra={"FontWeight": "FontWeight.Semibold", "Fill": COR_PRIMARIA_CLARA, "Size": "10"}))
        c.append(etiqueta(f"lblTipo{v}",
                          f'With({{_v: {_var(j)}}}, If(_v.n = 0, "vazia", _v.numerica, '
                          f'"numérica" & If(_v.nInv > 0, " ⚠", ""), "categórica"))',
                          x, 140, WCOL, 22, 9, cor=COR_SUAVE, extra={"Align": "Align.Center"}))

    # Linha da galeria: n.º, uma caixa por variável e botão apagar
    filhos = [etiqueta("lblGalId", "ThisItem.Id", 0, 4, 44, 32, 11, cor=COR_SUAVE,
                       extra={"Align": "Align.Center"})]
    for j, v in enumerate(VARS, start=1):
        x = XCOL - X0 + (j - 1) * PASSO
        numerica = f"{_var(j)}.numerica"
        filhos.append(Controlo(f"txtGal{v}", T_TEXTO, {
            # numa variável numérica mostra o número com vírgula decimal; senão, o texto escrito
            "Default": f"If({numerica} && !IsBlank(ThisItem.X{j}), {fmt_livre(f'ThisItem.X{j}')}, ThisItem.T{j})",
            "OnChange": F.onchange_celula(j),
            **pos(x, 4, WCOL, 32), "Font": FONTE, "Size": "11",
            "Align": f"If({numerica}, Align.Right, Align.Left)",
            "BorderColor": f"If({numerica} && {invalido('Self.Text')}, {COR_ERRO}, {COR_LINHA})",
            "HintText": '"vazio"'}))
    filhos.append(Controlo("btnGalApagar", T_BOTAO, {
        "Text": '"✕"',
        "OnSelect": ("// Apaga a linha, volta a numerar 1..n e atualiza os tipos das variáveis\n"
                     "RemoveIf(colDados, Id = ThisItem.Id);\n" + F.renumerar() + ";\n" + atualizar_variaveis()),
        **pos(XCOL - X0 + NV * PASSO, 6, 30, 28), "Font": FONTE, "Size": "11",
        "Fill": COR_PAINEL, "Color": COR_ERRO, "BorderColor": COR_LINHA, "BorderThickness": "1",
        "HoverFill": "RGBA(253, 236, 238, 1)", "HoverColor": COR_ERRO, "Tooltip": '"Apagar esta linha"'}))
    c.append(galeria("galDados", "colDados", X0, 166, 700, 500, 40, filhos, extra={
        "TemplateFill": "If(Mod(ThisItem.Id, 2) = 0, RGBA(248, 249, 250, 1), RGBA(255, 255, 255, 1))"}))

    vazios = ", ".join(f'T{j}: "", X{j}: Blank()' for j in range(1, NV + 1))
    c.append(botao("btnAdicionarLinha", '"+ Adicionar linha"',
                   "// Nova linha vazia no fim da tabela\n"
                   f"Collect(colDados, {{Id: Coalesce(Max(colDados, Id), 0) + 1, {vazios}}})",
                   X0, 676, 170, 36))
    c.append(botao("btnDadosExemplo", '"Repor dados de exemplo"',
                   f"Set(varNomes, {registo_nomes(NOMES_EXEMPLO)});\n"
                   f"ClearCollect(colDados, {tabela_dados(DADOS_EXEMPLO)});\n"
                   f"{atualizar_variaveis()};\n"
                   f"Set(varConfirmarApagar, false)",
                   X0 + 180, 676, 200, 36, primario=False))
    c.append(botao("btnApagarTudo",
                   'If(varConfirmarApagar, "Clique de novo para confirmar", "Apagar todos os dados")',
                   "// Pede confirmação: o 1.º clique arma, o 2.º apaga\n"
                   "If(varConfirmarApagar,\n    Clear(colDados);\n"
                   f"    {atualizar_variaveis().replace(chr(10), chr(10) + '    ')};\n"
                   "    Set(varConfirmarApagar, false),\n"
                   "    Set(varConfirmarApagar, true)\n)",
                   X0 + 390, 676, 250, 36, primario=False,
                   extra={"Color": COR_ERRO, "BorderColor": COR_ERRO, "HoverColor": COR_ERRO,
                          "HoverFill": "RGBA(253, 236, 238, 1)"}))
    nomes = "[" + ", ".join(f"varNomes.{v}" for v in VARS) + "]"
    c.append(etiqueta("lblAvisoNomes",
                      f'If(CountRows(Distinct({nomes}, Value)) < {NV}, "⚠ Há variáveis com o mesmo nome. Dê nomes '
                      'diferentes para as poder escolher nos outros ecrãs.", "O tipo de cada variável é detetado '
                      'automaticamente: numérica se pelo menos metade dos valores forem números (vírgula ou ponto '
                      'decimal); senão, categórica.")',
                      X0, 716, 700, 44, 10,
                      cor=f'If(CountRows(Distinct({nomes}, Value)) < {NV}, {COR_ERRO}, {COR_SUAVE})'))

    # ---------- Colagem a partir do Excel (lado direito) ----------
    XP, WP = 732, 618
    c.append(retangulo("retPainelColar", XP - 8, 72, WP + 16, 688, COR_PAINEL,
                       extra={"BorderColor": COR_LINHA, "BorderThickness": "1"}))
    c.append(etiqueta("lblColarTitulo", '"Colar dados do Excel"', XP, 78, 400, 30, 14, True))
    c.append(etiqueta("lblColarAjuda",
                      f'"Selecione até {NV} colunas no Excel, copie (Ctrl+C) e cole aqui (Ctrl+V). A 1.ª linha pode '
                      f'ter os nomes das variáveis. A 1.ª coluna colada vai para a variável 1, a 2.ª para a variável 2, '
                      f'e assim por diante. Aceita vírgula ou ponto decimal."',
                      XP, 106, WP, 44, 10, cor=COR_SUAVE))
    c.append(caixa_texto("txtColar", '""', XP, 152, WP, 190, dica="Cole aqui os dados (Ctrl+V)",
                         multilinha=True, extra={"Size": "10"}))
    c.append(etiqueta("lblCabecalho", '"A 1.ª linha é cabeçalho?"', XP, 350, 170, 34, 11))
    c.append(lista("drpCabecalho", '["Automático", "Sim", "Não"]', '"Automático"', XP + 172, 350, 130, 34))
    c.append(botao("btnAnalisar", '"Analisar"',
                   "// Parte o texto em linhas e colunas e caracteriza cada coluna\n"
                   f"ClearCollect(colColagem, {F.linhas('txtColar.Text')});\n"
                   f"ClearCollect(colColunas, {F.colunas()})",
                   XP + 314, 350, 140, 34))
    c.append(botao("btnLimparColagem", '"Limpar"',
                   "Reset(txtColar);\nClear(colColagem);\nClear(colColunas)",
                   XP + 464, 350, WP - 464, 34, primario=False))
    c.append(etiqueta("lblDiagnostico", F.texto_diagnostico(), XP, 394, WP, 270, 10,
                      extra={"VerticalAlign": "VerticalAlign.Top", "Fill": "RGBA(248, 249, 250, 1)",
                             "PaddingLeft": "8", "PaddingTop": "6",
                             "Color": "If(CountRows(colColagem) > 0 && Find(\"⚠\", Self.Text) > 0, "
                                      f"{COR_ERRO}, RGBA(33, 37, 41, 1))"}))
    c.append(botao("btnImportarSubstituir", '"Importar (substituir dados)"', F.importar_substituir(),
                   XP, 676, 300, 40, extra={"DisplayMode":
                                            "If(CountRows(colColagem) > 0, DisplayMode.Edit, DisplayMode.Disabled)"}))
    c.append(botao("btnImportarAcrescentar", '"Importar (acrescentar)"', F.importar_acrescentar(),
                   XP + 312, 676, WP - 312, 40, primario=False,
                   extra={"DisplayMode": "If(CountRows(colColagem) > 0, DisplayMode.Edit, DisplayMode.Disabled)"}))

    return Ecra(NOME, props_ecra(), c, "Entrada de dados")
