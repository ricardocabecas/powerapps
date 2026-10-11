"""Fase 4 — Correlação e regressão linear simples."""
import os
import sys
import urllib.parse
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ferramentas"))
from gerador import f_regressao as F, ecra_regressao as E  # noqa: E402
from gerador.f_comum import NOMES_EXEMPLO  # noqa: E402
from motor import pfx_valor, controlo_lista, controlo_texto, iguais  # noqa: E402
from referencia import regressao as R  # noqa: E402
from referencia.colagem import numero  # noqa: E402
import dados_teste as D  # noqa: E402

NOME = "Fase 4 — Correlação e regressão"
CAMPOS = ["n", "mediaX", "mediaY", "Sxx", "Syy", "Sxy", "sx", "sy", "cov", "r", "r2", "b", "a", "previsao"]


def contexto(xs, ys, x0):
    regs = [{"Id": i + 1, "N1": x, "N2": y, "N3": None, "C1": "", "C2": ""} for i, (x, y) in enumerate(zip(xs, ys))]
    return [{"nome": "varNomes", "expr": pfx_valor(NOMES_EXEMPLO)},
            {"nome": "colDados", "expr": pfx_valor(regs)},
            {"nome": "drpRegX", "expr": controlo_lista(NOMES_EXEMPLO["N1"])},
            {"nome": "drpRegY", "expr": controlo_lista(NOMES_EXEMPLO["N2"])},
            {"nome": "txtRegX0", "expr": controlo_texto(x0)}]


def tarefas():
    t = []
    for nome, (xs, ys, x0) in D.REGRESSAO.items():
        vs = contexto(xs, ys, x0)
        t.append({"id": f"f4.{nome}", "vars": vs, "expr": F.resultados()})
        t.append({"id": f"f4.html.{nome}", "vars": vs, "expr": F.html()})
        t.append({"id": f"f4.svg.{nome}", "vars": vs, "expr": E.grafico()})
    return t


def verificar(res):
    out = []
    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados", "graficos")
    os.makedirs(pasta, exist_ok=True)
    for nome, (xs, ys, x0) in D.REGRESSAO.items():
        ref = R.regressao(xs, ys, numero(x0)[0])
        r = res[f"f4.{nome}"]
        if not r["ok"]:
            out.append((f"regressão «{nome}»", False, r.get("erro")))
        else:
            v = r["valor"]
            difs = [f"{c}: Power Fx={v.get(c)} ref={ref[c]}" for c in CAMPOS + ["glR", "tR"]
                    if not iguais(v.get(c), ref[c], 1e-9)]
            # valor de p do teste de ρ = 0 (integração numérica): tolerância absoluta 1e-6
            if (v.get("pR") is None) != (ref["pR"] is None) or (ref["pR"] is not None and abs(v["pR"] - ref["pR"]) > 1e-6):
                difs.append(f"pR: Power Fx={v.get('pR')} ref={ref['pR']}")
            out.append((f"regressão «{nome}»", not difs,
                        f"n={v['n']}, r={v.get('r')}, b={v.get('b')}, a={v.get('a')}, ŷ(x0)={v.get('previsao')}, "
                        f"p(ρ=0)={v.get('pR')} (scipy {ref['pR']})"
                        if not difs else "; ".join(difs)))
        h = res[f"f4.html.{nome}"]
        out.append((f"tabela HTML «{nome}»", h["ok"] and "<table" in (h.get("valor") or ""), h.get("erro", "ok")))
        s = res[f"f4.svg.{nome}"]
        ok, det = s["ok"], s.get("erro", "")
        if ok:
            try:
                svg = urllib.parse.unquote(s["valor"][len("data:image/svg+xml;utf8,"):])
                raiz = ET.fromstring(svg)
                circ = [e for e in raiz.iter() if e.tag.endswith("circle")]
                npts = len(circ)
                # todos os pontos têm de ficar dentro da área do gráfico (x 70..620, y 40..330)
                dentro = all(69.9 <= float(e.get("cx")) <= 620.1 and 39.9 <= float(e.get("cy")) <= 330.1 for e in circ)
                ok = npts == ref["n"] and dentro
                det = (f"SVG válido, {npts} pontos" + (", com reta" if "clip-path" in svg else "") +
                       ("" if dentro else ", ⚠ pontos fora da área do gráfico"))
                with open(os.path.join(pasta, f"dispersao_{nome}.svg"), "w", encoding="utf-8") as f:
                    f.write(svg)
            except Exception as ex:  # noqa: BLE001
                ok, det = False, f"SVG inválido: {ex}"
        out.append((f"dispersão «{nome}»", ok, det))
    return out
