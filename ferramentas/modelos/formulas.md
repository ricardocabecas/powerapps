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
