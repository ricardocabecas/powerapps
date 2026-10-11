# Notas técnicas — decisões, fontes e limitações

## Documentação Microsoft consultada

O site `learn.microsoft.com` está bloqueado pela política de rede do ambiente onde a app foi construída, por isso
a documentação foi lida diretamente nos repositórios fonte oficiais da Microsoft no GitHub (são o mesmo
conteúdo publicado no Learn), em outubro de 2026:

| Tema | Ficheiro fonte (repositório) |
|---|---|
| Código fonte das canvas apps (`.pa.yaml`), formatos e versões do esquema | `MicrosoftDocs/powerapps-docs` → `powerapps-docs/maker/canvas-apps/power-apps-yaml.md` |
| Vista de código, copiar e colar YAML no Studio | `MicrosoftDocs/powerapps-docs` → `powerapps-docs/maker/canvas-apps/code-view.md` |
| Esquema oficial `pa.schema.yaml` v3.0 | `microsoft/PowerApps-Tooling` → `schemas/pa-yaml/v3.0/pa.schema.yaml` (cópia em `ferramentas/pa.schema.v3.0.yaml`) |
| Exemplos oficiais de ecrãs `.pa.yaml` | `microsoft/PowerApps-Tooling` → `src/schemas-tests/pa-yaml/v3.0/Examples/Src/Screens/Screen1.pa.yaml` |
| Gramática YAML das fórmulas (`=`, blocos multilinha, `#` e `:`) | `MicrosoftDocs/power-platform` → `power-platform/power-fx/yaml-formula-grammar.md` |
| Separadores por região (`,`/`;` e `;`/`;;`) | `MicrosoftDocs/power-platform` → `power-platform/power-fx/global.md` |
| Referência de funções (`Text`, `Value`, `Split`, `Sequence`, `Index`, `With`, `Table`, `Patch`, `Select`, trigonometria…) | `MicrosoftDocs/power-platform` → `power-platform/power-fx/reference/*.md` |
| Gramática de identificadores (permite `_` inicial) | `MicrosoftDocs/power-platform` → `power-platform/power-fx/expression-grammar.md` |

## O que a documentação diz e como foi aplicado

1. **Formato atual**: o único formato ativo é o *Source code* (`*.pa.yaml`). O formato da pré-visualização
   (sem versão) e o `*.fx.yaml` estão descontinuados e **não podem ser colados**. Os ficheiros desta app seguem
   o esquema v3.0: `Screens:` → nome do ecrã → `Properties` e `Children`; cada controlo é um item de lista
   `- Nome:` com `Control`, opcionalmente `Variant`, `Properties` e `Children`.
2. **Versão dos controlos**: «If no version is specified, the most current version of the control is used.»
   Por isso os ficheiros indicam só o tipo (`Control: Label`, `Control: Classic/Button`, …).
3. **Controlos clássicos**: os exemplos oficiais usam o prefixo `Classic/` para controlos clássicos que têm
   equivalente moderno (ex.: `Classic/Icon`). Esta app usa só controlos clássicos:
   `Label`, `Classic/Button`, `Classic/TextInput`, `Classic/DropDown`, `Gallery`, `Image`, `HtmlViewer`, `Rectangle`.
   Se o seu Studio recusar algum identificador, veja a secção «Resolução de problemas» do README.
4. **Galeria**: usa-se a variante documentada no exemplo oficial
   (`BrowseLayout_Vertical_TwoTextOneImageVariant_ver5.0`); os controlos interiores são os definidos no ficheiro.
5. **Fórmulas**: começam todas por `=`. Quando contêm `:` ou `#` (por exemplo `"data:image/svg+xml"` ou o
   formato `"#,##0.0000"`) ou ocupam várias linhas, são escritas como bloco YAML `|-`, como manda a gramática.
6. **Região**: «The app itself is stored in a language agnostic manner» — os ficheiros guardam as fórmulas no
   formato invariante (ponto decimal, `,` e `;`). O Studio mostra-as a cada autor com os separadores da sua região.
   Nos documentos para colar à mão (README e `docs/formulas.md`) as fórmulas estão em sintaxe pt-PT.
7. **Colar código**: a vista de código permite copiar e colar controlos (Ctrl+C / Ctrl+V ou menu *Colar código*);
   o Studio valida o código antes de criar os controlos e o navegador tem de dar acesso à área de transferência.
   A única limitação documentada é o objeto **App**, que não pode ser copiado nem colado — por isso esta app não
   precisa de nada em `App` (a inicialização está no `OnVisible` do primeiro ecrã).
8. **`Text` com idioma**: «If the custom format includes a period, … the language-format placeholder specifies
   whether the period is a decimal separator». Por isso todos os formatos levam `[$-en-US]` e o resultado é pedido em
   `"pt-PT"` (3.º argumento).
9. **`Select`** apenas *coloca em fila* o `OnSelect` de outro controlo; para evitar problemas de ordem, a app não
   usa `Select`: os resultados são fórmulas reativas.
10. **`Sequence`** está limitado a 50 000 registos; a integração numérica usa 300 nós por integral.

## Problema encontrado no esquema oficial

A expressão regular de `CodeComponent-ComponentName` no `pa.schema.yaml` v3.0 tem um parêntese a menos
(`^([a-zA-Z][a-zA-Z0-9]{1,7})_)?…`). Os validadores de JSON Schema recusam o esquema por isso. O gerador corrige
essa expressão **apenas em memória** antes de validar (só afeta controlos PCF, que esta app não usa).

## Interpretador Power Fx usado nos testes

Pacote NuGet `Microsoft.PowerFx.Interpreter` 1.8.1 em .NET 8 (`testes/motor-powerfx`). Configuração:
`Features.PowerFxV1`, `NumberIsFloat = true` (as canvas apps usam números de vírgula flutuante), funções
`Set`/`Collect` ativas. Os controlos são simulados com registos (`{Selected: {Value: …}}`, `{Text: …}`).

Diferenças conhecidas em relação ao Power Apps Studio:

* O interpretador **não aceita** o marcador `[$-en-US]` dentro do formato de `Text` (dá «argumentos inválidos»).
  O motor de testes retira-o antes de avaliar — no interpretador o formato já é lido em invariante, que é o que o
  marcador garante no Studio. Nos ficheiros `.pa.yaml` o marcador fica.
* `GroupBy` não está implementado no interpretador; a app não o usa (usa `Distinct` + `CountIf`/`Filter`).
* Funções só de canvas (`Navigate`, `Notify`, `Reset`, `Patch` numa coleção…) são verificadas apenas quanto à
  sintaxe.
* O separador de milhares de `Text(...; "pt-PT")` no interpretador é um espaço (U+00A0/U+202F). No Studio pode ser
  outro espaço; isso não afeta os cálculos.
