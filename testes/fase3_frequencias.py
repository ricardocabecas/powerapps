"""Fase 3 — Frequências e gráficos SVG."""
import os
import sys
import urllib.parse
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ferramentas"))
from gerador import f_frequencias as F, f_graficos as G  # noqa: E402
from gerador.f_comum import NOMES_EXEMPLO  # noqa: E402
from motor import pfx_valor, controlo_lista, controlo_texto, iguais  # noqa: E402
from referencia import frequencias as R  # noqa: E402
import dados_teste as D  # noqa: E402

NOME = "Fase 3 — Frequências e gráficos"
VARS = ["N1", "N2", "N3", "C1", "C2"]


def contexto(kv, valores, tipo, k, a, h):
    regs = []
    for i, v in enumerate(valores):
        r = {"Id": i + 1, "N1": None, "N2": None, "N3": None, "C1": "", "C2": ""}
        r[VARS[kv - 1]] = v if v is not None else (None if kv <= 3 else "")
        regs.append(r)
    def txt(x):
        return "" if x is None else str(x).replace(".", ",")
    return [{"nome": "varNomes", "expr": pfx_valor(NOMES_EXEMPLO)},
            {"nome": "colDados", "expr": pfx_valor(regs)},
            {"nome": "drpFreVar", "expr": controlo_lista(NOMES_EXEMPLO[VARS[kv - 1]])},
            {"nome": "drpFreTipo", "expr": controlo_lista(F.TIPOS[tipo - 1])},
            {"nome": "txtFreK", "expr": controlo_texto(txt(k))},
            {"nome": "txtFreInicio", "expr": controlo_texto(txt(a))},
            {"nome": "txtFreAmplitude", "expr": controlo_texto(txt(h))}]


def grafico():
    return (f"With({{_F: {F.tabela()}}}, If(_F.Tipo = 2, "
            f"{G.histograma('_F', '\"Histograma — \" & drpFreVar.Selected.Value', 'drpFreVar.Selected.Value')}, "
            f"{G.barras('_F', '\"Diagrama de barras — \" & drpFreVar.Selected.Value', 'drpFreVar.Selected.Value')}))")


def tarefas():
    t = []
    for (nome, kv, vals, tipo, k, a, h) in D.FREQUENCIAS:
        vs = contexto(kv, vals, tipo, k, a, h)
        t.append({"id": f"f3.{nome}", "vars": vs, "expr": F.tabela()})
        t.append({"id": f"f3.svg.{nome}", "vars": vs, "expr": grafico()})
        t.append({"id": f"f3.resumo.{nome}", "vars": vs, "expr": f"With({{_F: {F.tabela()}}}, {F.resumo()})"})
    return t


def svg_de_uri(uri):
    pref = "data:image/svg+xml;utf8,"
    assert uri.startswith(pref), "prefixo do URI"
    return urllib.parse.unquote(uri[len(pref):])


def verificar(res):
    out = []
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados", "graficos"), exist_ok=True)
    for (nome, kv, vals, tipo, k, a, h) in D.FREQUENCIAS:
        r = res[f"f3.{nome}"]
        if not r["ok"]:
            out.append((f"tabela «{nome}»", False, r.get("erro")))
            continue
        v = r["valor"]
        if tipo == 1 or kv >= 4:
            ref = {"Linhas": R.discreta(vals)}
        else:
            ref = R.classes(vals, k, a, h)
        difs = []
        if len(v["Linhas"]) != len(ref["Linhas"]):
            difs.append(f"n.º de linhas {len(v['Linhas'])}≠{len(ref['Linhas'])}")
        for lp, lr in zip(v["Linhas"], ref["Linhas"]):
            for campo in ["Classe", "ni", "fi", "Ni", "Fi", "Centro", "Li", "Ls", "Ordem"]:
                if not iguais(lp.get(campo), lr.get(campo), 1e-9):
                    difs.append(f"{lr['Classe']}.{campo}: Power Fx={lp.get(campo)} ref={lr.get(campo)}")
        if tipo == 2 and kv <= 3:
            for campo in ["k", "kSturges", "a", "h", "Fora"]:
                if not iguais(v.get(campo), ref[campo]):
                    difs.append(f"{campo}: Power Fx={v.get(campo)} ref={ref[campo]}")
        det = " | ".join(f"{l['Classe']}: {l['ni']}" for l in v["Linhas"][:8])
        out.append((f"tabela «{nome}»", not difs, det if not difs else "; ".join(difs[:6])))
        # Gráfico: URI de dados com SVG bem formado
        s = res[f"f3.svg.{nome}"]
        ok, det = s["ok"], s.get("erro", "")
        if ok:
            try:
                svg = svg_de_uri(s["valor"])
                raiz = ET.fromstring(svg)
                nrect = sum(1 for e in raiz.iter() if e.tag.endswith("rect")) - 1
                det = f"SVG válido, {len(svg)} caracteres, {nrect} barras"
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados", "graficos",
                                       f"{nome}.svg"), "w", encoding="utf-8") as f:
                    f.write(svg)
                ok = nrect == len(ref["Linhas"]) and "," not in "".join(
                    e.get("x", "") + e.get("y", "") + e.get("width", "") + e.get("height", "") for e in raiz.iter())
            except Exception as ex:  # noqa: BLE001
                ok, det = False, f"SVG inválido: {ex}"
        out.append((f"gráfico «{nome}»", ok, det))
        rs = res[f"f3.resumo.{nome}"]
        out.append((f"resumo «{nome}»", rs["ok"], (rs.get("valor") or rs.get("erro") or "").replace("\n", " ⏎ ")))
    return out
