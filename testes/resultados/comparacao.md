# Resultados da comparação Power Fx × referência Python/scipy

Gerado em 11/10/2026 por `testes/executar_testes.py`. As fórmulas foram executadas com o interpretador open source **Microsoft.PowerFx.Interpreter 1.8.1** (.NET 8), com números em vírgula flutuante (como nas canvas apps).

**Total: 1347/1347 verificações sem diferenças.**

## Sintaxe de todas as fórmulas dos ecrãs

646 fórmulas analisadas em formato invariante (ficheiros .pa.yaml) e convertidas para pt-PT (barra de fórmulas): **1292/1292 sem erros de sintaxe**.


## Fase 1 — Entrada de dados

**55/55 casos de acordo com a referência.**

| Caso | Resultado | Detalhe |
|---|---|---|
| colagem «virgula_com_cabecalho» (Automático) | ✅ | 3 linhas, cabeçalho=True, 0 inválidos, mapa={'N1': 1, 'N2': 2, 'N3': 0, 'C1': 3, 'C2': 0} |
| diagnóstico «virgula_com_cabecalho» (Automático) | ✅ | Linhas com dados: 3  ·  Colunas: 3 ⏎ Primeira linha: cabeçalho (nomes: Altura; Peso; Sexo) ⏎ ✔ Todos os valores das variáveis numéricas são válidos. |
| colagem «virgula_com_cabecalho» (Sim) | ✅ | 3 linhas, cabeçalho=True, 0 inválidos, mapa={'N1': 1, 'N2': 2, 'N3': 0, 'C1': 3, 'C2': 0} |
| diagnóstico «virgula_com_cabecalho» (Sim) | ✅ | Linhas com dados: 3  ·  Colunas: 3 ⏎ Primeira linha: cabeçalho (nomes: Altura; Peso; Sexo) ⏎ ✔ Todos os valores das variáveis numéricas são válidos. |
| colagem «virgula_com_cabecalho» (Não) | ✅ | 4 linhas, cabeçalho=False, 2 inválidos, mapa={'N1': 1, 'N2': 2, 'N3': 0, 'C1': 3, 'C2': 0} |
| diagnóstico «virgula_com_cabecalho» (Não) | ✅ | Linhas com dados: 4  ·  Colunas: 3 ⏎ Primeira linha: dados ⏎ ⚠ 2 valor(es) inválido(s) — ficarão em branco: ⏎    linha 1, Altura (cm): «Altura» ⏎    linha 1, Peso (kg): «Peso» |
| colagem «ponto_sem_cabecalho» (Automático) | ✅ | 3 linhas, cabeçalho=False, 0 inválidos, mapa={'N1': 1, 'N2': 2, 'N3': 0, 'C1': 0, 'C2': 0} |
| diagnóstico «ponto_sem_cabecalho» (Automático) | ✅ | Linhas com dados: 3  ·  Colunas: 2 ⏎ Primeira linha: dados ⏎ ✔ Todos os valores das variáveis numéricas são válidos. |
| colagem «uma_coluna» (Automático) | ✅ | 3 linhas, cabeçalho=True, 0 inválidos, mapa={'N1': 1, 'N2': 0, 'N3': 0, 'C1': 0, 'C2': 0} |
| diagnóstico «uma_coluna» (Automático) | ✅ | Linhas com dados: 3  ·  Colunas: 1 ⏎ Primeira linha: cabeçalho (nomes: Notas) ⏎ ✔ Todos os valores das variáveis numéricas são válidos. |
| colagem «linhas_vazias_e_espacos» (Automático) | ✅ | 3 linhas, cabeçalho=True, 0 inválidos, mapa={'N1': 1, 'N2': 0, 'N3': 0, 'C1': 2, 'C2': 0} |
| diagnóstico «linhas_vazias_e_espacos» (Automático) | ✅ | Linhas com dados: 3  ·  Colunas: 2  ·  Linhas vazias ignoradas: 3 ⏎ Primeira linha: cabeçalho (nomes: Valor; Grupo) ⏎ ✔ Todos os valores das variáveis numéricas são válidos. |
| colagem «invalidos» (Automático) | ✅ | 5 linhas, cabeçalho=True, 2 inválidos, mapa={'N1': 1, 'N2': 2, 'N3': 0, 'C1': 0, 'C2': 0} |
| diagnóstico «invalidos» (Automático) | ✅ | Linhas com dados: 5  ·  Colunas: 2 ⏎ Primeira linha: cabeçalho (nomes: X; Y) ⏎ ⚠ 2 valor(es) inválido(s) — ficarão em branco: ⏎    linha 3, X: «abc» ⏎    linha 4, Y: «1,2,3» |
| colagem «milhares_espaco» (Automático) | ✅ | 3 linhas, cabeçalho=True, 0 inválidos, mapa={'N1': 1, 'N2': 0, 'N3': 0, 'C1': 0, 'C2': 0} |
| diagnóstico «milhares_espaco» (Automático) | ✅ | Linhas com dados: 3  ·  Colunas: 1 ⏎ Primeira linha: cabeçalho (nomes: Rendimento) ⏎ ✔ Todos os valores das variáveis numéricas são válidos. |
| colagem «grupo_primeiro» (Automático) | ✅ | 3 linhas, cabeçalho=True, 0 inválidos, mapa={'N1': 2, 'N2': 0, 'N3': 0, 'C1': 1, 'C2': 0} |
| diagnóstico «grupo_primeiro» (Automático) | ✅ | Linhas com dados: 3  ·  Colunas: 2 ⏎ Primeira linha: cabeçalho (nomes: Turma; Nota) ⏎ ✔ Todos os valores das variáveis numéricas são válidos. |
| colagem «so_categorica» (Automático) | ✅ | 4 linhas, cabeçalho=False, 0 inválidos, mapa={'N1': 0, 'N2': 0, 'N3': 0, 'C1': 1, 'C2': 0} |
| diagnóstico «so_categorica» (Automático) | ✅ | Linhas com dados: 4  ·  Colunas: 1 ⏎ Primeira linha: dados ⏎ ✔ Todos os valores das variáveis numéricas são válidos. |
| colagem «linha_unica» (Automático) | ✅ | 1 linhas, cabeçalho=False, 0 inválidos, mapa={'N1': 1, 'N2': 2, 'N3': 0, 'C1': 0, 'C2': 0} |
| diagnóstico «linha_unica» (Automático) | ✅ | Linhas com dados: 1  ·  Colunas: 2 ⏎ Primeira linha: dados ⏎ ✔ Todos os valores das variáveis numéricas são válidos. |
| colagem «cinco_colunas» (Automático) | ✅ | 2 linhas, cabeçalho=True, 0 inválidos, mapa={'N1': 1, 'N2': 2, 'N3': 3, 'C1': 4, 'C2': 5} |
| diagnóstico «cinco_colunas» (Automático) | ✅ | Linhas com dados: 2  ·  Colunas: 5 ⏎ Primeira linha: cabeçalho (nomes: a; b; c; g1; g2) ⏎ ✔ Todos os valores das variáveis numéricas são válidos. |
| colagem «cientifica_e_percentagem» (Automático) | ✅ | 4 linhas, cabeçalho=True, 0 inválidos, mapa={'N1': 1, 'N2': 0, 'N3': 0, 'C1': 0, 'C2': 0} |
| diagnóstico «cientifica_e_percentagem» (Automático) | ✅ | Linhas com dados: 4  ·  Colunas: 1 ⏎ Primeira linha: cabeçalho (nomes: v) ⏎ ✔ Todos os valores das variáveis numéricas são válidos. |
| número «1,5» | ✅ | Power Fx=1.5 inválido=False \| referência=1.5 inválido=False |
| número «1.5» | ✅ | Power Fx=1.5 inválido=False \| referência=1.5 inválido=False |
| número « 2 » | ✅ | Power Fx=2 inválido=False \| referência=2.0 inválido=False |
| número «-3,25» | ✅ | Power Fx=-3.25 inválido=False \| referência=-3.25 inválido=False |
| número «1 234,5» | ✅ | Power Fx=1234.5 inválido=False \| referência=1234.5 inválido=False |
| número «1 000» | ✅ | Power Fx=1000 inválido=False \| referência=1000.0 inválido=False |
| número «abc» | ✅ | Power Fx=None inválido=True \| referência=None inválido=True |
| número «» | ✅ | Power Fx=None inválido=False \| referência=None inválido=False |
| número «  » | ✅ | Power Fx=None inválido=False \| referência=None inválido=False |
| número «1.2.3» | ✅ | Power Fx=None inválido=True \| referência=None inválido=True |
| número «1,2,3» | ✅ | Power Fx=None inválido=True \| referência=None inválido=True |
| número «5%» | ✅ | Power Fx=0.05 inválido=False \| referência=0.05 inválido=False |
| número «1e3» | ✅ | Power Fx=1000 inválido=False \| referência=1000.0 inválido=False |
| número «+4» | ✅ | Power Fx=4 inválido=False \| referência=4.0 inválido=False |
| número «0,0001» | ✅ | Power Fx=0.0001 inválido=False \| referência=0.0001 inválido=False |
| número «-0» | ✅ | Power Fx=0 inválido=False \| referência=-0.0 inválido=False |
| número «12,» | ✅ | Power Fx=12 inválido=False \| referência=12.0 inválido=False |
| número «,5» | ✅ | Power Fx=0.5 inválido=False \| referência=0.5 inválido=False |
| formatação 0 | ✅ | Power Fx=«0,0000» esperado=«0,0000» |
| formatação 1 | ✅ | Power Fx=«1,0000» esperado=«1,0000» |
| formatação -1 | ✅ | Power Fx=«-1,0000» esperado=«-1,0000» |
| formatação 3.14159265 | ✅ | Power Fx=«3,1416» esperado=«3,1416» |
| formatação 1234.5 | ✅ | Power Fx=«1 234,5000» esperado=«1 234,5000» |
| formatação -4e-05 | ✅ | Power Fx=«0,0000» esperado=«0,0000» |
| formatação 5e-05 | ✅ | Power Fx=«0,0001» esperado=«0,0001» |
| formatação 1234567.891 | ✅ | Power Fx=«1 234 567,8910» esperado=«1 234 567,8910» |
| formatação 1e-10 | ✅ | Power Fx=«0,0000» esperado=«0,0000» |
| formatação -2.5 | ✅ | Power Fx=«-2,5000» esperado=«-2,5000» |
| formatação 100 | ✅ | Power Fx=«100,0000» esperado=«100,0000» |

