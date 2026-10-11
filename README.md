# Estatística — app Power Apps (canvas) para aulas práticas

App de estatística para estudantes do ensino superior, feita só com **Power Fx e controlos nativos**
(sem componentes de código PCF, sem Power Automate, sem conectores premium). Interface em português de
Portugal, números com vírgula decimal, aceita dados com vírgula ou ponto decimal.

> **Estado:** em construção por fases. Fases 1 (entrada de dados), 2 (estatística descritiva), 3 (frequências e gráficos) e 4 (correlação e regressão) concluídas.

## Conteúdo do repositório

| Pasta | Conteúdo |
|---|---|
| `Src/` | Código fonte dos ecrãs, **um ficheiro `.pa.yaml` por ecrã**, pronto a colar no Studio |
| `colar/` | Os mesmos ecrãs, só com os controlos (alternativa se o Studio não aceitar colar o ecrã inteiro) |
| `docs/formulas.md` | Todas as fórmulas explicadas, em sintaxe pt-PT (material de apoio às aulas) |
| `docs/notas-tecnicas.md` | Fontes da documentação Microsoft consultada, decisões e limitações |
| `testes/` | Dados de teste, implementação de referência em Python/scipy, motor Power Fx e resultados |
| `ferramentas/` | Gerador (Python) que produz `Src/`, `colar/` e `docs/formulas.md` |

## Montar a app do zero no Power Apps Studio

1. Em [make.powerapps.com](https://make.powerapps.com) crie uma **app de tela em branco** (formato *Tablet*).
2. **Região:** o navegador deve estar em português (Portugal) para ver as fórmulas com `;`. Os ficheiros
   funcionam em qualquer região (o Studio converte o formato invariante).
3. **Acesso à área de transferência:** na primeira colagem o navegador pede autorização — aceite. No Edge, se
   necessário, acrescente `https://make.powerapps.com` aos sites com acesso à área de transferência.
4. **Ecrã de dados** — abra `Src/scrDados.pa.yaml`, selecione todo o conteúdo e copie (Ctrl+C). No Studio, na
   vista de árvore, clique com o botão direito em **Screen1** → **Colar** (ou selecione o ecrã e Ctrl+V).
   Deve aparecer o ecrã `scrDados`. Apague o `Screen1` vazio e, se necessário, arraste `scrDados` para o topo
   (o primeiro ecrã é o ecrã inicial).
5. **Restantes ecrãs, por esta ordem** (cada um depende de `colDados` e `varNomes`, criados pelo ecrã de dados):
   `Src/scrDescritiva.pa.yaml`, `Src/scrFrequencias.pa.yaml`, `Src/scrRegressao.pa.yaml`. Para cada ficheiro: copie todo o conteúdo e cole na vista de árvore (Ctrl+V).
6. Os botões da barra de navegação referem ecrãs que ainda não existem; ficam com erro até colar os ecrãs
   seguintes. Isso é esperado.

### Se o Studio não aceitar colar o ecrã inteiro

Crie um ecrã em branco, mude-lhe o nome para `scrDados`, copie o conteúdo de `colar/scrDados.controlos.yaml`,
selecione o ecrã e cole (Ctrl+V). Depois, nas propriedades do ecrã:

* `Fill` → `RGBA(244; 246; 249; 1)`
* `OnVisible` → copie a fórmula da secção **1.1 Inicialização** de `docs/formulas.md` (já em sintaxe pt-PT).

## Utilização (ecrã Dados)

* Edite diretamente as células da tabela; vírgula ou ponto decimal são aceites. Uma célula com texto que não é
  número fica com contorno vermelho e é tratada como valor em falta.
* Clique no cabeçalho de uma coluna para dar nome à variável.
* Para colar do Excel: copie as colunas (com ou sem linha de cabeçalho), cole na caixa da direita, carregue em
  **Analisar**, confirme a coluna de origem de cada variável e carregue em **Importar**.

## Testes

```bash
python3 ferramentas/gerar.py        # gera Src/, colar/ e docs/formulas.md e valida contra o esquema oficial
python3 testes/executar_testes.py   # corre as fórmulas no interpretador Power Fx e compara com a referência
```

Resultados em `testes/resultados/comparacao.md`.
