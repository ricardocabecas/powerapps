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

# Regressão: nome -> (x, y, x0 como texto)
REGRESSAO = {
    "exemplo_altura_peso": ([r[1] for r in DADOS_EXEMPLO], [r[2] for r in DADOS_EXEMPLO], "172,5"),
    "exemplo_altura_nota": ([r[1] for r in DADOS_EXEMPLO], [r[3] for r in DADOS_EXEMPLO], "150"),
    "reta_perfeita_positiva": ([1, 2, 3, 4, 5], [3, 5, 7, 9, 11], "2.5"),
    "reta_perfeita_negativa": ([0, 1, 2, 3], [10, 7.5, 5, 2.5], "10"),
    "y_constante": ([1, 2, 3, 4], [5, 5, 5, 5], "2"),
    "x_constante": ([2, 2, 2], [1, 2, 3], "2"),
    "n1": ([1], [2], "1"),
    "n2": ([1, 3], [2, 1], "2"),
    "com_faltas": ([1, 2, None, 4, 5, 6], [2.1, None, 3.3, 3.9, 5.2, 6.1], ""),
    "sem_correlacao": ([1, 2, 3, 4, 5], [2, 4, 1, 4, 2], "3"),
    "decimais_negativos": ([-1.5, -0.25, 0.5, 2.75, 3.1], [0.2, -1.1, 0.4, -2.6, -2.95], "-1"),
}

# Testes t: (nome, tipo, formato, var1 (N1), var2 (N2), grupos (C1), grupoA, grupoB, d0, alternativa)
_PESO_F = [r[2] for r in DADOS_EXEMPLO]
TESTES_T = [
    ("1amostra_altura_170_bilateral", 1, 1, _ALT, None, None, "", "", "170", 1),
    ("1amostra_altura_165_direita", 1, 1, _ALT, None, None, "", "", "165", 3),
    ("1amostra_altura_172_esquerda", 1, 1, _ALT, None, None, "", "", "172,5", 2),
    ("1amostra_n2", 1, 1, [3.5, 4.0], None, None, "", "", "0", 1),
    ("1amostra_n1", 1, 1, [3.5], None, None, "", "", "0", 1),
    ("1amostra_variancia_nula", 1, 1, [5, 5, 5, 5], None, None, "", "", "4", 1),
    ("ind_altura_sexo_FM", 2, 1, _ALT, None, _SEXO, "F", "M", "0", 1),
    ("ind_altura_sexo_FM_esquerda", 2, 1, _ALT, None, _SEXO, "F", "M", "0", 2),
    ("welch_altura_sexo_FM", 3, 1, _ALT, None, _SEXO, "F", "M", "0", 1),
    ("welch_d0_menos10_direita", 3, 1, _ALT, None, _SEXO, "F", "M", "-10", 3),
    ("ind_duas_colunas", 2, 2, [12, 15, 11, 14, 13, None], [10, 9, 12, 8, 11, 10], None, "", "", "0", 1),
    ("welch_duas_colunas_desiguais", 3, 2, [10.1, 10.3, 9.9, 10.0], [8, 14, 6, 15, 12, 3, 9], None, "", "", "0", 1),
    ("welch_gl_fracionarios_n2", 3, 2, [1, 2], [10, 30, 25], None, "", "", "0", 1),
    ("ind_um_grupo_vazio", 2, 1, [1, 2, 3, 4], None, ["A", "A", "A", "A"], "A", "B", "0", 1),
    ("emparelhado_peso_altura", 4, 1, _ALT, _PESO_F, None, "", "", "100", 1),
    ("emparelhado_antes_depois", 4, 1, [80, 75, 90, 68, 72, 85], [78, 74, 85, 69, 70, 80], None, "", "", "0", 3),
    ("emparelhado_com_faltas", 4, 1, [5, 6, None, 8, 7], [4, 6.5, 3, None, 5], None, "", "", "0", 1),
]
