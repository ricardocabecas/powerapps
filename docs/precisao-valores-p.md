# Precisão dos valores de p calculados em Power Fx

> Gerado por `testes/precisao_valores_p.py`, que executa as fórmulas da app no interpretador
> Microsoft.PowerFx.Interpreter 1.8.1 e compara com `scipy.stats` (1.18.1).

## Método usado na app

Os valores de p são integrais das funções densidade. O Power Fx não tem as funções Gama e Beta incompletas,
por isso a app calcula-os por **integração numérica** com `Sequence` (gera os nós) e `Sum` (soma pesada):

1. **Mudança de variável** que torna o integrando limitado e suave no intervalo de integração:
   * F(d₁, d₂) e t(ν) (t² ~ F(1, ν)): x = sen²θ na distribuição Beta, o que dá o integrando
     sen^(d₁−1)θ · cos^(d₂−1)θ em [0, π/2], sem as singularidades da densidade em 0;
   * χ²(k): u = v², o que dá v^(k−1) e^(−v²/2), sem a singularidade em 0 quando k = 1.
2. **Razão de dois integrais** (cauda / total): as constantes de normalização cancelam-se.
3. **Gauss-Legendre composto**, 3 nós por subintervalo × 100 subintervalos = 300 nós por integral, só na zona
   onde o integrando não é desprezável (± 10 «larguras» em torno do máximo).
4. Integrando calculado em **escala logarítmica** (`Exp(L − Lmax)`) para não haver números fora do alcance
   da vírgula flutuante com muitos graus de liberdade.

## Resultados

| Distribuição | Grelha testada | Pontos | Erro absoluto máximo | Onde | Pontos com erro ≥ 5×10⁻⁵ | Pontos que mudam na 4.ª casa |
|---|---|---|---|---|---|---|
| t | ν ∈ {1, 1.05, 1.3, 1.5, 1.8, 2, 2.5, 3, 4, 5, 7, 10, 15, 20, 30, 50, 100, 300, 1000, 10000, 100000}; |t| de 0 a 100 (p bilateral) | 336 | 2.3e-07 | argumentos (1, 1.3): app 0.4672421557, scipy 0.4672423876 | 0 | 0 |
| F | d₁ ∈ {1, 2, 3, 4, 5, 8, 10, 20, 40}; d₂ ∈ {1, 2, 3, 5, 8, 10, 20, 30, 60, 120, 500, 5000}; F de 0,01 a 1000 | 1404 | 4.9e-11 | argumentos (0.1, 4, 5000): app 0.9824716644, scipy 0.9824716644 | 0 | 0 |
| χ² | k ∈ {1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 50, 100, 200, 500, 1000}; χ² de 0,001 a 1200 | 357 | 5.5e-11 | argumentos (1, 4): app 0.9097959896, scipy 0.9097959896 | 0 | 0 |

Tarefas que falharam no interpretador: 0.

## Conclusão

Em toda a grelha, **nenhum valor de p difere do scipy na 4.ª casa decimal** (a app mostra 4 casas e
«< 0,0001» para valores menores). O maior erro aparece no teste t com graus de liberdade não inteiros perto de 1
(caso de Welch com amostras muito pequenas) e é da ordem de 10⁻⁷. Não foi preciso recorrer a tabelas de valores
críticos.

Zonas não cobertas pela grelha e que a app não usa: distribuição F com d₂ não inteiro entre 1 e 2 (o erro sobe
para ~3×10⁻⁵ com 100 subintervalos, ainda abaixo de meia unidade da 4.ª casa). Se no futuro for preciso mais
precisão, basta aumentar `N_SUB` em `ferramentas/gerador/f_inferencia.py` (nessa zona o erro desce cerca de
3 vezes sempre que se duplica o n.º de subintervalos), à custa de mais cálculo.
