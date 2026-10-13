"""Tabelas de frequências (dados discretos/categóricos e dados agrupados em classes)."""
from .f_comum import num, fmt_livre, indice_todas, col_num, col_txt, e_numerica

TIPOS = ["Valores distintos (discreta)", "Classes (dados agrupados)"]


def fmt_curto(expr):
    """Número -> texto pt-PT com no máximo 4 casas decimais e sem zeros à direita."""
    return (f'With({{_r: Round({expr}, 4)}}, If(_r = Int(_r), Text(_r, "[$-en-US]0", "pt-PT"), '
            f'Text(_r, "[$-en-US]0.####", "pt-PT")))')


def _acumular(base):
    """Acrescenta fi, Ni e Fi a uma tabela com ni (pela ordem das linhas)."""
    return f"""With({{_t: {base}, _ntot: Sum({base}, ni)}},
        ForAll(Sequence(CountRows(_t)) As _i,
            With({{_r: Index(_t, _i.Value), _Ni: Sum(FirstN(_t, _i.Value), ni)}},
                {{Ordem: _i.Value, Classe: _r.Classe, Centro: _r.Centro, Li: _r.Li, Ls: _r.Ls,
                 ni: _r.ni, fi: _r.ni / _ntot, Ni: _Ni, Fi: _Ni / _ntot}})))"""


def tabela(drp_var="drpFreVar", drp_tipo="drpFreTipo", txt_k="txtFreK", txt_inicio="txtFreInicio",
           txt_h="txtFreAmplitude"):
    """Registo com a tabela de frequências (Linhas) e os parâmetros usados."""
    return f"""With(
    {{_kv: {indice_todas(drp_var)}}},
    With({{_isn: {e_numerica("_kv")}}},
    With(
        {{_tipo: If(!_isn, 1, If({drp_tipo}.Selected.Value = "{TIPOS[1]}", 2, 1)),
         // Valores numéricos (variável numérica) ou textos (variável categórica), sem células vazias
         _x: Filter(ForAll(colDados As _d, {{x: If(_isn, {col_num("_kv")})}}), !IsBlank(x)),
         _g: Filter(ForAll(colDados As _d, {{g: If(!_isn, {col_txt("_kv")}, "")}}), !IsBlank(g))}},
        With(
            {{_n: If(!_isn, CountRows(_g), CountRows(_x)), _min: Min(_x, x), _max: Max(_x, x)}},
            With(
                // Classes: k pela regra de Sturges (ou o valor escrito), início no mínimo e amplitude (máx − início)/k
                {{_kS: If(_n > 0, RoundUp(1 + Log(_n, 2) - 1E-9, 0), 0),
                 _kU: {num(txt_k + ".Text")}, _aU: {num(txt_inicio + ".Text")}, _hU: {num(txt_h + ".Text")}}},
                With(
                    {{_k: If(!IsBlank(_kU) && _kU >= 1, Min(RoundDown(_kU, 0), 50), Max(_kS, 1)),
                     _a: Coalesce(_aU, _min)}},
                    With(
                        {{_h: If(!IsBlank(_hU) && _hU > 0, _hU, If(_max > _a, (_max - _a) / _k, 1))}},
                        With(
                            // Classe de cada valor: [Li ; Ls[ (a última é fechada à direita)
                            {{_cls: ForAll(_x As _v, {{c: With({{_z: (_v.x - _a) / _h}},
                                If(_z < -1E-9, 0, Min(RoundDown(_z + 1E-9, 0) + 1, If(_z <= _k + 1E-9, _k, _k + 1))))}})}},
                            {{
                                Tipo: _tipo, n: _n, k: _k, kSturges: _kS, a: _a, h: _h, Minimo: _min, Maximo: _max,
                                Fora: If(_tipo = 2, CountRows(Filter(_cls, c < 1 || c > _k)), 0),
                                Linhas: If(
                                    _n = 0, FirstN({_acumular('Table({Classe: "", Centro: 0, Li: 0, Ls: 0, ni: 0})')}, 0),
                                    _tipo = 2,
                                    {_acumular('''ForAll(Sequence(_k) As _c,
                                            {Classe: "[" & ''' + fmt_curto("_a + (_c.Value - 1) * _h") + ''' & " ; " & ''' + fmt_curto("_a + _c.Value * _h") + ''' & If(_c.Value = _k, "]", "["),
                                             Centro: _a + (_c.Value - 0.5) * _h, Li: _a + (_c.Value - 1) * _h, Ls: _a + _c.Value * _h,
                                             ni: CountIf(_cls, c = _c.Value)})''')},
                                    !_isn,
                                    {_acumular('''ForAll(Sort(Distinct(_g, g), Value) As _d,
                                            {Classe: _d.Value, Centro: Blank(), Li: Blank(), Ls: Blank(), ni: CountIf(_g, g = _d.Value)})''')},
                                    {_acumular('''ForAll(Sort(Distinct(_x, x), Value) As _d,
                                            {Classe: ''' + fmt_livre("_d.Value") + ''', Centro: _d.Value, Li: Blank(), Ls: Blank(),
                                             ni: CountIf(_x, x = _d.Value)})''')}
                                )
                            }}
                        )
                    )
                )
            )
        )
    )
))"""


def resumo(t="_F"):
    """Texto com os parâmetros usados (n, k, amplitude, início) e avisos."""
    return f"""If({t}.n = 0, "Não há valores para a variável escolhida.",
    "n = " & {t}.n & "   ·   " & CountRows({t}.Linhas) & If({t}.Tipo = 2, " classes", " valores distintos") &
    If({t}.Tipo = 2,
        Char(10) & "Regra de Sturges: k = ⌈1 + log₂ n⌉ = " & {t}.kSturges &
        Char(10) & "Amplitude das classes: h = " & {fmt_curto(t + ".h")} &
        "   ·   1.ª classe começa em " & {fmt_curto(t + ".a")} &
        Char(10) & "Mínimo = " & {fmt_curto(t + ".Minimo")} & "   ·   Máximo = " & {fmt_curto(t + ".Maximo")} &
        If({t}.Fora > 0, Char(10) & "⚠ " & {t}.Fora & " valor(es) ficaram fora das classes: ajuste o início ou a amplitude.", ""),
        ""))"""
