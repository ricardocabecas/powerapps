"""Conjuntos de dados pequenos para os testes (incluem casos limite)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ferramentas"))
from gerador.f_comum import DADOS_EXEMPLO, NOMES_EXEMPLO  # noqa: E402

TAB = "\t"
NL = "\r\n"   # o Excel no Windows copia com CR LF

# Textos colados (simulam cópias do Excel) -> nome do caso
COLAGENS = {
    "virgula_com_cabecalho": NL.join(["Altura\tPeso\tSexo", "165,5\t58,2\tF", "178\t72,0\tM", "160,25\t52\tF"]) + NL,
    "ponto_sem_cabecalho": "\n".join(["1.5\t2", "2.25\t3", "-3.5\t4"]),
    "uma_coluna": NL.join(["Notas", "12", "14,5", "9", ""]) + NL,
    "linhas_vazias_e_espacos": NL.join(["Valor\tGrupo", "  10 \t A ", "", "\t", "20\tB", "   ", "30\t  C  "]) + NL,
    "invalidos": NL.join(["X\tY", "1\t2", "abc\t3", "4\t1,2,3", "5\t", "6\t7"]) + NL,
    "milhares_espaco": NL.join(["Rendimento", "1 234,5", "2 000", "999,99"]) + NL,
    "grupo_primeiro": NL.join(["Turma\tNota", "A\t12", "B\t15", "A\t9,5"]) + NL,
    "so_categorica": NL.join(["Cor", "azul", "verde", "azul"]) + NL,
    "linha_unica": "3,5\t4,5",
    "cinco_colunas": NL.join(["a\tb\tc\tg1\tg2", "1\t2\t3\tx\ty", "4\t5\t6\tx\tz"]) + NL,
    "cientifica_e_percentagem": NL.join(["v", "1e3", "2,5E-2", "50%", "+7"]) + NL,
}

# Textos isolados para a conversão texto -> número
NUMEROS = ["1,5", "1.5", " 2 ", "-3,25", "1 234,5", "1 000", "abc", "", "  ", "1.2.3", "1,2,3", "5%",
           "1e3", "+4", "0,0001", "-0", "12,", ",5"]

# Valores para a formatação pt-PT (4 casas)
FORMATOS = [0, 1, -1, 3.14159265, 1234.5, -0.00004, 0.00005, 1234567.891, 1e-10, -2.5, 100]

# Estatística descritiva: (valores de N1, grupos C1 ou None)
DESCRITIVA = {
    "exemplo_altura": ([r[1] for r in DADOS_EXEMPLO], [r[4] for r in DADOS_EXEMPLO]),
    "exemplo_nota": ([r[3] for r in DADOS_EXEMPLO], [r[5] for r in DADOS_EXEMPLO]),
    "n1": ([7.5], None),
    "n2": ([3, 8], None),
    "n3": ([5, 1, 3], None),
    "repetidos": ([2, 2, 2, 3, 3, 4, 4, 4, 5], None),
    "todos_iguais_freq": ([1, 1, 2, 2, 3, 3], None),
    "variancia_nula": ([4, 4, 4, 4], None),
    "media_zero": ([-2, -1, 0, 1, 2], None),
    "com_faltas": ([1.5, None, 3, 5.25, None, 8, 2], ["A", "A", None, "B", "B", "B", None]),
    "negativos_decimais": ([-1.5, 2.25, 0, -3.75, 10.125, 0.001], None),
    "grandes": ([1000000.5, 2000000.25, 1500000, 1250000.75], None),
    "vazio": ([None, None], None),
    "grupos_desiguais": ([10, 12, 11, 20, 22, 5], ["x", "x", "x", "y", "y", "z"]),
}

# Frequências: (nome, índice da variável 1..5, coluna de valores, tipo, k, início, amplitude)
_ALT = [r[1] for r in DADOS_EXEMPLO]
_PESO = [r[2] for r in DADOS_EXEMPLO]
_NOTA = [r[3] for r in DADOS_EXEMPLO]
_SEXO = [r[4] for r in DADOS_EXEMPLO]
_TURMA = [r[5] for r in DADOS_EXEMPLO]
FREQUENCIAS = [
    ("nota_discreta", 3, _NOTA, 1, None, None, None),
    ("sexo_categorica", 4, _SEXO, 1, None, None, None),
    ("turma_categorica", 5, _TURMA, 1, None, None, None),
    ("altura_sturges", 1, _ALT, 2, None, None, None),
    ("altura_k4_inicio150_h10", 1, _ALT, 2, 4, 150, 10),
    ("altura_k3_inicio160_h10_fora", 1, _ALT, 2, 3, 160, 10),
    ("peso_sturges", 2, _PESO, 2, None, None, None),
    ("peso_k5_h8", 2, _PESO, 2, 5, 45, 8),
    ("fronteiras_exatas", 1, [0.1, 0.3, 0.5, 0.7, 0.9, 0.3], 2, 4, 0.1, 0.2),
    ("todos_iguais_classes", 1, [5, 5, 5], 2, None, None, None),
    ("um_valor", 1, [2.5], 2, None, None, None),
    ("discreta_decimais", 1, [1.5, 2.25, 1.5, None, 3], 1, None, None, None),
]
