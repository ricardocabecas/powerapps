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
