# Resultados da comparação Power Fx × referência Python/scipy

Gerado em 11/10/2026 por `testes/executar_testes.py`. As fórmulas foram executadas com o interpretador open source **Microsoft.PowerFx.Interpreter 1.8.1** (.NET 8), com números em vírgula flutuante (como nas canvas apps).

**Total: 1843/1843 verificações sem diferenças.**

## Sintaxe de todas as fórmulas dos ecrãs

866 fórmulas analisadas em formato invariante (ficheiros .pa.yaml) e convertidas para pt-PT (barra de fórmulas): **1732/1732 sem erros de sintaxe**.


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

## Fase 2 — Estatística descritiva

**56/56 casos de acordo com a referência.**

| Caso | Resultado | Detalhe |
|---|---|---|
| exemplo_altura (quartis 1) por grupo | ✅ | n=20, média=169.45, Q1=162.75, Q3=175.5, s²=72.15526315789472, moda=não existe (amodal) |
| exemplo_altura (quartis 2) por grupo | ✅ | n=20, média=169.45, Q1=162.25, Q3=176.5, s²=72.15526315789472, moda=não existe (amodal) |
| exemplo_altura (quartis 3) por grupo | ✅ | n=20, média=169.45, Q1=162.5, Q3=176, s²=72.15526315789472, moda=não existe (amodal) |
| exemplo_altura: tabela HTML | ✅ | 6149 caracteres |
| exemplo_nota (quartis 1) por grupo | ✅ | n=20, média=13.45, Q1=11.75, Q3=15.25, s²=6.681578947368422, moda=12; 14 (bimodal) — freq. 3 |
| exemplo_nota (quartis 2) por grupo | ✅ | n=20, média=13.45, Q1=11.25, Q3=15.75, s²=6.681578947368422, moda=12; 14 (bimodal) — freq. 3 |
| exemplo_nota (quartis 3) por grupo | ✅ | n=20, média=13.45, Q1=11.5, Q3=15.5, s²=6.681578947368422, moda=12; 14 (bimodal) — freq. 3 |
| exemplo_nota: tabela HTML | ✅ | 7082 caracteres |
| n1 (quartis 1) | ✅ | n=1, média=7.5, Q1=7.5, Q3=7.5, s²=None, moda=7,5 — freq. 1 |
| n1 (quartis 2) | ✅ | n=1, média=7.5, Q1=7.5, Q3=7.5, s²=None, moda=7,5 — freq. 1 |
| n1 (quartis 3) | ✅ | n=1, média=7.5, Q1=7.5, Q3=7.5, s²=None, moda=7,5 — freq. 1 |
| n1: tabela HTML | ✅ | 4166 caracteres |
| n2 (quartis 1) | ✅ | n=2, média=5.5, Q1=4.25, Q3=6.75, s²=12.5, moda=não existe (amodal) |
| n2 (quartis 2) | ✅ | n=2, média=5.5, Q1=3, Q3=8, s²=12.5, moda=não existe (amodal) |
| n2 (quartis 3) | ✅ | n=2, média=5.5, Q1=3, Q3=8, s²=12.5, moda=não existe (amodal) |
| n2: tabela HTML | ✅ | 4181 caracteres |
| n3 (quartis 1) | ✅ | n=3, média=3, Q1=2, Q3=4, s²=4, moda=não existe (amodal) |
| n3 (quartis 2) | ✅ | n=3, média=3, Q1=1, Q3=5, s²=4, moda=não existe (amodal) |
| n3 (quartis 3) | ✅ | n=3, média=3, Q1=1, Q3=5, s²=4, moda=não existe (amodal) |
| n3: tabela HTML | ✅ | 4179 caracteres |
| repetidos (quartis 1) | ✅ | n=9, média=3.2222222222222223, Q1=2, Q3=4, s²=1.1944444444444446, moda=2; 4 (bimodal) — freq. 3 |
| repetidos (quartis 2) | ✅ | n=9, média=3.2222222222222223, Q1=2, Q3=4, s²=1.1944444444444446, moda=2; 4 (bimodal) — freq. 3 |
| repetidos (quartis 3) | ✅ | n=9, média=3.2222222222222223, Q1=2, Q3=4, s²=1.1944444444444446, moda=2; 4 (bimodal) — freq. 3 |
| repetidos: tabela HTML | ✅ | 4185 caracteres |
| todos_iguais_freq (quartis 1) | ✅ | n=6, média=2, Q1=1.25, Q3=2.75, s²=0.8, moda=não existe (amodal) |
| todos_iguais_freq (quartis 2) | ✅ | n=6, média=2, Q1=1, Q3=3, s²=0.8, moda=não existe (amodal) |
| todos_iguais_freq (quartis 3) | ✅ | n=6, média=2, Q1=1, Q3=3, s²=0.8, moda=não existe (amodal) |
| todos_iguais_freq: tabela HTML | ✅ | 4180 caracteres |
| variancia_nula (quartis 1) | ✅ | n=4, média=4, Q1=4, Q3=4, s²=0, moda=não existe (amodal) |
| variancia_nula (quartis 2) | ✅ | n=4, média=4, Q1=4, Q3=4, s²=0, moda=não existe (amodal) |
| variancia_nula (quartis 3) | ✅ | n=4, média=4, Q1=4, Q3=4, s²=0, moda=não existe (amodal) |
| variancia_nula: tabela HTML | ✅ | 4179 caracteres |
| media_zero (quartis 1) | ✅ | n=5, média=0, Q1=-1, Q3=1, s²=2.5, moda=não existe (amodal) |
| media_zero (quartis 2) | ✅ | n=5, média=0, Q1=-1.5, Q3=1.5, s²=2.5, moda=não existe (amodal) |
| media_zero (quartis 3) | ✅ | n=5, média=0, Q1=-1.5, Q3=1.5, s²=2.5, moda=não existe (amodal) |
| media_zero: tabela HTML | ✅ | 4178 caracteres |
| com_faltas (quartis 1) por grupo | ✅ | n=5, média=3.95, Q1=2, Q3=5.25, s²=7.2, moda=não existe (amodal) |
| com_faltas (quartis 2) por grupo | ✅ | n=5, média=3.95, Q1=1.75, Q3=6.625, s²=7.2, moda=não existe (amodal) |
| com_faltas (quartis 3) por grupo | ✅ | n=5, média=3.95, Q1=1.75, Q3=6.625, s²=7.2, moda=não existe (amodal) |
| com_faltas: tabela HTML | ✅ | 6080 caracteres |
| negativos_decimais (quartis 1) | ✅ | n=6, média=1.1876666666666666, Q1=-1.125, Q3=1.6877499999999999, s²=23.085462666666665, moda=não existe (amodal) |
| negativos_decimais (quartis 2) | ✅ | n=6, média=1.1876666666666666, Q1=-2.0625, Q3=4.21875, s²=23.085462666666665, moda=não existe (amodal) |
| negativos_decimais (quartis 3) | ✅ | n=6, média=1.1876666666666666, Q1=-1.5, Q3=2.25, s²=23.085462666666665, moda=não existe (amodal) |
| negativos_decimais: tabela HTML | ✅ | 4186 caracteres |
| grandes (quartis 1) | ✅ | n=4, média=1437500.375, Q1=1187500.6875, Q3=1625000.0625, s²=182291520833.4375, moda=não existe (amodal) |
| grandes (quartis 2) | ✅ | n=4, média=1437500.375, Q1=1062500.5625, Q3=1875000.1875, s²=182291520833.4375, moda=não existe (amodal) |
| grandes (quartis 3) | ✅ | n=4, média=1437500.375, Q1=1125000.625, Q3=1750000.125, s²=182291520833.4375, moda=não existe (amodal) |
| grandes: tabela HTML | ✅ | 4287 caracteres |
| vazio (quartis 1) | ✅ | n=0, média=None, Q1=None, Q3=None, s²=None, moda=n.d. |
| vazio (quartis 2) | ✅ | n=0, média=None, Q1=None, Q3=None, s²=None, moda=n.d. |
| vazio (quartis 3) | ✅ | n=0, média=None, Q1=None, Q3=None, s²=None, moda=n.d. |
| vazio: tabela HTML | ✅ | 4215 caracteres |
| grupos_desiguais (quartis 1) por grupo | ✅ | n=6, média=13.333333333333334, Q1=10.25, Q3=18, s²=41.46666666666666, moda=não existe (amodal) |
| grupos_desiguais (quartis 2) por grupo | ✅ | n=6, média=13.333333333333334, Q1=8.75, Q3=20.5, s²=41.46666666666666, moda=não existe (amodal) |
| grupos_desiguais (quartis 3) por grupo | ✅ | n=6, média=13.333333333333334, Q1=10, Q3=20, s²=41.46666666666666, moda=não existe (amodal) |
| grupos_desiguais: tabela HTML | ✅ | 7053 caracteres |

