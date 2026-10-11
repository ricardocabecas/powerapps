"""Gráficos em SVG (histograma, diagrama de barras, dispersão), mostrados num controlo Imagem.

A imagem é um URI de dados: "data:image/svg+xml;utf8," & EncodeUrl(<texto SVG>).
Área do desenho: viewBox 0 0 640 400; área dos dados entre x = 70..620 e y = 40..330.
Todas as coordenadas são escritas com Text(...; "[$-en-US]0.00"; "en-US") para terem sempre
ponto decimal (o SVG não aceita vírgula), qualquer que seja a região do utilizador.
"""
from .f_frequencias import fmt_curto

X0, X1, Y0, Y1 = 70, 620, 40, 330      # Y0 = topo, Y1 = base (o SVG cresce para baixo)
L, A = X1 - X0, Y1 - Y0


def c(expr):
    """Coordenada SVG: número com ponto decimal e 2 casas."""
    return f'Text(Round({expr}, 2), "[$-en-US]0.00", "en-US")'


def inteiro(expr):
    return f'Text({expr}, "[$-en-US]0", "pt-PT")'


def esc(t):
    """Escapa &, < e > para texto dentro do SVG (XML)."""
    return f'Substitute(Substitute(Substitute({t}, "&", "&amp;"), "<", "&lt;"), ">", "&gt;")'


def passo_bonito(r):
    """Passo 'redondo' (1, 2 ou 5 × 10^m) próximo de r (> 0)."""
    # Int arredonda para baixo (também nos negativos: Int(-0,7) = -1), ao contrário de RoundDown
    return (f"With({{_e: Power(10, Int(Log({r}, 10) + 1E-9))}}, "
            f"With({{_f: {r} / _e}}, If(_f <= 1, 1, _f <= 2, 2, _f <= 5, 5, 10) * _e))")


def svg_uri(corpo):
    return f'"data:image/svg+xml;utf8," & EncodeUrl({corpo})'


def abre(titulo):
    return (f""""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 640 400' font-family='Segoe UI, Arial, sans-serif'>" &
    "<rect x='0' y='0' width='640' height='400' fill='white'/>" &
    "<text x='320' y='22' text-anchor='middle' font-size='15' font-weight='600' fill='rgb(33,37,41)'>" & {esc(titulo)} & "</text>\"""")


def texto(x, y, conteudo, ancora="middle", tam=10, cor="rgb(90,98,106)", extra=""):
    """Elemento <text> com coordenadas calculadas (x, y são expressões Power Fx)."""
    return (f""""<text x='" & {c(x)} & "' y='" & {c(y)} & "' text-anchor='{ancora}' font-size='{tam}' fill='{cor}'{extra}>" & """
            f"""{conteudo} & "</text>\"""")


def linha(x1, y1, x2, y2, cor="rgb(225,229,234)", extra=""):
    return (f""""<line x1='" & {c(x1)} & "' y1='" & {c(y1)} & "' x2='" & {c(x2)} & "' y2='" & {c(y2)} & """
            f""""' stroke='{cor}'{extra}/>\"""")


def eixo_y_contagens(ymax, passo, rotulo):
    """Linhas de grelha e rótulos do eixo vertical (contagens inteiras)."""
    return f"""Concat(Sequence(RoundDown({ymax} / {passo} + 1E-9, 0) + 1, 0) As _t,
        With({{_y: {Y1} - _t.Value * {passo} / {ymax} * {A}}},
            {linha(str(X0), "_y", str(X1), "_y")} &
            {texto(str(X0 - 8), "_y + 4", inteiro(f"_t.Value * {passo}"), "end", 11)})) &
    "<text transform='translate(18,{(Y0 + Y1) // 2}) rotate(-90)' text-anchor='middle' font-size='12' fill='rgb(90,98,106)'>{rotulo}</text>\""""


def escala_contagens(linhas):
    """Abre três With com _mx, _passo e _ymax (eixo vertical das frequências absolutas).
    Quem usa tem de fechar os três parênteses."""
    return (f"With({{_mx: Max(Max({linhas}, ni), 1)}}, "
            f"With({{_passo: Max(1, {passo_bonito('_mx / 5')})}}, "
            f"With({{_ymax: _passo * RoundUp(_mx * 1.08 / _passo - 1E-9, 0)}}, ")


def eixo_x(rotulo_x):
    return (f""""<line x1='{X0}' x2='{X1}' y1='{Y1}' y2='{Y1}' stroke='rgb(90,98,106)'/>" &
    "<text x='{(X0 + X1) // 2}' y='{Y1 + 40}' text-anchor='middle' font-size='12' fill='rgb(90,98,106)'>" & {esc(rotulo_x)} & "</text>\"""")


def histograma(t="_F", titulo='"Histograma"', rotulo_x='""'):
    """Histograma a partir do registo de frequências por classes (_F.Linhas com ni)."""
    return svg_uri(f"""With({{_lin: {t}.Linhas, _k: CountRows({t}.Linhas)}},
    {escala_contagens("_lin")}
    With({{_bw: {L} / Max(_k, 1), _salto: RoundUp(_k / 10, 0)}},
    {abre(titulo)} &
    {eixo_y_contagens("_ymax", "_passo", "Frequência absoluta (nᵢ)")} &
    // Barras contíguas: largura = amplitude da classe, altura proporcional a nᵢ
    Concat(Sequence(_k) As _i, With({{_r: Index(_lin, _i.Value)}},
        With({{_hb: _r.ni / _ymax * {A}}},
            "<rect x='" & {c(f"{X0} + (_i.Value - 1) * _bw")} & "' y='" & {c(f"{Y1} - _hb")} & "' width='" & {c("_bw")} &
            "' height='" & {c("_hb")} & "' fill='rgb(31,78,121)' stroke='white' stroke-width='1'/>" &
            If(_r.ni > 0, {texto(f"{X0} + (_i.Value - 0.5) * _bw", f"{Y1} - _hb - 4", inteiro("_r.ni"), cor="rgb(33,37,41)")}, "")))) &
    // Limites das classes no eixo horizontal (só alguns, se forem muitas classes)
    Concat(Sequence(_k + 1, 0) As _j,
        If(Mod(_j.Value, _salto) = 0 || _j.Value = _k,
            {texto(f"{X0} + _j.Value * _bw", str(Y1 + 16), fmt_curto(f"{t}.a + _j.Value * {t}.h"))}, "")) &
    {eixo_x(rotulo_x)} &
    "</svg>"
    )))))""")


def barras(t="_F", titulo='"Diagrama de barras"', rotulo_x='""'):
    """Diagrama de barras (barras separadas) para dados discretos ou categóricos."""
    rot = esc('If(Len(_r.Classe) > 12, Left(_r.Classe, 11) & "…", _r.Classe)')
    return svg_uri(f"""With({{_lin: {t}.Linhas, _k: CountRows({t}.Linhas)}},
    {escala_contagens("_lin")}
    With({{_slot: {L} / Max(_k, 1), _salto: RoundUp(_k / 12, 0)}},
    {abre(titulo)} &
    {eixo_y_contagens("_ymax", "_passo", "Frequência absoluta (nᵢ)")} &
    // Uma barra por valor/categoria (70 % do espaço disponível, no máximo 90 px)
    Concat(Sequence(_k) As _i, With({{_r: Index(_lin, _i.Value)}},
        With({{_hb: _r.ni / _ymax * {A}, _xc: {X0} + (_i.Value - 0.5) * _slot, _lb: Min(0.7 * _slot, 90)}},
            "<rect x='" & {c("_xc - _lb / 2")} & "' y='" & {c(f"{Y1} - _hb")} & "' width='" & {c("_lb")} &
            "' height='" & {c("_hb")} & "' fill='rgb(46,117,182)'/>" &
            {texto("_xc", f"{Y1} - _hb - 4", inteiro("_r.ni"), cor="rgb(33,37,41)")} &
            If(Mod(_i.Value - 1, _salto) = 0, {texto("_xc", str(Y1 + 16), rot)}, "")))) &
    {eixo_x(rotulo_x)} &
    "</svg>"
    )))))""")
