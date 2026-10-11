# Resultados da comparação Power Fx × referência Python/scipy

Gerado em 11/10/2026 por `testes/executar_testes.py`. As fórmulas foram executadas com o interpretador open source **Microsoft.PowerFx.Interpreter 1.8.1** (.NET 8), com números em vírgula flutuante (como nas canvas apps).

**Total: 2725/2725 verificações sem diferenças.**

## Sintaxe de todas as fórmulas dos ecrãs

1289 fórmulas analisadas em formato invariante (ficheiros .pa.yaml) e convertidas para pt-PT (barra de fórmulas): **2578/2578 sem erros de sintaxe**.


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

