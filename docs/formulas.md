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

```powerfx
IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(Self.Text); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank())
```

Um texto é **inválido** quando não está vazio e a conversão dá erro:

```powerfx
(Len(Trim(Self.Text)) > 0 && IsError(Value(Substitute(Substitute(Substitute(Substitute(Trim(Self.Text); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US")))
```

Exemplos: `1,5` → 1,5 · `1.5` → 1,5 · `1 234,5` → 1234,5 · `5%` → 0,05 · `1,2,3` → inválido · `abc` → inválido.

### Formatação dos resultados (vírgula decimal)

Todos os números são mostrados com 4 casas decimais, vírgula decimal e espaço como separador de milhares.
Um valor em branco mostra `n.d.` (não definido, por exemplo a variância com n = 1):

```powerfx
With({_v: _valor}; If(IsBlank(_v); "n.d."; Text(If(Abs(_v) < 5e-05; 0; _v); "[$-en-US]#,##0.0000"; "pt-PT")))
```

## 1. Entrada de dados (ecrã `scrDados`)

### 1.1 Inicialização (`scrDados.OnVisible`)

Na primeira abertura cria `varNomes`, a coleção `colDados` com dados de exemplo (20 estudantes fictícios) e
as coleções auxiliares da colagem. `ClearCollect` seguido de `Clear` serve só para o Power Apps ficar a
conhecer o tipo das colunas.

```powerfx
// Inicialização: corre apenas na primeira vez que o ecrã é aberto
If(!varIniciado;
    Set(varIniciado; true);;
    // Nomes das variáveis (podem ser alterados no cabeçalho da tabela)
    Set(varNomes; {N1: "Altura (cm)"; N2: "Peso (kg)"; N3: "Nota (0-20)"; C1: "Sexo"; C2: "Turma"});;
    // Coleção com os dados: N1-N3 numéricas, C1-C2 categóricas (grupo)
    ClearCollect(colDados; Table(
        {Id: 1; N1: 165; N2: 58,5; N3: 14; C1: "F"; C2: "A"};
        {Id: 2; N1: 178; N2: 72; N3: 12; C1: "M"; C2: "A"};
        {Id: 3; N1: 160; N2: 52,3; N3: 16; C1: "F"; C2: "B"};
        {Id: 4; N1: 182; N2: 80,1; N3: 11; C1: "M"; C2: "B"};
        {Id: 5; N1: 170; N2: 65,4; N3: 13; C1: "M"; C2: "C"};
        {Id: 6; N1: 158; N2: 49,8; N3: 17; C1: "F"; C2: "A"};
        {Id: 7; N1: 175; N2: 70,2; N3: 10; C1: "M"; C2: "C"};
        {Id: 8; N1: 168; N2: 61; N3: 15; C1: "F"; C2: "B"};
        {Id: 9; N1: 185; N2: 85,6; N3: 9; C1: "M"; C2: "A"};
        {Id: 10; N1: 162; N2: 55,1; N3: 18; C1: "F"; C2: "C"};
        {Id: 11; N1: 172; N2: 68,3; N3: 12; C1: "M"; C2: "B"};
        {Id: 12; N1: 166; N2: 60,2; N3: 14; C1: "F"; C2: "A"};
        {Id: 13; N1: 180; N2: 77,5; N3: 11; C1: "M"; C2: "C"};
        {Id: 14; N1: 155; N2: 48; N3: 16; C1: "F"; C2: "B"};
        {Id: 15; N1: 174; N2: 69,9; N3: 13; C1: "M"; C2: "A"};
        {Id: 16; N1: 163; N2: 57,4; N3: 15; C1: "F"; C2: "C"};
        {Id: 17; N1: 177; N2: 74,8; N3: 10; C1: "M"; C2: "B"};
        {Id: 18; N1: 169; N2: 63,1; N3: 14; C1: "F"; C2: "C"};
        {Id: 19; N1: 171; N2: 66,7; N3: 12; C1: "M"; C2: "A"};
        {Id: 20; N1: 159; N2: 51,6; N3: 17; C1: "F"; C2: "B"}
    ));;
    // Coleções auxiliares da colagem (ficam vazias até carregar em Analisar)
    ClearCollect(colColagem; {Linha: 0; Celulas: Table({Texto: ""}); NCel: 0});;
    Clear(colColagem);;
    ClearCollect(colColunas; {Col: 0; Topo: ""; TopoNumerico: false; NNaoVazias: 0; NNumeros: 0; Numerica: false; Rotulo: ""});;
    Clear(colColunas)
)
```

### 1.2 Galeria editável

A galeria `galDados` tem `Items = colDados`. Cada célula numérica é uma caixa de texto:

* `Default` mostra o número com vírgula decimal e só as casas necessárias:

```powerfx
With({_v: ThisItem.N1}; If(IsBlank(_v); ""; If(_v = Int(_v); Text(_v; "[$-en-US]0"; "pt-PT"); Text(_v; "[$-en-US]0.##########"; "pt-PT"))))
```

* `OnChange` converte o que o aluno escreveu e grava com `Patch` na linha certa (procurada pelo `Id`); se o
  texto não for um número aparece um aviso:

```powerfx
// Converte o texto (vírgula ou ponto decimal) e grava na coleção
Patch(colDados; LookUp(colDados; Id = ThisItem.Id); {N1: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(Self.Text); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank())});;
If((Len(Trim(Self.Text)) > 0 && IsError(Value(Substitute(Substitute(Substitute(Substitute(Trim(Self.Text); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US")));
    Notify("«" & Self.Text & "» não é um número válido: a célula ficou vazia."; NotificationType.Warning))
```

* `BorderColor` fica vermelho enquanto o texto for inválido.

O botão ✕ apaga a linha e volta a numerar as linhas de 1 a n (através de uma coleção temporária, porque não se
pode alterar uma coleção dentro de um `ForAll` que a percorre):

```powerfx
RemoveIf(colDados; Id = ThisItem.Id);;
ClearCollect(colTemp; ForAll(Sequence(CountRows(colDados)) As _i; Patch(Index(colDados; _i.Value); {Id: _i.Value})));;
ClearCollect(colDados; colTemp);;
Clear(colTemp)
```

### 1.3 Colar colunas do Excel

Quando se copiam células no Excel, a área de transferência recebe texto em que **as linhas são separadas por
mudança de linha** (`Char(10)`, precedido de `Char(13)` no Windows) e **as colunas por tabulação** (`Char(9)`).

**Passo 1 — partir o texto em linhas e células** (botão *Analisar*, coleção `colColagem`). `Split` parte o texto,
`Trim` limpa os espaços e as linhas sem nenhuma célula preenchida são ignoradas:

```powerfx
With(
    // Retira os retornos de carro (Char(13)) do Windows e parte o texto em linhas
    {_linhas: Split(Substitute(txtColar.Text; Char(13); ""); Char(10))};
    Filter(
        ForAll(Sequence(CountRows(_linhas)) As _i;
            With(
                // Parte cada linha nas tabulações (colunas do Excel) e limpa os espaços
                {_cel: ForAll(Split(Index(_linhas; _i.Value).Value; Char(9)) As _c;
                    {Texto: Trim(Substitute(_c.Value; UniChar(160); " "))})};
                {Linha: _i.Value; Celulas: _cel; NCel: CountRows(Filter(_cel; Texto <> ""))}
            )
        );
        // Ignora linhas vazias (ou só com tabulações/espaços)
        NCel > 0
    )
)
```

**Passo 2 — caracterizar as colunas** (coleção `colColunas`). Uma coluna é considerada numérica se pelo menos
metade das células preenchidas (a partir da 2.ª linha) forem números:

```powerfx
With(
    {_m: CountRows(colColagem); _k: Coalesce(Max(colColagem; CountRows(Celulas)); 0)};
    With(
        {_corpo: If(_m >= 2; LastN(colColagem; _m - 1); colColagem); _topo: First(colColagem)};
        ForAll(Sequence(_k) As _j;
            With(
                {_txt: ForAll(_corpo As _r;
                    {T: If(_j.Value <= CountRows(_r.Celulas); Index(_r.Celulas; _j.Value).Texto; "")});
                 _t1: If(_j.Value <= CountRows(_topo.Celulas); Index(_topo.Celulas; _j.Value).Texto; "")};
                With(
                    {_nv: CountRows(Filter(_txt; T <> ""));
                     _nn: CountRows(Filter(_txt; T <> "" && !IsBlank(IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(T); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()))))};
                    {Col: _j.Value; Topo: _t1; TopoNumerico: !IsBlank(IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_t1); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()));
                     NNaoVazias: _nv; NNumeros: _nn; Numerica: _nn > 0 && _nn * 2 >= _nv;
                     Rotulo: _j.Value & " · " & Left(_t1; 18)}
                )
            )
        )
    )
)
```

**Passo 3 — cabeçalho.** No modo *Automático*, a 1.ª linha é cabeçalho quando alguma coluna numérica tem
texto não numérico na 1.ª linha:

```powerfx
Switch(drpCabecalho.Selected.Value; "Sim"; true; "Não"; false; CountRows(colColagem) >= 2 && CountRows(Filter(colColunas; Numerica && Topo <> "" && !TopoNumerico)) > 0)
```

**Passo 4 — escolher a coluna de origem de cada variável.** As listas `drpMapN1`…`drpMapC2` mostram
`n.º · 1.ª célula`; por omissão as colunas numéricas vão para `N1`, `N2`, `N3` e as de texto para `C1`, `C2`.
Exemplo para `N1`:

```powerfx
With({_f: Filter(colColunas; Numerica)}; If(CountRows(_f) >= 1; Index(_f; 1).Rotulo; "—"))
```

**Passo 5 — importar.** Constrói-se um registo com as linhas prontas para `colDados`, a lista de valores
inválidos (que ficam em branco) e os nomes vindos do cabeçalho:

```powerfx
With(
    // Opções escolhidas: cabeçalho e coluna de origem de cada variável
    {_cab: Switch(drpCabecalho.Selected.Value; "Sim"; true; "Não"; false; CountRows(colColagem) >= 2 && CountRows(Filter(colColunas; Numerica && Topo <> "" && !TopoNumerico)) > 0);
      _jN1: IfError(Value(First(Split(drpMapN1.Selected.Value; " ")).Value; "en-US"); 0);
      _jN2: IfError(Value(First(Split(drpMapN2.Selected.Value; " ")).Value; "en-US"); 0);
      _jN3: IfError(Value(First(Split(drpMapN3.Selected.Value; " ")).Value; "en-US"); 0);
      _jC1: IfError(Value(First(Split(drpMapC1.Selected.Value; " ")).Value; "en-US"); 0);
      _jC2: IfError(Value(First(Split(drpMapC2.Selected.Value; " ")).Value; "en-US"); 0)};
    With(
        {_corpo: If(_cab; LastN(colColagem; CountRows(colColagem) - 1); colColagem);
          // Se houver cabeçalho, os nomes das variáveis vêm da 1.ª linha
          _nomes: With({_c1: First(colColagem)}; {N1: If(_cab && _jN1 > 0; If(_jN1 >= 1 && _jN1 <= CountRows(_c1.Celulas); Index(_c1.Celulas; _jN1).Texto; ""); varNomes.N1); N2: If(_cab && _jN2 > 0; If(_jN2 >= 1 && _jN2 <= CountRows(_c1.Celulas); Index(_c1.Celulas; _jN2).Texto; ""); varNomes.N2); N3: If(_cab && _jN3 > 0; If(_jN3 >= 1 && _jN3 <= CountRows(_c1.Celulas); Index(_c1.Celulas; _jN3).Texto; ""); varNomes.N3); C1: If(_cab && _jC1 > 0; If(_jC1 >= 1 && _jC1 <= CountRows(_c1.Celulas); Index(_c1.Celulas; _jC1).Texto; ""); varNomes.C1); C2: If(_cab && _jC2 > 0; If(_jC2 >= 1 && _jC2 <= CountRows(_c1.Celulas); Index(_c1.Celulas; _jC2).Texto; ""); varNomes.C2)})};
        With(
            {_reg: ForAll(Sequence(CountRows(_corpo)) As _i;
                With({_r: Index(_corpo; _i.Value)};
                    With({_tN1: If(_jN1 >= 1 && _jN1 <= CountRows(_r.Celulas); Index(_r.Celulas; _jN1).Texto; ""); _tN2: If(_jN2 >= 1 && _jN2 <= CountRows(_r.Celulas); Index(_r.Celulas; _jN2).Texto; ""); _tN3: If(_jN3 >= 1 && _jN3 <= CountRows(_r.Celulas); Index(_r.Celulas; _jN3).Texto; ""); _tC1: If(_jC1 >= 1 && _jC1 <= CountRows(_r.Celulas); Index(_r.Celulas; _jC1).Texto; ""); _tC2: If(_jC2 >= 1 && _jC2 <= CountRows(_r.Celulas); Index(_r.Celulas; _jC2).Texto; "")};
                        {Id: 0 + _i.Value; N1: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_tN1); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()); N2: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_tN2); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()); N3: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_tN3); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()); C1: _tC1; C2: _tC2;
                         Linha: _r.Linha; _IN1: (Len(Trim(_tN1)) > 0 && IsError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_tN1); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"))); _IN2: (Len(Trim(_tN2)) > 0 && IsError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_tN2); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"))); _IN3: (Len(Trim(_tN3)) > 0 && IsError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_tN3); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"))); _TN1: _tN1; _TN2: _tN2; _TN3: _tN3}
                    )
                )
            )};
            {
                // Registos prontos a juntar a colDados
                Linhas: ForAll(_reg; {Id: Id; N1: N1; N2: N2; N3: N3; C1: C1; C2: C2});
                // Valores não numéricos em colunas numéricas (ficam em branco)
                Invalidos: Sort(Table(
            ForAll(Filter(_reg; _IN1) As _x; {Linha: _x.Linha; Variavel: _nomes.N1; Texto: _x._TN1});
            ForAll(Filter(_reg; _IN2) As _x; {Linha: _x.Linha; Variavel: _nomes.N2; Texto: _x._TN2});
            ForAll(Filter(_reg; _IN3) As _x; {Linha: _x.Linha; Variavel: _nomes.N3; Texto: _x._TN3})
                ); Linha);
                Cabecalho: _cab;
                Nomes: _nomes
            }
        )
    )
)
```

O botão *Importar (substituir dados)* usa esse registo assim:

```powerfx
// Substitui todos os dados pelos dados colados
Set(varImportacao; /* registo de importação (ver acima) */);;
ClearCollect(colDados; varImportacao.Linhas);;
If(varImportacao.Cabecalho; Set(varNomes; varImportacao.Nomes));;
Notify(
    "Importadas " & CountRows(varImportacao.Linhas) & " linhas." &
    If(CountRows(varImportacao.Invalidos) > 0;
        " Atenção: " & CountRows(varImportacao.Invalidos) & " valor(es) inválido(s) ficaram em branco."; "");
    If(CountRows(varImportacao.Invalidos) > 0; NotificationType.Warning; NotificationType.Success)
)
```

O texto de diagnóstico (`lblDiagnostico`) usa o mesmo registo para mostrar, **antes de importar**, quantas
linhas e colunas foram detetadas, se a 1.ª linha é cabeçalho e quais os valores inválidos (com o n.º da linha
no texto colado, para os encontrar no Excel).

## 2. Estatística descritiva (ecrã `scrDescritiva`)

### 2.1 Escolha da variável e dos grupos

As listas pendentes mostram os nomes dados pelos alunos (`[varNomes.N1; varNomes.N2; varNomes.N3]`). O nome
escolhido é convertido no índice da variável (1, 2 ou 3) com `Switch`:

```powerfx
Switch(drpDesVar.Selected.Value; varNomes.N1; 1; varNomes.N2; 2; varNomes.N3; 3; 1)
```

Os valores da variável (e, se se pedir agrupamento, o grupo de cada observação) obtêm-se de `colDados`,
ignorando as células vazias:

```powerfx
Filter(ForAll(colDados As _d; {x: Switch(_k; 1; _d.N1; 2; _d.N2; _d.N3); g: Switch(_kg; 1; _d.C1; _d.C2)}); !IsBlank(x))
```

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

```powerfx
Switch(_metodo; 1; With({_h: (_n - 1) * 0,25 + 1}; With({_b: RoundDown(_h; 0)}; Index(_s; _b).x + (_h - _b) * (Index(_s; Min(_b + 1; _n)).x - Index(_s; _b).x))); 2; With({_h: Min(Max((_n + 1) * 0,25; 1); _n)}; With({_b: RoundDown(_h; 0)}; Index(_s; _b).x + (_h - _b) * (Index(_s; Min(_b + 1; _n)).x - Index(_s; _b).x))); With({_m: RoundDown(_n / 2; 0)}; If(_m = 0; First(_s).x; If(Mod(_m; 2) = 1; Index(_s; 0 + (_m + 1) / 2).x; (Index(_s; 0 + _m / 2).x + Index(_s; 0 + _m / 2 + 1).x) / 2))))
```

### 2.3 Fórmula completa

Todas as medidas são calculadas num só registo. `With` encadeados guardam os resultados intermédios
(amostra ordenada, n, soma, média, soma dos quadrados dos desvios, frequências):

```powerfx
With(
    // Amostra ordenada por ordem crescente e dimensão
    {_s: Sort(_valores; x)};
    With({_n: CountRows(_s); _metodo: _metodo};
    With({_soma: Sum(_s; x); _min: First(_s).x; _max: Last(_s).x};
    With({_media: If(_n > 0; _soma / _n)};
    With(
        // Soma dos quadrados dos desvios em relação à média e frequência de cada valor (para a moda)
        {_sq: Sum(_s; Power(x - _media; 2));
         _freq: ForAll(Distinct(_s; x) As _d; {v: _d.Value; f: CountIf(_s; x = _d.Value)})};
    With({_fmax: Max(_freq; f); _modas: Filter(_freq; f = Max(_freq; f))};
    {
        n: _n;
        soma: If(_n > 0; _soma);
        media: _media;
        // Mediana: valor central (n ímpar) ou média dos dois centrais (n par)
        mediana: If(_n > 0; If(Mod(_n; 2) = 1; Index(_s; 0 + (_n + 1) / 2).x; (Index(_s; 0 + _n / 2).x + Index(_s; 0 + _n / 2 + 1).x) / 2));
        moda: If(_n = 0; "n.d.";
            If(_n > 1 && CountRows(_modas) = CountRows(_freq);
                "não existe (amodal)";
                Concat(FirstN(_modas; 5); With({_v: v}; If(IsBlank(_v); ""; If(_v = Int(_v); Text(_v; "[$-en-US]0"; "pt-PT"); Text(_v; "[$-en-US]0.##########"; "pt-PT")))); "; ") &
                If(CountRows(_modas) > 5; "; …"; "") &
                If(CountRows(_modas) = 2; " (bimodal)"; CountRows(_modas) > 2; " (multimodal)"; "") &
                " — freq. " & _fmax));
        minimo: _min;
        maximo: _max;
        amplitude: If(_n > 0; _max - _min);
        q1: If(_n > 0; Switch(_metodo; 1; With({_h: (_n - 1) * 0,25 + 1}; With({_b: RoundDown(_h; 0)}; Index(_s; _b).x + (_h - _b) * (Index(_s; Min(_b + 1; _n)).x - Index(_s; _b).x))); 2; With({_h: Min(Max((_n + 1) * 0,25; 1); _n)}; With({_b: RoundDown(_h; 0)}; Index(_s; _b).x + (_h - _b) * (Index(_s; Min(_b + 1; _n)).x - Index(_s; _b).x))); With({_m: RoundDown(_n / 2; 0)}; If(_m = 0; First(_s).x; If(Mod(_m; 2) = 1; Index(_s; 0 + (_m + 1) / 2).x; (Index(_s; 0 + _m / 2).x + Index(_s; 0 + _m / 2 + 1).x) / 2)))));
        q3: If(_n > 0; Switch(_metodo; 1; With({_h: (_n - 1) * 0,75 + 1}; With({_b: RoundDown(_h; 0)}; Index(_s; _b).x + (_h - _b) * (Index(_s; Min(_b + 1; _n)).x - Index(_s; _b).x))); 2; With({_h: Min(Max((_n + 1) * 0,75; 1); _n)}; With({_b: RoundDown(_h; 0)}; Index(_s; _b).x + (_h - _b) * (Index(_s; Min(_b + 1; _n)).x - Index(_s; _b).x))); With({_m: RoundDown(_n / 2; 0)}; If(_m = 0; First(_s).x; If(Mod(_m; 2) = 1; Index(_s; (_n - _m) + (_m + 1) / 2).x; (Index(_s; (_n - _m) + _m / 2).x + Index(_s; (_n - _m) + _m / 2 + 1).x) / 2)))));
        // Variância amostral (divisor n − 1) e populacional (divisor n)
        varA: If(_n >= 2; _sq / (_n - 1));
        varP: If(_n >= 1; _sq / _n);
        dpA: If(_n >= 2; Sqrt(_sq / (_n - 1)));
        dpP: If(_n >= 1; Sqrt(_sq / _n));
        // Coeficiente de variação (com o desvio padrão amostral), em %
        cv: If(_n >= 2 && _media <> 0; Sqrt(_sq / (_n - 1)) / Abs(_media) * 100)
    }
    )))))
)
```

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

```powerfx
With({_t: _base; _ntot: Sum(_base; ni)};
        ForAll(Sequence(CountRows(_t)) As _i;
            With({_r: Index(_t; _i.Value); _Ni: Sum(FirstN(_t; _i.Value); ni)};
                {Ordem: _i.Value; Classe: _r.Classe; Centro: _r.Centro; Li: _r.Li; Ls: _r.Ls;
                 ni: _r.ni; fi: _r.ni / _ntot; Ni: _Ni; Fi: _Ni / _ntot})))
```

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

```powerfx
With(
    {_kv: Switch(drpFreVar.Selected.Value; varNomes.N1; 1; varNomes.N2; 2; varNomes.N3; 3; varNomes.C1; 4; varNomes.C2; 5; 1)};
    With(
        {_tipo: If(_kv >= 4; 1; If(drpFreTipo.Selected.Value = "Classes (dados agrupados)"; 2; 1));
         // Valores numéricos (variáveis 1 a 3) e categóricos (4 e 5), sem células vazias
         _x: Filter(ForAll(colDados As _d; {x: Switch(_kv; 1; _d.N1; 2; _d.N2; 3; _d.N3; Blank())}); !IsBlank(x));
         _g: Filter(ForAll(colDados As _d; {g: Switch(_kv; 4; _d.C1; 5; _d.C2; "")}); !IsBlank(g))};
        With(
            {_n: If(_kv >= 4; CountRows(_g); CountRows(_x)); _min: Min(_x; x); _max: Max(_x; x)};
            With(
                // Classes: k pela regra de Sturges (ou o valor escrito), início no mínimo e amplitude (máx − início)/k
                {_kS: If(_n > 0; RoundUp(1 + Log(_n; 2) - 1E-9; 0); 0);
                 _kU: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(txtFreK.Text); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()); _aU: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(txtFreInicio.Text); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()); _hU: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(txtFreAmplitude.Text); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank())};
                With(
                    {_k: If(!IsBlank(_kU) && _kU >= 1; Min(RoundDown(_kU; 0); 50); Max(_kS; 1));
                     _a: Coalesce(_aU; _min)};
                    With(
                        {_h: If(!IsBlank(_hU) && _hU > 0; _hU; If(_max > _a; (_max - _a) / _k; 1))};
                        With(
                            // Classe de cada valor: [Li ; Ls[ (a última é fechada à direita)
                            {_cls: ForAll(_x As _v; {c: With({_z: (_v.x - _a) / _h};
                                If(_z < -1E-9; 0; Min(RoundDown(_z + 1E-9; 0) + 1; If(_z <= _k + 1E-9; _k; _k + 1))))})};
                            {
                                Tipo: _tipo; n: _n; k: _k; kSturges: _kS; a: _a; h: _h; Minimo: _min; Maximo: _max;
                                Fora: If(_tipo = 2; CountRows(Filter(_cls; c < 1 || c > _k)); 0);
                                Linhas: If(
                                    _n = 0; FirstN(With({_t: Table({Classe: ""; Centro: 0; Li: 0; Ls: 0; ni: 0}); _ntot: Sum(Table({Classe: ""; Centro: 0; Li: 0; Ls: 0; ni: 0}); ni)};
        ForAll(Sequence(CountRows(_t)) As _i;
            With({_r: Index(_t; _i.Value); _Ni: Sum(FirstN(_t; _i.Value); ni)};
                {Ordem: _i.Value; Classe: _r.Classe; Centro: _r.Centro; Li: _r.Li; Ls: _r.Ls;
                 ni: _r.ni; fi: _r.ni / _ntot; Ni: _Ni; Fi: _Ni / _ntot}))); 0);
                                    _tipo = 2;
                                    With({_t: ForAll(Sequence(_k) As _c;
                                            {Classe: "[" & With({_r: Round(_a + (_c.Value - 1) * _h; 4)}; If(_r = Int(_r); Text(_r; "[$-en-US]0"; "pt-PT"); Text(_r; "[$-en-US]0.####"; "pt-PT"))) & " ; " & With({_r: Round(_a + _c.Value * _h; 4)}; If(_r = Int(_r); Text(_r; "[$-en-US]0"; "pt-PT"); Text(_r; "[$-en-US]0.####"; "pt-PT"))) & If(_c.Value = _k; "]"; "[");
                                             Centro: _a + (_c.Value - 0,5) * _h; Li: _a + (_c.Value - 1) * _h; Ls: _a + _c.Value * _h;
                                             ni: CountIf(_cls; c = _c.Value)}); _ntot: Sum(ForAll(Sequence(_k) As _c;
                                            {Classe: "[" & With({_r: Round(_a + (_c.Value - 1) * _h; 4)}; If(_r = Int(_r); Text(_r; "[$-en-US]0"; "pt-PT"); Text(_r; "[$-en-US]0.####"; "pt-PT"))) & " ; " & With({_r: Round(_a + _c.Value * _h; 4)}; If(_r = Int(_r); Text(_r; "[$-en-US]0"; "pt-PT"); Text(_r; "[$-en-US]0.####"; "pt-PT"))) & If(_c.Value = _k; "]"; "[");
                                             Centro: _a + (_c.Value - 0,5) * _h; Li: _a + (_c.Value - 1) * _h; Ls: _a + _c.Value * _h;
                                             ni: CountIf(_cls; c = _c.Value)}); ni)};
        ForAll(Sequence(CountRows(_t)) As _i;
            With({_r: Index(_t; _i.Value); _Ni: Sum(FirstN(_t; _i.Value); ni)};
                {Ordem: _i.Value; Classe: _r.Classe; Centro: _r.Centro; Li: _r.Li; Ls: _r.Ls;
                 ni: _r.ni; fi: _r.ni / _ntot; Ni: _Ni; Fi: _Ni / _ntot})));
                                    _kv >= 4;
                                    With({_t: ForAll(Sort(Distinct(_g; g); Value) As _d;
                                            {Classe: _d.Value; Centro: Blank(); Li: Blank(); Ls: Blank(); ni: CountIf(_g; g = _d.Value)}); _ntot: Sum(ForAll(Sort(Distinct(_g; g); Value) As _d;
                                            {Classe: _d.Value; Centro: Blank(); Li: Blank(); Ls: Blank(); ni: CountIf(_g; g = _d.Value)}); ni)};
        ForAll(Sequence(CountRows(_t)) As _i;
            With({_r: Index(_t; _i.Value); _Ni: Sum(FirstN(_t; _i.Value); ni)};
                {Ordem: _i.Value; Classe: _r.Classe; Centro: _r.Centro; Li: _r.Li; Ls: _r.Ls;
                 ni: _r.ni; fi: _r.ni / _ntot; Ni: _Ni; Fi: _Ni / _ntot})));
                                    With({_t: ForAll(Sort(Distinct(_x; x); Value) As _d;
                                            {Classe: With({_v: _d.Value}; If(IsBlank(_v); ""; If(_v = Int(_v); Text(_v; "[$-en-US]0"; "pt-PT"); Text(_v; "[$-en-US]0.##########"; "pt-PT")))); Centro: _d.Value; Li: Blank(); Ls: Blank();
                                             ni: CountIf(_x; x = _d.Value)}); _ntot: Sum(ForAll(Sort(Distinct(_x; x); Value) As _d;
                                            {Classe: With({_v: _d.Value}; If(IsBlank(_v); ""; If(_v = Int(_v); Text(_v; "[$-en-US]0"; "pt-PT"); Text(_v; "[$-en-US]0.##########"; "pt-PT")))); Centro: _d.Value; Li: Blank(); Ls: Blank();
                                             ni: CountIf(_x; x = _d.Value)}); ni)};
        ForAll(Sequence(CountRows(_t)) As _i;
            With({_r: Index(_t; _i.Value); _Ni: Sum(FirstN(_t; _i.Value); ni)};
                {Ordem: _i.Value; Classe: _r.Classe; Centro: _r.Centro; Li: _r.Li; Ls: _r.Ls;
                 ni: _r.ni; fi: _r.ni / _ntot; Ni: _Ni; Fi: _Ni / _ntot})))
                                )
                            }
                        )
                    )
                )
            )
        )
    )
)
```

### 3.4 Gráficos em SVG

O controlo **Imagem** aceita um *URI de dados*: `"data:image/svg+xml;utf8," & EncodeUrl(<texto SVG>)`. O texto
SVG é construído com `Concat` (uma barra por linha da tabela). Duas precauções:

* as **coordenadas** são escritas com `Text(…; "[$-en-US]0.00"; "en-US")`, para terem sempre ponto decimal
  (o SVG não aceita vírgula), mesmo num computador em pt-PT;
* os **nomes** escritos pelos alunos passam por `Substitute` para escapar `&`, `<` e `>`.

O eixo vertical usa um passo «redondo» (1, 2 ou 5 × 10ᵐ):

```powerfx
With({_e: Power(10; Int(Log(_mx / 5; 10) + 1E-9))}; With({_f: _mx / 5 / _e}; If(_f <= 1; 1; _f <= 2; 2; _f <= 5; 5; 10) * _e))
```

* **Histograma** (dados em classes): retângulos contíguos com largura igual à amplitude da classe e altura
  proporcional a nᵢ.
* **Diagrama de barras** (dados discretos ou categóricos): barras separadas, uma por valor/categoria.

Fórmula do histograma:

```powerfx
"data:image/svg+xml;utf8," & EncodeUrl(With({_lin: _F.Linhas; _k: CountRows(_F.Linhas)};
    With({_mx: Max(Max(_lin; ni); 1)}; With({_passo: Max(1; With({_e: Power(10; Int(Log(_mx / 5; 10) + 1E-9))}; With({_f: _mx / 5 / _e}; If(_f <= 1; 1; _f <= 2; 2; _f <= 5; 5; 10) * _e)))}; With({_ymax: _passo * RoundUp(_mx * 1,08 / _passo - 1E-9; 0)}; 
    With({_bw: 550 / Max(_k; 1); _salto: RoundUp(_k / 10; 0)};
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 640 400' font-family='Segoe UI, Arial, sans-serif'>" &
    "<rect x='0' y='0' width='640' height='400' fill='white'/>" &
    "<text x='320' y='22' text-anchor='middle' font-size='15' font-weight='600' fill='rgb(33,37,41)'>" & Substitute(Substitute(Substitute(_titulo; "&"; "&amp;"); "<"; "&lt;"); ">"; "&gt;") & "</text>" &
    Concat(Sequence(RoundDown(_ymax / _passo + 1E-9; 0) + 1; 0) As _t;
        With({_y: 330 - _t.Value * _passo / _ymax * 290};
            "<line x1='" & Text(Round(70; 2); "[$-en-US]0.00"; "en-US") & "' y1='" & Text(Round(_y; 2); "[$-en-US]0.00"; "en-US") & "' x2='" & Text(Round(620; 2); "[$-en-US]0.00"; "en-US") & "' y2='" & Text(Round(_y; 2); "[$-en-US]0.00"; "en-US") & "' stroke='rgb(225,229,234)'/>" &
            "<text x='" & Text(Round(62; 2); "[$-en-US]0.00"; "en-US") & "' y='" & Text(Round(_y + 4; 2); "[$-en-US]0.00"; "en-US") & "' text-anchor='end' font-size='11' fill='rgb(90,98,106)'>" & Text(_t.Value * _passo; "[$-en-US]0"; "pt-PT") & "</text>")) &
    "<text transform='translate(18,185) rotate(-90)' text-anchor='middle' font-size='12' fill='rgb(90,98,106)'>Frequência absoluta (nᵢ)</text>" &
    // Barras contíguas: largura = amplitude da classe, altura proporcional a nᵢ
    Concat(Sequence(_k) As _i; With({_r: Index(_lin; _i.Value)};
        With({_hb: _r.ni / _ymax * 290};
            "<rect x='" & Text(Round(70 + (_i.Value - 1) * _bw; 2); "[$-en-US]0.00"; "en-US") & "' y='" & Text(Round(330 - _hb; 2); "[$-en-US]0.00"; "en-US") & "' width='" & Text(Round(_bw; 2); "[$-en-US]0.00"; "en-US") &
            "' height='" & Text(Round(_hb; 2); "[$-en-US]0.00"; "en-US") & "' fill='rgb(31,78,121)' stroke='white' stroke-width='1'/>" &
            If(_r.ni > 0; "<text x='" & Text(Round(70 + (_i.Value - 0,5) * _bw; 2); "[$-en-US]0.00"; "en-US") & "' y='" & Text(Round(330 - _hb - 4; 2); "[$-en-US]0.00"; "en-US") & "' text-anchor='middle' font-size='10' fill='rgb(33,37,41)'>" & Text(_r.ni; "[$-en-US]0"; "pt-PT") & "</text>"; "")))) &
    // Limites das classes no eixo horizontal (só alguns, se forem muitas classes)
    Concat(Sequence(_k + 1; 0) As _j;
        If(Mod(_j.Value; _salto) = 0 || _j.Value = _k;
            "<text x='" & Text(Round(70 + _j.Value * _bw; 2); "[$-en-US]0.00"; "en-US") & "' y='" & Text(Round(346; 2); "[$-en-US]0.00"; "en-US") & "' text-anchor='middle' font-size='10' fill='rgb(90,98,106)'>" & With({_r: Round(_F.a + _j.Value * _F.h; 4)}; If(_r = Int(_r); Text(_r; "[$-en-US]0"; "pt-PT"); Text(_r; "[$-en-US]0.####"; "pt-PT"))) & "</text>"; "")) &
    "<line x1='70' x2='620' y1='330' y2='330' stroke='rgb(90,98,106)'/>" &
    "<text x='345' y='370' text-anchor='middle' font-size='12' fill='rgb(90,98,106)'>" & Substitute(Substitute(Substitute(_rotulo; "&"; "&amp;"); "<"; "&lt;"); ">"; "&gt;") & "</text>" &
    "</svg>"
    ))))))
```

## 4. Correlação e regressão linear simples (ecrã `scrRegressao`)

### 4.1 Pares de valores

Só entram as observações com **x e y preenchidos** (eliminação por pares):

```powerfx
Filter(ForAll(colDados As _d; {x: Switch(_kx; 1; _d.N1; 2; _d.N2; _d.N3); y: Switch(_ky; 1; _d.N1; 2; _d.N2; _d.N3)}); !IsBlank(x) && !IsBlank(y))
```

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

```powerfx
With(
    {_p: Filter(ForAll(colDados As _d; {x: Switch(Switch(drpRegX.Selected.Value; varNomes.N1; 1; varNomes.N2; 2; varNomes.N3; 3; 1); 1; _d.N1; 2; _d.N2; _d.N3); y: Switch(Switch(drpRegY.Selected.Value; varNomes.N1; 1; varNomes.N2; 2; varNomes.N3; 3; 1); 1; _d.N1; 2; _d.N2; _d.N3)}); !IsBlank(x) && !IsBlank(y)); _x0: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(txtRegX0.Text); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank())};
    With({_n: CountRows(_p)};
    With({_mx: If(_n > 0; Average(_p; x)); _my: If(_n > 0; Average(_p; y))};
    With(
        // Somas de quadrados e de produtos dos desvios em relação às médias
        {_Sxx: Sum(_p; Power(x - _mx; 2)); _Syy: Sum(_p; Power(y - _my; 2)); _Sxy: Sum(_p; (x - _mx) * (y - _my))};
    With(
        {_b: If(_n >= 2 && _Sxx > 0; _Sxy / _Sxx);
         _r: If(_n >= 2 && _Sxx > 0 && _Syy > 0; _Sxy / Sqrt(_Sxx * _Syy))};
    {
        n: _n; mediaX: _mx; mediaY: _my;
        Sxx: If(_n > 0; _Sxx); Syy: If(_n > 0; _Syy); Sxy: If(_n > 0; _Sxy);
        sx: If(_n >= 2; Sqrt(_Sxx / (_n - 1))); sy: If(_n >= 2; Sqrt(_Syy / (_n - 1)));
        // Covariância amostral
        cov: If(_n >= 2; _Sxy / (_n - 1));
        r: _r;
        r2: If(!IsBlank(_r); _r * _r);
        // Reta dos mínimos quadrados: ŷ = a + b·x
        b: _b;
        a: If(!IsBlank(_b); _my - _b * _mx);
        minX: Min(_p; x); maxX: Max(_p; x); minY: Min(_p; y); maxY: Max(_p; y);
        x0: _x0;
        previsao: If(!IsBlank(_b) && !IsBlank(_x0); _my - _b * _mx + _b * _x0);
        // Teste H0: ρ = 0  —  t = r √(n − 2) / √(1 − r²), com n − 2 graus de liberdade
        glR: If(_n >= 3 && !IsBlank(_r); _n - 2);
        tR: If(_n >= 3 && !IsBlank(_r) && _r * _r < 1; _r * Sqrt((_n - 2) / (1 - _r * _r)));
        pR: If(_n >= 3 && !IsBlank(_r);
               If(_r * _r >= 1; 0;
                  With({_f: Power(_r * Sqrt((_n - 2) / (1 - _r * _r)); 2); _d1: 1; _d2: _n - 2};
                      If(_f <= 0; 1;
                      With({_t0: Atan(Sqrt(_d1 * _f / _d2)); _sg: 1 / Sqrt(Max(_d1 + _d2 - 2; 1));
                            _ts: If(_d2 > 1; Atan(Sqrt(Max(_d1 - 1; 0) / (_d2 - 1))); Pi() / 2)};
                      With({_lo: Max(0; _ts - 10 * _sg); _hi: Min(Pi() / 2; _ts + 10 * _sg)};
                          If(_t0 >= _hi; 0;
                              With({_nd: ForAll(Sequence(300; 0) As _i; With({_s: RoundDown(_i.Value / 3; 0); _m: Mod(_i.Value; 3)}; {u: (_s + 0,5 + (_m - 1) * 0,3872983346207417) / 100; w: If(_m = 1; 8 / 9; 5 / 9) / 200}))};
                          With({_Ltot: ForAll(_nd; With({t: _lo + u * (_hi - _lo)}; {L: (_d1 - 1) * Ln(Sin(t)) + (_d2 - 1) * Ln(Cos(t)); w: w * (_hi - _lo)}));
                                _Lcau: ForAll(_nd; With({t: Max(_t0; _lo) + u * (_hi - Max(_t0; _lo))}; {L: (_d1 - 1) * Ln(Sin(t)) + (_d2 - 1) * Ln(Cos(t)); w: w * (_hi - Max(_t0; _lo))}))};
                              With({_M: Max(_Ltot; L)};
                                  Min(1; Sum(_Lcau; Exp(L - _M) * w) / Sum(_Ltot; Exp(L - _M) * w))))))))))))
    }
    ))))
)
```

A previsão avisa quando há **extrapolação** (x fora do intervalo dos x observados).

### 4.3 Diagrama de dispersão com a reta

Os eixos usam passos «redondos» e uma margem de 4 %. Atenção a um pormenor do Power Fx: `RoundDown` e
`RoundUp` arredondam **em direção a zero** (`RoundDown(-2,5; 0)` = −2), por isso para o «chão» de um número
negativo usa-se `Int` (`Int(-2,5)` = −3) e para o «teto» `-Int(-x)`:

```powerfx
// início e fim do eixo dos x, múltiplos do passo _xp
{_x0: _xp * Int((_minX - 0,04 * _xd) / _xp + 1E-9);
 _x1: -_xp * Int(-(_maxX + 0,04 * _xd) / _xp + 1E-9)}
```

A reta é desenhada de um lado ao outro do gráfico e recortada à área dos dados com um `clipPath` SVG.

## 5. Inferência (ecrãs `scrTestesT`, `scrAnova`, `scrQuiQuadrado`)

### 5.1 Regra de decisão

Em todos os testes: **rejeita-se H₀ quando p ≤ α**, com α escolhido pelo aluno (0,10; 0,05; 0,01; 0,001). A app
escreve a decisão e uma conclusão por extenso no contexto dos dados. O nível α lê-se da lista pendente:

```powerfx
Value(Substitute(drpTtAlfa.Selected.Value; ","; "."); "en-US")
```

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

```powerfx
ForAll(Sequence(300; 0) As _i; With({_s: RoundDown(_i.Value / 3; 0); _m: Mod(_i.Value; 3)}; {u: (_s + 0,5 + (_m - 1) * 0,3872983346207417) / 100; w: If(_m = 1; 8 / 9; 5 / 9) / 200}))
```

**Valor de p da distribuição F** (`_f`, `_d1`, `_d2`):

```powerfx
With({_f: _estatisticaF; _d1: _gl1; _d2: _gl2};
    If(_f <= 0; 1;
    With({_t0: Atan(Sqrt(_d1 * _f / _d2)); _sg: 1 / Sqrt(Max(_d1 + _d2 - 2; 1));
          _ts: If(_d2 > 1; Atan(Sqrt(Max(_d1 - 1; 0) / (_d2 - 1))); Pi() / 2)};
    With({_lo: Max(0; _ts - 10 * _sg); _hi: Min(Pi() / 2; _ts + 10 * _sg)};
        If(_t0 >= _hi; 0;
            With({_nd: ForAll(Sequence(300; 0) As _i; With({_s: RoundDown(_i.Value / 3; 0); _m: Mod(_i.Value; 3)}; {u: (_s + 0,5 + (_m - 1) * 0,3872983346207417) / 100; w: If(_m = 1; 8 / 9; 5 / 9) / 200}))};
        With({_Ltot: ForAll(_nd; With({t: _lo + u * (_hi - _lo)}; {L: (_d1 - 1) * Ln(Sin(t)) + (_d2 - 1) * Ln(Cos(t)); w: w * (_hi - _lo)}));
              _Lcau: ForAll(_nd; With({t: Max(_t0; _lo) + u * (_hi - Max(_t0; _lo))}; {L: (_d1 - 1) * Ln(Sin(t)) + (_d2 - 1) * Ln(Cos(t)); w: w * (_hi - Max(_t0; _lo))}))};
            With({_M: Max(_Ltot; L)};
                Min(1; Sum(_Lcau; Exp(L - _M) * w) / Sum(_Ltot; Exp(L - _M) * w))))))))))
```

**Valor de p do qui-quadrado**:

```powerfx
With({_x: _estatisticaQui2; _k: _gl};
    If(_x <= 0; 1;
    With({_v0: Sqrt(_x); _vs: Sqrt(Max(_k - 1; 0))};
    With({_lo: Max(0; _vs - 10); _hi: _vs + 10};
        If(_v0 >= _hi; 0;
            With({_nd: ForAll(Sequence(300; 0) As _i; With({_s: RoundDown(_i.Value / 3; 0); _m: Mod(_i.Value; 3)}; {u: (_s + 0,5 + (_m - 1) * 0,3872983346207417) / 100; w: If(_m = 1; 8 / 9; 5 / 9) / 200}))};
        With({_Ltot: ForAll(_nd; With({t: _lo + u * (_hi - _lo)}; {L: (_k - 1) * Ln(t) - t * t / 2; w: w * (_hi - _lo)}));
              _Lcau: ForAll(_nd; With({t: Max(_v0; _lo) + u * (_hi - Max(_v0; _lo))}; {L: (_k - 1) * Ln(t) - t * t / 2; w: w * (_hi - Max(_v0; _lo))}))};
            With({_M: Max(_Ltot; L)};
                Min(1; Sum(_Lcau; Exp(L - _M) * w) / Sum(_Ltot; Exp(L - _M) * w))))))))))
```

**Valor de p do teste t** segundo a hipótese alternativa (1 bilateral, 2 à esquerda, 3 à direita):

```powerfx
With({_tt: _t; _p2: With({_f: Power((_t); 2); _d1: 1; _d2: _gl};
    If(_f <= 0; 1;
    With({_t0: Atan(Sqrt(_d1 * _f / _d2)); _sg: 1 / Sqrt(Max(_d1 + _d2 - 2; 1));
          _ts: If(_d2 > 1; Atan(Sqrt(Max(_d1 - 1; 0) / (_d2 - 1))); Pi() / 2)};
    With({_lo: Max(0; _ts - 10 * _sg); _hi: Min(Pi() / 2; _ts + 10 * _sg)};
        If(_t0 >= _hi; 0;
            With({_nd: ForAll(Sequence(300; 0) As _i; With({_s: RoundDown(_i.Value / 3; 0); _m: Mod(_i.Value; 3)}; {u: (_s + 0,5 + (_m - 1) * 0,3872983346207417) / 100; w: If(_m = 1; 8 / 9; 5 / 9) / 200}))};
        With({_Ltot: ForAll(_nd; With({t: _lo + u * (_hi - _lo)}; {L: (_d1 - 1) * Ln(Sin(t)) + (_d2 - 1) * Ln(Cos(t)); w: w * (_hi - _lo)}));
              _Lcau: ForAll(_nd; With({t: Max(_t0; _lo) + u * (_hi - Max(_t0; _lo))}; {L: (_d1 - 1) * Ln(Sin(t)) + (_d2 - 1) * Ln(Cos(t)); w: w * (_hi - Max(_t0; _lo))}))};
            With({_M: Max(_Ltot; L)};
                Min(1; Sum(_Lcau; Exp(L - _M) * w) / Sum(_Ltot; Exp(L - _M) * w))))))))))}; Switch(_alt; 1; _p2; 2; If(_tt < 0; _p2 / 2; 1 - _p2 / 2); If(_tt > 0; _p2 / 2; 1 - _p2 / 2)))
```

### 5.3 Testes t

| Teste | Estatística | Graus de liberdade |
|---|---|---|
| Uma amostra (H₀: μ = μ₀) | t = (x̄ − μ₀) / (s / √n) | n − 1 |
| Duas amostras independentes, variâncias iguais (H₀: μ₁ − μ₂ = Δ₀) | t = (x̄₁ − x̄₂ − Δ₀) / (sₚ √(1/n₁ + 1/n₂)), sₚ² = [(n₁ − 1)s₁² + (n₂ − 1)s₂²] / (n₁ + n₂ − 2) | n₁ + n₂ − 2 |
| Duas amostras independentes, Welch (variâncias diferentes) | t = (x̄₁ − x̄₂ − Δ₀) / √(s₁²/n₁ + s₂²/n₂) | (s₁²/n₁ + s₂²/n₂)² / [(s₁²/n₁)²/(n₁ − 1) + (s₂²/n₂)²/(n₂ − 1)] |
| Emparelhadas (H₀: μ_D = Δ₀, D = X − Y) | t = (d̄ − Δ₀) / (s_D / √n) | n − 1 (n = n.º de pares completos) |

As duas amostras independentes podem vir de **uma variável numérica + uma variável de grupo** (escolhem-se os dois
grupos) ou de **duas colunas numéricas**. Fórmula completa (registo com todos os resultados):

```powerfx
With(
    // Opções escolhidas no ecrã
    {_tipo: Switch(drpTtTipo.Selected.Value; "Uma amostra"; 1; "Duas amostras independentes (variâncias iguais)"; 2; "Duas amostras independentes (Welch, variâncias diferentes)"; 3; "Amostras emparelhadas"; 4; 1);
     _fmt: If(drpTtFormato.Selected.Value = "Duas colunas numéricas"; 2; 1);
     _alt: Switch(drpTtAlternativa.Selected.Value; "Unilateral à esquerda (<)"; 2; "Unilateral à direita (>)"; 3; 1); _alfa: Value(Substitute(drpTtAlfa.Selected.Value; ","; "."); "en-US");
     _d0: Coalesce(IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(txtTtMu0.Text); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()); 0);
     _k1: Switch(drpTtVar.Selected.Value; varNomes.N1; 1; varNomes.N2; 2; varNomes.N3; 3; 1); _k2: Switch(drpTtVar2.Selected.Value; varNomes.N1; 1; varNomes.N2; 2; varNomes.N3; 3; 1); _kg: Switch(drpTtGrupoVar.Selected.Value; varNomes.C2; 2; 1);
     _gA: drpTtGrupoA.Selected.Value; _gB: drpTtGrupoB.Selected.Value};
    With(
        // Amostra A (ou diferenças, no teste emparelhado) e amostra B
        {_A: Switch(_tipo; 1; Filter(ForAll(colDados As _d; {x: Switch(_k1; 1; _d.N1; 2; _d.N2; _d.N3)}); !IsBlank(x)); 4; Filter(ForAll(colDados As _d; With({_a: Switch(_k1; 1; _d.N1; 2; _d.N2; _d.N3); _b: Switch(_k2; 1; _d.N1; 2; _d.N2; _d.N3)}; {x: If(IsBlank(_a) || IsBlank(_b); Blank(); _a - _b)})); !IsBlank(x));
                If(_fmt = 1; Filter(ForAll(colDados As _d; {x: Switch(_k1; 1; _d.N1; 2; _d.N2; _d.N3); g: Switch(_kg; 1; _d.C1; _d.C2)}); !IsBlank(x) && g = _gA); Filter(ForAll(colDados As _d; {x: Switch(_k1; 1; _d.N1; 2; _d.N2; _d.N3)}); !IsBlank(x))));
         _B: If(_tipo = 2 || _tipo = 3;
                If(_fmt = 1; Filter(ForAll(colDados As _d; {x: Switch(_k1; 1; _d.N1; 2; _d.N2; _d.N3); g: Switch(_kg; 1; _d.C1; _d.C2)}); !IsBlank(x) && g = _gB); Filter(ForAll(colDados As _d; {x: Switch(_k2; 1; _d.N1; 2; _d.N2; _d.N3)}); !IsBlank(x))); FirstN(Table({x: 0}); 0))};
    With({_n1: CountRows(_A); _n2: CountRows(_B)};
    With({_m1: If(_n1 > 0; Average(_A; x)); _m2: If(_n2 > 0; Average(_B; x))};
    With(
        // Variâncias amostrais (divisor n − 1)
        {_v1: If(_n1 >= 2; Sum(_A; Power(x - _m1; 2)) / (_n1 - 1));
         _v2: If(_n2 >= 2; Sum(_B; Power(x - _m2; 2)) / (_n2 - 1))};
    With(
        // Erro padrão e graus de liberdade de cada teste
        {_ep: Switch(_tipo;
                1; If(_n1 >= 2; Sqrt(_v1 / _n1));
                4; If(_n1 >= 2; Sqrt(_v1 / _n1));
                2; If(_n1 >= 2 && _n2 >= 2;
                      Sqrt(((_n1 - 1) * _v1 + (_n2 - 1) * _v2) / (_n1 + _n2 - 2) * (1 / _n1 + 1 / _n2)));
                If(_n1 >= 2 && _n2 >= 2; Sqrt(_v1 / _n1 + _v2 / _n2)));
         _gl: Switch(_tipo;
                1; If(_n1 >= 2; _n1 - 1);
                4; If(_n1 >= 2; _n1 - 1);
                2; If(_n1 >= 2 && _n2 >= 2; _n1 + _n2 - 2);
                // Welch–Satterthwaite
                If(_n1 >= 2 && _n2 >= 2 && _v1 + _v2 > 0;
                   Power(_v1 / _n1 + _v2 / _n2; 2) /
                   (Power(_v1 / _n1; 2) / (_n1 - 1) + Power(_v2 / _n2; 2) / (_n2 - 1))))};
    With(
        {_t: If(!IsBlank(_ep) && _ep > 0;
                (If(_tipo = 2 || _tipo = 3; _m1 - _m2; _m1) - _d0) / _ep)};
    With(
        {_p: If(!IsBlank(_t) && _gl > 0; With({_tt: _t; _p2: With({_f: Power((_t); 2); _d1: 1; _d2: _gl};
            If(_f <= 0; 1;
            With({_t0: Atan(Sqrt(_d1 * _f / _d2)); _sg: 1 / Sqrt(Max(_d1 + _d2 - 2; 1));
                  _ts: If(_d2 > 1; Atan(Sqrt(Max(_d1 - 1; 0) / (_d2 - 1))); Pi() / 2)};
            With({_lo: Max(0; _ts - 10 * _sg); _hi: Min(Pi() / 2; _ts + 10 * _sg)};
                If(_t0 >= _hi; 0;
                    With({_nd: ForAll(Sequence(300; 0) As _i; With({_s: RoundDown(_i.Value / 3; 0); _m: Mod(_i.Value; 3)}; {u: (_s + 0,5 + (_m - 1) * 0,3872983346207417) / 100; w: If(_m = 1; 8 / 9; 5 / 9) / 200}))};
                With({_Ltot: ForAll(_nd; With({t: _lo + u * (_hi - _lo)}; {L: (_d1 - 1) * Ln(Sin(t)) + (_d2 - 1) * Ln(Cos(t)); w: w * (_hi - _lo)}));
                      _Lcau: ForAll(_nd; With({t: Max(_t0; _lo) + u * (_hi - Max(_t0; _lo))}; {L: (_d1 - 1) * Ln(Sin(t)) + (_d2 - 1) * Ln(Cos(t)); w: w * (_hi - Max(_t0; _lo))}))};
                    With({_M: Max(_Ltot; L)};
                        Min(1; Sum(_Lcau; Exp(L - _M) * w) / Sum(_Ltot; Exp(L - _M) * w))))))))))}; Switch(_alt; 1; _p2; 2; If(_tt < 0; _p2 / 2; 1 - _p2 / 2); If(_tt > 0; _p2 / 2; 1 - _p2 / 2))))};
    {
        tipo: _tipo; alt: _alt; alfa: _alfa; d0: _d0;
        n1: _n1; n2: _n2; m1: _m1; m2: _m2; v1: _v1; v2: _v2;
        s1: If(!IsBlank(_v1); Sqrt(_v1)); s2: If(!IsBlank(_v2); Sqrt(_v2));
        sp: If(_tipo = 2 && _n1 >= 2 && _n2 >= 2; Sqrt(((_n1 - 1) * _v1 + (_n2 - 1) * _v2) / (_n1 + _n2 - 2)));
        ep: _ep; t: _t; gl: _gl; p: _p;
        motivo: If(_n1 < 2 || ((_tipo = 2 || _tipo = 3) && _n2 < 2);
                   "cada amostra precisa de pelo menos 2 observações.";
                   "o erro padrão é zero (todos os valores iguais: variância nula), por isso t não está definido.")
    }
    )))))))
)
```

### 5.4 ANOVA a um fator

Com k grupos, nᵢ observações e média x̄ᵢ no grupo i, N = Σnᵢ e x̄ a média global:

| Fonte | SQ | gl | QM | F |
|---|---|---|---|---|
| Entre grupos | SQE = Σ nᵢ (x̄ᵢ − x̄)² | k − 1 | QME = SQE / (k − 1) | F = QME / QMD |
| Dentro dos grupos | SQD = Σᵢ Σⱼ (xᵢⱼ − x̄ᵢ)² | N − k | QMD = SQD / (N − k) | |
| Total | SQT = SQE + SQD | N − 1 | | |

p = P(F(k − 1, N − k) ≥ F). A app mostra também η² = SQE / SQT.

```powerfx
With(
    {_fmt: If(drpAnoFormato.Selected.Value = "Colunas numéricas como grupos"; 2; 1);
     _k: Switch(drpAnoVar.Selected.Value; varNomes.N1; 1; varNomes.N2; 2; varNomes.N3; 3; 1); _kg: Switch(drpAnoFator.Selected.Value; varNomes.C2; 2; 1); _alfa: Value(Substitute(drpAnoAlfa.Selected.Value; ","; "."); "en-US")};
    With(
        // Resumo de cada grupo: n, média, soma e soma dos quadrados dos desvios em relação à média do grupo
        {_g: If(_fmt = 1; ForAll(Sort(Filter(Distinct(colDados; Switch(_kg; 1; C1; C2)); !IsBlank(Value)); Value) As _G; With({_v: Filter(ForAll(colDados As _d; {x: Switch(_k; 1; _d.N1; 2; _d.N2; _d.N3); g: Switch(_kg; 1; _d.C1; _d.C2)}); !IsBlank(x) && g = _G.Value)}; With({_n: CountRows(_v)}; With({_m: If(_n > 0; Average(_v; x))}; {Grupo: _G.Value; n: _n; media: _m; soma: Sum(_v; x); sq: Sum(_v; Power(x - _m; 2))})))); Filter(ForAll(Sequence(3) As _j; With({_v: Filter(ForAll(colDados As _d; {x: Switch(_j.Value; 1; _d.N1; 2; _d.N2; _d.N3)}); !IsBlank(x))}; With({_n: CountRows(_v)}; With({_m: If(_n > 0; Average(_v; x))}; {Grupo: Switch(_j.Value; 1; varNomes.N1; 2; varNomes.N2; varNomes.N3); n: _n; media: _m; soma: Sum(_v; x); sq: Sum(_v; Power(x - _m; 2))})))); n > 0))};
    With({_N: Sum(_g; n); _kk: CountRows(_g)};
    With({_mg: If(_N > 0; Sum(_g; soma) / _N)};
    With(
        // SQ entre grupos (fator) e SQ dentro dos grupos (residual)
        {_SQE: Sum(_g; n * Power(media - _mg; 2)); _SQD: Sum(_g; sq)};
    With(
        {_QME: If(_kk >= 2; _SQE / (_kk - 1)); _QMD: If(_N > _kk; _SQD / (_N - _kk))};
    With(
        {_F: If(_kk >= 2 && _N > _kk && _SQD > 0; _QME / _QMD)};
    {
        Grupos: _g; k: _kk; N: _N; mediaGlobal: _mg; alfa: _alfa;
        SQE: _SQE; SQD: _SQD; SQT: _SQE + _SQD;
        glE: _kk - 1; glD: _N - _kk; glT: _N - 1;
        QME: _QME; QMD: _QMD; F: _F;
        p: If(!IsBlank(_F); With({_f: _F; _d1: _kk - 1; _d2: _N - _kk};
                If(_f <= 0; 1;
                With({_t0: Atan(Sqrt(_d1 * _f / _d2)); _sg: 1 / Sqrt(Max(_d1 + _d2 - 2; 1));
                      _ts: If(_d2 > 1; Atan(Sqrt(Max(_d1 - 1; 0) / (_d2 - 1))); Pi() / 2)};
                With({_lo: Max(0; _ts - 10 * _sg); _hi: Min(Pi() / 2; _ts + 10 * _sg)};
                    If(_t0 >= _hi; 0;
                        With({_nd: ForAll(Sequence(300; 0) As _i; With({_s: RoundDown(_i.Value / 3; 0); _m: Mod(_i.Value; 3)}; {u: (_s + 0,5 + (_m - 1) * 0,3872983346207417) / 100; w: If(_m = 1; 8 / 9; 5 / 9) / 200}))};
                    With({_Ltot: ForAll(_nd; With({t: _lo + u * (_hi - _lo)}; {L: (_d1 - 1) * Ln(Sin(t)) + (_d2 - 1) * Ln(Cos(t)); w: w * (_hi - _lo)}));
                          _Lcau: ForAll(_nd; With({t: Max(_t0; _lo) + u * (_hi - Max(_t0; _lo))}; {L: (_d1 - 1) * Ln(Sin(t)) + (_d2 - 1) * Ln(Cos(t)); w: w * (_hi - Max(_t0; _lo))}))};
                        With({_M: Max(_Ltot; L)};
                            Min(1; Sum(_Lcau; Exp(L - _M) * w) / Sum(_Ltot; Exp(L - _M) * w)))))))))));
        eta2: If(_SQE + _SQD > 0; _SQE / (_SQE + _SQD));
        motivo: If(_kk < 2; "são precisos pelo menos 2 grupos com dados.";
                   _N <= _kk; "é preciso que pelo menos um grupo tenha mais do que uma observação (N > k).";
                   "a variabilidade dentro dos grupos é nula (SQ dentro = 0), por isso F não está definido.")
    }
    ))))))
)
```

### 5.5 Qui-quadrado

* **Aderência**: k categorias com frequências observadas Oᵢ e proporções esperadas pᵢ (iguais ou indicadas pelo
  aluno; são normalizadas para somar 1). Eᵢ = n·pᵢ, χ² = Σ (Oᵢ − Eᵢ)² / Eᵢ, gl = k − 1.
* **Independência**: tabela r × c, Eᵢⱼ = Rᵢ·Cⱼ / N (totais de linha e coluna), χ² = Σ (Oᵢⱼ − Eᵢⱼ)² / Eᵢⱼ,
  gl = (r − 1)(c − 1). Não se aplica a correção de continuidade de Yates.
* **Regra de Cochran** (aviso): no máximo 20 % das células com E < 5 e nenhuma com E < 1.

As frequências podem vir das variáveis da tabela de dados (as variáveis numéricas são tratadas como categorias)
ou de uma **tabela colada do Excel**. Na tabela colada, a 1.ª linha é cabeçalho se tiver texto a partir da
2.ª coluna e a 1.ª coluna tem os nomes das linhas se tiver texto:

```powerfx
With({_lin: With(
        // Retira os retornos de carro (Char(13)) do Windows e parte o texto em linhas
        {_linhas: Split(Substitute(txtQuiTabela.Text; Char(13); ""); Char(10))};
        Filter(
            ForAll(Sequence(CountRows(_linhas)) As _i;
                With(
                    // Parte cada linha nas tabulações (colunas do Excel) e limpa os espaços
                    {_cel: ForAll(Split(Index(_linhas; _i.Value).Value; Char(9)) As _c;
                        {Texto: Trim(Substitute(_c.Value; UniChar(160); " "))})};
                    {Linha: _i.Value; Celulas: _cel; NCel: CountRows(Filter(_cel; Texto <> ""))}
                )
            );
            // Ignora linhas vazias (ou só com tabulações/espaços)
            NCel > 0
        )
    )};
    With({_m: CountRows(_lin); _kc: Coalesce(Max(_lin; CountRows(Celulas)); 0)};
    With({_cab: _m >= 2 && CountRows(Filter(Sequence(Max(_kc - 1; 0); 2) As _j;
                With({_t: If(_j.Value <= CountRows(First(_lin).Celulas); Index(First(_lin).Celulas; _j.Value).Texto; "")}; _t <> "" && IsBlank(IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_t); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()))))) > 0};
    With({_corpo: If(_cab; LastN(_lin; _m - 1); _lin)};
    With({_rot: CountRows(Filter(_corpo As _r; With({_t: If(1 <= CountRows(_r.Celulas); Index(_r.Celulas; 1).Texto; "")}; _t <> "" && IsBlank(IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_t); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()))))) > 0};
    With({_c0: If(_rot; 1; 0)};
    With({_nc: Max(_kc - _c0; 0); _nr: CountRows(_corpo)};
    {
        Linhas: ForAll(Sequence(_nr) As _i; {nome: If(_rot; If(1 <= CountRows(Index(_corpo; _i.Value).Celulas); Index(Index(_corpo; _i.Value).Celulas; 1).Texto; ""); "Linha " & _i.Value)});
        Colunas: ForAll(Sequence(_nc) As _j; {nome: If(_cab; If(_j.Value + _c0 <= CountRows(First(_lin).Celulas); Index(First(_lin).Celulas; _j.Value + _c0).Texto; ""); "Coluna " & _j.Value)});
        Celulas: ForAll(Sequence(_nr * _nc; 0) As _q;
            With({_i: RoundDown(_q.Value / _nc; 0) + 1; _j: Mod(_q.Value; _nc) + 1};
                With({_t: If(_j + _c0 <= CountRows(Index(_corpo; _i).Celulas); Index(Index(_corpo; _i).Celulas; _j + _c0).Texto; "")};
                    {i: _i; j: _j; t: _t; O: With({_o: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_t); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank())}; If(IsBlank(_o) || _o < 0; 0; _o));
                     invalido: _t <> "" && (IsBlank(IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_t); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank())) || IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_t); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()) < 0)})));
        TemRotulos: _rot
    }
    ))))))
)
```

Proporções esperadas escritas pelo aluno (separadas por `;`, tabulação ou mudança de linha):

```powerfx
Filter(ForAll(Split(Substitute(Substitute(Substitute(txtQuiProporcoes.Text; Char(13); ""); Char(9); Char(10)); ";"; Char(10)); Char(10)) As _s; {p: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_s.Value); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank())}); !IsBlank(p))
```

Fórmula completa do teste:

```powerfx
With(
    {_tipo: If(drpQuiTipo.Selected.Value = "Independência (tabela de contingência)"; 2; 1);
     _orig: If(drpQuiOrigem.Selected.Value = "Tabela colada do Excel"; 2; 1);
     _k1: Switch(drpQuiVar1.Selected.Value; varNomes.N1; 1; varNomes.N2; 2; varNomes.N3; 3; varNomes.C1; 4; varNomes.C2; 5; 1); _k2: Switch(drpQuiVar2.Selected.Value; varNomes.N1; 1; varNomes.N2; 2; varNomes.N3; 3; varNomes.C1; 4; varNomes.C2; 5; 1);
     _alfa: Value(Substitute(drpQuiAlfa.Selected.Value; ","; "."); "en-US")};
    With(
        // Tabela observada: nomes das linhas e colunas e células {i, j, O} (na aderência há só 1 coluna)
        {_T: If(_orig = 2; With({_lin: With(
                    // Retira os retornos de carro (Char(13)) do Windows e parte o texto em linhas
                    {_linhas: Split(Substitute(txtQuiTabela.Text; Char(13); ""); Char(10))};
                    Filter(
                        ForAll(Sequence(CountRows(_linhas)) As _i;
                            With(
                                // Parte cada linha nas tabulações (colunas do Excel) e limpa os espaços
                                {_cel: ForAll(Split(Index(_linhas; _i.Value).Value; Char(9)) As _c;
                                    {Texto: Trim(Substitute(_c.Value; UniChar(160); " "))})};
                                {Linha: _i.Value; Celulas: _cel; NCel: CountRows(Filter(_cel; Texto <> ""))}
                            )
                        );
                        // Ignora linhas vazias (ou só com tabulações/espaços)
                        NCel > 0
                    )
                )};
                With({_m: CountRows(_lin); _kc: Coalesce(Max(_lin; CountRows(Celulas)); 0)};
                With({_cab: _m >= 2 && CountRows(Filter(Sequence(Max(_kc - 1; 0); 2) As _j;
                            With({_t: If(_j.Value <= CountRows(First(_lin).Celulas); Index(First(_lin).Celulas; _j.Value).Texto; "")}; _t <> "" && IsBlank(IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_t); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()))))) > 0};
                With({_corpo: If(_cab; LastN(_lin; _m - 1); _lin)};
                With({_rot: CountRows(Filter(_corpo As _r; With({_t: If(1 <= CountRows(_r.Celulas); Index(_r.Celulas; 1).Texto; "")}; _t <> "" && IsBlank(IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_t); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()))))) > 0};
                With({_c0: If(_rot; 1; 0)};
                With({_nc: Max(_kc - _c0; 0); _nr: CountRows(_corpo)};
                {
                    Linhas: ForAll(Sequence(_nr) As _i; {nome: If(_rot; If(1 <= CountRows(Index(_corpo; _i.Value).Celulas); Index(Index(_corpo; _i.Value).Celulas; 1).Texto; ""); "Linha " & _i.Value)});
                    Colunas: ForAll(Sequence(_nc) As _j; {nome: If(_cab; If(_j.Value + _c0 <= CountRows(First(_lin).Celulas); Index(First(_lin).Celulas; _j.Value + _c0).Texto; ""); "Coluna " & _j.Value)});
                    Celulas: ForAll(Sequence(_nr * _nc; 0) As _q;
                        With({_i: RoundDown(_q.Value / _nc; 0) + 1; _j: Mod(_q.Value; _nc) + 1};
                            With({_t: If(_j + _c0 <= CountRows(Index(_corpo; _i).Celulas); Index(Index(_corpo; _i).Celulas; _j + _c0).Texto; "")};
                                {i: _i; j: _j; t: _t; O: With({_o: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_t); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank())}; If(IsBlank(_o) || _o < 0; 0; _o));
                                 invalido: _t <> "" && (IsBlank(IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_t); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank())) || IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_t); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank()) < 0)})));
                    TemRotulos: _rot
                }
                ))))))
            );
            With({_pr: Filter(ForAll(colDados As _d; With({_A: With({_val: Switch(_k1; 1; _d.N1; 2; _d.N2; 3; _d.N3; Blank())}; {cat: If(_k1 <= 3; If(IsBlank(_val); ""; With({_v: _val}; If(IsBlank(_v); ""; If(_v = Int(_v); Text(_v; "[$-en-US]0"; "pt-PT"); Text(_v; "[$-en-US]0.##########"; "pt-PT"))))); Switch(_k1; 4; _d.C1; _d.C2)); ord: If(_k1 <= 3; _val; 0)}); _B: With({_val: Switch(_k2; 1; _d.N1; 2; _d.N2; 3; _d.N3; Blank())}; {cat: If(_k2 <= 3; If(IsBlank(_val); ""; With({_v: _val}; If(IsBlank(_v); ""; If(_v = Int(_v); Text(_v; "[$-en-US]0"; "pt-PT"); Text(_v; "[$-en-US]0.##########"; "pt-PT"))))); Switch(_k2; 4; _d.C1; _d.C2)); ord: If(_k2 <= 3; _val; 0)})};
                        {a: _A.cat; oa: _A.ord; b: If(_tipo = 2; _B.cat; "Total"); ob: If(_tipo = 2; _B.ord; 0)}));
                        a <> "" && b <> "")};
                With({_L: With({_ls: ForAll(Distinct(_pr; a) As _c; {nome: _c.Value; o: LookUp(_pr; a = _c.Value).oa})}; If(_k1 <= 3; Sort(_ls; o); Sort(_ls; nome))); _C: With({_ls: ForAll(Distinct(_pr; b) As _c; {nome: _c.Value; o: LookUp(_pr; b = _c.Value).ob})}; If(If(_tipo = 2; _k2; 4) <= 3; Sort(_ls; o); Sort(_ls; nome)))};
                    {Linhas: _L; Colunas: _C;
                     Celulas: ForAll(Sequence(CountRows(_L) * CountRows(_C); 0) As _q;
                        With({_i: RoundDown(_q.Value / CountRows(_C); 0) + 1; _j: Mod(_q.Value; CountRows(_C)) + 1};
                            {i: _i; j: _j; t: "";
                             O: CountIf(_pr; a = Index(_L; _i).nome && b = Index(_C; _j).nome); invalido: false}));
                     TemRotulos: true})))};
    With(
        // Aderência: frequências observadas = última coluna; se a tabela colada não tiver nomes de texto
        // e tiver 2 ou mais colunas, a 1.ª coluna dá os nomes das categorias (ex.: faces de um dado 1 a 6)
        {_cel: If(_tipo = 1; ForAll(Filter(_T.Celulas; j = CountRows(_T.Colunas)) As _x;
                                    {i: _x.i; j: 1; O: _x.O});
                   ForAll(_T.Celulas As _x; {i: _x.i; j: _x.j; O: _x.O}));
         _Lin: If(_tipo = 1 && !_T.TemRotulos && CountRows(_T.Colunas) >= 2;
                  ForAll(Filter(_T.Celulas; j = 1) As _x; {nome: _x.t}); _T.Linhas);
         _nr: CountRows(_T.Linhas); _nc: If(_tipo = 1; 1; CountRows(_T.Colunas))};
    With({_N: Sum(_cel; O);
          _Ri: ForAll(Sequence(_nr) As _r; {i: _r.Value; R: Sum(Filter(_cel; i = _r.Value); O)});
          _Cj: ForAll(Sequence(_nc) As _c; {j: _c.Value; C: Sum(Filter(_cel; j = _c.Value); O)});
          _pind: Filter(ForAll(Split(Substitute(Substitute(Substitute(txtQuiProporcoes.Text; Char(13); ""); Char(9); Char(10)); ";"; Char(10)); Char(10)) As _s; {p: IfError(Value(Substitute(Substitute(Substitute(Substitute(Trim(_s.Value); " "; ""); UniChar(160); ""); UniChar(8239); ""); ","; "."); "en-US"); Blank())}); !IsBlank(p));
          _esp: If(drpQuiEsperadas.Selected.Value = "Proporções indicadas"; 2; 1)};
    With(
        // Frequências esperadas: n·pᵢ (aderência) ou Rᵢ·Cⱼ/N (independência)
        {_E: ForAll(_cel As _o;
            {i: _o.i; j: _o.j; O: _o.O;
             E: If(_tipo = 1;
                   If(_esp = 1; _N / _nr;
                      If(CountRows(_pind) = _nr && Sum(_pind; p) > 0; _N * Index(_pind; _o.i).p / Sum(_pind; p)));
                   LookUp(_Ri; i = _o.i).R * LookUp(_Cj; j = _o.j).C / _N)})};
    With(
        {_ok: _N > 0 && _nr >= 2 && (_tipo = 1 || _nc >= 2) && CountRows(Filter(_E; IsBlank(E) || E <= 0)) = 0};
    With(
        {_q2: If(_ok; Sum(_E; Power(O - E; 2) / E));
         _gl: If(_tipo = 1; _nr - 1; (_nr - 1) * (_nc - 1))};
    {
        tipo: _tipo; alfa: _alfa; Linhas: _Lin; Colunas: _T.Colunas; Celulas: _E;
        nr: _nr; nc: _nc; N: _N; Ri: _Ri; Cj: _Cj;
        qui2: _q2; gl: _gl;
        p: If(!IsBlank(_q2); With({_x: _q2; _k: _gl};
                If(_x <= 0; 1;
                With({_v0: Sqrt(_x); _vs: Sqrt(Max(_k - 1; 0))};
                With({_lo: Max(0; _vs - 10); _hi: _vs + 10};
                    If(_v0 >= _hi; 0;
                        With({_nd: ForAll(Sequence(300; 0) As _i; With({_s: RoundDown(_i.Value / 3; 0); _m: Mod(_i.Value; 3)}; {u: (_s + 0,5 + (_m - 1) * 0,3872983346207417) / 100; w: If(_m = 1; 8 / 9; 5 / 9) / 200}))};
                    With({_Ltot: ForAll(_nd; With({t: _lo + u * (_hi - _lo)}; {L: (_k - 1) * Ln(t) - t * t / 2; w: w * (_hi - _lo)}));
                          _Lcau: ForAll(_nd; With({t: Max(_v0; _lo) + u * (_hi - Max(_v0; _lo))}; {L: (_k - 1) * Ln(t) - t * t / 2; w: w * (_hi - Max(_v0; _lo))}))};
                        With({_M: Max(_Ltot; L)};
                            Min(1; Sum(_Lcau; Exp(L - _M) * w) / Sum(_Ltot; Exp(L - _M) * w)))))))))));
        baixas: CountRows(Filter(_E; E < 5)); muitoBaixas: CountRows(Filter(_E; E < 1));
        invalidos: CountRows(Filter(_T.Celulas; invalido));
        proporcoes: If(_tipo = 1; If(_esp = 1; ForAll(Sequence(_nr) As _r; {p: 1 / _nr});
                        ForAll(_pind As _x; {p: _x.p / Sum(_pind; p)})));
        motivo: If(_N = 0; "não há observações.";
                   _nr < 2; "são precisas pelo menos 2 categorias (linhas).";
                   _tipo = 2 && _nc < 2; "são precisas pelo menos 2 colunas na tabela de contingência.";
                   _tipo = 1 && _esp = 2 && CountRows(_pind) <> _nr;
                       "indique tantas proporções esperadas quantas as categorias (" & _nr & "), pela ordem da tabela.";
                   "há frequências esperadas nulas (uma linha ou coluna sem observações ou uma proporção igual a 0).")
    }
    ))))))
)
```

### 5.6 Teste de significância do coeficiente de correlação (ecrã `scrRegressao`)

H₀: ρ = 0 contra H₁: ρ ≠ 0, com t = r √(n − 2) / √(1 − r²) e n − 2 graus de liberdade (precisa de n ≥ 3).
