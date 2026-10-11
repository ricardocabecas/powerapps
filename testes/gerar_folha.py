"""Gera docs/folha-verificacao.md: valores esperados (calculados com numpy/scipy) para confirmar na app,
usando os dados de exemplo que a app carrega na primeira abertura."""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import dados_teste as D  # noqa: E402
from referencia import descritiva as RD, frequencias as RF, regressao as RR, inferencia as RI  # noqa: E402
from referencia import colagem as RC  # noqa: E402

NB = " "


def f(v, casas=4):
    if v is None:
        return "n.d."
    v = 0.0 if abs(v) < 0.5 * 10 ** -casas else v
    s = f"{v:,.{casas}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", " ")


def fp(p):
    return "< 0,0001" if p < 0.0001 else f(p)


def main():
    E = D.DADOS_EXEMPLO
    alt = [r[1] for r in E]
    peso = [r[2] for r in E]
    nota = [r[3] for r in E]
    sexo = [r[4] for r in E]
    turma = [r[5] for r in E]
    L = []
    a = L.append
    a("# Folha de verificação — valores esperados na app")
    a("")
    a("> Gerada por `testes/gerar_folha.py`. Os valores esperados foram calculados com **numpy/scipy** (implementação")
    a("> de referência), não com as fórmulas da app. Use os **dados de exemplo** (20 estudantes) que a app carrega na")
    a("> primeira abertura — ou carregue em *Repor dados de exemplo* no ecrã Dados.")
    a(">")
    a("> As mesmas fórmulas já foram executadas no interpretador Power Fx (ver `testes/resultados/comparacao.md`);")
    a("> esta folha serve para confirmar que, **dentro do Power Apps Studio**, tudo se comporta igual.")
    a("")
    a("Marque cada linha depois de confirmar. Os números devem coincidir em todas as casas mostradas.")
    a("")

    # Dados
    a("## 1. Ecrãs Início e Dados")
    a("")
    a("| ✓ | Ação | Resultado esperado |")
    a("|---|---|---|")
    a("| ☐ | Abrir a app (pré-visualização, F5) | Abre o ecrã **Início** com «Dados atuais: 20 linhas · Variáveis numéricas: Altura (cm), Peso (kg), Nota (0-20) · Variáveis de grupo: Sexo, Turma» e 7 cartões |")
    a("| ☐ | Carregar no cartão «1. Dados» | Tabela com 20 linhas; cabeçalhos «Altura (cm)», «Peso (kg)», «Nota (0-20)», «Sexo», «Turma» |")
    a("| ☐ | Na linha 1, escrever `165,5` em Altura e sair da célula | Fica `165,5`; o resumo continua com 0 células vazias |")
    a("| ☐ | Escrever `abc` numa célula numérica | Aviso «não é um número válido»; contorno vermelho; a célula conta como vazia |")
    a("| ☐ | Escrever `1.5` (com ponto) | É aceite e mostrado como `1,5` |")
    a("| ☐ | Carregar em *Repor dados de exemplo* | Volta aos 20 estudantes |")
    cola = D.COLAGENS["invalidos"]
    ref = RC.importar(cola, "Automático", D.NOMES_EXEMPLO)
    a("| ☐ | Colar na caixa da direita o texto abaixo* e carregar em *Analisar* | «Linhas com dados: 5 · Colunas: 2»; «Primeira linha: cabeçalho (nomes: X; Y)»; "
      "«⚠ 2 valor(es) inválido(s)»: linha 3, X: «abc» e linha 4, Y: «1,2,3» |")
    a(f"| ☐ | Carregar em *Importar (substituir dados)* | {len(ref['Linhas'])} linhas; variáveis 1 e 2 passam a chamar-se X e Y; "
      "notificação com o aviso dos 2 valores inválidos |")
    a("| ☐ | Carregar em *Repor dados de exemplo* antes de continuar | Volta aos 20 estudantes |")
    a("")
    a("\\* Texto a colar (pode copiar destas 6 linhas para o Excel em 2 colunas e daí para a app, ou escrever com tabulações):")
    a("")
    a("```")
    a(cola.replace("\r\n", "\n").rstrip("\n").replace("\t", "<TAB>"))
    a("```")
    a("")

    # Descritiva
    a("## 2. Ecrã Descritiva")
    a("")
    for nome, vals in [("Altura (cm)", alt), ("Nota (0-20)", nota)]:
        r1, r2, r3 = (RD.descritiva(vals, m) for m in (1, 2, 3))
        a(f"**Variável: {nome}, sem grupos**")
        a("")
        a("| ✓ | Medida | Valor esperado |")
        a("|---|---|---|")
        for rot, k, c in [("n", "n", 0), ("Soma", "soma", 4), ("Média", "media", 4), ("Mediana", "mediana", 4),
                          ("Mínimo", "minimo", 4), ("Máximo", "maximo", 4), ("Amplitude total", "amplitude", 4),
                          ("Variância amostral (n − 1)", "varA", 4), ("Desvio padrão amostral", "dpA", 4),
                          ("Variância populacional (n)", "varP", 4), ("Desvio padrão populacional", "dpP", 4)]:
            a(f"| ☐ | {rot} | {f(r1[k], c)} |")
        a(f"| ☐ | Moda | {r1['moda']} |")
        a(f"| ☐ | CV | {f(r1['cv'], 2)} % |")
        a(f"| ☐ | Q₁ / Q₃ / AIQ — QUARTIL.INC | {f(r1['q1'])} / {f(r1['q3'])} / {f(r1['q3'] - r1['q1'])} |")
        a(f"| ☐ | Q₁ / Q₃ / AIQ — QUARTIL.EXC / SPSS | {f(r2['q1'])} / {f(r2['q3'])} / {f(r2['q3'] - r2['q1'])} |")
        a(f"| ☐ | Q₁ / Q₃ / AIQ — mediana de cada metade | {f(r3['q1'])} / {f(r3['q3'])} / {f(r3['q3'] - r3['q1'])} |")
        a("")
    a("**Altura (cm), agrupar por Sexo** (colunas Total, F, M):")
    a("")
    a("| ✓ | Medida | Total | F | M |")
    a("|---|---|---|---|---|")
    gF = RD.descritiva([x for x, s in zip(alt, sexo) if s == "F"])
    gM = RD.descritiva([x for x, s in zip(alt, sexo) if s == "M"])
    tt = RD.descritiva(alt)
    for rot, k in [("n", "n"), ("Média", "media"), ("Desvio padrão amostral", "dpA")]:
        c = 0 if k == "n" else 4
        a(f"| ☐ | {rot} | {f(tt[k], c)} | {f(gF[k], c)} | {f(gM[k], c)} |")
    a("")

    # Frequências
    a("## 3. Ecrã Frequências")
    a("")
    rc = RF.classes(alt)
    a("**Altura (cm), «Classes (dados agrupados)», caixas vazias** → regra de Sturges")
    a("")
    a(f"Resumo: n = 20 · {rc['k']} classes · Sturges k = {rc['kSturges']} · h = {RF.fmt_curto(rc['h'])} · "
      f"início {RF.fmt_curto(rc['a'])}. Deve aparecer um **histograma** com {rc['k']} barras contíguas.")
    a("")
    a("| ✓ | Classe | nᵢ | fᵢ | Nᵢ | Fᵢ |")
    a("|---|---|---|---|---|---|")
    for l in rc["Linhas"]:
        a(f"| ☐ | {l['Classe']} | {l['ni']} | {f(l['fi'])} | {l['Ni']} | {f(l['Fi'])} |")
    a("")
    rc2 = RF.classes(alt, 3, 160, 10)
    a(f"**Mesmos dados com n.º de classes = 3, início = 160, amplitude = 10** → aviso «⚠ {rc2['Fora']} valor(es) "
      f"ficaram fora das classes» e contagens " + ", ".join(f"{l['Classe']}: {l['ni']}" for l in rc2["Linhas"]) + ".")
    a("")
    rd = RF.discreta(nota)
    a("**Nota (0-20), «Valores distintos»** → **diagrama de barras** com " + str(len(rd)) + " barras:")
    a("")
    a("| ✓ | Valor | nᵢ | fᵢ (%) | Nᵢ | Fᵢ |")
    a("|---|---|---|---|---|---|")
    for l in rd:
        a(f"| ☐ | {l['Classe']} | {l['ni']} | {f(l['fi'] * 100, 2)} | {l['Ni']} | {f(l['Fi'])} |")
    a("")
    a("**Sexo** → a lista «Tipo de tabela» fica desativada; F: 10, M: 10 (fᵢ = 0,5000 cada).")
    a("")

    # Regressão
    rr = RR.regressao(alt, peso, 172.5)
    a("## 4. Ecrã Regressão")
    a("")
    a("x = Altura (cm), y = Peso (kg), valor de x = `172,5`")
    a("")
    a("| ✓ | Medida | Valor esperado |")
    a("|---|---|---|")
    for rot, k in [("n", "n"), ("x̄", "mediaX"), ("ȳ", "mediaY"), ("Sxx", "Sxx"), ("Syy", "Syy"), ("Sxy", "Sxy"),
                   ("Covariância amostral", "cov"), ("r", "r"), ("R²", "r2"), ("Declive b", "b"),
                   ("Ordenada na origem a", "a"), ("ŷ para x = 172,5", "previsao"), ("t (H₀: ρ = 0)", "tR"),
                   ("gl", "glR")]:
        a(f"| ☐ | {rot} | {f(rr[k], 0 if k in ('n', 'glR') else 4)} |")
    a(f"| ☐ | Valor de p (ρ = 0) | {fp(rr['pR'])} |")
    a(f"| ☐ | Equação | ŷ = {f(rr['a'])} + {f(rr['b'])} · x |")
    a("| ☐ | Gráfico | 20 pontos e uma reta vermelha crescente; eixos com vírgula decimal |")
    a("| ☐ | Escrever `250` no valor de x | Aviso de extrapolação |")
    a("")

    # Testes t
    a("## 5. Ecrã Testes t (α = 0,05)")
    a("")
    a("| ✓ | Configuração | t | gl | p | Decisão |")
    a("|---|---|---|---|---|---|")

    def lt(desc, r, gl_casas=0):
        dec = "rejeita-se H₀" if r["p"] <= 0.05 else "não se rejeita H₀"
        a(f"| ☐ | {desc} | {f(r['t'])} | {f(r['gl'], gl_casas)} | {fp(r['p'])} | {dec} |")
    lt("Uma amostra, Altura, μ₀ = 170, bilateral", RI.teste_t(1, alt, d0=170, alt=1))
    lt("Uma amostra, Altura, μ₀ = 165, unilateral à direita", RI.teste_t(1, alt, d0=165, alt=3))
    aF = [x for x, s in zip(alt, sexo) if s == "F"]
    aM = [x for x, s in zip(alt, sexo) if s == "M"]
    lt("Independentes (variâncias iguais), Altura por Sexo, grupo 1 = F, grupo 2 = M, Δ₀ = 0, bilateral",
       RI.teste_t(2, aF, aM, 0, 1))
    lt("Welch, Altura por Sexo, F vs M, bilateral", RI.teste_t(3, aF, aM, 0, 1), 4)
    lt("Emparelhadas, X = Altura, Y = Peso, Δ₀ = 100, bilateral", RI.teste_t(4, alt, peso, 100, 1))
    a("")

    # ANOVA
    a("## 6. Ecrã ANOVA (α = 0,05)")
    a("")
    niv = sorted(set(turma))
    ra = RI.anova([[x for x, t in zip(alt, turma) if t == n] for n in niv])
    a("Variável Altura (cm), fator Turma:")
    a("")
    a("| ✓ | Fonte | SQ | gl | QM | F | p |")
    a("|---|---|---|---|---|---|---|")
    a(f"| ☐ | Entre grupos | {f(ra['SQE'])} | {ra['glE']} | {f(ra['QME'])} | {f(ra['F'])} | {fp(ra['p'])} |")
    a(f"| ☐ | Dentro dos grupos | {f(ra['SQD'])} | {ra['glD']} | {f(ra['QMD'])} | | |")
    a(f"| ☐ | Total | {f(ra['SQT'])} | {ra['glT']} | | | |")
    a("")
    a("Decisão esperada: não se rejeita H₀.")
    a("")
    rs = RI.anova([aF, aM])
    a(f"Controlo cruzado: fator **Sexo** (2 grupos) → F = {f(rs['F'])}, p = {fp(rs['p'])}, igual ao p do teste t com "
      "variâncias iguais (F = t²).")
    a("")

    # Qui-quadrado
    a("## 7. Ecrã Qui-quadrado (α = 0,05)")
    a("")
    a("| ✓ | Configuração | χ² | gl | p | Observações |")
    a("|---|---|---|---|---|---|")
    from collections import Counter
    ct = Counter(turma)
    q1 = RI.qui_aderencia([ct[k] for k in sorted(ct)])
    a(f"| ☐ | Aderência, variáveis, Turma, proporções iguais | {f(q1['qui2'])} | {q1['gl']} | {fp(q1['p'])} | "
      f"esperadas 6,6667 cada |")
    q2 = RI.qui_aderencia([ct[k] for k in sorted(ct)], [0.5, 0.25, 0.25])
    a(f"| ☐ | Aderência, Turma, proporções indicadas `0,5; 0,25; 0,25` | {f(q2['qui2'])} | {q2['gl']} | {fp(q2['p'])} | "
      "esperadas 10; 5; 5 |")
    cst = Counter(zip(sexo, turma))
    tab = [[cst[(s, t)] for t in sorted(set(turma))] for s in sorted(set(sexo))]
    q3 = RI.qui_independencia(tab)
    a(f"| ☐ | Independência, variáveis, linhas Sexo × colunas Turma | {f(q3['qui2'])} | {q3['gl']} | {fp(q3['p'])} | "
      f"aviso de Cochran: {q3['baixas']} de 6 células com E < 5 |")
    q4 = RI.qui_independencia([[30, 10], [15, 25]])
    a(f"| ☐ | Independência, tabela colada (abaixo) | {f(q4['qui2'])} | {q4['gl']} | {fp(q4['p'])} | "
      "esperadas 22,5 e 17,5 |")
    q5 = RI.qui_aderencia([8, 12, 9, 11, 6, 14])
    a(f"| ☐ | Aderência, tabela colada de um dado (abaixo), proporções iguais | {f(q5['qui2'])} | {q5['gl']} | "
      f"{fp(q5['p'])} | categorias 1 a 6 |")
    a("")
    a("Tabela de contingência a colar (3 linhas, tabulações entre colunas; o 1.º campo da 1.ª linha fica vazio):")
    a("")
    a("```\n<TAB>Sim<TAB>Não\nHomem<TAB>30<TAB>10\nMulher<TAB>15<TAB>25\n```")
    a("")
    a("Tabela de um dado (aderência):")
    a("")
    a("```\nFace<TAB>Obs\n1<TAB>8\n2<TAB>12\n3<TAB>9\n4<TAB>11\n5<TAB>6\n6<TAB>14\n```")
    a("")

    a("## 8. Verificações de interface (não automatizáveis aqui)")
    a("")
    a("| ✓ | O quê | Como confirmar |")
    a("|---|---|---|")
    for o, c in [
        ("Colagem dos ecrãs", "Cada ficheiro de `Src/` cola sem erros e cria o ecrã com o nome indicado"),
        ("Navegação", "Os 8 botões da barra superior (Início … Qui-quadrado) e os 7 cartões do Início mudam de ecrã; o botão do ecrã atual aparece branco"),
        ("Separador decimal", "Todos os números aparecem com vírgula decimal (ex.: 169,4500)"),
        ("Tabelas HTML", "As tabelas dos ecrãs Descritiva, Regressão, Testes t, ANOVA e Qui-quadrado aparecem formatadas e cabem no painel"),
        ("Gráficos SVG", "Histograma, diagrama de barras e dispersão aparecem no controlo Imagem, com texto legível"),
        ("Listas pendentes", "Mudar a variável/teste atualiza os resultados de imediato (sem botão Calcular)"),
        ("Campos que aparecem e desaparecem", "Testes t: os campos de grupo só aparecem nos testes independentes com «variável + grupo»"),
        ("Desempenho", "Com 200 linhas de dados, cada ecrã responde em menos de 1–2 segundos"),
    ]:
        a(f"| ☐ | {o} | {c} |")
    a("")
    out = os.path.join(AQUI, "..", "docs", "folha-verificacao.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("docs/folha-verificacao.md escrito")


if __name__ == "__main__":
    main()
