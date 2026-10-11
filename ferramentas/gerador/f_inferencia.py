"""Inferência: valores de p por integração numérica (Power Fx puro) e testes de hipóteses.

Valores de p
------------
Todas as distribuições usadas (t, F e qui-quadrado) reduzem-se a dois integrais com integrandos
limitados e suaves, depois de uma mudança de variável:

* F(d1, d2):   P(F > f) = ∫[θ0, π/2] sen^(d1−1)θ · cos^(d2−1)θ dθ  /  ∫[0, π/2] (o mesmo) dθ,
               com θ0 = atan(√(d1·f/d2))     (substituição x = sen²θ na distribuição Beta)
* t(ν):        P(|T| > |t|) = P(F(1, ν) > t²)   (o caso d1 = 1 do anterior)
* χ²(k):       P(χ² > x) = ∫[√x, ∞] v^(k−1) e^(−v²/2) dv  /  ∫[0, ∞] (o mesmo) dv   (substituição u = v²)

As constantes de normalização (funções Gama) cancelam-se na razão, por isso não é preciso a função
Gama, que o Power Fx não tem. Cada integral é calculado pela regra de Gauss-Legendre composta com
3 nós por subintervalo e 100 subintervalos (300 nós, gerados com Sequence e somados com Sum), só na
zona onde o integrando não é desprezável (± 10 «larguras» à volta do máximo). O integrando é avaliado
em escala logarítmica (Exp(L − Lmax)) para evitar números demasiado grandes ou pequenos.
"""
from .f_comum import num, fmt, indice_num
from .f_frequencias import fmt_curto

N_SUB = 100                       # subintervalos de Gauss-Legendre
G3 = "0.3872983346207417"         # √(3/5) / 2

ALTERNATIVAS = ["Bilateral (≠)", "Unilateral à esquerda (<)", "Unilateral à direita (>)"]
ALFAS = ["0,10", "0,05", "0,01", "0,001"]


def _nos():
    """Nós (u em ]0,1[) e pesos de Gauss-Legendre composto com N_SUB subintervalos."""
    return (f"ForAll(Sequence({3 * N_SUB}, 0) As _i, "
            f"With({{_s: RoundDown(_i.Value / 3, 0), _m: Mod(_i.Value, 3)}}, "
            f"{{u: (_s + 0.5 + (_m - 1) * {G3}) / {N_SUB}, w: If(_m = 1, 8 / 9, 5 / 9) / {2 * N_SUB}}}))")


def _razao(L, lo, hi, a):
    """∫[a, hi] e^L / ∫[lo, hi] e^L, com L uma expressão na variável t (texto com '{t}')."""
    Lt = L.replace("{t}", "t")
    return f"""With({{_nd: {_nos()}}},
        With({{_Ltot: ForAll(_nd, With({{t: {lo} + u * ({hi} - {lo})}}, {{L: {Lt}, w: w * ({hi} - {lo})}})),
              _Lcau: ForAll(_nd, With({{t: {a} + u * ({hi} - {a})}}, {{L: {Lt}, w: w * ({hi} - {a})}}))}},
            With({{_M: Max(_Ltot, L)}},
                Min(1, Sum(_Lcau, Exp(L - _M) * w) / Sum(_Ltot, Exp(L - _M) * w)))))"""


def p_f(f, d1, d2):
    """P(F(d1, d2) > f): valor de p do teste F (cauda direita)."""
    return f"""With({{_f: {f}, _d1: {d1}, _d2: {d2}}},
    If(_f <= 0, 1,
    With({{_t0: Atan(Sqrt(_d1 * _f / _d2)), _sg: 1 / Sqrt(Max(_d1 + _d2 - 2, 1)),
          _ts: If(_d2 > 1, Atan(Sqrt(Max(_d1 - 1, 0) / (_d2 - 1))), Pi() / 2)}},
    With({{_lo: Max(0, _ts - 10 * _sg), _hi: Min(Pi() / 2, _ts + 10 * _sg)}},
        If(_t0 >= _hi, 0,
            {_razao("(_d1 - 1) * Ln(Sin({t})) + (_d2 - 1) * Ln(Cos({t}))", "_lo", "_hi", "Max(_t0, _lo)")})))))"""


def p_t_bilateral(t, gl):
    """P(|T| > |t|) com T ~ t(gl), via P(F(1, gl) > t²)."""
    return p_f(f"Power({t}, 2)", "1", gl)


def p_t(t, gl, alt):
    """Valor de p do teste t segundo a hipótese alternativa (1 ≠, 2 <, 3 >)."""
    return (f"With({{_tt: {t}, _p2: {p_t_bilateral('(' + t + ')', gl)}}}, "
            f"Switch({alt}, 1, _p2, 2, If(_tt < 0, _p2 / 2, 1 - _p2 / 2), If(_tt > 0, _p2 / 2, 1 - _p2 / 2)))")


def p_qui(x, k):
    """P(χ²(k) > x)."""
    return f"""With({{_x: {x}, _k: {k}}},
    If(_x <= 0, 1,
    With({{_v0: Sqrt(_x), _vs: Sqrt(Max(_k - 1, 0))}},
    With({{_lo: Max(0, _vs - 10), _hi: _vs + 10}},
        If(_v0 >= _hi, 0,
            {_razao("(_k - 1) * Ln({t}) - {t} * {t} / 2", "_lo", "_hi", "Max(_v0, _lo)")})))))"""


def fmt_p(p):
    return f'With({{_pp: {p}}}, If(IsBlank(_pp), "n.d.", _pp < 0.0001, "< 0,0001", {fmt("_pp")}))'


def igual_p(p):
    """' = 0,0123' ou ' < 0,0001' (para escrever a seguir a 'p')."""
    return f'With({{_pp: {p}}}, If(IsBlank(_pp), " = n.d.", _pp < 0.0001, " < 0,0001", " = " & {fmt("_pp")}))'


def alfa(drp):
    return f'Value(Substitute({drp}.Selected.Value, ",", "."), "en-US")'


def indice_alt(drp):
    return f'Switch({drp}.Selected.Value, "{ALTERNATIVAS[1]}", 2, "{ALTERNATIVAS[2]}", 3, 1)'


# ---------------------------------------------------------------------------
# Textos comuns às conclusões
# ---------------------------------------------------------------------------
def alfa_pct(a="_alfa"):
    return f'{fmt_curto(a + " * 100")} & " %"'


def bloco_decisao(p, a, frase_h1, motivo_nd):
    """HTML com a decisão e a conclusão por extenso (rejeita H0 se p ≤ α)."""
    return f"""If(IsBlank({p}),
        "<div style='border-left:4px solid #b00020;padding:6px 10px;background:#fdecee'>Não é possível calcular o teste: " & {motivo_nd} & "</div>",
        If({p} <= {a},
            "<div style='border-left:4px solid #107c10;padding:6px 10px;background:#e8f5e8'><b>Decisão: rejeita-se H₀</b> (p" & {igual_p(p)} & " ≤ α = " & {fmt_curto(a)} & ").<br>" &
            "Conclusão: ao nível de significância de " & {alfa_pct(a)} & ", há evidência estatística de que " & {frase_h1} & ".</div>",
            "<div style='border-left:4px solid #1f4e79;padding:6px 10px;background:#eef3f9'><b>Decisão: não se rejeita H₀</b> (p" & {igual_p(p)} & " > α = " & {fmt_curto(a)} & ").<br>" &
            "Conclusão: ao nível de significância de " & {alfa_pct(a)} & ", não há evidência estatística suficiente de que " & {frase_h1} & ".</div>"))"""


def esc_html(t):
    return f'Substitute(Substitute(Substitute({t}, "&", "&amp;"), "<", "&lt;"), ">", "&gt;")'


def tabela_html(cabecalhos, linhas_expr, alinhar=None):
    """Tabela HTML simples: cabeçalhos fixos e corpo dado por uma expressão de texto."""
    th = "".join(f"<th style='padding:5px 8px;text-align:{'left' if i == 0 else 'right'}'>{c}</th>"
                 for i, c in enumerate(cabecalhos))
    return (f""""<table style='border-collapse:collapse;margin:4px 0 10px 0'><tr style='background:#1f4e79;color:#ffffff'>{th}</tr>" & """
            f"""{linhas_expr} & "</table>\"""")


def td(v, esq=False):
    return f""""<td style='padding:4px 8px;text-align:{'left' if esq else 'right'};border-bottom:1px solid #e1e5ea'>" & {v} & "</td>\""""


ESTILO = "\"<div style='font-family:Segoe UI,Arial;font-size:13px;color:#212529;line-height:1.45'>\""


def secao(titulo):
    return f'"<h4 style=\'margin:12px 0 4px 0;color:#1f4e79\'>{titulo}</h4>"'


# ---------------------------------------------------------------------------
# Testes t
# ---------------------------------------------------------------------------
TIPOS_T = ["Uma amostra",
           "Duas amostras independentes (variâncias iguais)",
           "Duas amostras independentes (Welch, variâncias diferentes)",
           "Amostras emparelhadas"]
FORMATOS_IND = ["Variável numérica + variável de grupo", "Duas colunas numéricas"]


def indice_cat(drp):
    return f"Switch({drp}.Selected.Value, varNomes.C2, 2, 1)"


def niveis(kg):
    """Valores distintos (não vazios) da variável categórica kg, por ordem alfabética."""
    return f"Sort(Filter(Distinct(colDados, Switch({kg}, 1, C1, C2)), !IsBlank(Value)), Value)"


def _amostra(k):
    return f"Filter(ForAll(colDados As _d, {{x: Switch({k}, 1, _d.N1, 2, _d.N2, _d.N3)}}), !IsBlank(x))"


def _amostra_grupo(k, kg, nivel):
    return (f"Filter(ForAll(colDados As _d, {{x: Switch({k}, 1, _d.N1, 2, _d.N2, _d.N3), "
            f"g: Switch({kg}, 1, _d.C1, _d.C2)}}), !IsBlank(x) && g = {nivel})")


def _diferencas(k1, k2):
    return (f"Filter(ForAll(colDados As _d, With({{_a: Switch({k1}, 1, _d.N1, 2, _d.N2, _d.N3), "
            f"_b: Switch({k2}, 1, _d.N1, 2, _d.N2, _d.N3)}}, {{x: If(IsBlank(_a) || IsBlank(_b), Blank(), _a - _b)}})), "
            f"!IsBlank(x))")


def teste_t():
    """Registo com os resultados do teste t escolhido no ecrã scrTestesT."""
    tipos = ", ".join(f'"{t}", {i + 1}' for i, t in enumerate(TIPOS_T))
    vazio = 'FirstN(Table({x: 0}), 0)'
    return f"""With(
    // Opções escolhidas no ecrã
    {{_tipo: Switch(drpTtTipo.Selected.Value, {tipos}, 1),
     _fmt: If(drpTtFormato.Selected.Value = "{FORMATOS_IND[1]}", 2, 1),
     _alt: {indice_alt("drpTtAlternativa")}, _alfa: {alfa("drpTtAlfa")},
     _d0: Coalesce({num("txtTtMu0.Text")}, 0),
     _k1: {indice_num("drpTtVar")}, _k2: {indice_num("drpTtVar2")}, _kg: {indice_cat("drpTtGrupoVar")},
     _gA: drpTtGrupoA.Selected.Value, _gB: drpTtGrupoB.Selected.Value}},
    With(
        // Amostra A (ou diferenças, no teste emparelhado) e amostra B
        {{_A: Switch(_tipo, 1, {_amostra("_k1")}, 4, {_diferencas("_k1", "_k2")},
                If(_fmt = 1, {_amostra_grupo("_k1", "_kg", "_gA")}, {_amostra("_k1")})),
         _B: If(_tipo = 2 || _tipo = 3,
                If(_fmt = 1, {_amostra_grupo("_k1", "_kg", "_gB")}, {_amostra("_k2")}), {vazio})}},
    With({{_n1: CountRows(_A), _n2: CountRows(_B)}},
    With({{_m1: If(_n1 > 0, Average(_A, x)), _m2: If(_n2 > 0, Average(_B, x))}},
    With(
        // Variâncias amostrais (divisor n − 1)
        {{_v1: If(_n1 >= 2, Sum(_A, Power(x - _m1, 2)) / (_n1 - 1)),
         _v2: If(_n2 >= 2, Sum(_B, Power(x - _m2, 2)) / (_n2 - 1))}},
    With(
        // Erro padrão e graus de liberdade de cada teste
        {{_ep: Switch(_tipo,
                1, If(_n1 >= 2, Sqrt(_v1 / _n1)),
                4, If(_n1 >= 2, Sqrt(_v1 / _n1)),
                2, If(_n1 >= 2 && _n2 >= 2,
                      Sqrt(((_n1 - 1) * _v1 + (_n2 - 1) * _v2) / (_n1 + _n2 - 2) * (1 / _n1 + 1 / _n2))),
                If(_n1 >= 2 && _n2 >= 2, Sqrt(_v1 / _n1 + _v2 / _n2))),
         _gl: Switch(_tipo,
                1, If(_n1 >= 2, _n1 - 1),
                4, If(_n1 >= 2, _n1 - 1),
                2, If(_n1 >= 2 && _n2 >= 2, _n1 + _n2 - 2),
                // Welch–Satterthwaite
                If(_n1 >= 2 && _n2 >= 2 && _v1 + _v2 > 0,
                   Power(_v1 / _n1 + _v2 / _n2, 2) /
                   (Power(_v1 / _n1, 2) / (_n1 - 1) + Power(_v2 / _n2, 2) / (_n2 - 1))))}},
    With(
        {{_t: If(!IsBlank(_ep) && _ep > 0,
                (If(_tipo = 2 || _tipo = 3, _m1 - _m2, _m1) - _d0) / _ep)}},
    With(
        {{_p: If(!IsBlank(_t) && _gl > 0, {p_t("_t", "_gl", "_alt").replace(chr(10), chr(10) + "        ")})}},
    {{
        tipo: _tipo, alt: _alt, alfa: _alfa, d0: _d0,
        n1: _n1, n2: _n2, m1: _m1, m2: _m2, v1: _v1, v2: _v2,
        s1: If(!IsBlank(_v1), Sqrt(_v1)), s2: If(!IsBlank(_v2), Sqrt(_v2)),
        sp: If(_tipo = 2 && _n1 >= 2 && _n2 >= 2, Sqrt(((_n1 - 1) * _v1 + (_n2 - 1) * _v2) / (_n1 + _n2 - 2))),
        ep: _ep, t: _t, gl: _gl, p: _p,
        motivo: If(_n1 < 2 || ((_tipo = 2 || _tipo = 3) && _n2 < 2),
                   "cada amostra precisa de pelo menos 2 observações.",
                   "o erro padrão é zero (todos os valores iguais: variância nula), por isso t não está definido.")
    }}
    )))))))
)"""


def html_teste_t():
    nome1 = "drpTtVar.Selected.Value"
    nome2 = "drpTtVar2.Selected.Value"
    grupoA = f'If(_R.tipo = 4, "D", If(drpTtFormato.Selected.Value = "{FORMATOS_IND[1]}", {nome1}, drpTtGrupoA.Selected.Value))'
    grupoB = f'If(drpTtFormato.Selected.Value = "{FORMATOS_IND[1]}", {nome2}, drpTtGrupoB.Selected.Value)'
    rel = 'Switch(_R.alt, 1, "≠", 2, "<", ">")'
    rel_txt = 'Switch(_R.alt, 1, "diferente de", 2, "menor do que", "maior do que")'
    rel_txt2 = 'Switch(_R.alt, 1, "diferente da", 2, "menor do que a", "maior do que a")'
    d0 = fmt_curto("_R.d0")
    linha_amostra = (lambda rot, n, m, s: f'"<tr>" & {td(rot, True)} & {td(fmt(n, 0))} & {td(fmt(m))} & '
                     f'{td(fmt(s))} & {td(fmt(f"If(!IsBlank({s}), Power({s}, 2))"))} & "</tr>"')
    frase = f"""Switch(_R.tipo,
            1, "a média de " & {esc_html(nome1)} & " é " & {rel_txt} & " " & {d0},
            4, "a média das diferenças (" & {esc_html(nome1)} & " − " & {esc_html(nome2)} & ") é " & {rel_txt} & " " & {d0},
            If(_R.d0 = 0,
               "a média de " & {esc_html(nome1)} & " em «" & {esc_html(grupoA)} & "» é " & {rel_txt2} & " média em «" & {esc_html(grupoB)} & "»",
               "a diferença entre as médias (μ₁ − μ₂) é " & {rel_txt} & " " & {d0}))"""
    return f"""With({{_R: {teste_t().replace(chr(10), chr(10) + "    ")}}},
    {ESTILO} &
    {secao("Dados")} &
    {tabela_html(["Amostra", "n", "Média", "Desvio padrão (s)", "Variância (s²)"],
                 'If(_R.tipo = 4, ' + linha_amostra('"Diferenças D = " & ' + esc_html(nome1) + ' & " − " & ' + esc_html(nome2), "_R.n1", "_R.m1", "_R.s1") + ', ' +
                 linha_amostra('If(_R.tipo = 1, ' + esc_html(nome1) + ', "1: " & ' + esc_html(grupoA) + ')', "_R.n1", "_R.m1", "_R.s1") +
                 ' & If(_R.tipo = 2 || _R.tipo = 3, ' + linha_amostra('"2: " & ' + esc_html(grupoB), "_R.n2", "_R.m2", "_R.s2") + ', ""))')} &
    {secao("Hipóteses")} &
    Switch(_R.tipo,
        1, "H₀: μ = " & {d0} & "<br>H₁: μ " & {rel} & " " & {d0} & "<br><span style='color:#5a626a'>μ = média de " & {esc_html(nome1)} & " na população</span>",
        4, "H₀: μ<sub>D</sub> = " & {d0} & "<br>H₁: μ<sub>D</sub> " & {rel} & " " & {d0} & "<br><span style='color:#5a626a'>μ<sub>D</sub> = média da diferença D = " & {esc_html(nome1)} & " − " & {esc_html(nome2)} & " na população</span>",
        "H₀: μ₁ − μ₂ = " & {d0} & "<br>H₁: μ₁ − μ₂ " & {rel} & " " & {d0} & "<br><span style='color:#5a626a'>μ₁ e μ₂ = médias populacionais nas amostras 1 e 2</span>") &
    {secao("Estatística de teste")} &
    Switch(_R.tipo,
        1, "t = (x̄ − μ₀) / (s / √n)",
        4, "t = (d̄ − Δ₀) / (s<sub>D</sub> / √n)",
        2, "t = (x̄₁ − x̄₂ − Δ₀) / (s<sub>p</sub> √(1/n₁ + 1/n₂)), com s<sub>p</sub>² = [(n₁ − 1)s₁² + (n₂ − 1)s₂²] / (n₁ + n₂ − 2) &nbsp; (s<sub>p</sub> = " & {fmt("_R.sp")} & ")",
        "t = (x̄₁ − x̄₂ − Δ₀) / √(s₁²/n₁ + s₂²/n₂)") &
    "<br>Erro padrão = " & {fmt("_R.ep")} & " &nbsp;·&nbsp; <b>t = " & {fmt("_R.t")} & "</b>" &
    {secao("Graus de liberdade")} &
    Switch(_R.tipo, 1, "gl = n − 1 = ", 4, "gl = n − 1 = ", 2, "gl = n₁ + n₂ − 2 = ",
        "gl de Welch–Satterthwaite = (s₁²/n₁ + s₂²/n₂)² / [(s₁²/n₁)²/(n₁ − 1) + (s₂²/n₂)²/(n₂ − 1)] = ") &
    "<b>" & If(_R.tipo = 3, {fmt("_R.gl")}, {fmt("_R.gl", 0)}) & "</b>" &
    {secao("Valor de p")} &
    Switch(_R.alt, 1, "p = P(|T| ≥ |t|)", 2, "p = P(T ≤ t)", "p = P(T ≥ t)") & "<b>" & {igual_p("_R.p")} & "</b>" &
    " &nbsp;<span style='color:#5a626a'>(T segue a distribuição t de Student com os gl indicados)</span>" &
    {secao("Decisão e conclusão")} &
    {bloco_decisao("_R.p", "_R.alfa", frase, "_R.motivo")} &
    If((_R.tipo = 2 || _R.tipo = 3) && _R.v1 > 0 && _R.v2 > 0,
        "<p style='color:#5a626a;font-size:12px'>Razão entre a maior e a menor variância: " &
        {fmt("Max(_R.v1, _R.v2) / Min(_R.v1, _R.v2)", 2)} &
        ". Regra prática: se for superior a 4, prefira o teste de Welch (não assume variâncias iguais).</p>", "") &
    "</div>"
)"""


# ---------------------------------------------------------------------------
# ANOVA a um fator
# ---------------------------------------------------------------------------
FORMATOS_ANOVA = ["Variável numérica + fator (grupo)", "Colunas numéricas como grupos"]


def _resumo_grupo(nome, valores):
    return (f"With({{_v: {valores}}}, With({{_n: CountRows(_v)}}, With({{_m: If(_n > 0, Average(_v, x))}}, "
            f"{{Grupo: {nome}, n: _n, media: _m, soma: Sum(_v, x), sq: Sum(_v, Power(x - _m, 2))}})))")


def anova():
    """Registo com a tabela da ANOVA a um fator (ecrã scrAnova)."""
    por_fator = (f"ForAll({niveis('_kg')} As _G, "
                 f"{_resumo_grupo('_G.Value', _amostra_grupo('_k', '_kg', '_G.Value'))})")
    por_colunas = (f"Filter(ForAll(Sequence(3) As _j, "
                   f"{_resumo_grupo('Switch(_j.Value, 1, varNomes.N1, 2, varNomes.N2, varNomes.N3)', _amostra('_j.Value'))}), n > 0)")
    return f"""With(
    {{_fmt: If(drpAnoFormato.Selected.Value = "{FORMATOS_ANOVA[1]}", 2, 1),
     _k: {indice_num("drpAnoVar")}, _kg: {indice_cat("drpAnoFator")}, _alfa: {alfa("drpAnoAlfa")}}},
    With(
        // Resumo de cada grupo: n, média, soma e soma dos quadrados dos desvios em relação à média do grupo
        {{_g: If(_fmt = 1, {por_fator}, {por_colunas})}},
    With({{_N: Sum(_g, n), _kk: CountRows(_g)}},
    With({{_mg: If(_N > 0, Sum(_g, soma) / _N)}},
    With(
        // SQ entre grupos (fator) e SQ dentro dos grupos (residual)
        {{_SQE: Sum(_g, n * Power(media - _mg, 2)), _SQD: Sum(_g, sq)}},
    With(
        {{_QME: If(_kk >= 2, _SQE / (_kk - 1)), _QMD: If(_N > _kk, _SQD / (_N - _kk))}},
    With(
        {{_F: If(_kk >= 2 && _N > _kk && _SQD > 0, _QME / _QMD)}},
    {{
        Grupos: _g, k: _kk, N: _N, mediaGlobal: _mg, alfa: _alfa,
        SQE: _SQE, SQD: _SQD, SQT: _SQE + _SQD,
        glE: _kk - 1, glD: _N - _kk, glT: _N - 1,
        QME: _QME, QMD: _QMD, F: _F,
        p: If(!IsBlank(_F), {p_f("_F", "_kk - 1", "_N - _kk").replace(chr(10), chr(10) + "            ")}),
        eta2: If(_SQE + _SQD > 0, _SQE / (_SQE + _SQD)),
        motivo: If(_kk < 2, "são precisos pelo menos 2 grupos com dados.",
                   _N <= _kk, "é preciso que pelo menos um grupo tenha mais do que uma observação (N > k).",
                   "a variabilidade dentro dos grupos é nula (SQ dentro = 0), por isso F não está definido.")
    }}
    ))))))
)"""


def html_anova():
    linha_g = (f'Concat(_R.Grupos, "<tr>" & {td(esc_html("Grupo"), True)} & {td(fmt("n", 0))} & {td(fmt("media"))} & '
               f'{td(fmt("If(n >= 2, Sqrt(sq / (n - 1)))"))} & {td(fmt("If(n >= 2, sq / (n - 1))"))} & "</tr>")')
    linhas_anova = (
        f'"<tr>" & {td(chr(34) + "Entre grupos (fator)" + chr(34), True)} & {td(fmt("_R.SQE"))} & {td(fmt("_R.glE", 0))} & '
        f'{td(fmt("_R.QME"))} & {td("\"<b>\" & " + fmt("_R.F") + " & \"</b>\"")} & {td("\"<b>\" & " + fmt_p("_R.p") + " & \"</b>\"")} & "</tr>" & '
        f'"<tr>" & {td(chr(34) + "Dentro dos grupos (residual)" + chr(34), True)} & {td(fmt("_R.SQD"))} & {td(fmt("_R.glD", 0))} & '
        f'{td(fmt("_R.QMD"))} & {td(chr(34) + chr(34))} & {td(chr(34) + chr(34))} & "</tr>" & '
        f'"<tr style=\'font-weight:600\'>" & {td(chr(34) + "Total" + chr(34), True)} & {td(fmt("_R.SQT"))} & {td(fmt("_R.glT", 0))} & '
        f'{td(chr(34) + chr(34))} & {td(chr(34) + chr(34))} & {td(chr(34) + chr(34))} & "</tr>"')
    frase = ('"existem diferenças entre as médias de " & ' + esc_html('_nomeVar') +
             ' & " nos " & _R.k & " grupos (pelo menos duas médias populacionais são diferentes)"')
    return f"""With({{_R: {anova().replace(chr(10), chr(10) + "    ")},
      _nomeVar: If(drpAnoFormato.Selected.Value = "{FORMATOS_ANOVA[1]}", "cada coluna", drpAnoVar.Selected.Value)}},
    {ESTILO} &
    {secao("Resumo dos grupos")} &
    {tabela_html(["Grupo", "n", "Média", "Desvio padrão", "Variância"], linha_g)} &
    "Média global x̄ = " & {fmt("_R.mediaGlobal")} & " &nbsp;·&nbsp; N = " & {fmt("_R.N", 0)} & " &nbsp;·&nbsp; k = " & {fmt("_R.k", 0)} & " grupos" &
    {secao("Hipóteses")} &
    "H₀: μ₁ = μ₂ = … = μ<sub>k</sub> (todas as médias populacionais são iguais)<br>" &
    "H₁: pelo menos duas médias populacionais são diferentes" &
    {secao("Tabela da ANOVA")} &
    {tabela_html(["Fonte de variação", "SQ", "gl", "QM = SQ / gl", "F = QM<sub>entre</sub> / QM<sub>dentro</sub>", "Valor de p"], linhas_anova)} &
    "<span style='color:#5a626a;font-size:12px'>SQ<sub>entre</sub> = Σ nᵢ (x̄ᵢ − x̄)² &nbsp;·&nbsp; SQ<sub>dentro</sub> = Σᵢ Σⱼ (xᵢⱼ − x̄ᵢ)² " &
    "&nbsp;·&nbsp; gl: k − 1, N − k e N − 1 &nbsp;·&nbsp; p = P(F ≥ F<sub>obs</sub>) com F ~ F(k − 1, N − k)" &
    " &nbsp;·&nbsp; η² = SQ<sub>entre</sub> / SQ<sub>total</sub> = " & {fmt("_R.eta2")} & "</span>" &
    {secao("Decisão e conclusão")} &
    {bloco_decisao("_R.p", "_R.alfa", frase, "_R.motivo")} &
    "<p style='color:#5a626a;font-size:12px'>Pressupostos: observações independentes, normalidade em cada grupo e " &
    "variâncias semelhantes (homocedasticidade). Se rejeitar H₀, a ANOVA não diz quais as médias diferentes: " &
    "é preciso um teste de comparações múltiplas.</p>" &
    "</div>"
)"""


# ---------------------------------------------------------------------------
# Qui-quadrado (aderência e independência)
# ---------------------------------------------------------------------------
TIPOS_QUI = ["Aderência (bondade do ajuste)", "Independência (tabela de contingência)"]
ORIGENS_QUI = ["Variáveis da tabela de dados", "Tabela colada do Excel"]
ESPERADAS_QUI = ["Proporções iguais", "Proporções indicadas"]


def _categorias(kv, d="_d"):
    """Valor de uma variável (1-3 numéricas, 4-5 categóricas) como texto de categoria e chave de ordenação."""
    from .f_comum import fmt_livre
    return (f"With({{_val: Switch({kv}, 1, {d}.N1, 2, {d}.N2, 3, {d}.N3, Blank())}}, "
            f"{{cat: If({kv} <= 3, If(IsBlank(_val), \"\", {fmt_livre('_val')}), Switch({kv}, 4, {d}.C1, {d}.C2)), "
            f"ord: If({kv} <= 3, _val, 0)}})")


def _niveis_de(tab, campo, ordem, kv):
    """Categorias distintas de um campo, por ordem numérica (variáveis numéricas) ou alfabética."""
    return (f"With({{_ls: ForAll(Distinct({tab}, {campo}) As _c, {{nome: _c.Value, "
            f"o: LookUp({tab}, {campo} = _c.Value).{ordem}}})}}, If({kv} <= 3, Sort(_ls, o), Sort(_ls, nome)))")


def matriz_colada(txt="txtQuiTabela.Text"):
    """Tabela de frequências colada do Excel -> {Linhas, Colunas, Celulas{i, j, O}, Invalidos}.
    1.ª linha = cabeçalho se tiver texto não numérico a partir da 2.ª coluna;
    1.ª coluna = nomes das linhas se tiver texto não numérico (fora do cabeçalho)."""
    from . import f_dados as FD
    from .f_comum import num as _num
    cel = lambda r, j: f'If({j} <= CountRows({r}.Celulas), Index({r}.Celulas, {j}).Texto, "")'  # noqa: E731
    return f"""With({{_lin: {FD.linhas(txt).replace(chr(10), chr(10) + "    ")}}},
    With({{_m: CountRows(_lin), _kc: Coalesce(Max(_lin, CountRows(Celulas)), 0)}},
    With({{_cab: _m >= 2 && CountRows(Filter(Sequence(Max(_kc - 1, 0), 2) As _j,
                With({{_t: {cel("First(_lin)", "_j.Value")}}}, _t <> "" && IsBlank({_num("_t")})))) > 0}},
    With({{_corpo: If(_cab, LastN(_lin, _m - 1), _lin)}},
    With({{_rot: CountRows(Filter(_corpo As _r, With({{_t: {cel("_r", "1")}}}, _t <> "" && IsBlank({_num("_t")})))) > 0}},
    With({{_c0: If(_rot, 1, 0)}},
    With({{_nc: Max(_kc - _c0, 0), _nr: CountRows(_corpo)}},
    {{
        Linhas: ForAll(Sequence(_nr) As _i, {{nome: If(_rot, {cel("Index(_corpo, _i.Value)", "1")}, "Linha " & _i.Value)}}),
        Colunas: ForAll(Sequence(_nc) As _j, {{nome: If(_cab, {cel("First(_lin)", "_j.Value + _c0")}, "Coluna " & _j.Value)}}),
        Celulas: ForAll(Sequence(_nr * _nc, 0) As _q,
            With({{_i: RoundDown(_q.Value / _nc, 0) + 1, _j: Mod(_q.Value, _nc) + 1}},
                With({{_t: {cel("Index(_corpo, _i)", "_j + _c0")}}},
                    {{i: _i, j: _j, t: _t, O: With({{_o: {_num("_t")}}}, If(IsBlank(_o) || _o < 0, 0, _o)),
                     invalido: _t <> "" && (IsBlank({_num("_t")}) || {_num("_t")} < 0)}}))),
        TemRotulos: _rot
    }}
    ))))))
)"""


def _props_indicadas(txt="txtQuiProporcoes.Text"):
    from .f_comum import num as _num
    return (f"Filter(ForAll(Split(Substitute(Substitute(Substitute({txt}, Char(13), \"\"), Char(9), Char(10)), \";\", Char(10)), "
            f"Char(10)) As _s, {{p: {_num('_s.Value')}}}), !IsBlank(p))")


def qui_quadrado():
    """Registo com o teste do qui-quadrado escolhido (ecrã scrQuiQuadrado)."""
    return f"""With(
    {{_tipo: If(drpQuiTipo.Selected.Value = "{TIPOS_QUI[1]}", 2, 1),
     _orig: If(drpQuiOrigem.Selected.Value = "{ORIGENS_QUI[1]}", 2, 1),
     _k1: {_indice_todas("drpQuiVar1")}, _k2: {_indice_todas("drpQuiVar2")},
     _alfa: {alfa("drpQuiAlfa")}}},
    With(
        // Tabela observada: nomes das linhas e colunas e células {{i, j, O}} (na aderência há só 1 coluna)
        {{_T: If(_orig = 2, {matriz_colada().replace(chr(10), chr(10) + "            ")},
            With({{_pr: Filter(ForAll(colDados As _d, With({{_A: {_categorias("_k1")}, _B: {_categorias("_k2")}}},
                        {{a: _A.cat, oa: _A.ord, b: If(_tipo = 2, _B.cat, "Total"), ob: If(_tipo = 2, _B.ord, 0)}})),
                        a <> "" && b <> "")}},
                With({{_L: {_niveis_de("_pr", "a", "oa", "_k1")}, _C: {_niveis_de("_pr", "b", "ob", "If(_tipo = 2, _k2, 4)")}}},
                    {{Linhas: _L, Colunas: _C,
                     Celulas: ForAll(Sequence(CountRows(_L) * CountRows(_C), 0) As _q,
                        With({{_i: RoundDown(_q.Value / CountRows(_C), 0) + 1, _j: Mod(_q.Value, CountRows(_C)) + 1}},
                            {{i: _i, j: _j, t: "",
                             O: CountIf(_pr, a = Index(_L, _i).nome && b = Index(_C, _j).nome), invalido: false}})),
                     TemRotulos: true}})))}},
    With(
        // Aderência: frequências observadas = última coluna; se a tabela colada não tiver nomes de texto
        // e tiver 2 ou mais colunas, a 1.ª coluna dá os nomes das categorias (ex.: faces de um dado 1 a 6)
        {{_cel: If(_tipo = 1, ForAll(Filter(_T.Celulas, j = CountRows(_T.Colunas)) As _x,
                                    {{i: _x.i, j: 1, O: _x.O}}),
                   ForAll(_T.Celulas As _x, {{i: _x.i, j: _x.j, O: _x.O}})),
         _Lin: If(_tipo = 1 && !_T.TemRotulos && CountRows(_T.Colunas) >= 2,
                  ForAll(Filter(_T.Celulas, j = 1) As _x, {{nome: _x.t}}), _T.Linhas),
         _nr: CountRows(_T.Linhas), _nc: If(_tipo = 1, 1, CountRows(_T.Colunas))}},
    With({{_N: Sum(_cel, O),
          _Ri: ForAll(Sequence(_nr) As _r, {{i: _r.Value, R: Sum(Filter(_cel, i = _r.Value), O)}}),
          _Cj: ForAll(Sequence(_nc) As _c, {{j: _c.Value, C: Sum(Filter(_cel, j = _c.Value), O)}}),
          _pind: {_props_indicadas()},
          _esp: If(drpQuiEsperadas.Selected.Value = "{ESPERADAS_QUI[1]}", 2, 1)}},
    With(
        // Frequências esperadas: n·pᵢ (aderência) ou Rᵢ·Cⱼ/N (independência)
        {{_E: ForAll(_cel As _o,
            {{i: _o.i, j: _o.j, O: _o.O,
             E: If(_tipo = 1,
                   If(_esp = 1, _N / _nr,
                      If(CountRows(_pind) = _nr && Sum(_pind, p) > 0, _N * Index(_pind, _o.i).p / Sum(_pind, p))),
                   LookUp(_Ri, i = _o.i).R * LookUp(_Cj, j = _o.j).C / _N)}})}},
    With(
        {{_ok: _N > 0 && _nr >= 2 && (_tipo = 1 || _nc >= 2) && CountRows(Filter(_E, IsBlank(E) || E <= 0)) = 0}},
    With(
        {{_q2: If(_ok, Sum(_E, Power(O - E, 2) / E)),
         _gl: If(_tipo = 1, _nr - 1, (_nr - 1) * (_nc - 1))}},
    {{
        tipo: _tipo, alfa: _alfa, Linhas: _Lin, Colunas: _T.Colunas, Celulas: _E,
        nr: _nr, nc: _nc, N: _N, Ri: _Ri, Cj: _Cj,
        qui2: _q2, gl: _gl,
        p: If(!IsBlank(_q2), {p_qui("_q2", "_gl").replace(chr(10), chr(10) + "            ")}),
        baixas: CountRows(Filter(_E, E < 5)), muitoBaixas: CountRows(Filter(_E, E < 1)),
        invalidos: CountRows(Filter(_T.Celulas, invalido)),
        proporcoes: If(_tipo = 1, If(_esp = 1, ForAll(Sequence(_nr) As _r, {{p: 1 / _nr}}),
                        ForAll(_pind As _x, {{p: _x.p / Sum(_pind, p)}}))),
        motivo: If(_N = 0, "não há observações.",
                   _nr < 2, "são precisas pelo menos 2 categorias (linhas).",
                   _tipo = 2 && _nc < 2, "são precisas pelo menos 2 colunas na tabela de contingência.",
                   _tipo = 1 && _esp = 2 && CountRows(_pind) <> _nr,
                       "indique tantas proporções esperadas quantas as categorias (" & _nr & "), pela ordem da tabela.",
                   "há frequências esperadas nulas (uma linha ou coluna sem observações ou uma proporção igual a 0).")
    }}
    ))))))
)"""


def _indice_todas(drp):
    from .f_comum import indice_todas
    return indice_todas(drp)


def html_qui():
    from .f_comum import fmt_livre  # noqa: F401
    nome1 = esc_html("drpQuiVar1.Selected.Value")
    nome2 = esc_html("drpQuiVar2.Selected.Value")
    th = "\"<th style='padding:5px 8px;text-align:right'>\""
    # tabela de contingência (observadas ou esperadas) com totais
    def tabela(campo, casas):
        val = fmt(f"LookUp(_R.Celulas, i = _r.Value && j = _c.Value).{campo}", casas)
        return f"""\"<table style='border-collapse:collapse;margin:4px 0 10px 0'><tr style='background:#1f4e79;color:#ffffff'><th style='padding:5px 8px'></th>\" &
        Concat(Sequence(_R.nc) As _c, {th} & {esc_html("Index(_R.Colunas, _c.Value).nome")} & "</th>") & {th} & "Total</th></tr>" &
        Concat(Sequence(_R.nr) As _r, "<tr>" & {td(esc_html("Index(_R.Linhas, _r.Value).nome"), True)} &
            Concat(Sequence(_R.nc) As _c, {td(val)}) & {td(fmt("LookUp(_R.Ri, i = _r.Value).R", 0))} & "</tr>") &
        "<tr style='font-weight:600'>" & {td(chr(34) + "Total" + chr(34), True)} &
        Concat(Sequence(_R.nc) As _c, {td(fmt("LookUp(_R.Cj, j = _c.Value).C", 0))}) & {td(fmt("_R.N", 0))} & "</tr></table>\""""
    linhas_ader = (f'Concat(Sequence(_R.nr) As _r, With({{_e: LookUp(_R.Celulas, i = _r.Value)}}, "<tr>" & '
                   f'{td(esc_html("Index(_R.Linhas, _r.Value).nome"), True)} & {td(fmt("_e.O", 0))} & '
                   f'{td(fmt("If(_r.Value <= CountRows(_R.proporcoes), Index(_R.proporcoes, _r.Value).p)"))} & {td(fmt("_e.E"))} & '
                   f'{td(fmt("If(_e.E > 0, Power(_e.O - _e.E, 2) / _e.E)"))} & "</tr>"))')
    frase = (f'If(_R.tipo = 1, If(drpQuiOrigem.Selected.Value = "{ORIGENS_QUI[1]}", '
             f'"as frequências da tabela colada não seguem as proporções esperadas", '
             f'"a distribuição de " & {nome1} & " não segue as proporções esperadas"), '
             f'"existe associação entre " & If(drpQuiOrigem.Selected.Value = "{ORIGENS_QUI[1]}", '
             f'"as linhas e as colunas da tabela", {nome1} & " e " & {nome2}) & " (não são independentes)")')
    return f"""With({{_R: {qui_quadrado().replace(chr(10), chr(10) + "    ")}}},
    {ESTILO} &
    If(_R.tipo = 1,
        {secao("Frequências observadas e esperadas")} &
        {tabela_html(["Categoria", "Observada (Oᵢ)", "Proporção esperada (pᵢ)", "Esperada (Eᵢ = n·pᵢ)", "(Oᵢ − Eᵢ)² / Eᵢ"], linhas_ader)} &
        "n = " & {fmt("_R.N", 0)},
        {secao("Frequências observadas (Oᵢⱼ)")} & {tabela("O", 0)} &
        {secao("Frequências esperadas sob H₀ (Eᵢⱼ = Rᵢ · Cⱼ / N)")} & {tabela("E", 4)}) &
    If(_R.invalidos > 0, "<p style='color:#b00020'>⚠ " & _R.invalidos & " célula(s) da tabela colada não são números ≥ 0 e foram contadas como 0.</p>", "") &
    {secao("Hipóteses")} &
    If(_R.tipo = 1,
        "H₀: as proporções populacionais são as esperadas (p₁, …, p<sub>k</sub> da tabela)<br>H₁: pelo menos uma proporção é diferente da esperada",
        "H₀: as duas variáveis são independentes<br>H₁: as duas variáveis não são independentes (estão associadas)") &
    {secao("Estatística de teste")} &
    "χ² = Σ (O − E)² / E = <b>" & {fmt("_R.qui2")} & "</b>" &
    {secao("Graus de liberdade")} &
    If(_R.tipo = 1, "gl = k − 1 = ", "gl = (linhas − 1)(colunas − 1) = ") & "<b>" & {fmt("_R.gl", 0)} & "</b>" &
    {secao("Valor de p")} &
    "p = P(χ² ≥ χ²<sub>obs</sub>)<b>" & {igual_p("_R.p")} & "</b>" &
    {secao("Decisão e conclusão")} &
    {bloco_decisao("_R.p", "_R.alfa", frase, "_R.motivo")} &
    If(_R.baixas > 0,
        "<p style='color:#b00020'>⚠ " & _R.baixas & " de " & CountRows(_R.Celulas) & " células (" &
        {fmt("_R.baixas / CountRows(_R.Celulas) * 100", 1)} & " %) têm frequência esperada inferior a 5" &
        If(_R.muitoBaixas > 0, " e " & _R.muitoBaixas & " inferior a 1", "") &
        ". Regra de Cochran: no máximo 20 % das células com E &lt; 5 e nenhuma com E &lt; 1. " &
        If(_R.baixas / CountRows(_R.Celulas) > 0.2 || _R.muitoBaixas > 0,
            "A regra não é cumprida: a aproximação pelo qui-quadrado pode não ser fiável; considere agrupar categorias" &
            If(_R.tipo = 2 && _R.nr = 2 && _R.nc = 2, " ou usar o teste exato de Fisher", "") & ".",
            "A regra é cumprida.") & "</p>", "") &
    "</div>"
)"""
