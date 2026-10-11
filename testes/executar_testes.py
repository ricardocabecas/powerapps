"""Executa todos os testes: sintaxe de todas as fórmulas (invariante e pt-PT) e
comparação dos cálculos Power Fx com a implementação de referência em Python/scipy.

    python3 testes/executar_testes.py

Escreve testes/resultados/comparacao.md e testes/resultados/resultados.json.
"""
import datetime
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "ferramentas"))

from gerador.pfx import para_pt_pt  # noqa: E402
from motor import correr  # noqa: E402
import gerar  # noqa: E402

import fase1_dados  # noqa: E402

FASES = [fase1_dados]
for _m in ["fase2_descritiva", "fase3_frequencias", "fase4_regressao", "fase5_inferencia"]:
    try:
        FASES.append(__import__(_m))
    except ImportError:
        pass


def tarefas_sintaxe():
    gerar.main()
    with open(os.path.join(AQUI, "resultados", "tmp", "formulas.json"), encoding="utf-8") as f:
        formulas = json.load(f)
    t = []
    for i, d in enumerate(formulas):
        t.append({"id": f"sint.inv.{i}", "modo": "analisar", "expr": d["formula"]})
        t.append({"id": f"sint.pt.{i}", "modo": "analisar", "cultura": "pt-PT", "expr": para_pt_pt(d["formula"])})
    return formulas, t


def main():
    formulas, t = tarefas_sintaxe()
    for fase in FASES:
        t += fase.tarefas()
    print(f"A executar {len(t)} tarefas no interpretador Power Fx…")
    res = correr(t)

    linhas = []
    total_ok = total = 0
    # Sintaxe
    falhas = []
    for i, d in enumerate(formulas):
        for tipo in ("inv", "pt"):
            r = res[f"sint.{tipo}.{i}"]
            if not r["ok"]:
                falhas.append(f"{d['ecra']}.{d['controlo']}.{d['propriedade']} ({tipo}): {r.get('erro')}")
    n_sint = 2 * len(formulas)
    total += n_sint
    total_ok += n_sint - len(falhas)
    linhas.append("## Sintaxe de todas as fórmulas dos ecrãs\n")
    linhas.append(f"{len(formulas)} fórmulas analisadas em formato invariante (ficheiros .pa.yaml) e convertidas "
                  f"para pt-PT (barra de fórmulas): **{n_sint - len(falhas)}/{n_sint} sem erros de sintaxe**.\n")
    for f_ in falhas:
        linhas.append(f"- ❌ {f_}")
    linhas.append("")

    detalhe = {}
    for fase in FASES:
        out = fase.verificar(res)
        ok = sum(1 for _, o, _ in out if o)
        total += len(out)
        total_ok += ok
        linhas.append(f"## {fase.NOME}\n")
        linhas.append(f"**{ok}/{len(out)} casos de acordo com a referência.**\n")
        linhas.append("| Caso | Resultado | Detalhe |")
        linhas.append("|---|---|---|")
        for caso, o, det in out:
            det = str(det).replace("|", "\\|").replace("\n", " ")
            if len(det) > 400:
                det = det[:400] + "…"
            linhas.append(f"| {caso} | {'✅' if o else '❌'} | {det} |")
        linhas.append("")
        detalhe[fase.NOME] = [{"caso": c, "ok": o, "detalhe": str(d)} for c, o, d in out]

    cab = [
        "# Resultados da comparação Power Fx × referência Python/scipy\n",
        f"Gerado em {datetime.date.today().strftime('%d/%m/%Y')} por `testes/executar_testes.py`. "
        "As fórmulas foram executadas com o interpretador open source **Microsoft.PowerFx.Interpreter 1.8.1** "
        "(.NET 8), com números em vírgula flutuante (como nas canvas apps).\n",
        f"**Total: {total_ok}/{total} verificações sem diferenças.**\n",
    ]
    with open(os.path.join(AQUI, "resultados", "comparacao.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(cab + linhas) + "\n")
    with open(os.path.join(AQUI, "resultados", "resultados.json"), "w", encoding="utf-8") as f:
        json.dump({"total": total, "ok": total_ok, "sintaxe_falhas": falhas, "fases": detalhe}, f,
                  ensure_ascii=False, indent=1)
    print(f"Total: {total_ok}/{total} verificações sem diferenças.")
    import gerar_folha
    gerar_folha.main()
    return 0 if total_ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
