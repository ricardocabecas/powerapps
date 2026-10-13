"""Fórmulas do ecrã de entrada de dados (formato invariante)."""
from .f_comum import (num, invalido, tabela_dados, registo_nomes, atualizar_variaveis, e_numerica,
                      DADOS_EXEMPLO, NOMES_EXEMPLO, NOMES_PADRAO, VARS, NV)


def iniciar():
    return f"""// Inicialização: corre apenas na primeira vez que o ecrã é aberto
If(!varIniciado,
    Set(varIniciado, true);
    // Nomes das variáveis (podem ser alterados no cabeçalho da tabela)
    Set(varNomes, {registo_nomes(NOMES_EXEMPLO)});
    // Coleção com os dados: para cada variável k, Tk = texto escrito e Xk = número (ou vazio)
    ClearCollect(colDados, {tabela_dados(DADOS_EXEMPLO).replace(chr(10), chr(10) + "    ")});
    // Coleções auxiliares da colagem (ficam vazias até carregar em Analisar)
    ClearCollect(colColagem, {LINHAS_VAZIA});
    Clear(colColagem);
    ClearCollect(colColunas, {COLUNAS_VAZIA});
    Clear(colColunas);
    // Tipo de cada variável (numérica/categórica), detetado a partir dos dados
    {atualizar_variaveis().replace(chr(10), chr(10) + "    ")}
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


def _cel(r, j):
    return f'If({j} <= CountRows({r}.Celulas), Index({r}.Celulas, {j}).Texto, "")'


def importar(base, nomes_novos=True):
    """Registo de importação: a coluna j do texto colado vai para a variável Vj (j = 1 a NV).
    Linhas = registos prontos para colDados; Invalidos = textos não numéricos em colunas numéricas;
    Nomes = nomes das variáveis (da 1.ª linha, se for cabeçalho; senão «Variável j»)."""
    flags = ",\n          ".join(f"_num{j}: Coalesce(LookUp(colColunas, Col = {j}).Numerica, false)"
                                  for j in range(1, NV + 1))
    celulas = ", ".join(f"_t{j}: {_cel('_r', str(j))}" for j in range(1, NV + 1))
    campos = ", ".join(f"T{j}: _t{j}, X{j}: {num(f'_t{j}')}" for j in range(1, NV + 1))
    lista_inv = ",\n            ".join(
        f"ForAll(Filter(_corpo As _r, _num{j} && {invalido(_cel('_r', str(j)))}) As _x, "
        f"{{Linha: _x.Linha, Variavel: _nomes.V{j}, Texto: {_cel('_x', str(j))}}})"
        for j in range(1, NV + 1))
    if nomes_novos:
        nomes = ", ".join(
            f'V{j}: With({{_h: If(_cab, {_cel("_c1", str(j))}, "")}}, If(_h <> "", _h, "{NOMES_PADRAO[f"V{j}"]}"))'
            for j in range(1, NV + 1))
    else:
        nomes = ", ".join(f"V{j}: varNomes.V{j}" for j in range(1, NV + 1))
    return f"""With(
    // A 1.ª linha é cabeçalho? E que colunas são numéricas (pelo menos metade das células são números)?
    {{_cab: {cabecalho()},
      {flags}}},
    With(
        {{_corpo: If(_cab, LastN(colColagem, CountRows(colColagem) - 1), colColagem),
          _nomes: With({{_c1: First(colColagem)}}, {{{nomes}}})}},
        {{
            // Registos prontos a juntar a colDados: a coluna j vai para a variável Vj
            Linhas: ForAll(Sequence(CountRows(_corpo)) As _i,
                With({{_r: Index(_corpo, _i.Value)}},
                    With({{{celulas}}},
                        {{Id: {base} + _i.Value, {campos}}}))),
            // Textos não numéricos em colunas numéricas (ficam como valores em falta)
            Invalidos: Sort(Table(
            {lista_inv}
            ), Linha),
            Cabecalho: _cab,
            Nomes: _nomes
        }}
    )
)"""


def texto_diagnostico():
    tipo_col = ('Col & ". " & If(_R.Cabecalho && Topo <> "", Topo, "Variável " & Col) & '
                '" (" & If(Numerica, "numérica", "categórica") & ")"')
    return f"""If(CountRows(colColagem) = 0,
    "Cole os dados na caixa acima e carregue em «Analisar».",
    With({{_R: {importar("0").replace(chr(10), chr(10) + "    ")}}},
        "Linhas com dados: " & CountRows(_R.Linhas) & "  ·  Colunas: " & CountRows(colColunas) &
        With({{_vazias: Last(colColagem).Linha - First(colColagem).Linha + 1 - CountRows(colColagem)}},
            If(_vazias > 0, "  ·  Linhas vazias ignoradas: " & _vazias, "")) & Char(10) &
        "Primeira linha: " & If(_R.Cabecalho, "cabeçalho (nomes das variáveis)", "dados") & Char(10) &
        "Variáveis: " & Concat(FirstN(colColunas, {NV}), {tipo_col}, "  ·  ") & Char(10) &
        If(CountRows(colColunas) > {NV}, "⚠ Só as primeiras {NV} colunas são importadas." & Char(10), "") &
        If(CountRows(_R.Invalidos) = 0,
            "✔ Todos os valores das colunas numéricas são números válidos.",
            "⚠ " & CountRows(_R.Invalidos) & " valor(es) não numérico(s) em colunas numéricas — ficarão como valores em falta:" & Char(10) &
            Concat(FirstN(_R.Invalidos, 5), "   linha " & Linha & ", " & Variavel & ": «" & Texto & "»", Char(10)) &
            If(CountRows(_R.Invalidos) > 5, Char(10) & "   … e mais " & (CountRows(_R.Invalidos) - 5), "")
        )
    )
)"""


def _notificar(verbo):
    return f"""Notify(
    "{verbo} " & CountRows(varImportacao.Linhas) & " linhas." &
    If(CountRows(varImportacao.Invalidos) > 0,
        " Atenção: " & CountRows(varImportacao.Invalidos) & " valor(es) não numérico(s) ficaram como valores em falta.", ""),
    If(CountRows(varImportacao.Invalidos) > 0, NotificationType.Warning, NotificationType.Success)
)"""


def importar_substituir():
    return f"""// Substitui todos os dados (e os nomes das variáveis) pelos dados colados
Set(varImportacao, {importar("0")});
ClearCollect(colDados, varImportacao.Linhas);
Set(varNomes, varImportacao.Nomes);
{atualizar_variaveis()};
{_notificar("Importadas")}"""


def importar_acrescentar():
    return f"""// Acrescenta os dados colados no fim da tabela (os nomes das variáveis mantêm-se)
Set(varImportacao, {importar("Coalesce(Max(colDados, Id), 0)", nomes_novos=False)});
Collect(colDados, varImportacao.Linhas);
{atualizar_variaveis()};
{_notificar("Acrescentadas")}"""


def onchange_celula(j):
    """OnChange de uma célula da galeria: guarda o texto e o número e volta a detetar os tipos."""
    return (f"// Guarda o texto (T{j}) e o número (X{j}; vírgula ou ponto decimal) e atualiza os tipos\n"
            f"Patch(colDados, LookUp(colDados, Id = ThisItem.Id), {{T{j}: Trim(Self.Text), X{j}: {num('Self.Text')}}});\n"
            f"{atualizar_variaveis()};\n"
            f"If({e_numerica(str(j))} && {invalido('Self.Text')},\n"
            f'    Notify("«" & Self.Text & "» não é um número: nesta variável numérica conta como valor em falta.", '
            f"NotificationType.Warning))")


ecra_dados_onchange = onchange_celula
onchange_numero = onchange_celula


def importar_substituir_resumo():
    """Versão abreviada (para a documentação) do botão Importar (substituir)."""
    return (importar_substituir().replace(importar("0"), "/* registo de importação (ver acima) */")
            .replace(atualizar_variaveis(), "Set(varVariaveis, /* tabela das variáveis (ver 0.) */)"))


def renumerar():
    """Volta a numerar as linhas 1..n (depois de apagar)."""
    return """ClearCollect(colTemp, ForAll(Sequence(CountRows(colDados)) As _i, Patch(Index(colDados, _i.Value), {Id: _i.Value})));
ClearCollect(colDados, colTemp);
Clear(colTemp)"""
