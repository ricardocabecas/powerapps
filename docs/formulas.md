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
