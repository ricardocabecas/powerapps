"""Fórmulas do ecrã de entrada de dados (formato invariante)."""
from .f_comum import (num, invalido, tabela_dados, registo_nomes, DADOS_EXEMPLO, NOMES_EXEMPLO,
                      VARS, VARS_NUM, VARS_CAT)


def iniciar():
    return f"""// Inicialização: corre apenas na primeira vez que o ecrã é aberto
If(!varIniciado,
    Set(varIniciado, true);
    // Nomes das variáveis (podem ser alterados no cabeçalho da tabela)
    Set(varNomes, {registo_nomes(NOMES_EXEMPLO)});
    // Coleção com os dados: N1-N3 numéricas, C1-C2 categóricas (grupo)
    ClearCollect(colDados, {tabela_dados(DADOS_EXEMPLO).replace(chr(10), chr(10) + "    ")});
    // Coleções auxiliares da colagem (ficam vazias até carregar em Analisar)
    ClearCollect(colColagem, {LINHAS_VAZIA});
    Clear(colColagem);
    ClearCollect(colColunas, {COLUNAS_VAZIA});
    Clear(colColunas)
)"""


# Registos-modelo para criar as coleções auxiliares com o tipo certo
LINHAS_VAZIA = '{Linha: 0, Celulas: Table({Texto: ""}), NCel: 0}'
COLUNAS_VAZIA = ('{Col: 0, Topo: "", TopoNumerico: false, NNaoVazias: 0, NNumeros: 0, '
                 'Numerica: false, Rotulo: ""}')


def linhas(t):
    """Texto colado -> tabela de linhas não vazias.
    Cada linha tem o n.º original (Linha) e a tabela das células (Celulas, campo Texto),
    obtidas com Split por mudança de linha (Char(10)) e por tabulação (Char(9))."""
    return f"""With(
    // Retira os retornos de carro (Char(13)) do Windows e parte o texto em linhas
    {{_linhas: Split(Substitute({t}, Char(13), ""), Char(10))}},
    Filter(
        ForAll(Sequence(CountRows(_linhas)) As _i,
            With(
                // Parte cada linha nas tabulações (colunas do Excel) e limpa os espaços
                {{_cel: ForAll(Split(Index(_linhas, _i.Value).Value, Char(9)) As _c,
                    {{Texto: Trim(Substitute(_c.Value, UniChar(160), " "))}})}},
                {{Linha: _i.Value, Celulas: _cel, NCel: CountRows(Filter(_cel, Texto <> ""))}}
            )
        ),
        // Ignora linhas vazias (ou só com tabulações/espaços)
        NCel > 0
    )
)"""


def colunas():
    """Caracterização das colunas coladas (usa colColagem).
    Uma coluna é numérica se pelo menos metade das células não vazias (excluindo a
    1.ª linha, que pode ser cabeçalho) forem números."""
    return f"""With(
    {{_m: CountRows(colColagem), _k: Coalesce(Max(colColagem, CountRows(Celulas)), 0)}},
    With(
        {{_corpo: If(_m >= 2, LastN(colColagem, _m - 1), colColagem), _topo: First(colColagem)}},
        ForAll(Sequence(_k) As _j,
            With(
                {{_txt: ForAll(_corpo As _r,
                    {{T: If(_j.Value <= CountRows(_r.Celulas), Index(_r.Celulas, _j.Value).Texto, "")}}),
                 _t1: If(_j.Value <= CountRows(_topo.Celulas), Index(_topo.Celulas, _j.Value).Texto, "")}},
                With(
                    {{_nv: CountRows(Filter(_txt, T <> "")),
                     _nn: CountRows(Filter(_txt, T <> "" && !IsBlank({num("T")})))}},
                    {{Col: _j.Value, Topo: _t1, TopoNumerico: !IsBlank({num("_t1")}),
                     NNaoVazias: _nv, NNumeros: _nn, Numerica: _nn > 0 && _nn * 2 >= _nv,
                     Rotulo: _j.Value & " · " & Left(_t1, 18)}}
                )
            )
        )
    )
)"""


def cabecalho():
    """A 1.ª linha é cabeçalho? Automático: sim se alguma coluna numérica tiver texto na 1.ª linha."""
    return ('Switch(drpCabecalho.Selected.Value, "Sim", true, "Não", false, '
            'CountRows(colColagem) >= 2 && '
            'CountRows(Filter(colColunas, Numerica && Topo <> "" && !TopoNumerico)) > 0)')


def itens_mapa():
    return 'Table({Value: "—"}, ForAll(colColunas, {Value: Rotulo}))'


def default_mapa(v):
    """Coluna sugerida para cada variável: N1-N3 = 1.ª a 3.ª colunas numéricas,
    C1-C2 = 1.ª e 2.ª colunas de texto."""
    if v in VARS_NUM:
        filtro, pos = "Numerica", VARS_NUM.index(v) + 1
    else:
        filtro, pos = "!Numerica && NNaoVazias > 0", VARS_CAT.index(v) + 1
    return (f'With({{_f: Filter(colColunas, {filtro})}}, '
            f'If(CountRows(_f) >= {pos}, Index(_f, {pos}).Rotulo, "—"))')


def coluna_escolhida(drp):
    """Texto da lista ('2 · Altura') -> n.º da coluna (0 = nenhuma)."""
    return f'IfError(Value(First(Split({drp}.Selected.Value, " ")).Value, "en-US"), 0)'


def _cel(r, j):
    return f'If({j} >= 1 && {j} <= CountRows({r}.Celulas), Index({r}.Celulas, {j}).Texto, "")'


def importar(base):
    """Constrói o registo de importação: linhas para colDados, valores inválidos e nomes."""
    js = ",\n      ".join(f"_j{v}: {coluna_escolhida('drpMap' + v)}" for v in VARS)
    celulas = ", ".join(f"_t{v}: {_cel('_r', '_j' + v)}" for v in VARS)
    campos_num = ", ".join(f"{v}: {num('_t' + v)}" for v in VARS_NUM)
    campos_cat = ", ".join(f"{v}: _t{v}" for v in VARS_CAT)
    invs = ", ".join(f"_I{v}: {invalido('_t' + v)}" for v in VARS_NUM)
    textos = ", ".join(f"_T{v}: _t{v}" for v in VARS_NUM)
    lista_inv = ",\n            ".join(
        f'ForAll(Filter(_reg, _I{v}) As _x, {{Linha: _x.Linha, Variavel: _nomes.{v}, Texto: _x._T{v}}})'
        for v in VARS_NUM)
    nomes = ", ".join(f"{v}: If(_cab && _j{v} > 0, {_cel('_c1', '_j' + v)}, varNomes.{v})" for v in VARS)
    return f"""With(
    // Opções escolhidas: cabeçalho e coluna de origem de cada variável
    {{_cab: {cabecalho()},
      {js}}},
    With(
        {{_corpo: If(_cab, LastN(colColagem, CountRows(colColagem) - 1), colColagem),
          // Se houver cabeçalho, os nomes das variáveis vêm da 1.ª linha
          _nomes: With({{_c1: First(colColagem)}}, {{{nomes}}})}},
        With(
            {{_reg: ForAll(Sequence(CountRows(_corpo)) As _i,
                With({{_r: Index(_corpo, _i.Value)}},
                    With({{{celulas}}},
                        {{Id: {base} + _i.Value, {campos_num}, {campos_cat},
                         Linha: _r.Linha, {invs}, {textos}}}
                    )
                )
            )}},
            {{
                // Registos prontos a juntar a colDados
                Linhas: ForAll(_reg, {{Id: Id, {", ".join(f"{v}: {v}" for v in VARS)}}}),
                // Valores não numéricos em colunas numéricas (ficam em branco)
                Invalidos: Sort(Table(
            {lista_inv}
                ), Linha),
                Cabecalho: _cab,
                Nomes: _nomes
            }}
        )
    )
)"""


def texto_diagnostico():
    return f"""If(CountRows(colColagem) = 0,
    "Cole os dados na caixa acima e carregue em «Analisar».",
    With({{_R: {importar("0").replace(chr(10), chr(10) + "    ")}}},
        "Linhas com dados: " & CountRows(_R.Linhas) & "  ·  Colunas: " & CountRows(colColunas) &
        With({{_vazias: Last(colColagem).Linha - First(colColagem).Linha + 1 - CountRows(colColagem)}},
            If(_vazias > 0, "  ·  Linhas vazias ignoradas: " & _vazias, "")) & Char(10) &
        "Primeira linha: " & If(_R.Cabecalho, "cabeçalho (nomes: " & Concat(colColunas, Topo, "; ") & ")", "dados") &
        Char(10) &
        If(CountRows(_R.Invalidos) = 0,
            "✔ Todos os valores das variáveis numéricas são válidos.",
            "⚠ " & CountRows(_R.Invalidos) & " valor(es) inválido(s) — ficarão em branco:" & Char(10) &
            Concat(FirstN(_R.Invalidos, 6), "   linha " & Linha & ", " & Variavel & ": «" & Texto & "»", Char(10)) &
            If(CountRows(_R.Invalidos) > 6, Char(10) & "   … e mais " & (CountRows(_R.Invalidos) - 6), "")
        )
    )
)"""


def importar_substituir():
    return f"""// Substitui todos os dados pelos dados colados
Set(varImportacao, {importar("0")});
ClearCollect(colDados, varImportacao.Linhas);
If(varImportacao.Cabecalho, Set(varNomes, varImportacao.Nomes));
Notify(
    "Importadas " & CountRows(varImportacao.Linhas) & " linhas." &
    If(CountRows(varImportacao.Invalidos) > 0,
        " Atenção: " & CountRows(varImportacao.Invalidos) & " valor(es) inválido(s) ficaram em branco.", ""),
    If(CountRows(varImportacao.Invalidos) > 0, NotificationType.Warning, NotificationType.Success)
)"""


def importar_acrescentar():
    return f"""// Acrescenta os dados colados no fim da tabela (os nomes das variáveis mantêm-se)
Set(varImportacao, {importar("Coalesce(Max(colDados, Id), 0)")});
Collect(colDados, varImportacao.Linhas);
Notify(
    "Acrescentadas " & CountRows(varImportacao.Linhas) & " linhas." &
    If(CountRows(varImportacao.Invalidos) > 0,
        " Atenção: " & CountRows(varImportacao.Invalidos) & " valor(es) inválido(s) ficaram em branco.", ""),
    If(CountRows(varImportacao.Invalidos) > 0, NotificationType.Warning, NotificationType.Success)
)"""


def onchange_numero(v):
    """OnChange de uma célula numérica da galeria."""
    return (f"// Converte o texto (vírgula ou ponto decimal) e grava na coleção\n"
            f"Patch(colDados, LookUp(colDados, Id = ThisItem.Id), {{{v}: {num('Self.Text')}}});\n"
            f"If({invalido('Self.Text')},\n"
            f'    Notify("«" & Self.Text & "» não é um número válido: a célula ficou vazia.", '
            f"NotificationType.Warning))")


ecra_dados_onchange = onchange_numero


def importar_substituir_resumo():
    """Versão abreviada (para a documentação) do botão Importar (substituir)."""
    return importar_substituir().replace(importar("0"), "/* registo de importação (ver acima) */")


def renumerar():
    """Volta a numerar as linhas 1..n (depois de apagar)."""
    return """ClearCollect(colTemp, ForAll(Sequence(CountRows(colDados)) As _i, Patch(Index(colDados, _i.Value), {Id: _i.Value})));
ClearCollect(colDados, colTemp);
Clear(colTemp)"""
