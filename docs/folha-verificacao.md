# Folha de verificação — valores esperados na app

> Gerada por `testes/gerar_folha.py`. Os valores esperados foram calculados com **numpy/scipy** (implementação
> de referência), não com as fórmulas da app. Use os **dados de exemplo** (20 estudantes) que a app carrega na
> primeira abertura — ou carregue em *Repor dados de exemplo* no ecrã Dados.
>
> As mesmas fórmulas já foram executadas no interpretador Power Fx (ver `testes/resultados/comparacao.md`);
> esta folha serve para confirmar que, **dentro do Power Apps Studio**, tudo se comporta igual.

Marque cada linha depois de confirmar. Os números devem coincidir em todas as casas mostradas.

## 1. Ecrã Dados

| ✓ | Ação | Resultado esperado |
|---|---|---|
| ☐ | Abrir a app (pré-visualização, F5) | Tabela com 20 linhas; cabeçalhos «Altura (cm)», «Peso (kg)», «Nota (0-20)», «Sexo», «Turma» |
| ☐ | Na linha 1, escrever `165,5` em Altura e sair da célula | Fica `165,5`; o resumo continua com 0 células vazias |
| ☐ | Escrever `abc` numa célula numérica | Aviso «não é um número válido»; contorno vermelho; a célula conta como vazia |
| ☐ | Escrever `1.5` (com ponto) | É aceite e mostrado como `1,5` |
| ☐ | Carregar em *Repor dados de exemplo* | Volta aos 20 estudantes |
| ☐ | Colar na caixa da direita o texto abaixo* e carregar em *Analisar* | «Linhas com dados: 5 · Colunas: 2»; «Primeira linha: cabeçalho (nomes: X; Y)»; «⚠ 2 valor(es) inválido(s)»: linha 3, X: «abc» e linha 4, Y: «1,2,3» |
| ☐ | Carregar em *Importar (substituir dados)* | 5 linhas; variáveis 1 e 2 passam a chamar-se X e Y; notificação com o aviso dos 2 valores inválidos |
| ☐ | Carregar em *Repor dados de exemplo* antes de continuar | Volta aos 20 estudantes |

\* Texto a colar (pode copiar destas 6 linhas para o Excel em 2 colunas e daí para a app, ou escrever com tabulações):

```
X<TAB>Y
1<TAB>2
abc<TAB>3
4<TAB>1,2,3
5<TAB>
6<TAB>7
```

## 2. Ecrã Descritiva

**Variável: Altura (cm), sem grupos**

| ✓ | Medida | Valor esperado |
|---|---|---|
| ☐ | n | 20 |
| ☐ | Soma | 3 389,0000 |
| ☐ | Média | 169,4500 |
| ☐ | Mediana | 169,5000 |
| ☐ | Mínimo | 155,0000 |
| ☐ | Máximo | 185,0000 |
| ☐ | Amplitude total | 30,0000 |
| ☐ | Variância amostral (n − 1) | 72,1553 |
| ☐ | Desvio padrão amostral | 8,4944 |
| ☐ | Variância populacional (n) | 68,5475 |
| ☐ | Desvio padrão populacional | 8,2793 |
| ☐ | Moda | não existe (amodal) |
| ☐ | CV | 5,01 % |
| ☐ | Q₁ / Q₃ / AIQ — QUARTIL.INC | 162,7500 / 175,5000 / 12,7500 |
| ☐ | Q₁ / Q₃ / AIQ — QUARTIL.EXC / SPSS | 162,2500 / 176,5000 / 14,2500 |
| ☐ | Q₁ / Q₃ / AIQ — mediana de cada metade | 162,5000 / 176,0000 / 13,5000 |

**Variável: Nota (0-20), sem grupos**

| ✓ | Medida | Valor esperado |
|---|---|---|
| ☐ | n | 20 |
| ☐ | Soma | 269,0000 |
| ☐ | Média | 13,4500 |
| ☐ | Mediana | 13,5000 |
| ☐ | Mínimo | 9,0000 |
| ☐ | Máximo | 18,0000 |
| ☐ | Amplitude total | 9,0000 |
| ☐ | Variância amostral (n − 1) | 6,6816 |
| ☐ | Desvio padrão amostral | 2,5849 |
| ☐ | Variância populacional (n) | 6,3475 |
| ☐ | Desvio padrão populacional | 2,5194 |
| ☐ | Moda | 12; 14 (bimodal) — freq. 3 |
| ☐ | CV | 19,22 % |
| ☐ | Q₁ / Q₃ / AIQ — QUARTIL.INC | 11,7500 / 15,2500 / 3,5000 |
| ☐ | Q₁ / Q₃ / AIQ — QUARTIL.EXC / SPSS | 11,2500 / 15,7500 / 4,5000 |
| ☐ | Q₁ / Q₃ / AIQ — mediana de cada metade | 11,5000 / 15,5000 / 4,0000 |

**Altura (cm), agrupar por Sexo** (colunas Total, F, M):

| ✓ | Medida | Total | F | M |
|---|---|---|---|---|
| ☐ | n | 20 | 10 | 10 |
| ☐ | Média | 169,4500 | 162,5000 | 176,4000 |
| ☐ | Desvio padrão amostral | 8,4944 | 4,5522 | 4,9261 |

## 3. Ecrã Frequências

**Altura (cm), «Classes (dados agrupados)», caixas vazias** → regra de Sturges

Resumo: n = 20 · 6 classes · Sturges k = 6 · h = 5 · início 155. Deve aparecer um **histograma** com 6 barras contíguas.

| ✓ | Classe | nᵢ | fᵢ | Nᵢ | Fᵢ |
|---|---|---|---|---|---|
| ☐ | [155 ; 160[ | 3 | 0,1500 | 3 | 0,1500 |
| ☐ | [160 ; 165[ | 3 | 0,1500 | 6 | 0,3000 |
| ☐ | [165 ; 170[ | 4 | 0,2000 | 10 | 0,5000 |
| ☐ | [170 ; 175[ | 4 | 0,2000 | 14 | 0,7000 |
| ☐ | [175 ; 180[ | 3 | 0,1500 | 17 | 0,8500 |
| ☐ | [180 ; 185] | 3 | 0,1500 | 20 | 1,0000 |

**Mesmos dados com n.º de classes = 3, início = 160, amplitude = 10** → aviso «⚠ 3 valor(es) ficaram fora das classes» e contagens [160 ; 170[: 7, [170 ; 180[: 7, [180 ; 190]: 3.

**Nota (0-20), «Valores distintos»** → **diagrama de barras** com 10 barras:

| ✓ | Valor | nᵢ | fᵢ (%) | Nᵢ | Fᵢ |
|---|---|---|---|---|---|
| ☐ | 9 | 1 | 5,00 | 1 | 0,0500 |
| ☐ | 10 | 2 | 10,00 | 3 | 0,1500 |
| ☐ | 11 | 2 | 10,00 | 5 | 0,2500 |
| ☐ | 12 | 3 | 15,00 | 8 | 0,4000 |
| ☐ | 13 | 2 | 10,00 | 10 | 0,5000 |
| ☐ | 14 | 3 | 15,00 | 13 | 0,6500 |
| ☐ | 15 | 2 | 10,00 | 15 | 0,7500 |
| ☐ | 16 | 2 | 10,00 | 17 | 0,8500 |
| ☐ | 17 | 2 | 10,00 | 19 | 0,9500 |
| ☐ | 18 | 1 | 5,00 | 20 | 1,0000 |

**Sexo** → a lista «Tipo de tabela» fica desativada; F: 10, M: 10 (fᵢ = 0,5000 cada).

## 4. Ecrã Regressão

x = Altura (cm), y = Peso (kg), valor de x = `172,5`

| ✓ | Medida | Valor esperado |
|---|---|---|
| ☐ | n | 20 |
| ☐ | x̄ | 169,4500 |
| ☐ | ȳ | 64,3750 |
| ☐ | Sxx | 1 370,9500 |
| ☐ | Syy | 2 112,3975 |
| ☐ | Sxy | 1 692,6250 |
| ☐ | Covariância amostral | 89,0855 |
| ☐ | r | 0,9946 |
| ☐ | R² | 0,9893 |
| ☐ | Declive b | 1,2346 |
| ☐ | Ordenada na origem a | -144,8342 |
| ☐ | ŷ para x = 172,5 | 68,1406 |
| ☐ | t (H₀: ρ = 0) | 40,7786 |
| ☐ | gl | 18 |
| ☐ | Valor de p (ρ = 0) | < 0,0001 |
| ☐ | Equação | ŷ = -144,8342 + 1,2346 · x |
| ☐ | Gráfico | 20 pontos e uma reta vermelha crescente; eixos com vírgula decimal |
| ☐ | Escrever `250` no valor de x | Aviso de extrapolação |

## 5. Ecrã Testes t (α = 0,05)

| ✓ | Configuração | t | gl | p | Decisão |
|---|---|---|---|---|---|
| ☐ | Uma amostra, Altura, μ₀ = 170, bilateral | -0,2896 | 19 | 0,7753 | não se rejeita H₀ |
| ☐ | Uma amostra, Altura, μ₀ = 165, unilateral à direita | 2,3428 | 19 | 0,0151 | rejeita-se H₀ |
| ☐ | Independentes (variâncias iguais), Altura por Sexo, grupo 1 = F, grupo 2 = M, Δ₀ = 0, bilateral | -6,5533 | 18 | < 0,0001 | rejeita-se H₀ |
| ☐ | Welch, Altura por Sexo, F vs M, bilateral | -6,5533 | 17,8890 | < 0,0001 | rejeita-se H₀ |
| ☐ | Emparelhadas, X = Altura, Y = Peso, Δ₀ = 100, bilateral | 9,9885 | 19 | < 0,0001 | rejeita-se H₀ |

## 6. Ecrã ANOVA (α = 0,05)

Variável Altura (cm), fator Turma:

| ✓ | Fonte | SQ | gl | QM | F | p |
|---|---|---|---|---|---|---|
| ☐ | Entre grupos | 42,4024 | 2 | 21,2012 | 0,2713 | 0,7656 |
| ☐ | Dentro dos grupos | 1 328,5476 | 17 | 78,1499 | | |
| ☐ | Total | 1 370,9500 | 19 | | | |

Decisão esperada: não se rejeita H₀.

Controlo cruzado: fator **Sexo** (2 grupos) → F = 42,9462, p = < 0,0001, igual ao p do teste t com variâncias iguais (F = t²).

## 7. Ecrã Qui-quadrado (α = 0,05)

| ✓ | Configuração | χ² | gl | p | Observações |
|---|---|---|---|---|---|
| ☐ | Aderência, variáveis, Turma, proporções iguais | 0,1000 | 2 | 0,9512 | esperadas 6,6667 cada |
| ☐ | Aderência, Turma, proporções indicadas `0,5; 0,25; 0,25` | 1,9000 | 2 | 0,3867 | esperadas 10; 5; 5 |
| ☐ | Independência, variáveis, linhas Sexo × colunas Turma | 0,2857 | 2 | 0,8669 | aviso de Cochran: 6 de 6 células com E < 5 |
| ☐ | Independência, tabela colada (abaixo) | 11,4286 | 1 | 0,0007 | esperadas 22,5 e 17,5 |
| ☐ | Aderência, tabela colada de um dado (abaixo), proporções iguais | 4,2000 | 5 | 0,5210 | categorias 1 a 6 |

Tabela de contingência a colar (3 linhas, tabulações entre colunas; o 1.º campo da 1.ª linha fica vazio):

```
<TAB>Sim<TAB>Não
Homem<TAB>30<TAB>10
Mulher<TAB>15<TAB>25
```

Tabela de um dado (aderência):

```
Face<TAB>Obs
1<TAB>8
2<TAB>12
3<TAB>9
4<TAB>11
5<TAB>6
6<TAB>14
```

## 8. Verificações de interface (não automatizáveis aqui)

| ✓ | O quê | Como confirmar |
|---|---|---|
| ☐ | Colagem dos ecrãs | Cada ficheiro de `Src/` cola sem erros e cria o ecrã com o nome indicado |
| ☐ | Navegação | Os 7 botões da barra superior mudam de ecrã; o botão do ecrã atual aparece branco |
| ☐ | Separador decimal | Todos os números aparecem com vírgula decimal (ex.: 169,4500) |
| ☐ | Tabelas HTML | As tabelas dos ecrãs Descritiva, Regressão, Testes t, ANOVA e Qui-quadrado aparecem formatadas e cabem no painel |
| ☐ | Gráficos SVG | Histograma, diagrama de barras e dispersão aparecem no controlo Imagem, com texto legível |
| ☐ | Listas pendentes | Mudar a variável/teste atualiza os resultados de imediato (sem botão Calcular) |
| ☐ | Campos que aparecem e desaparecem | Testes t: os campos de grupo só aparecem nos testes independentes com «variável + grupo» |
| ☐ | Desempenho | Com 200 linhas de dados, cada ecrã responde em menos de 1–2 segundos |

