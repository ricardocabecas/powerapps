"""Correlação de Pearson e regressão linear simples (formato invariante)."""
from .f_comum import num, fmt, indice_num
from .f_frequencias import fmt_curto
from . import f_graficos as G


def pares(kx, ky):
    """Pares (x, y) com os dois valores preenchidos (as linhas com um valor em falta são ignoradas)."""
    return (f"Filter(ForAll(colDados As _d, {{x: Switch({kx}, 1, _d.N1, 2, _d.N2, _d.N3), "
            f"y: Switch({ky}, 1, _d.N1, 2, _d.N2, _d.N3)}}), !IsBlank(x) && !IsBlank(y))")


def resultados(drp_x="drpRegX", drp_y="drpRegY", txt_x0="txtRegX0"):
    return f"""With(
    {{_p: {pares(indice_num(drp_x), indice_num(drp_y))}, _x0: {num(txt_x0 + ".Text")}}},
    With({{_n: CountRows(_p)}},
    With({{_mx: If(_n > 0, Average(_p, x)), _my: If(_n > 0, Average(_p, y))}},
    With(
        // Somas de quadrados e de produtos dos desvios em relação às médias
        {{_Sxx: Sum(_p, Power(x - _mx, 2)), _Syy: Sum(_p, Power(y - _my, 2)), _Sxy: Sum(_p, (x - _mx) * (y - _my))}},
    With(
        {{_b: If(_n >= 2 && _Sxx > 0, _Sxy / _Sxx),
         _r: If(_n >= 2 && _Sxx > 0 && _Syy > 0, _Sxy / Sqrt(_Sxx * _Syy))}},
    {{
        n: _n, mediaX: _mx, mediaY: _my,
        Sxx: If(_n > 0, _Sxx), Syy: If(_n > 0, _Syy), Sxy: If(_n > 0, _Sxy),
        sx: If(_n >= 2, Sqrt(_Sxx / (_n - 1))), sy: If(_n >= 2, Sqrt(_Syy / (_n - 1))),
        // Covariância amostral
        cov: If(_n >= 2, _Sxy / (_n - 1)),
        r: _r,
        r2: If(!IsBlank(_r), _r * _r),
        // Reta dos mínimos quadrados: ŷ = a + b·x
        b: _b,
        a: If(!IsBlank(_b), _my - _b * _mx),
        minX: Min(_p, x), maxX: Max(_p, x), minY: Min(_p, y), maxY: Max(_p, y),
        x0: _x0,
        previsao: If(!IsBlank(_b) && !IsBlank(_x0), _my - _b * _mx + _b * _x0)
    }}
    ))))
)"""


def equacao(R="_R"):
    return (f'If(IsBlank({R}.b), "não definida", "ŷ = " & {fmt(R + ".a")} & '
            f'If({R}.b < 0, " − ", " + ") & {fmt(f"Abs({R}.b)")} & " · x")')


def interpretacao(R="_R"):
    return (f'If(IsBlank({R}.r), "não definida",\n'
            f'        With({{_ar: Abs({R}.r)}}, If(_ar < 0.3, "fraca", _ar < 0.7, "moderada", "forte")) & " e " &\n'
            f'        If({R}.r > 0, "positiva", {R}.r < 0, "negativa", "nula"))')


def html(R_expr=None):
    R_expr = R_expr or resultados()
    linhas = [
        ("N.º de pares (x, y)", "n", fmt("_R.n", 0)),
        ("Média de x", "x̄", fmt("_R.mediaX")),
        ("Média de y", "ȳ", fmt("_R.mediaY")),
        ("Desvio padrão amostral de x", "s<sub>x</sub>", fmt("_R.sx")),
        ("Desvio padrão amostral de y", "s<sub>y</sub>", fmt("_R.sy")),
        ("Soma dos quadrados de x", "Sxx = Σ(xᵢ − x̄)²", fmt("_R.Sxx")),
        ("Soma dos quadrados de y", "Syy = Σ(yᵢ − ȳ)²", fmt("_R.Syy")),
        ("Soma dos produtos", "Sxy = Σ(xᵢ − x̄)(yᵢ − ȳ)", fmt("_R.Sxy")),
        ("Covariância amostral", "s<sub>xy</sub> = Sxy / (n − 1)", fmt("_R.cov")),
        ("Coeficiente de correlação de Pearson", "r = Sxy / √(Sxx·Syy)", fmt("_R.r")),
        ("Coeficiente de determinação", "R² = r²", fmt("_R.r2")),
        ("Declive", "b = Sxy / Sxx", fmt("_R.b")),
        ("Ordenada na origem", "a = ȳ − b·x̄", fmt("_R.a")),
        ("Equação da reta", "", equacao()),
        ("Correlação (indicativo)", "|r| < 0,3 fraca · < 0,7 moderada", interpretacao()),
    ]
    corpo = " &\n    ".join(
        f'"<tr{" style=" + chr(39) + "background:#f3f6fa" + chr(39) if i % 2 else ""}>'
        f"<td style='padding:4px 8px'>{rot}" + (f"<br><span style='color:#5a626a;font-size:12px'>{s}</span>" if s else "") +
        f"</td><td style='padding:4px 8px;text-align:right;white-space:nowrap'>\" & {v} & \"</td></tr>\""
        for i, (rot, s, v) in enumerate(linhas))
    return f"""With({{_R: {R_expr.replace(chr(10), chr(10) + "    ")}}},
    "<div style='font-family:Segoe UI,Arial;font-size:13px;color:#212529'>" &
    "<table style='border-collapse:collapse;width:100%'>" &
    "<tr style='background:#1f4e79;color:#ffffff'><th style='text-align:left;padding:6px 8px'>Medida e fórmula</th>" &
    "<th style='text-align:right;padding:6px 8px'>Valor</th></tr>" &
    {corpo} &
    "</table>" &
    "<h4 style='margin:14px 0 4px 0;color:#1f4e79'>Previsão</h4>" &
    If(IsBlank(_R.x0), "<p>Escreva um valor de x para obter a previsão ŷ.</p>",
        IsBlank(_R.previsao), "<p>Não é possível prever: a reta não está definida.</p>",
        "<p style='font-size:15px'>Para x = " & {fmt_curto("_R.x0")} & ": <b>ŷ = " & {fmt("_R.previsao")} & "</b></p>" &
        If(_R.x0 < _R.minX || _R.x0 > _R.maxX,
            "<p style='color:#b00020'>⚠ Extrapolação: x está fora do intervalo observado [" & {fmt_curto("_R.minX")} &
            " ; " & {fmt_curto("_R.maxX")} & "]; a previsão é pouco fiável.</p>", "")) &
    If(_R.n < 2, "<p style='color:#b00020'>São precisos pelo menos 2 pares de valores.</p>",
        IsBlank(_R.b), "<p style='color:#b00020'>Todos os valores de x são iguais (Sxx = 0): a reta e r não estão definidos.</p>",
        IsBlank(_R.r), "<p style='color:#b00020'>Todos os valores de y são iguais (Syy = 0): r não está definido.</p>", "") &
    "</div>"
)"""


def _escala(lo, hi, prefixo):
    """Abre 3 With com o início (_x0), fim (_x1) e passo (_xp) 'redondos' de um eixo (prefixo _x ou _y)."""
    return (f"With({{{prefixo}d: If({hi} > {lo}, {hi} - {lo}, Max(Abs({hi}), 1))}}, "
            f"With({{{prefixo}p: {G.passo_bonito(prefixo + 'd / 5')}}}, "
            # chão = Int(v); teto = -Int(-v)  (RoundDown/RoundUp arredondam em direção a zero)
            # margem de 4 % para os pontos extremos não ficarem em cima dos eixos
            f"With({{{prefixo}0: {prefixo}p * Int(({lo} - 0.04 * {prefixo}d) / {prefixo}p + 1E-9), "
            f"{prefixo}1: -{prefixo}p * Int(-({hi} + 0.04 * {prefixo}d) / {prefixo}p + 1E-9)}}, ")


def dispersao(R="_R", pares_expr="_P", titulo='"Diagrama de dispersão"', rx='"x"', ry='"y"'):
    """Diagrama de dispersão com a reta de regressão (recortada à área do gráfico)."""
    X0, X1, Y0, Y1, L, A = G.X0, G.X1, G.Y0, G.Y1, G.L, G.A
    px = f"{X0} + (({{v}}) - _x0) / (_x1 - _x0) * {L}"
    py = f"{Y1} - (({{v}}) - _y0) / (_y1 - _y0) * {A}"
    PX = lambda v: px.replace("{v}", v)  # noqa: E731
    PY = lambda v: py.replace("{v}", v)  # noqa: E731
    return G.svg_uri(f"""If({R}.n = 0, "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 640 400'><text x='320' y='200' text-anchor='middle' font-family='Segoe UI, Arial' font-size='14'>Sem pares de valores</text></svg>",
    {_escala(R + ".minX", R + ".maxX", "_x")}
    {_escala(R + ".minY", R + ".maxY", "_y")}
    {G.abre(titulo)} &
    "<defs><clipPath id='area'><rect x='{X0}' y='{Y0}' width='{L}' height='{A}'/></clipPath></defs>" &
    // Grelha e marcas dos eixos
    Concat(Sequence(Round((_x1 - _x0) / _xp, 0) + 1, 0) As _t, With({{_v: _x0 + _t.Value * _xp}},
        {G.linha(PX("_v"), str(Y0), PX("_v"), str(Y1))} &
        {G.texto(PX("_v"), str(Y1 + 16), fmt_curto("_v"))})) &
    Concat(Sequence(Round((_y1 - _y0) / _yp, 0) + 1, 0) As _t, With({{_v: _y0 + _t.Value * _yp}},
        {G.linha(str(X0), PY("_v"), str(X1), PY("_v"))} &
        {G.texto(str(X0 - 8), PY("_v") + " + 4", fmt_curto("_v"), "end")})) &
    "<rect x='{X0}' y='{Y0}' width='{L}' height='{A}' fill='none' stroke='rgb(90,98,106)'/>" &
    // Pontos observados
    Concat({pares_expr}, "<circle cx='" & {G.c(PX("x"))} & "' cy='" & {G.c(PY("y"))} &
        "' r='4.5' fill='rgb(46,117,182)' fill-opacity='0.75' stroke='rgb(31,78,121)'/>") &
    // Reta de regressão ŷ = a + b·x desenhada de um lado ao outro e recortada à área do gráfico
    If(IsBlank({R}.b), "",
        "<line clip-path='url(#area)' x1='{X0}' x2='{X1}' y1='" & {G.c(PY(f"{R}.a + {R}.b * _x0"))} &
        "' y2='" & {G.c(PY(f"{R}.a + {R}.b * _x1"))} & "' stroke='rgb(192,0,0)' stroke-width='2'/>" &
        "<text x='{X1 - 6}' y='{Y0 + 18}' text-anchor='end' font-size='12' fill='rgb(192,0,0)'>" &
        {G.esc(equacao(R))} & If(IsBlank({R}.r), "", "   (r = " & {fmt(R + ".r")} & ")") & "</text>") &
    "<text x='{(X0 + X1) // 2}' y='{Y1 + 40}' text-anchor='middle' font-size='12' fill='rgb(90,98,106)'>" & {G.esc(rx)} & "</text>" &
    "<text transform='translate(18,{(Y0 + Y1) // 2}) rotate(-90)' text-anchor='middle' font-size='12' fill='rgb(90,98,106)'>" & {G.esc(ry)} & "</text>" &
    "</svg>"
    ))))))
)""")
