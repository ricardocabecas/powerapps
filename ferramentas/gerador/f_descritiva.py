"""Fórmulas da estatística descritiva (formato invariante)."""
from .f_comum import fmt, fmt_livre, vetor_num, indice_num

METODOS_QUARTIS = [
    "Excel QUARTIL.INC — (n−1)p+1",
    "Excel QUARTIL.EXC / SPSS — (n+1)p",
    "Mediana de cada metade",
]
SEM_GRUPOS = "(sem grupos)"


def _q_interp(p, tipo):
    """Quantil por interpolação linear na amostra ordenada _s (n = _n).
    tipo 7: posição h = (n−1)p + 1  (Excel QUARTIL.INC, R/numpy por omissão)
    tipo 6: posição h = (n+1)p, limitada a [1, n]  (Excel QUARTIL.EXC, SPSS, Minitab)"""
    h = f"(_n - 1) * {p} + 1" if tipo == 7 else f"Min(Max((_n + 1) * {p}, 1), _n)"
    return (f"With({{_h: {h}}}, With({{_b: RoundDown(_h, 0)}}, "
            f"Index(_s, _b).x + (_h - _b) * (Index(_s, Min(_b + 1, _n)).x - Index(_s, _b).x)))")


def _med_bloco(ini, m):
    """Mediana das m observações ordenadas que começam na posição ini+1 de _s."""
    return (f"If(Mod({m}, 2) = 1, Index(_s, {ini} + ({m} + 1) / 2).x, "
            f"(Index(_s, {ini} + {m} / 2).x + Index(_s, {ini} + {m} / 2 + 1).x) / 2)")


def _q_metades(qual):
    """Quartil como mediana da metade inferior/superior (exclui o valor central se n for ímpar)."""
    if qual == 1:
        bloco = _med_bloco("0", "_m")
    else:
        bloco = _med_bloco("(_n - _m)", "_m")
    return f"With({{_m: RoundDown(_n / 2, 0)}}, If(_m = 0, First(_s).x, {bloco}))"


def quartil(qual, metodo="_metodo"):
    p = {1: "0.25", 3: "0.75"}[qual]
    return (f"Switch({metodo}, 1, {_q_interp(p, 7)}, 2, {_q_interp(p, 6)}, {_q_metades(qual)})")


def resultados(vetor, metodo="_metodo"):
    """Registo com todas as medidas descritivas de uma tabela {x} de valores numéricos."""
    return f"""With(
    // Amostra ordenada por ordem crescente e dimensão
    {{_s: Sort({vetor}, x)}},
    With({{_n: CountRows(_s), _metodo: {metodo}}},
    With({{_soma: Sum(_s, x), _min: First(_s).x, _max: Last(_s).x}},
    With({{_media: If(_n > 0, _soma / _n)}},
    With(
        // Soma dos quadrados dos desvios em relação à média e frequência de cada valor (para a moda)
        {{_sq: Sum(_s, Power(x - _media, 2)),
         _freq: ForAll(Distinct(_s, x) As _d, {{v: _d.Value, f: CountIf(_s, x = _d.Value)}})}},
    With({{_fmax: Max(_freq, f), _modas: Filter(_freq, f = Max(_freq, f))}},
    {{
        n: _n,
        soma: If(_n > 0, _soma),
        media: _media,
        // Mediana: valor central (n ímpar) ou média dos dois centrais (n par)
        mediana: If(_n > 0, {_med_bloco("0", "_n")}),
        moda: If(_n = 0, "n.d.",
            If(_n > 1 && CountRows(_modas) = CountRows(_freq),
                "não existe (amodal)",
                Concat(FirstN(_modas, 5), {fmt_livre("v")}, "; ") &
                If(CountRows(_modas) > 5, "; …", "") &
                If(CountRows(_modas) = 2, " (bimodal)", CountRows(_modas) > 2, " (multimodal)", "") &
                " — freq. " & _fmax)),
        minimo: _min,
        maximo: _max,
        amplitude: If(_n > 0, _max - _min),
        q1: If(_n > 0, {quartil(1)}),
        q3: If(_n > 0, {quartil(3)}),
        // Variância amostral (divisor n − 1) e populacional (divisor n)
        varA: If(_n >= 2, _sq / (_n - 1)),
        varP: If(_n >= 1, _sq / _n),
        dpA: If(_n >= 2, Sqrt(_sq / (_n - 1))),
        dpP: If(_n >= 1, Sqrt(_sq / _n)),
        // Coeficiente de variação (com o desvio padrão amostral), em %
        cv: If(_n >= 2 && _media <> 0, Sqrt(_sq / (_n - 1)) / Abs(_media) * 100)
    }}
    )))))
)"""


def vetor_com_grupo(k, kg):
    """Tabela {x, g}: valor da variável numérica k e grupo da variável categórica kg (1 = C1, 2 = C2)."""
    return (f"Filter(ForAll(colDados As _d, {{x: Switch({k}, 1, _d.N1, 2, _d.N2, _d.N3), "
            f"g: Switch({kg}, 1, _d.C1, _d.C2)}}), !IsBlank(x))")


def indice_grupo(drp):
    """0 = sem grupos, 1 = C1, 2 = C2."""
    return f"Switch({drp}.Selected.Value, varNomes.C1, 1, varNomes.C2, 2, 0)"


def colunas(drp_var="drpDesVar", drp_grupo="drpDesGrupo", drp_metodo="drpDesQuartis"):
    """Tabela de colunas de resultados: 'Total' e, se houver agrupamento, uma coluna por grupo."""
    metodo = (f"Switch({drp_metodo}.Selected.Value, " +
              ", ".join(f'"{m}", {i + 1}' for i, m in enumerate(METODOS_QUARTIS)) + ", 1)")
    return f"""With(
    {{_k: {indice_num(drp_var)}, _kg: {indice_grupo(drp_grupo)}}},
    With({{_dados: {vetor_com_grupo("_k", "If(_kg = 0, 1, _kg)")}}},
        Table(
            // Coluna com todos os dados
            Patch({resultados("ForAll(_dados, {x: x})", metodo).replace(chr(10), chr(10) + "            ")},
                {{Grupo: "Total"}}),
            // Uma coluna por grupo (valores distintos não vazios da variável categórica)
            // (sem agrupamento a lista de grupos fica vazia)
            ForAll(If(_kg = 0, FirstN(Distinct(_dados, g), 0),
                      Sort(Filter(Distinct(_dados, g), !IsBlank(Value)), Value)) As _G,
                Patch({resultados("ForAll(Filter(_dados, g = _G.Value), {x: x})", metodo).replace(chr(10), chr(10) + "                ")},
                    {{Grupo: _G.Value}}))
        )
    )
)"""


# Linhas da tabela: (rótulo, símbolo / fórmula, campo, casas decimais, sufixo)
LINHAS = [
    ("Dimensão da amostra", "n", "n", 0, ""),
    ("Soma", "Σ xᵢ", "soma", 4, ""),
    ("Média", "x̄ = Σ xᵢ / n", "media", 4, ""),
    ("Mediana", "Me = Q₂", "mediana", 4, ""),
    ("Moda", "Mo", "moda", None, ""),
    ("Mínimo", "x₍₁₎", "minimo", 4, ""),
    ("Máximo", "x₍ₙ₎", "maximo", 4, ""),
    ("Amplitude total", "máx − mín", "amplitude", 4, ""),
    ("1.º quartil", "Q₁", "q1", 4, ""),
    ("3.º quartil", "Q₃", "q3", 4, ""),
    ("Amplitude interquartil", "AIQ = Q₃ − Q₁", "aiq", 4, ""),
    ("Variância amostral", "s² = Σ(xᵢ − x̄)² / (n − 1)", "varA", 4, ""),
    ("Desvio padrão amostral", "s = √s²", "dpA", 4, ""),
    ("Variância populacional", "σ² = Σ(xᵢ − x̄)² / n", "varP", 4, ""),
    ("Desvio padrão populacional", "σ = √σ²", "dpP", 4, ""),
    ("Coeficiente de variação", "CV = s / |x̄| × 100", "cv", 2, " %"),
]


def _celula(campo, casas, suf):
    if campo == "moda":
        return "_c.moda"
    if campo == "aiq":
        expr = "If(!IsBlank(_c.q1), _c.q3 - _c.q1)"
    else:
        expr = f"_c.{campo}"
    f = fmt(expr, casas)
    return f"{f} & If(IsBlank({expr}), \"\", \"{suf}\")" if suf else f


def html(colunas_expr=None):
    """Tabela HTML com as medidas (uma coluna por grupo)."""
    colunas_expr = colunas_expr or colunas()
    linhas = []
    for i, (rot, simb, campo, casas, suf) in enumerate(LINHAS):
        fundo = " style='background:#f3f6fa'" if i % 2 else ""
        linhas.append(
            f'"<tr{fundo}><td style=\'padding:4px 8px;white-space:nowrap\'>{rot}</td>'
            f'<td style=\'padding:4px 8px;color:#5a626a;white-space:nowrap\'>{simb}</td>" & '
            f'Concat(_cols As _c, "<td style=\'padding:4px 8px;text-align:right\'>" & {_celula(campo, casas, suf)} & "</td>") & '
            f'"</tr>"')
    corpo = " &\n        ".join(linhas)
    return f"""With({{_cols: {colunas_expr.replace(chr(10), chr(10) + "    ")}}},
    "<div style='font-family:Segoe UI,Arial;font-size:13px;color:#212529'>" &
    "<table style='border-collapse:collapse;width:100%'>" &
    "<tr style='background:#1f4e79;color:#ffffff'><th style='text-align:left;padding:6px 8px'>Medida</th>" &
    "<th style='text-align:left;padding:6px 8px'>Símbolo / fórmula</th>" &
    Concat(_cols, "<th style='text-align:right;padding:6px 8px'>" & EncodeHTML(Grupo) & "</th>") & "</tr>" &
        {corpo} &
    "</table>" &
    If(First(_cols).n = 0, "<p style='color:#b00020'>Não há valores numéricos para a variável escolhida.</p>", "") &
    "<p style='color:#5a626a;font-size:12px'>n.d. = não definido (por exemplo, a variância amostral precisa de n ≥ 2 " &
    "e o CV não se calcula quando a média é 0). Moda: «amodal» quando todos os valores têm a mesma frequência " &
    "(por exemplo, todos diferentes). Valores em branco na tabela de dados são ignorados.</p></div>"
)"""
