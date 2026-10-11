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
            "<div style='border-left:4px solid #107c10;padding:6px 10px;background:#e8f5e8'><b>Decisão: rejeita-se H₀</b> (p = " & {fmt_p(p)} & " ≤ α = " & {fmt_curto(a)} & ").<br>" &
            "Conclusão: ao nível de significância de " & {alfa_pct(a)} & ", há evidência estatística de que " & {frase_h1} & ".</div>",
            "<div style='border-left:4px solid #1f4e79;padding:6px 10px;background:#eef3f9'><b>Decisão: não se rejeita H₀</b> (p = " & {fmt_p(p)} & " > α = " & {fmt_curto(a)} & ").<br>" &
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
    Switch(_R.alt, 1, "p = P(|T| ≥ |t|) = ", 2, "p = P(T ≤ t) = ", "p = P(T ≥ t) = ") & "<b>" & {fmt_p("_R.p")} & "</b>" &
    " &nbsp;<span style='color:#5a626a'>(T segue a distribuição t de Student com os gl indicados)</span>" &
    {secao("Decisão e conclusão")} &
    {bloco_decisao("_R.p", "_R.alfa", frase, "_R.motivo")} &
    If((_R.tipo = 2 || _R.tipo = 3) && _R.v1 > 0 && _R.v2 > 0,
        "<p style='color:#5a626a;font-size:12px'>Razão entre a maior e a menor variância: " &
        {fmt("Max(_R.v1, _R.v2) / Min(_R.v1, _R.v2)", 2)} &
        ". Regra prática: se for superior a 4, prefira o teste de Welch (não assume variâncias iguais).</p>", "") &
    "</div>"
)"""
