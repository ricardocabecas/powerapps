# Estatística — app Power Apps (canvas) para aulas práticas

App de estatística para estudantes do ensino superior, feita só com **Power Fx e controlos nativos clássicos**:
sem componentes de código (PCF), sem Power Automate e sem conectores premium (nem sequer usa fontes de dados —
tudo vive em coleções). Interface em português de Portugal, números com vírgula decimal, aceita dados com
vírgula ou ponto decimal.

## O que a app faz

| Ecrã | Conteúdo |
|---|---|
| **Dados** (`scrDados`) | Tabela editável (galeria ligada à coleção `colDados`) com 3 variáveis numéricas e 2 categóricas (de grupo), nomes editáveis; colar uma ou várias colunas do Excel com deteção de cabeçalho, escolha da coluna de origem e aviso dos valores inválidos |
| **Descritiva** (`scrDescritiva`) | n, soma, média, mediana, moda, mínimo, máximo, amplitude, quartis (3 métodos), AIQ, variância e desvio padrão **amostrais (n − 1)** e **populacionais (n)**, CV; opcionalmente por grupo |
| **Frequências** (`scrFrequencias`) | Frequências absolutas, relativas e acumuladas para dados discretos/categóricos e para dados em classes (Sturges, início e amplitude configuráveis); **histograma** e **diagrama de barras** em SVG |
| **Regressão** (`scrRegressao`) | r de Pearson, R², declive, ordenada na origem, equação da reta, previsão para um x (com aviso de extrapolação), teste de ρ = 0; **diagrama de dispersão com a reta** em SVG |
| **Testes t** (`scrTestesT`) | Uma amostra; duas amostras independentes com variâncias iguais e de Welch; amostras emparelhadas; bilateral ou unilateral |
| **ANOVA** (`scrAnova`) | ANOVA a um fator com resumo dos grupos e tabela completa (SQ, gl, QM, F, p) e η² |
| **Qui-quadrado** (`scrQuiQuadrado`) | Aderência (proporções iguais ou indicadas) e independência, a partir das variáveis ou de uma tabela colada do Excel, com frequências esperadas e aviso da regra de Cochran |

Em cada teste a app mostra **hipóteses, estatística de teste, graus de liberdade, valor de p e uma conclusão por
extenso** para o nível de significância escolhido pelo aluno. Os valores de p são calculados em Power Fx puro, por
integração numérica (Gauss-Legendre com `Sequence` e `Sum`); o erro medido face ao scipy é inferior a 10⁻⁶ —
ver [docs/precisao-valores-p.md](docs/precisao-valores-p.md).

## Conteúdo do repositório

| Pasta / ficheiro | Conteúdo |
|---|---|
| `Src/` | Código fonte dos ecrãs, **um ficheiro `.pa.yaml` por ecrã** (formato invariante, esquema v3.0), pronto a colar no Studio |
| `colar/` | Os mesmos ecrãs só com os controlos (alternativa se o Studio não aceitar colar o ecrã inteiro) |
| `docs/formulas.md` | Todas as fórmulas explicadas, **em sintaxe pt-PT** (material de apoio às aulas) |
| `docs/folha-verificacao.md` | Valores esperados (calculados com scipy) para confirmar a app no Studio |
| `docs/precisao-valores-p.md` | Método e precisão dos valores de p |
| `docs/notas-tecnicas.md` | Documentação Microsoft consultada, decisões, limitações e diferenças do interpretador |
| `testes/` | Dados de teste, implementação de referência em Python/scipy, motor Power Fx (.NET) e resultados |
| `ferramentas/` | Gerador (Python) que produz `Src/`, `colar/` e `docs/formulas.md` a partir de uma única fonte |

## Montar a app do zero no Power Apps Studio

### Antes de começar

* **Região**: para ver as fórmulas com `;` e `;;` (como em `docs/formulas.md`), o navegador deve estar em
  português (Portugal). Os ficheiros `.pa.yaml` estão no formato invariante exigido pelo Power Apps e funcionam em
  qualquer região — o Studio converte-os ao mostrar.
* **Área de transferência**: na primeira colagem o navegador pede acesso — aceite. No Edge, se a colagem não
  funcionar, acrescente `https://make.powerapps.com` aos sites com acesso à área de transferência.
* Não é preciso configurar nada no objeto **App** (que, segundo a documentação, não pode ser colado): a
  inicialização está no `OnVisible` do ecrã de dados.

### Passos, por esta ordem

1. Em [make.powerapps.com](https://make.powerapps.com) → **Criar** → **Aplicação de tela em branco**, formato
   **Tablet** (1366 × 768). Dê-lhe um nome (ex.: «Estatística»).
2. **Ecrã de dados (tem de ser o primeiro)**: abra `Src/scrDados.pa.yaml` num editor de texto, selecione tudo
   (Ctrl+A) e copie (Ctrl+C). No Studio, na **Vista de árvore**, clique com o botão direito em `Screen1` →
   **Colar** (ou selecione-o e prima Ctrl+V). Aparece o ecrã `scrDados`.
3. Apague o `Screen1` vazio. Confirme que `scrDados` é o **primeiro** ecrã da árvore (é o ecrã inicial e o seu
   `OnVisible` cria `colDados` e `varNomes`, que os outros ecrãs usam).
4. **Restantes ecrãs, por esta ordem**, da mesma forma (copiar o ficheiro todo e colar na vista de árvore):
   1. `Src/scrDescritiva.pa.yaml`
   2. `Src/scrFrequencias.pa.yaml`
   3. `Src/scrRegressao.pa.yaml`
   4. `Src/scrTestesT.pa.yaml`
   5. `Src/scrAnova.pa.yaml`
   6. `Src/scrQuiQuadrado.pa.yaml`

   A ordem da árvore deve ficar igual à dos botões da barra superior.
5. Enquanto não estiverem colados todos os ecrãs, os botões de navegação que apontam para ecrãs ainda inexistentes
   mostram erro — é normal. Depois de colar o último, os erros devem desaparecer; se algum persistir, guarde a
   app, feche e volte a abrir (o Studio volta a validar todas as fórmulas).
6. Selecione `scrDados` e prima **F5** (pré-visualizar) uma vez: o `OnVisible` carrega os 20 estudantes de
   exemplo e os nomes das variáveis. Feche a pré-visualização: a partir daí os outros ecrãs já mostram resultados
   também no modo de edição.
7. **Guarde** e **Publique**. Partilhe com os alunos (como não há conectores nem fontes de dados, não é preciso
   dar permissões a nada além da própria app).
8. Confirme os resultados com a [folha de verificação](docs/folha-verificacao.md).

### Se o Studio não aceitar colar um ecrã inteiro

Para cada ecrã: crie um ecrã em branco (**Novo ecrã** → **Em branco**), mude-lhe o nome para o nome do ficheiro
(ex.: `scrDescritiva`), copie o conteúdo de `colar/<ecrã>.controlos.yaml`, selecione o ecrã e cole (Ctrl+V).
Depois, nas propriedades do ecrã, escreva:

* `Fill` → `RGBA(244; 246; 249; 1)` (todos os ecrãs);
* só em `scrDados`: `OnVisible` → a fórmula da secção **1.1 Inicialização** de
  [docs/formulas.md](docs/formulas.md) (já em sintaxe pt-PT).

### Resolução de problemas

| Sintoma | Causa provável e solução |
|---|---|
| «A área de transferência não contém código YAML» | O navegador bloqueou o acesso à área de transferência (ver *Antes de começar*). |
| Erro num tipo de controlo (ex.: `Classic/Button` desconhecido) | Os ficheiros indicam só o tipo, sem versão (a documentação diz que, sem versão, o Studio usa a mais recente). Se o seu Studio usar outro identificador, insira um controlo desse tipo à mão, clique com o botão direito → **Ver código**, veja o identificador (`Control: …`) e substitua-o no ficheiro antes de colar. Tipos usados: `Label`, `Classic/Button`, `Classic/TextInput`, `Classic/DropDown`, `Gallery`, `Image`, `HtmlViewer`, `Rectangle`. Para mudar todos de uma vez, altere `ferramentas/gerador/comum.py` e corra `python3 ferramentas/gerar.py`. |
| Erro na variante da galeria | Mude `Variant:` da galeria para a que o seu Studio gera numa galeria vertical em branco (veja com **Ver código**). |
| Resultados vazios nos ecrãs de análise | Ainda não correu o `OnVisible` de `scrDados` (passo 6). |
| Os números aparecem com ponto | Verifique se a fórmula tem o marcador `"[$-en-US]…"` e o 3.º argumento `"pt-PT"` em `Text`. |

## Utilização em aula (resumo)

* **Dados**: edite as células (vírgula ou ponto decimal). Uma célula com texto que não é número fica com contorno
  vermelho e conta como valor em falta. Clique no cabeçalho para dar nome a uma variável.
* **Colar do Excel**: copie as colunas (com ou sem linha de nomes), cole na caixa da direita, carregue em
  **Analisar**, confirme a coluna de origem de cada variável e **Importar** (substituir ou acrescentar). Os valores
  inválidos são listados com o n.º da linha antes de importar e ficam em branco.
* Os ecrãs de análise **atualizam-se sozinhos** quando muda os dados ou as opções.

## Validação

Tudo o que foi validado fora do Studio (ver [testes/resultados/comparacao.md](testes/resultados/comparacao.md)):

* Os 7 ficheiros `.pa.yaml` foram validados contra o **esquema oficial** `pa.schema.yaml` v3.0 da Microsoft;
  os nomes de controlos são únicos em toda a app; parênteses equilibrados em todas as fórmulas.
* As **2 444 fórmulas** dos ecrãs foram analisadas sem erros de sintaxe pelo **interpretador open source Power Fx**
  (`Microsoft.PowerFx.Interpreter` 1.8.1, .NET 8) em formato invariante **e** convertidas para pt-PT.
* Os cálculos foram **executados no interpretador** com conjuntos de dados pequenos (incluindo n pequeno, valores
  repetidos, variância nula, média zero, valores em falta, células com frequência esperada baixa) e comparados com
  a referência em Python/numpy/scipy: **todas as verificações sem diferenças** (tolerância 10⁻⁹ nas medidas e
  10⁻⁶ nos valores de p).
* Os SVG gerados são XML bem formado, sem vírgulas nas coordenadas, e foram inspecionados visualmente num navegador.

**Não foi possível validar** sem acesso ao Power Apps Studio: a colagem real dos ficheiros, o aspeto visual dos
controlos, a renderização do controlo *Texto HTML* e do controlo *Imagem* dentro do Studio e o desempenho no
navegador. Para isso serve a [folha de verificação](docs/folha-verificacao.md).

### Correr os testes

Requisitos: Python 3 com `numpy`, `scipy`, `pyyaml`, `jsonschema`; .NET 8 SDK (o pacote NuGet é descarregado
automaticamente).

```bash
python3 ferramentas/gerar.py              # gera Src/, colar/, docs/formulas.md e valida contra o esquema
python3 testes/executar_testes.py         # executa as fórmulas no interpretador Power Fx e compara com scipy
python3 testes/precisao_valores_p.py      # mede a precisão dos valores de p numa grelha alargada
```

## Limitações conhecidas

* Nada ficou por fazer por exigir PCF: todas as funcionalidades pedidas foram feitas com Power Fx e controlos nativos.
* Não incluídos (não pedidos): teste exato de Fisher, correção de Yates, comparações múltiplas após a ANOVA,
  testes não paramétricos. A app avisa quando a regra de Cochran não é cumprida e quando a ANOVA rejeita H₀.
* Pensada para turmas e conjuntos de dados de aula (dezenas a poucas centenas de linhas). As fórmulas são reativas;
  com milhares de linhas os ecrãs podem ficar lentos.
* Os dados vivem na sessão (coleção) e perdem-se ao fechar a app; guarde-os no Excel e volte a colar.
