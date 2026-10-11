"""Gera os ficheiros da app a partir das definições em Python.

    python3 ferramentas/gerar.py

Produz:
  Src/<ecrã>.pa.yaml           um ficheiro por ecrã (formato de código fonte, "Screens:")
  colar/<ecrã>.controlos.yaml  só os controlos do ecrã (formato de "copiar código" de controlos)
  testes/resultados/tmp/formulas.json  todas as fórmulas, para os testes de sintaxe
e valida cada ficheiro contra o esquema oficial pa.schema.yaml v3.0.
"""
import json
import os
import sys

import yaml
import jsonschema

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

from gerador.pfx import verificar_parenteses  # noqa: E402
from gerador.yaml_pa import ecra_yaml, controlos_yaml, todas_formulas, todos_controlos  # noqa: E402
from gerador import ecra_dados, ecra_descritiva, ecra_frequencias, ecra_regressao, ecra_testes_t, ecra_anova, ecra_qui  # noqa: E402

MODULOS = [ecra_dados, ecra_descritiva, ecra_frequencias, ecra_regressao, ecra_testes_t, ecra_anova, ecra_qui]


def ecras():
    return [m.construir() for m in MODULOS]


def validar(texto, esquema, nome):
    doc = yaml.safe_load(texto)
    jsonschema.validate(doc, esquema)
    # Verificações extra: nomes de controlos únicos e fórmulas a começar por "="
    return doc


def gerar_documentos():
    """Preenche os modelos em ferramentas/modelos/*.md e escreve-os em docs/.
    Marcadores:  {{pt: <expressão Python>}}  -> bloco de código com a fórmula em sintaxe pt-PT
                 {{inv: <expressão Python>}} -> bloco de código com a fórmula em formato invariante
                 {{txt: <expressão Python>}} -> texto simples"""
    import re
    from gerador.pfx import para_pt_pt
    from gerador import f_comum, f_dados  # noqa: F401
    ctx = {"F_comum": f_comum, "F_dados": f_dados}
    for nome in ("f_descritiva", "f_frequencias", "f_regressao", "f_inferencia", "f_graficos"):
        try:
            ctx["F_" + nome[2:]] = __import__("gerador." + nome, fromlist=["x"])
        except ImportError:
            pass
    pasta = os.path.join(AQUI, "modelos")
    for fich in sorted(os.listdir(pasta)):
        txt = open(os.path.join(pasta, fich), encoding="utf-8").read()

        def subst(m):
            tipo, expr = m.group(1), m.group(2).strip()
            val = eval(expr, ctx)
            if tipo == "txt":
                return str(val)
            f = para_pt_pt(val) if tipo == "pt" else val
            return "```powerfx\n" + f.strip("\n") + "\n```"
        txt = re.sub(r"\{\{(pt|inv|txt):(.*?)\}\}", subst, txt, flags=re.S)
        with open(os.path.join(RAIZ, "docs", fich), "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
        print(f"docs/{fich} gerado.")


def main():
    esquema = yaml.safe_load(open(os.path.join(AQUI, "pa.schema.v3.0.yaml"), encoding="utf-8"))
    # O esquema oficial tem um parêntese a menos na expressão regular de CodeComponent
    # (controlos PCF, que esta app não usa). Corrige-se só em memória para o validador aceitar o esquema.
    cc = esquema["definitions"]["CodeComponent-ComponentName"]
    if cc["pattern"].startswith("^([a-zA-Z][a-zA-Z0-9]{1,7})_)?"):
        cc["pattern"] = "^(" + cc["pattern"][1:]
    os.makedirs(os.path.join(RAIZ, "Src"), exist_ok=True)
    os.makedirs(os.path.join(RAIZ, "colar"), exist_ok=True)
    os.makedirs(os.path.join(RAIZ, "testes", "resultados", "tmp"), exist_ok=True)
    nomes_vistos = {}
    formulas = []
    for e in ecras():
        txt = ecra_yaml(e)
        validar(txt, esquema, e.nome)
        with open(os.path.join(RAIZ, "Src", e.nome + ".pa.yaml"), "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
        txt_c = controlos_yaml(e)
        lista = yaml.safe_load(txt_c)
        assert isinstance(lista, list)
        with open(os.path.join(RAIZ, "colar", e.nome + ".controlos.yaml"), "w", encoding="utf-8",
                  newline="\n") as f:
            f.write(txt_c)
        # nomes únicos em toda a app (exigência do Power Apps)
        for c in todos_controlos(e):
            if c.nome in nomes_vistos:
                raise SystemExit(f"Nome repetido: {c.nome} ({e.nome} e {nomes_vistos[c.nome]})")
            nomes_vistos[c.nome] = e.nome
        for (ecra, ctl, prop, f) in todas_formulas(e):
            erro = verificar_parenteses(f)
            if erro:
                raise SystemExit(f"Parênteses desequilibrados em {ecra}.{ctl}.{prop}: {erro}")
            formulas.append({"ecra": ecra, "controlo": ctl, "propriedade": prop, "formula": f})
        print(f"{e.nome}: {len(todos_controlos(e))} controlos, {len(txt.splitlines())} linhas — esquema OK")
    with open(os.path.join(RAIZ, "testes", "resultados", "tmp", "formulas.json"), "w", encoding="utf-8") as f:
        json.dump(formulas, f, ensure_ascii=False, indent=1)
    print(f"{len(formulas)} fórmulas exportadas.")
    gerar_documentos()


if __name__ == "__main__":
    main()
