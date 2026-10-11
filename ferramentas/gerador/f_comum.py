"""Fórmulas Power Fx partilhadas (formato invariante).

Cada função devolve o texto de uma (sub)fórmula. As fórmulas usadas nos ecrãs e nos
testes automáticos são exatamente as mesmas cadeias de texto.
"""

# Variáveis do modelo de dados: campo da coleção colDados -> descrição
VARS_NUM = ["N1", "N2", "N3"]
VARS_CAT = ["C1", "C2"]
VARS = VARS_NUM + VARS_CAT

NOMES_EXEMPLO = {"N1": "Altura (cm)", "N2": "Peso (kg)", "N3": "Nota (0-20)", "C1": "Sexo", "C2": "Turma"}

# (Id, N1, N2, N3, C1, C2) — dados fictícios de 20 estudantes
DADOS_EXEMPLO = [
    (1, 165, 58.5, 14, "F", "A"), (2, 178, 72.0, 12, "M", "A"), (3, 160, 52.3, 16, "F", "B"),
    (4, 182, 80.1, 11, "M", "B"), (5, 170, 65.4, 13, "M", "C"), (6, 158, 49.8, 17, "F", "A"),
    (7, 175, 70.2, 10, "M", "C"), (8, 168, 61.0, 15, "F", "B"), (9, 185, 85.6, 9, "M", "A"),
    (10, 162, 55.1, 18, "F", "C"), (11, 172, 68.3, 12, "M", "B"), (12, 166, 60.2, 14, "F", "A"),
    (13, 180, 77.5, 11, "M", "C"), (14, 155, 48.0, 16, "F", "B"), (15, 174, 69.9, 13, "M", "A"),
    (16, 163, 57.4, 15, "F", "C"), (17, 177, 74.8, 10, "M", "B"), (18, 169, 63.1, 14, "F", "C"),
    (19, 171, 66.7, 12, "M", "A"), (20, 159, 51.6, 17, "F", "B"),
]


def num_pfx(v):
    """Número Python -> literal Power Fx invariante."""
    if isinstance(v, int) or float(v).is_integer():
        return str(int(v))
    return repr(float(v))


def texto_pfx(s):
    return '"' + s.replace('"', '""') + '"'


def tabela_dados(linhas):
    """Literal Table(...) para a coleção colDados."""
    regs = []
    for (i, a, b, c, d, e) in linhas:
        def n(v):
            return "Blank()" if v is None else num_pfx(v)

        def t(v):
            return "Blank()" if v is None else texto_pfx(v)
        regs.append(f"{{Id: {i}, N1: {n(a)}, N2: {n(b)}, N3: {n(c)}, C1: {t(d)}, C2: {t(e)}}}")
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


def itens_numericas():
    """Itens das listas pendentes de variáveis numéricas (nomes dados pelo utilizador)."""
    return "[varNomes.N1, varNomes.N2, varNomes.N3]"


def itens_categoricas():
    return "[varNomes.C1, varNomes.C2]"


def itens_todas():
    return "[varNomes.N1, varNomes.N2, varNomes.N3, varNomes.C1, varNomes.C2]"


def indice_num(drp):
    """Nome escolhido numa lista pendente -> índice da variável numérica (1, 2 ou 3)."""
    return f'Switch({drp}.Selected.Value, varNomes.N1, 1, varNomes.N2, 2, varNomes.N3, 3, 1)'


def indice_todas(drp):
    """Índice 1-3 = numéricas, 4-5 = categóricas."""
    return (f'Switch({drp}.Selected.Value, varNomes.N1, 1, varNomes.N2, 2, varNomes.N3, 3, '
            f'varNomes.C1, 4, varNomes.C2, 5, 1)')


def vetor_num(k):
    """Tabela {x} com os valores não vazios da variável numérica de índice k (expressão)."""
    return (f'Filter(ForAll(colDados As _d, {{x: Switch({k}, 1, _d.N1, 2, _d.N2, _d.N3)}}), !IsBlank(x))')
