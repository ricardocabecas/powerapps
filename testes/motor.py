"""Ligação ao motor Power Fx (.NET) e utilitários de comparação."""
import json
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(AQUI, "resultados", "tmp")
PROJ = os.path.join(AQUI, "motor-powerfx")


def correr(tarefas):
    """Executa uma lista de tarefas no interpretador Power Fx e devolve {id: resultado}."""
    os.makedirs(TMP, exist_ok=True)
    ent = os.path.join(TMP, "entrada.json")
    sai = os.path.join(TMP, "saida.json")
    with open(ent, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, ensure_ascii=False)
    subprocess.run(["dotnet", "build", PROJ, "-c", "Release", "--nologo", "-v", "q"], check=True,
                   stdout=subprocess.DEVNULL)
    dll = os.path.join(PROJ, "bin", "Release", "net8.0", "MotorPowerFx.dll")
    subprocess.run(["dotnet", dll, ent, sai], check=True, stdout=subprocess.DEVNULL)
    with open(sai, encoding="utf-8") as f:
        return {r["id"]: r for r in json.load(f)}


def pfx_valor(v):
    """Valor Python -> expressão Power Fx (para preparar variáveis de contexto)."""
    if v is None:
        return "Blank()"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(float(v)) if not float(v).is_integer() else str(int(v))
    if isinstance(v, str):
        return '"' + v.replace('"', '""') + '"'
    if isinstance(v, dict):
        return "{" + ", ".join(f"{k}: {pfx_valor(x)}" for k, x in v.items()) + "}"
    if isinstance(v, list):
        if not v:
            raise ValueError("lista vazia sem tipo")
        return "Table(" + ", ".join(pfx_valor(x) for x in v) + ")"
    raise TypeError(type(v))


def controlo_lista(valor):
    """Simula uma lista pendente clássica: Nome.Selected.Value."""
    return "{Selected: {Value: " + pfx_valor(valor) + "}}"


def controlo_texto(valor):
    """Simula uma caixa de texto clássica: Nome.Text."""
    return "{Text: " + pfx_valor(valor) + "}"


def iguais(a, b, tol=1e-9):
    """Compara valores (números com tolerância relativa/absoluta)."""
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(iguais(a[k], b[k], tol) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(iguais(x, y, tol) for x, y in zip(a, b))
    return a == b
