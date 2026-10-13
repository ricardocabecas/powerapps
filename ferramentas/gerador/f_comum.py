"""Fórmulas Power Fx partilhadas (formato invariante).

Cada função devolve o texto de uma (sub)fórmula. As fórmulas usadas nos ecrãs e nos
testes automáticos são exatamente as mesmas cadeias de texto.
"""

# Modelo de dados: NV variáveis genéricas V1..VNV. Na coleção colDados cada variável k tem dois campos:
#   Tk  texto tal como foi escrito ou colado (já limpo de espaços nas pontas)
#   Xk  o número correspondente (vírgula ou ponto decimal), ou vazio se o texto não for um número
# O tipo de cada variável (numérica ou categórica) é detetado a partir dos dados (ver variaveis()).
NV = 6
VARS = [f"V{k}" for k in range(1, NV + 1)]

NOMES_EXEMPLO = {"V1": "Altura (cm)", "V2": "Peso (kg)", "V3": "Nota (0-20)", "V4": "Sexo", "V5": "Turma",
                 "V6": "Variável 6"}
NOMES_PADRAO = {v: f"Variável {i + 1}" for i, v in enumerate(VARS)}

# (Id, V1, V2, V3, V4, V5) — dados fictícios de 20 estudantes (V6 fica vazia)
DADOS_EXEMPLO = [
    (1, 165, 58.5, 14, "F", "A"), (2, 178, 72.0, 12, "M", "A"), (3, 160, 52.3, 16, "F", "B"),
    (4, 182, 80.1, 11, "M", "B"), (5, 170, 65.4, 13, "M", "C"), (6, 158, 49.8, 17, "F", "A"),
    (7, 175, 70.2, 10, "M", "C"), (8, 168, 61.0, 15, "F", "B"), (9, 185, 85.6, 9, "M", "A"),
    (10, 162, 55.1, 18, "F", "C"), (11, 172, 68.3, 12, "M", "B"), (12, 166, 60.2, 14, "F", "A"),
    (13, 180, 77.5, 11, "M", "C"), (14, 155, 48.0, 16, "F", "B"), (15, 174, 69.9, 13, "M", "A"),
    (16, 163, 57.4, 15, "F", "C"), (17, 177, 74.8, 10, "M", "B"), (18, 169, 63.1, 14, "F", "C"),
    (19, 171, 66.7, 12, "M", "A"), (20, 159, 51.6, 17, "F", "B"),
]


def texto_pt(v):
    """Valor Python -> texto como apareceria escrito em pt-PT (1.5 -> '1,5')."""
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if float(v).is_integer():
        return str(int(v))
    return repr(float(v)).replace(".", ",")


def num_pfx(v):
    """Número Python -> literal Power Fx invariante."""
    if isinstance(v, int) or float(v).is_integer():
        return str(int(v))
    return repr(float(v))


def texto_pfx(s):
    return '"' + s.replace('"', '""') + '"'


def tabela_dados(linhas):
    """Literal Table(...) para a coleção colDados (cada linha: Id seguido dos valores de V1, V2, ...)."""
    regs = []
    for linha in linhas:
        i, vals = linha[0], list(linha[1:]) + [None] * (NV - len(linha) + 1)
        campos = [f"Id: {i}"]
        for k, v in enumerate(vals[:NV], start=1):
            t = texto_pt(v)
            x = num_pfx(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else "Blank()"
            campos.append(f"T{k}: {texto_pfx(t)}, X{k}: {x}")
        regs.append("{" + ", ".join(campos) + "}")
    return "Table(\n    " + ",\n    ".join(regs) + "\n)"


def registo_nomes(nomes):
    return "{" + ", ".join(f"{k}: {texto_pfx(nomes[k])}" for k in VARS) + "}"


def normalizar(t):
    """Texto -> texto pronto para Value(..., "en-US"):
    retira espaços (incluindo os espaços inseparáveis que o Excel usa como separador de
    milhares) e troca a vírgula decimal por ponto."""
    return (f'Substitute(Substitute(Substitute(Substitute(Trim({t}), " ", ""), UniChar(160), ""), '
            f'UniChar(8239), ""), ",", ".")')


def num(t):
    """Texto -> número, aceitando vírgula ou ponto decimal; Blank() se vazio ou inválido."""
    return f'IfError(Value({normalizar(t)}, "en-US"), Blank())'


def invalido(t):
    """true se o texto não está vazio e não representa um número."""
    return f'(Len(Trim({t})) > 0 && IsError(Value({normalizar(t)}, "en-US")))'


def fmt(expr, casas=4, nd='"n.d."'):
    """Número -> texto com vírgula decimal (pt-PT) e espaço como separador de milhares.
    O marcador [$-en-US] indica que o formato está escrito com ponto decimal; o terceiro
    argumento ("pt-PT") define o idioma do resultado. Valores em branco mostram 'n.d.'
    (não definido) e o -0 é evitado."""
    formato = "#,##0" + ("." + "0" * casas if casas > 0 else "")
    lim = 0.5 * 10 ** (-casas)
    return (f'With({{_v: {expr}}}, If(IsBlank(_v), {nd}, '
            f'Text(If(Abs(_v) < {num_pfx(lim) if casas else "0.5"}, 0, _v), "[$-en-US]{formato}", "pt-PT")))')


def fmt_livre(expr):
    """Número -> texto pt-PT com as casas decimais necessárias (até 10), sem zeros à direita."""
    return (f'With({{_v: {expr}}}, If(IsBlank(_v), "", If(_v = Int(_v), Text(_v, "[$-en-US]0", "pt-PT"), '
            f'Text(_v, "[$-en-US]0.##########", "pt-PT"))))')


def col_num(k, d="_d"):
    """Valor numérico (Xk) da variável de índice k (expressão) no registo d."""
    return "Switch(" + k + ", " + ", ".join(f"{i}, {d}.X{i}" for i in range(1, NV + 1)) + ", Blank())"


def col_txt(k, d="_d"):
    """Texto (Tk) da variável de índice k no registo d."""
    return "Switch(" + k + ", " + ", ".join(f"{i}, {d}.T{i}" for i in range(1, NV + 1)) + ', "")'


def col_cat(k, isnum, d="_d"):
    """Categoria da variável k no registo d: o número formatado (variável numérica) ou o texto."""
    return f"If({isnum}, {fmt_livre(col_num(k, d))}, {col_txt(k, d)})"


def variaveis():
    """Tabela com uma linha por variável: k, nome, n (células preenchidas), nNum (números),
    numerica (pelo menos metade das células preenchidas são números) e nInv (inválidos).
    É guardada em varVariaveis sempre que os dados ou os nomes mudam."""
    nomes = ", ".join(f"{i}, varNomes.V{i}" for i in range(1, NV + 1))
    return f"""ForAll(Sequence({NV}) As _k,
    With({{_nv: CountRows(Filter(colDados, !IsBlank({col_txt("_k.Value", "ThisRecord")}))),
          _nn: CountRows(Filter(colDados, !IsBlank({col_num("_k.Value", "ThisRecord")})))}},
        {{k: _k.Value, nome: Switch(_k.Value, {nomes}, ""), n: _nv, nNum: _nn,
         numerica: _nn > 0 && _nn * 2 >= _nv, nInv: If(_nn > 0 && _nn * 2 >= _nv, _nv - _nn, 0)}}))"""


def atualizar_variaveis():
    return f"Set(varVariaveis, {variaveis()})"


def itens_numericas():
    """Itens das listas de variáveis numéricas: só as variáveis detetadas como numéricas."""
    return "ForAll(Filter(varVariaveis, numerica) As _v, {Value: _v.nome})"


def itens_todas():
    """Todas as variáveis com dados (numéricas e categóricas)."""
    return "ForAll(Filter(varVariaveis, n > 0) As _v, {Value: _v.nome})"


itens_categoricas = itens_todas


def default_numerica(i):
    """Nome da i-ésima variável numérica (para o valor inicial de uma lista)."""
    return (f'With({{_f: Filter(varVariaveis, numerica)}}, '
            f'If(CountRows(_f) >= {i}, Index(_f, {i}).nome, Coalesce(First(_f).nome, "")))')


def default_categorica(i=1):
    """Nome da i-ésima variável categórica (ou, se não houver, da 1.ª variável com dados)."""
    return (f'With({{_f: Filter(varVariaveis, !numerica && n > 0)}}, '
            f'If(CountRows(_f) >= {i}, Index(_f, {i}).nome, CountRows(_f) >= 1, First(_f).nome, '
            f'Coalesce(First(Filter(varVariaveis, n > 0)).nome, "")))')


def indice(drp):
    """Nome escolhido numa lista -> índice k da variável (0 se nenhuma)."""
    return f"Coalesce(LookUp(varVariaveis, nome = {drp}.Selected.Value).k, 0)"


indice_num = indice
indice_todas = indice


def e_numerica(k):
    """true se a variável de índice k (expressão) é numérica."""
    return f"Coalesce(LookUp(varVariaveis, k = {k}).numerica, false)"


def vetor_num(k):
    """Tabela {x} com os valores numéricos não vazios da variável de índice k (expressão)."""
    return f"Filter(ForAll(colDados As _d, {{x: {col_num(k)}}}), !IsBlank(x))"


def categorias(k, isnum):
    """Categorias distintas (texto) da variável k, por ordem numérica (variável numérica) ou alfabética."""
    return f"""With({{_c: Filter(ForAll(colDados As _d, {{g: {col_cat(k, isnum)}, o: If({isnum}, {col_num(k)}, 0)}}), !IsBlank(g))}},
        ForAll(If({isnum}, Sort(ForAll(Distinct(_c, g) As _u, {{g: _u.Value, o: LookUp(_c, g = _u.Value).o}}), o),
                  Sort(ForAll(Distinct(_c, g) As _u, {{g: _u.Value, o: 0}}), g)) As _z, {{Value: _z.g}}))"""


def niveis_ordenados(tab, isnum):
    """Valores distintos (não vazios) do campo g de uma tabela {g, o}, como tabela {Value},
    por ordem numérica de o (grupo numérico) ou alfabética."""
    return (f"ForAll(If({isnum}, Sort(ForAll(Filter(Distinct({tab}, g), !IsBlank(Value)) As _u, "
            f"{{g: _u.Value, o: LookUp({tab}, g = _u.Value).o}}), o), "
            f"Sort(ForAll(Filter(Distinct({tab}, g), !IsBlank(Value)) As _u, {{g: _u.Value, o: 0}}), g)) As _z, "
            f"{{Value: _z.g}})")
