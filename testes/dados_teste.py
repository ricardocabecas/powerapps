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
