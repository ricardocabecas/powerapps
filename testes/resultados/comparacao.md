# Resultados da comparação Power Fx × referência Python/scipy

Gerado em 11/10/2026 por `testes/executar_testes.py`. As fórmulas foram executadas com o interpretador open source **Microsoft.PowerFx.Interpreter 1.8.1** (.NET 8), com números em vírgula flutuante (como nas canvas apps).

**Total: 6432/6432 verificações sem diferenças.**

## Sintaxe de todas as fórmulas dos ecrãs

3086 fórmulas analisadas em formato invariante (ficheiros .pa.yaml) e convertidas para pt-PT (barra de fórmulas): **6172/6172 sem erros de sintaxe**.


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

## Fase 3 — Frequências e gráficos

**36/36 casos de acordo com a referência.**

| Caso | Resultado | Detalhe |
|---|---|---|
| tabela «nota_discreta» | ✅ | 9: 1 \| 10: 2 \| 11: 2 \| 12: 3 \| 13: 2 \| 14: 3 \| 15: 2 \| 16: 2 |
| gráfico «nota_discreta» | ✅ | SVG válido, 4144 caracteres, 10 barras |
| resumo «nota_discreta» | ✅ | n = 20   ·   10 valores distintos |
| tabela «sexo_categorica» | ✅ | F: 10 \| M: 10 |
| gráfico «sexo_categorica» | ✅ | SVG válido, 2311 caracteres, 2 barras |
| resumo «sexo_categorica» | ✅ | n = 20   ·   2 valores distintos |
| tabela «turma_categorica» | ✅ | A: 7 \| B: 7 \| C: 6 |
| gráfico «turma_categorica» | ✅ | SVG válido, 2241 caracteres, 3 barras |
| resumo «turma_categorica» | ✅ | n = 20   ·   3 valores distintos |
| tabela «altura_sturges» | ✅ | [155 ; 160[: 3 \| [160 ; 165[: 3 \| [165 ; 170[: 4 \| [170 ; 175[: 4 \| [175 ; 180[: 3 \| [180 ; 185]: 3 |
| gráfico «altura_sturges» | ✅ | SVG válido, 3512 caracteres, 6 barras |
| resumo «altura_sturges» | ✅ | n = 20   ·   6 classes ⏎ Regra de Sturges: k = ⌈1 + log₂ n⌉ = 6 ⏎ Amplitude das classes: h = 5   ·   1.ª classe começa em 155 ⏎ Mínimo = 155   ·   Máximo = 185 |
| tabela «altura_k4_inicio150_h10» | ✅ | [150 ; 160[: 3 \| [160 ; 170[: 7 \| [170 ; 180[: 7 \| [180 ; 190]: 3 |
| gráfico «altura_k4_inicio150_h10» | ✅ | SVG válido, 2744 caracteres, 4 barras |
| resumo «altura_k4_inicio150_h10» | ✅ | n = 20   ·   4 classes ⏎ Regra de Sturges: k = ⌈1 + log₂ n⌉ = 6 ⏎ Amplitude das classes: h = 10   ·   1.ª classe começa em 150 ⏎ Mínimo = 155   ·   Máximo = 185 |
| tabela «altura_k3_inicio160_h10_fora» | ✅ | [160 ; 170[: 7 \| [170 ; 180[: 7 \| [180 ; 190]: 3 |
| gráfico «altura_k3_inicio160_h10_fora» | ✅ | SVG válido, 2441 caracteres, 3 barras |
| resumo «altura_k3_inicio160_h10_fora» | ✅ | n = 20   ·   3 classes ⏎ Regra de Sturges: k = ⌈1 + log₂ n⌉ = 6 ⏎ Amplitude das classes: h = 10   ·   1.ª classe começa em 160 ⏎ Mínimo = 155   ·   Máximo = 185 ⏎ ⚠ 3 valor(es) ficaram fora das classes: ajuste o início ou a amplitude. |
| tabela «peso_sturges» | ✅ | [48 ; 54,2667[: 4 \| [54,2667 ; 60,5333[: 4 \| [60,5333 ; 66,8[: 4 \| [66,8 ; 73,0667[: 4 \| [73,0667 ; 79,3333[: 2 \| [79,3333 ; 85,6]: 2 |
| gráfico «peso_sturges» | ✅ | SVG válido, 3521 caracteres, 6 barras |
| resumo «peso_sturges» | ✅ | n = 20   ·   6 classes ⏎ Regra de Sturges: k = ⌈1 + log₂ n⌉ = 6 ⏎ Amplitude das classes: h = 6,2667   ·   1.ª classe começa em 48 ⏎ Mínimo = 48   ·   Máximo = 85,6 |
| tabela «peso_k5_h8» | ✅ | [45 ; 53[: 4 \| [53 ; 61[: 4 \| [61 ; 69[: 5 \| [69 ; 77[: 4 \| [77 ; 85]: 2 |
| gráfico «peso_k5_h8» | ✅ | SVG válido, 3375 caracteres, 5 barras |
| resumo «peso_k5_h8» | ✅ | n = 20   ·   5 classes ⏎ Regra de Sturges: k = ⌈1 + log₂ n⌉ = 6 ⏎ Amplitude das classes: h = 8   ·   1.ª classe começa em 45 ⏎ Mínimo = 48   ·   Máximo = 85,6 ⏎ ⚠ 1 valor(es) ficaram fora das classes: ajuste o início ou a amplitude. |
| tabela «fronteiras_exatas» | ✅ | [0,1 ; 0,3[: 1 \| [0,3 ; 0,5[: 2 \| [0,5 ; 0,7[: 1 \| [0,7 ; 0,9]: 2 |
| gráfico «fronteiras_exatas» | ✅ | SVG válido, 2576 caracteres, 4 barras |
| resumo «fronteiras_exatas» | ✅ | n = 6   ·   4 classes ⏎ Regra de Sturges: k = ⌈1 + log₂ n⌉ = 4 ⏎ Amplitude das classes: h = 0,2   ·   1.ª classe começa em 0,1 ⏎ Mínimo = 0,1   ·   Máximo = 0,9 |
| tabela «todos_iguais_classes» | ✅ | [5 ; 6[: 3 \| [6 ; 7[: 0 \| [7 ; 8]: 0 |
| gráfico «todos_iguais_classes» | ✅ | SVG válido, 2247 caracteres, 3 barras |
| resumo «todos_iguais_classes» | ✅ | n = 3   ·   3 classes ⏎ Regra de Sturges: k = ⌈1 + log₂ n⌉ = 3 ⏎ Amplitude das classes: h = 1   ·   1.ª classe começa em 5 ⏎ Mínimo = 5   ·   Máximo = 5 |
| tabela «um_valor» | ✅ | [2,5 ; 3,5]: 1 |
| gráfico «um_valor» | ✅ | SVG válido, 1499 caracteres, 1 barras |
| resumo «um_valor» | ✅ | n = 1   ·   1 classes ⏎ Regra de Sturges: k = ⌈1 + log₂ n⌉ = 1 ⏎ Amplitude das classes: h = 1   ·   1.ª classe começa em 2,5 ⏎ Mínimo = 2,5   ·   Máximo = 2,5 |
| tabela «discreta_decimais» | ✅ | 1,5: 2 \| 2,25: 1 \| 3: 1 |
| gráfico «discreta_decimais» | ✅ | SVG válido, 2090 caracteres, 3 barras |
| resumo «discreta_decimais» | ✅ | n = 4   ·   3 valores distintos |

## Fase 4 — Correlação e regressão

**33/33 casos de acordo com a referência.**

| Caso | Resultado | Detalhe |
|---|---|---|
| regressão «exemplo_altura_peso» | ✅ | n=20, r=0.9946312973208253, b=1.2346365658849703, a=-144.83416608920822, ŷ(x0)=68.14064152594915, p(ρ=0)=3.4511670810845736e-19 (scipy 3.4511670811081557e-19) |
| tabela HTML «exemplo_altura_peso» | ✅ | ok |
| dispersão «exemplo_altura_peso» | ✅ | SVG válido, 20 pontos, com reta |
| regressão «exemplo_altura_nota» | ✅ | n=20, r=-0.9133869564529047, b=-0.27794594988876326, a=60.547941208650926, ŷ(x0)=18.856048725336436, p(ρ=0)=1.8961535146080336e-08 (scipy 1.8961535146153764e-08) |
| tabela HTML «exemplo_altura_nota» | ✅ | ok |
| dispersão «exemplo_altura_nota» | ✅ | SVG válido, 20 pontos, com reta |
| regressão «reta_perfeita_positiva» | ✅ | n=5, r=1, b=2, a=1, ŷ(x0)=6, p(ρ=0)=0 (scipy 0.0) |
| tabela HTML «reta_perfeita_positiva» | ✅ | ok |
| dispersão «reta_perfeita_positiva» | ✅ | SVG válido, 5 pontos, com reta |
| regressão «reta_perfeita_negativa» | ✅ | n=4, r=-1, b=-2.5, a=10, ŷ(x0)=-15, p(ρ=0)=0 (scipy 0.0) |
| tabela HTML «reta_perfeita_negativa» | ✅ | ok |
| dispersão «reta_perfeita_negativa» | ✅ | SVG válido, 4 pontos, com reta |
| regressão «y_constante» | ✅ | n=4, r=None, b=0, a=5, ŷ(x0)=5, p(ρ=0)=None (scipy None) |
| tabela HTML «y_constante» | ✅ | ok |
| dispersão «y_constante» | ✅ | SVG válido, 4 pontos, com reta |
| regressão «x_constante» | ✅ | n=3, r=None, b=None, a=None, ŷ(x0)=None, p(ρ=0)=None (scipy None) |
| tabela HTML «x_constante» | ✅ | ok |
| dispersão «x_constante» | ✅ | SVG válido, 3 pontos |
| regressão «n1» | ✅ | n=1, r=None, b=None, a=None, ŷ(x0)=None, p(ρ=0)=None (scipy None) |
| tabela HTML «n1» | ✅ | ok |
| dispersão «n1» | ✅ | SVG válido, 1 pontos |
| regressão «n2» | ✅ | n=2, r=-1, b=-0.5, a=2.5, ŷ(x0)=1.5, p(ρ=0)=None (scipy None) |
| tabela HTML «n2» | ✅ | ok |
| dispersão «n2» | ✅ | SVG válido, 2 pontos, com reta |
| regressão «com_faltas» | ✅ | n=4, r=0.9862673700913519, b=0.7928571428571427, a=1.1535714285714285, ŷ(x0)=None, p(ρ=0)=0.013732629908648078 (scipy 0.013732629908647986) |
| tabela HTML «com_faltas» | ✅ | ok |
| dispersão «com_faltas» | ✅ | SVG válido, 4 pontos, com reta |
| regressão «sem_correlacao» | ✅ | n=5, r=0, b=0, a=2.6, ŷ(x0)=2.6, p(ρ=0)=1 (scipy 1.0) |
| tabela HTML «sem_correlacao» | ✅ | ok |
| dispersão «sem_correlacao» | ✅ | SVG válido, 5 pontos, com reta |
| regressão «decimais_negativos» | ✅ | n=5, r=-0.8672854478323896, b=-0.6807714635876927, a=-0.5836902534993229, ŷ(x0)=0.09708121008836978, p(ρ=0)=0.056868470776834865 (scipy 0.056868470776834684) |
| tabela HTML «decimais_negativos» | ✅ | ok |
| dispersão «decimais_negativos» | ✅ | SVG válido, 5 pontos, com reta |

## Fase 5 — Inferência

**80/80 casos de acordo com a referência.**

| Caso | Resultado | Detalhe |
|---|---|---|
| qui-quadrado «ader_sexo_iguais» | ✅ | χ²=0, gl=1, p=1 (scipy 1.0), células com E<5: 0 |
| relatório qui-quadrado «ader_sexo_iguais» | ✅ | ok |
| qui-quadrado «ader_turma_iguais» | ✅ | χ²=0.09999999999999999, gl=2, p=0.95122942449563 (scipy 0.951229424500714), células com E<5: 0 |
| relatório qui-quadrado «ader_turma_iguais» | ✅ | ok |
| qui-quadrado «ader_turma_indicadas» | ✅ | χ²=1.9000000000000001, gl=2, p=0.3867410234458508 (scipy 0.38674102345450123), células com E<5: 0 |
| relatório qui-quadrado «ader_turma_indicadas» | ✅ | ok |
| qui-quadrado «ader_nota_numerica_pesos» | ✅ | χ²=2.5208333333333335, gl=9, p=0.9803179534746087 (scipy 0.980317953485687), células com E<5: 10 |
| relatório qui-quadrado «ader_nota_numerica_pesos» | ✅ | ok |
| qui-quadrado «ader_colada_dado» | ✅ | χ²=4.2, gl=5, p=0.5209949534257625 (scipy 0.5209949534314051), células com E<5: 0 |
| relatório qui-quadrado «ader_colada_dado» | ✅ | ok |
| qui-quadrado «ader_colada_percentagens» | ✅ | χ²=2, gl=2, p=0.36787944116331894 (scipy 0.36787944117144245), células com E<5: 0 |
| relatório qui-quadrado «ader_colada_percentagens» | ✅ | ok |
| qui-quadrado «ader_esperadas_baixas» | ✅ | χ²=6.199999999999999, gl=2, p=0.0450492023935935 (scipy 0.04504920239355781), células com E<5: 3 |
| relatório qui-quadrado «ader_esperadas_baixas» | ✅ | ok |
| qui-quadrado «ader_proporcoes_em_falta» | ✅ | teste não calculado: indique tantas proporções esperadas quantas as categorias (3), pela ordem da tabela. |
| relatório qui-quadrado «ader_proporcoes_em_falta» | ✅ | ok |
| qui-quadrado «indep_sexo_turma» | ✅ | χ²=0.2857142857142857, gl=2, p=0.8668778997406118 (scipy 0.8668778997501817), células com E<5: 6 |
| relatório qui-quadrado «indep_sexo_turma» | ✅ | ok |
| qui-quadrado «indep_colada_2x2» | ✅ | χ²=11.42857142857143, gl=1, p=0.000723232716418553 (scipy 0.0007232327164301923), células com E<5: 0 |
| relatório qui-quadrado «indep_colada_2x2» | ✅ | ok |
| qui-quadrado «indep_colada_sem_nomes_3x3» | ✅ | χ²=10.06955879810639, gl=4, p=0.039272132877815724 (scipy 0.03927213287544329), células com E<5: 0 |
| relatório qui-quadrado «indep_colada_sem_nomes_3x3» | ✅ | ok |
| qui-quadrado «indep_colada_esperadas_baixas» | ✅ | χ²=3.555555555555556, gl=2, p=0.16901331540381886 (scipy 0.16901331540606604), células com E<5: 5 |
| relatório qui-quadrado «indep_colada_esperadas_baixas» | ✅ | ok |
| qui-quadrado «indep_colada_linha_vazia» | ✅ | teste não calculado: há frequências esperadas nulas (uma linha ou coluna sem observações ou uma proporção igual a 0). |
| relatório qui-quadrado «indep_colada_linha_vazia» | ✅ | ok |
| qui-quadrado «indep_colada_invalidos» | ✅ | χ²=5, gl=1, p=0.02534731867762744 (scipy 0.025347318677468325), células com E<5: 3 |
| relatório qui-quadrado «indep_colada_invalidos» | ✅ | ok |
| ANOVA «altura_por_turma» | ✅ | F=0.27128891198766825, gl=(2, 17), p=0.7656350924930889 (scipy 0.7656350924935016) |
| relatório ANOVA «altura_por_turma» | ✅ | ok |
| ANOVA «nota_por_turma» | ✅ | F=0.17722573233773714, gl=(2, 17), p=0.8391184244256376 (scipy 0.8391184244260104) |
| relatório ANOVA «nota_por_turma» | ✅ | ok |
| ANOVA «tres_grupos_desiguais» | ✅ | F=36.822222222222216, gl=(2, 6), p=0.000427550372854951 (scipy 0.00042755037285496377) |
| relatório ANOVA «tres_grupos_desiguais» | ✅ | ok |
| ANOVA «dois_grupos_igual_t» | ✅ | F=42.94615954556684, gl=(1, 18), p=3.702650750247683e-06 (scipy 3.702650750255917e-06) |
| relatório ANOVA «dois_grupos_igual_t» | ✅ | ok |
| ANOVA «grupo_com_n1» | ✅ | F=27, gl=(1, 2), p=0.03509871864598464 (scipy 0.03509871864598465) |
| relatório ANOVA «grupo_com_n1» | ✅ | ok |
| ANOVA «variancia_dentro_nula» | ✅ | F=None, gl=(1, 2), p=None (scipy None) |
| relatório ANOVA «variancia_dentro_nula» | ✅ | ok |
| ANOVA «um_so_grupo» | ✅ | F=None, gl=(0, 2), p=None (scipy None) |
| relatório ANOVA «um_so_grupo» | ✅ | ok |
| ANOVA «colunas_como_grupos» | ✅ | F=18.58008658008658, gl=(2, 8), p=0.0009847762225222532 (scipy 0.0009847762225222944) |
| relatório ANOVA «colunas_como_grupos» | ✅ | ok |
| ANOVA «colunas_com_vazia» | ✅ | F=10, gl=(1, 4), p=0.034109423167409586 (scipy 0.03410942316740961) |
| relatório ANOVA «colunas_com_vazia» | ✅ | ok |
| teste t «1amostra_altura_170_bilateral» | ✅ | t=-0.28956340830869276, gl=19, p=0.775286438213695 (scipy 0.7752864382137891) |
| relatório t «1amostra_altura_170_bilateral» | ✅ | ok |
| teste t «1amostra_altura_165_direita» | ✅ | t=2.3428312126793687, gl=19, p=0.01508741001969021 (scipy 0.01508741001968566) |
| relatório t «1amostra_altura_165_direita» | ✅ | ok |
| teste t «1amostra_altura_172_esquerda» | ✅ | t=-1.6057607188027234, gl=19, p=0.062409487445890956 (scipy 0.062409487445887805) |
| relatório t «1amostra_altura_172_esquerda» | ✅ | ok |
| teste t «1amostra_n2» | ✅ | t=15, gl=1, p=0.04237860926989309 (scipy 0.04237860926989283) |
| relatório t «1amostra_n2» | ✅ | ok |
| teste t «1amostra_n1» | ✅ | t=None, gl=None, p=None (scipy None) |
| relatório t «1amostra_n1» | ✅ | ok |
| teste t «1amostra_variancia_nula» | ✅ | t=None, gl=3, p=None (scipy None) |
| relatório t «1amostra_variancia_nula» | ✅ | ok |
| teste t «ind_altura_sexo_FM» | ✅ | t=-6.5533319422692795, gl=18, p=3.702650750247683e-06 (scipy 3.702650750255874e-06) |
| relatório t «ind_altura_sexo_FM» | ✅ | ok |
| teste t «ind_altura_sexo_FM_esquerda» | ✅ | t=-6.5533319422692795, gl=18, p=1.8513253751238415e-06 (scipy 1.851325375127937e-06) |
| relatório t «ind_altura_sexo_FM_esquerda» | ✅ | ok |
| teste t «welch_altura_sexo_FM» | ✅ | t=-6.5533319422692795, gl=17.888962171928235, p=3.818401627395311e-06 (scipy 3.8184016274034145e-06) |
| relatório t «welch_altura_sexo_FM» | ✅ | ok |
| teste t «welch_d0_menos10_direita» | ✅ | t=-1.8387046456726777, gl=17.888962171928235, p=0.9586899134854601 (scipy 0.9586899134854648) |
| relatório t «welch_d0_menos10_direita» | ✅ | ok |
| teste t «ind_duas_colunas» | ✅ | t=3.3234702564419836, gl=9, p=0.008891040066831049 (scipy 0.008891040066830983) |
| relatório t «ind_duas_colunas» | ✅ | ok |
| teste t «welch_duas_colunas_desiguais» | ✅ | t=0.30562873784578987, gl=6.032273852579569, p=0.7701597909404814 (scipy 0.7701597909404835) |
| relatório t «welch_duas_colunas_desiguais» | ✅ | ok |
| teste t «welch_gl_fracionarios_n2» | ✅ | t=-3.3443794565778315, gl=2.027593804617546, p=0.07749387508187552 (scipy 0.07749387493182988) |
| relatório t «welch_gl_fracionarios_n2» | ✅ | ok |
| teste t «ind_um_grupo_vazio» | ✅ | t=None, gl=None, p=None (scipy None) |
| relatório t «ind_um_grupo_vazio» | ✅ | ok |
| teste t «emparelhado_peso_altura» | ✅ | t=9.988467827373201, gl=19, p=5.361750091034704e-09 (scipy 5.361750091066275e-09) |
| relatório t «emparelhado_peso_altura» | ✅ | ok |
| teste t «emparelhado_antes_depois» | ✅ | t=2.4445060351935237, gl=5, p=0.029164651403131372 (scipy 0.029164651403131323) |
| relatório t «emparelhado_antes_depois» | ✅ | ok |
| teste t «emparelhado_com_faltas» | ✅ | t=1.1470786693528088, gl=2, p=0.3700592116512881 (scipy 0.37005921165128797) |
| relatório t «emparelhado_com_faltas» | ✅ | ok |

