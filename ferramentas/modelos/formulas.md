# Fórmulas da app de Estatística — explicação e material de apoio

> Documento gerado automaticamente por `ferramentas/gerar.py` a partir das mesmas fórmulas que estão nos
> ficheiros `Src/*.pa.yaml`. Não editar à mão: alterar o modelo `ferramentas/modelos/formulas.md`.

Todas as fórmulas deste documento estão escritas na **sintaxe pt-PT da barra de fórmulas** do Power Apps
Studio, que é o que vê quando o seu navegador/Windows está em português de Portugal:

| Elemento | Ficheiros `.pa.yaml` (invariante) | Barra de fórmulas (pt-PT) |
|---|---|---|
| Separador decimal | `1.5` | `1,5` |
| Separador de argumentos, campos e registos | `,` | `;` |
| Encadear instruções (comportamento) | `;` | `;;` |

Os nomes das funções (`Sum`, `Filter`, `If`…) e das propriedades (`Text`, `Items`…) são sempre em inglês.
O conteúdo dos textos entre aspas nunca muda: por exemplo, o formato `"[$-en-US]#,##0.0000"` continua com
ponto e vírgula **dentro** das aspas, porque o marcador `[$-en-US]` diz ao Power Apps que o formato está
escrito à inglesa (ponto decimal). O terceiro argumento `"pt-PT"` faz com que o resultado saia com vírgula
decimal.

## 0. Convenções

* **Nomes de controlos** começam pelo tipo: `lbl` etiqueta, `txt` caixa de texto, `drp` lista pendente,
  `btn` botão, `gal` galeria, `img` imagem, `htm` texto HTML, `ret` retângulo. O nome dos ecrãs começa por `scr`.
* **Variáveis globais** começam por `var` (`varNomes`, `varImportacao`…) e **coleções** por `col`
  (`colDados`, `colColagem`…).
* **Variáveis locais** criadas com `With` começam por `_` (`_n`, `_media`…). Assim distinguem-se logo das
  colunas das tabelas e dos nomes de controlos. A gramática do Power Fx permite identificadores começados por `_`.
* Os cálculos são **reativos**: cada resultado é uma fórmula que depende dos dados e das escolhas feitas
  nas listas pendentes. Quando os dados mudam, os resultados atualizam-se sozinhos (não há botão «Calcular»).

### Modelo de dados

A coleção `colDados` tem uma linha por observação (unidade estatística) e as colunas:

| Campo | Tipo | Significado |
|---|---|---|
| `Id` | número | n.º da linha (1, 2, 3…) |
| `N1`, `N2`, `N3` | número | três variáveis numéricas (em branco = valor em falta) |
| `C1`, `C2` | texto | duas variáveis categóricas (de grupo) |

Os nomes que os alunos dão às variáveis ficam no registo `varNomes` (`varNomes.N1`, …, `varNomes.C2`).

### Conversão de texto em número (vírgula ou ponto decimal)

O `Value` do Power Fx interpreta o texto segundo um idioma. Para aceitar as duas convenções, a app limpa o
texto (retira espaços, incluindo o espaço inseparável que o Excel usa como separador de milhares), troca a
vírgula por ponto e lê o número em `"en-US"`. `IfError` devolve vazio (`Blank()`) se o texto não for um número:

{{pt: F_comum.num("Self.Text")}}

Um texto é **inválido** quando não está vazio e a conversão dá erro:

{{pt: F_comum.invalido("Self.Text")}}

Exemplos: `1,5` → 1,5 · `1.5` → 1,5 · `1 234,5` → 1234,5 · `5%` → 0,05 · `1,2,3` → inválido · `abc` → inválido.

### Formatação dos resultados (vírgula decimal)

Todos os números são mostrados com 4 casas decimais, vírgula decimal e espaço como separador de milhares.
Um valor em branco mostra `n.d.` (não definido, por exemplo a variância com n = 1):

{{pt: F_comum.fmt("_valor")}}

## 1. Entrada de dados (ecrã `scrDados`)

### 1.1 Inicialização (`scrDados.OnVisible`)

Na primeira abertura cria `varNomes`, a coleção `colDados` com dados de exemplo (20 estudantes fictícios) e
as coleções auxiliares da colagem. `ClearCollect` seguido de `Clear` serve só para o Power Apps ficar a
conhecer o tipo das colunas.

{{pt: F_dados.iniciar()}}

### 1.2 Galeria editável

A galeria `galDados` tem `Items = colDados`. Cada célula numérica é uma caixa de texto:

* `Default` mostra o número com vírgula decimal e só as casas necessárias:

{{pt: F_comum.fmt_livre("ThisItem.N1")}}

* `OnChange` converte o que o aluno escreveu e grava com `Patch` na linha certa (procurada pelo `Id`); se o
  texto não for um número aparece um aviso:

{{pt: F_dados.ecra_dados_onchange("N1")}}

* `BorderColor` fica vermelho enquanto o texto for inválido.

O botão ✕ apaga a linha e volta a numerar as linhas de 1 a n (através de uma coleção temporária, porque não se
pode alterar uma coleção dentro de um `ForAll` que a percorre):

{{pt: "RemoveIf(colDados, Id = ThisItem.Id);\n" + F_dados.renumerar()}}

### 1.3 Colar colunas do Excel

Quando se copiam células no Excel, a área de transferência recebe texto em que **as linhas são separadas por
mudança de linha** (`Char(10)`, precedido de `Char(13)` no Windows) e **as colunas por tabulação** (`Char(9)`).

**Passo 1 — partir o texto em linhas e células** (botão *Analisar*, coleção `colColagem`). `Split` parte o texto,
`Trim` limpa os espaços e as linhas sem nenhuma célula preenchida são ignoradas:

{{pt: F_dados.linhas("txtColar.Text")}}

**Passo 2 — caracterizar as colunas** (coleção `colColunas`). Uma coluna é considerada numérica se pelo menos
metade das células preenchidas (a partir da 2.ª linha) forem números:

{{pt: F_dados.colunas()}}

**Passo 3 — cabeçalho.** No modo *Automático*, a 1.ª linha é cabeçalho quando alguma coluna numérica tem
texto não numérico na 1.ª linha:

{{pt: F_dados.cabecalho()}}

**Passo 4 — escolher a coluna de origem de cada variável.** As listas `drpMapN1`…`drpMapC2` mostram
`n.º · 1.ª célula`; por omissão as colunas numéricas vão para `N1`, `N2`, `N3` e as de texto para `C1`, `C2`.
Exemplo para `N1`:

{{pt: F_dados.default_mapa("N1")}}

**Passo 5 — importar.** Constrói-se um registo com as linhas prontas para `colDados`, a lista de valores
inválidos (que ficam em branco) e os nomes vindos do cabeçalho:

{{pt: F_dados.importar("0")}}

O botão *Importar (substituir dados)* usa esse registo assim:

{{pt: F_dados.importar_substituir_resumo()}}

O texto de diagnóstico (`lblDiagnostico`) usa o mesmo registo para mostrar, **antes de importar**, quantas
linhas e colunas foram detetadas, se a 1.ª linha é cabeçalho e quais os valores inválidos (com o n.º da linha
no texto colado, para os encontrar no Excel).

## 2. Estatística descritiva (ecrã `scrDescritiva`)

### 2.1 Escolha da variável e dos grupos

As listas pendentes mostram os nomes dados pelos alunos (`[varNomes.N1; varNomes.N2; varNomes.N3]`). O nome
escolhido é convertido no índice da variável (1, 2 ou 3) com `Switch`:

{{pt: F_comum.indice_num("drpDesVar")}}

Os valores da variável (e, se se pedir agrupamento, o grupo de cada observação) obtêm-se de `colDados`,
ignorando as células vazias:

{{pt: F_descritiva.vetor_com_grupo("_k", "_kg")}}

### 2.2 Medidas

Seja x₍₁₎ ≤ x₍₂₎ ≤ … ≤ x₍ₙ₎ a amostra ordenada.

| Medida | Definição |
|---|---|
| Média | x̄ = (x₁ + … + xₙ) / n |
| Mediana | x₍₍ₙ₊₁₎/₂₎ se n é ímpar; média de x₍ₙ/₂₎ e x₍ₙ/₂₊₁₎ se n é par |
| Moda | valor(es) com maior frequência; «amodal» se todos têm a mesma frequência |
| Amplitude total | x₍ₙ₎ − x₍₁₎ |
| Amplitude interquartil | AIQ = Q₃ − Q₁ |
| Variância amostral | s² = Σ(xᵢ − x̄)² / (n − 1) — estimador da variância da população; precisa de n ≥ 2 |
| Variância populacional | σ² = Σ(xᵢ − x̄)² / n — quando os dados são a população toda |
| Desvio padrão | raiz quadrada da variância respetiva |
| Coeficiente de variação | CV = s / \|x̄\| × 100 % (com o desvio padrão amostral; não definido se x̄ = 0) |

**Quartis — três métodos** (a app deixa escolher; a mediana é igual nos três):

1. **Excel QUARTIL.INC** (também o método por omissão do R e do numpy): posição h = (n − 1)·p + 1.
2. **Excel QUARTIL.EXC / SPSS / Minitab**: posição h = (n + 1)·p, limitada ao intervalo [1, n].
3. **Mediana de cada metade**: Q₁ é a mediana das ⌊n/2⌋ menores observações e Q₃ a das ⌊n/2⌋ maiores
   (quando n é ímpar, o valor central não entra em nenhuma das metades).

Nos métodos 1 e 2, se h não for inteiro interpola-se linearmente: Q = x₍⌊h⌋₎ + (h − ⌊h⌋)·(x₍⌊h⌋₊₁₎ − x₍⌊h⌋₎).

*Exemplo* (n = 9: 2, 2, 2, 3, 3, 4, 4, 4, 5): método 1 → h = 3, Q₁ = 2; método 2 → h = 2,5, Q₁ = 2;
método 3 → metade inferior 2, 2, 2, 3 → Q₁ = 2. Para Q₃: método 1 → h = 7, Q₃ = 4; método 2 → h = 7,5,
Q₃ = 4; método 3 → metade superior 4, 4, 4, 5 → Q₃ = 4.

Em Power Fx, o 1.º quartil pelo método escolhido (`_s` é a amostra ordenada, `_n` a sua dimensão):

{{pt: F_descritiva.quartil(1)}}

### 2.3 Fórmula completa

Todas as medidas são calculadas num só registo. `With` encadeados guardam os resultados intermédios
(amostra ordenada, n, soma, média, soma dos quadrados dos desvios, frequências):

{{pt: F_descritiva.resultados("_valores", "_metodo")}}

A tabela `htmDescritiva` (controlo *Texto HTML*) aplica esta fórmula a todos os dados («Total») e, se for
escolhida uma variável de agrupamento, a cada grupo (`ForAll` sobre os valores distintos do grupo), e mostra
uma coluna por grupo.

## 3. Frequências e gráficos (ecrã `scrFrequencias`)

### 3.1 Definições

Para cada valor (ou classe) i, com n observações no total:

* **nᵢ** — frequência absoluta (n.º de observações iguais ao valor ou dentro da classe);
* **fᵢ = nᵢ / n** — frequência relativa (também em %);
* **Nᵢ = n₁ + … + nᵢ** — frequência absoluta acumulada;
* **Fᵢ = Nᵢ / n** — frequência relativa acumulada.

### 3.2 Dados discretos e categóricos

Os valores distintos obtêm-se com `Distinct`, ordenados com `Sort`, e cada frequência com `CountIf`. As
acumuladas somam as primeiras i linhas (`Sum(FirstN(_t; i); ni)`):

{{pt: F_frequencias._acumular("_base")}}

### 3.3 Dados agrupados em classes

* **N.º de classes** — por omissão a **regra de Sturges**: k = ⌈1 + log₂ n⌉ (por exemplo n = 20 → k = 6).
* **Início** — por omissão o mínimo da amostra.
* **Amplitude** — por omissão h = (máximo − início) / k, para a última classe terminar no máximo.
* Classes **[Lᵢ ; Lᵢ₊₁[** fechadas à esquerda e abertas à direita; a última é fechada dos dois lados para
  incluir o máximo. (O separador «;» evita confusão com a vírgula decimal.)

Cada valor x é atribuído à classe i = ⌊(x − início) / h⌋ + 1 (com uma pequena tolerância de 10⁻⁹ para que os
valores exatamente sobre um limite não «caiam» na classe anterior por erros de arredondamento). Os valores que
ficam antes do início ou depois da última classe são contados e assinalados com um aviso.

Fórmula completa (devolve as linhas da tabela e os parâmetros usados):

{{pt: F_frequencias.tabela()}}

### 3.4 Gráficos em SVG

O controlo **Imagem** aceita um *URI de dados*: `"data:image/svg+xml;utf8," & EncodeUrl(<texto SVG>)`. O texto
SVG é construído com `Concat` (uma barra por linha da tabela). Duas precauções:

* as **coordenadas** são escritas com `Text(…; "[$-en-US]0.00"; "en-US")`, para terem sempre ponto decimal
  (o SVG não aceita vírgula), mesmo num computador em pt-PT;
* os **nomes** escritos pelos alunos passam por `Substitute` para escapar `&`, `<` e `>`.

O eixo vertical usa um passo «redondo» (1, 2 ou 5 × 10ᵐ):

{{pt: F_graficos.passo_bonito("_mx / 5")}}

* **Histograma** (dados em classes): retângulos contíguos com largura igual à amplitude da classe e altura
  proporcional a nᵢ.
* **Diagrama de barras** (dados discretos ou categóricos): barras separadas, uma por valor/categoria.

Fórmula do histograma:

{{pt: F_graficos.histograma("_F", "_titulo", "_rotulo")}}

## 4. Correlação e regressão linear simples (ecrã `scrRegressao`)

### 4.1 Pares de valores

Só entram as observações com **x e y preenchidos** (eliminação por pares):

{{pt: F_regressao.pares("_kx", "_ky")}}

### 4.2 Fórmulas

Com x̄ e ȳ as médias dos n pares:

| Medida | Fórmula |
|---|---|
| Somas de quadrados e de produtos | Sxx = Σ(xᵢ − x̄)², Syy = Σ(yᵢ − ȳ)², Sxy = Σ(xᵢ − x̄)(yᵢ − ȳ) |
| Covariância amostral | sₓᵧ = Sxy / (n − 1) |
| Coeficiente de correlação de Pearson | r = Sxy / √(Sxx · Syy), com −1 ≤ r ≤ 1 |
| Coeficiente de determinação | R² = r² (proporção da variabilidade de y explicada pela reta) |
| Declive da reta dos mínimos quadrados | b = Sxy / Sxx |
| Ordenada na origem | a = ȳ − b · x̄ |
| Equação e previsão | ŷ = a + b · x |

Casos não definidos (a app mostra `n.d.` e uma explicação): n < 2; todos os x iguais (Sxx = 0: não há reta);
todos os y iguais (Syy = 0: a reta é horizontal, b = 0, mas r não está definido).

As somas calculam-se **a partir dos desvios em relação à média** (método de duas passagens), que é
numericamente mais estável do que a fórmula Σxᵢyᵢ − n·x̄·ȳ quando os valores são grandes.

{{pt: F_regressao.resultados()}}

A previsão avisa quando há **extrapolação** (x fora do intervalo dos x observados).

### 4.3 Diagrama de dispersão com a reta

Os eixos usam passos «redondos» e uma margem de 4 %. Atenção a um pormenor do Power Fx: `RoundDown` e
`RoundUp` arredondam **em direção a zero** (`RoundDown(-2,5; 0)` = −2), por isso para o «chão» de um número
negativo usa-se `Int` (`Int(-2,5)` = −3) e para o «teto» `-Int(-x)`:

{{pt: "// início e fim do eixo dos x, múltiplos do passo _xp\n{_x0: _xp * Int((_minX - 0.04 * _xd) / _xp + 1E-9),\n _x1: -_xp * Int(-(_maxX + 0.04 * _xd) / _xp + 1E-9)}"}}

A reta é desenhada de um lado ao outro do gráfico e recortada à área dos dados com um `clipPath` SVG.

## 5. Inferência (ecrãs `scrTestesT`, `scrAnova`, `scrQuiQuadrado`)

### 5.1 Regra de decisão

Em todos os testes: **rejeita-se H₀ quando p ≤ α**, com α escolhido pelo aluno (0,10; 0,05; 0,01; 0,001). A app
escreve a decisão e uma conclusão por extenso no contexto dos dados. O nível α lê-se da lista pendente:

{{pt: F_inferencia.alfa("drpTtAlfa")}}

### 5.2 Valores de p por integração numérica

O Power Fx não tem funções de distribuição (nem a função Gama). Os valores de p calculam-se com **integração
numérica** em Power Fx puro, com `Sequence` (nós) e `Sum` (soma pesada). Detalhes e precisão medida em
`docs/precisao-valores-p.md` (erro máximo 2,3×10⁻⁷; nenhum valor difere do scipy na 4.ª casa decimal).

**Ideia matemática.** Para a distribuição F(d₁, d₂), fazendo x = d₁F/(d₁F + d₂) obtém-se uma Beta(d₁/2, d₂/2) e,
com x = sen²θ,

  P(F > f) = ∫ de θ₀ a π/2 de sen^(d₁−1)θ · cos^(d₂−1)θ dθ  ÷  ∫ de 0 a π/2 do mesmo integrando,
  com θ₀ = atan(√(d₁ f / d₂)).

O integrando é limitado (os expoentes são ≥ 0), por isso a regra de Gauss-Legendre é muito precisa. As constantes
(funções Beta/Gama) cancelam-se na razão. Para o qui-quadrado, com u = v²:

  P(χ² > x) = ∫ de √x a ∞ de v^(k−1) e^(−v²/2) dv  ÷  ∫ de 0 a ∞ do mesmo integrando.

Para o t de Student usa-se T² ~ F(1, ν): o p bilateral é P(F(1, ν) > t²); os unilaterais são metade (ou 1 menos
metade), conforme o sinal de t.

**Nós e pesos de Gauss-Legendre** (100 subintervalos × 3 nós; u em ]0, 1[; os pesos somam 1):

{{pt: F_inferencia._nos()}}

**Valor de p da distribuição F** (`_f`, `_d1`, `_d2`):

{{pt: F_inferencia.p_f("_estatisticaF", "_gl1", "_gl2")}}

**Valor de p do qui-quadrado**:

{{pt: F_inferencia.p_qui("_estatisticaQui2", "_gl")}}

**Valor de p do teste t** segundo a hipótese alternativa (1 bilateral, 2 à esquerda, 3 à direita):

{{pt: F_inferencia.p_t("_t", "_gl", "_alt")}}

### 5.3 Testes t

| Teste | Estatística | Graus de liberdade |
|---|---|---|
| Uma amostra (H₀: μ = μ₀) | t = (x̄ − μ₀) / (s / √n) | n − 1 |
| Duas amostras independentes, variâncias iguais (H₀: μ₁ − μ₂ = Δ₀) | t = (x̄₁ − x̄₂ − Δ₀) / (sₚ √(1/n₁ + 1/n₂)), sₚ² = [(n₁ − 1)s₁² + (n₂ − 1)s₂²] / (n₁ + n₂ − 2) | n₁ + n₂ − 2 |
| Duas amostras independentes, Welch (variâncias diferentes) | t = (x̄₁ − x̄₂ − Δ₀) / √(s₁²/n₁ + s₂²/n₂) | (s₁²/n₁ + s₂²/n₂)² / [(s₁²/n₁)²/(n₁ − 1) + (s₂²/n₂)²/(n₂ − 1)] |
| Emparelhadas (H₀: μ_D = Δ₀, D = X − Y) | t = (d̄ − Δ₀) / (s_D / √n) | n − 1 (n = n.º de pares completos) |

As duas amostras independentes podem vir de **uma variável numérica + uma variável de grupo** (escolhem-se os dois
grupos) ou de **duas colunas numéricas**. Fórmula completa (registo com todos os resultados):

{{pt: F_inferencia.teste_t()}}

### 5.4 ANOVA a um fator

Com k grupos, nᵢ observações e média x̄ᵢ no grupo i, N = Σnᵢ e x̄ a média global:

| Fonte | SQ | gl | QM | F |
|---|---|---|---|---|
| Entre grupos | SQE = Σ nᵢ (x̄ᵢ − x̄)² | k − 1 | QME = SQE / (k − 1) | F = QME / QMD |
| Dentro dos grupos | SQD = Σᵢ Σⱼ (xᵢⱼ − x̄ᵢ)² | N − k | QMD = SQD / (N − k) | |
| Total | SQT = SQE + SQD | N − 1 | | |

p = P(F(k − 1, N − k) ≥ F). A app mostra também η² = SQE / SQT.

{{pt: F_inferencia.anova()}}

### 5.5 Qui-quadrado

* **Aderência**: k categorias com frequências observadas Oᵢ e proporções esperadas pᵢ (iguais ou indicadas pelo
  aluno; são normalizadas para somar 1). Eᵢ = n·pᵢ, χ² = Σ (Oᵢ − Eᵢ)² / Eᵢ, gl = k − 1.
* **Independência**: tabela r × c, Eᵢⱼ = Rᵢ·Cⱼ / N (totais de linha e coluna), χ² = Σ (Oᵢⱼ − Eᵢⱼ)² / Eᵢⱼ,
  gl = (r − 1)(c − 1). Não se aplica a correção de continuidade de Yates.
* **Regra de Cochran** (aviso): no máximo 20 % das células com E < 5 e nenhuma com E < 1.

As frequências podem vir das variáveis da tabela de dados (as variáveis numéricas são tratadas como categorias)
ou de uma **tabela colada do Excel**. Na tabela colada, a 1.ª linha é cabeçalho se tiver texto a partir da
2.ª coluna e a 1.ª coluna tem os nomes das linhas se tiver texto:

{{pt: F_inferencia.matriz_colada()}}

Proporções esperadas escritas pelo aluno (separadas por `;`, tabulação ou mudança de linha):

{{pt: F_inferencia._props_indicadas()}}

Fórmula completa do teste:

{{pt: F_inferencia.qui_quadrado()}}

### 5.6 Teste de significância do coeficiente de correlação (ecrã `scrRegressao`)

H₀: ρ = 0 contra H₁: ρ ≠ 0, com t = r √(n − 2) / √(1 − r²) e n − 2 graus de liberdade (precisa de n ≥ 3).
