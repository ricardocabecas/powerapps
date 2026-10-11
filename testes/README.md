# Testes

| Ficheiro / pasta | Conteúdo |
|---|---|
| `dados_teste.py` | Conjuntos de dados pequenos e casos limite (texto colado, n = 1 e 2, valores repetidos, variância nula, média zero, valores em falta, classes com valores nas fronteiras, x ou y constantes, gl fracionários de Welch, células com frequência esperada baixa, tabelas coladas com inválidos ou linhas vazias) |
| `referencia/` | Implementação de referência independente em Python (numpy, scipy.stats, aritmética exata com `Fraction` nas classes) |
| `motor-powerfx/` | Programa .NET 8 que executa fórmulas com o interpretador open source **Microsoft.PowerFx.Interpreter 1.8.1** |
| `motor.py` | Ligação Python ↔ motor (simula listas pendentes e caixas de texto com registos) |
| `fase1_dados.py` … `fase5_inferencia.py` | Casos de cada fase: executam as **mesmas cadeias de fórmulas** que estão nos ficheiros `.pa.yaml` e comparam com a referência |
| `executar_testes.py` | Corre tudo: sintaxe de todas as fórmulas (invariante e pt-PT) + casos das 5 fases; gera a folha de verificação |
| `precisao_valores_p.py` | Mede a precisão dos valores de p numa grelha alargada (→ `docs/precisao-valores-p.md`) |
| `gerar_folha.py` | Gera `docs/folha-verificacao.md` a partir da referência scipy |
| `resultados/comparacao.md` | Relatório da última execução (um ✅/❌ por caso, com os valores obtidos) |
| `resultados/resultados.json` | O mesmo em JSON |
| `resultados/graficos/` | SVG produzidos pelas fórmulas da app nos casos de teste (abrem em qualquer navegador) |

Tolerâncias: 10⁻⁹ (relativa) nas medidas descritivas, regressão, estatísticas de teste e graus de liberdade;
10⁻⁶ (absoluta) nos valores de p, que vêm de integração numérica (a app mostra 4 casas decimais).
