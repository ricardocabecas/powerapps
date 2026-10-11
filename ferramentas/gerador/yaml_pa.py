"""Emissor de ficheiros .pa.yaml (esquema de código fonte v3.0 das canvas apps).

Regras seguidas (documentação Microsoft "Power Fx YAML formula grammar" e esquema
https://raw.githubusercontent.com/microsoft/PowerApps-Tooling/refs/heads/master/schemas/pa-yaml/v3.0/pa.schema.yaml):

* todas as fórmulas começam por "=";
* fórmulas numa só linha não podem conter "#" nem ":" (mesmo dentro de texto);
  nesses casos, ou quando têm várias linhas, usa-se um bloco YAML "|-";
* os controlos são uma sequência de mapas {Nome: {Control, Variant?, Properties, Children?}};
  a ordem na sequência define a ordem Z (o último fica por cima);
* as fórmulas ficam no formato invariante (ponto decimal, vírgula como separador).
"""


class Controlo:
    def __init__(self, nome, tipo, props, variante=None, filhos=None):
        self.nome = nome
        self.tipo = tipo
        self.props = props
        self.variante = variante
        self.filhos = filhos or []


class Ecra:
    def __init__(self, nome, props, filhos, titulo=""):
        self.nome = nome
        self.props = props
        self.filhos = filhos
        self.titulo = titulo


def _chave(nome):
    # Nomes simples não precisam de aspas; os nossos nomes são todos simples.
    if not nome.replace("_", "").isalnum():
        raise ValueError("Nome de controlo inválido: " + nome)
    return nome


def _formula(chave, f, ind):
    pad = " " * ind
    f = f.strip("\n")
    precisa_bloco = ("\n" in f) or (":" in f) or ("#" in f) or f != f.strip() or f.startswith("'")
    if not precisa_bloco:
        return [f"{pad}{chave}: ={f}"]
    linhas = [f"{pad}{chave}: |-"]
    for i, l in enumerate(f.split("\n")):
        if "\t" in l:
            raise ValueError("Tabulações não são permitidas no YAML")
        l = l.rstrip()
        linhas.append(f"{pad}  {'=' if i == 0 else ''}{l}" if l else "")
    return linhas


def _props(props, ind):
    out = []
    for k in props:
        out += _formula(k, props[k], ind)
    return out


def _controlo(c, ind):
    pad = " " * ind
    out = [f"{pad}- {_chave(c.nome)}:", f"{pad}    Control: {c.tipo}"]
    if c.variante:
        out.append(f"{pad}    Variant: {c.variante}")
    if c.props:
        out.append(f"{pad}    Properties:")
        out += _props(c.props, ind + 6)
    if c.filhos:
        out.append(f"{pad}    Children:")
        for f in c.filhos:
            out += _controlo(f, ind + 6)
    return out


def ecra_yaml(e, cabecalho=""):
    """Ficheiro de ecrã no formato de código fonte (Screens: ...)."""
    out = [cabecalho.rstrip()] if cabecalho else []
    out += ["Screens:", f"  {_chave(e.nome)}:"]
    if e.props:
        out.append("    Properties:")
        out += _props(e.props, 6)
    out.append("    Children:")
    for c in e.filhos:
        out += _controlo(c, 6)
    return "\n".join(out) + "\n"


def controlos_yaml(e, cabecalho=""):
    """Só os controlos do ecrã, no formato que o Studio produz ao copiar controlos."""
    out = [cabecalho.rstrip()] if cabecalho else []
    for c in e.filhos:
        out += _controlo(c, 0)
    return "\n".join(out) + "\n"


def todas_formulas(e):
    """Lista (ecrã, controlo, propriedade, fórmula) para validação e documentação."""
    res = [(e.nome, e.nome, k, v) for k, v in e.props.items()]

    def rec(c):
        for k, v in c.props.items():
            res.append((e.nome, c.nome, k, v))
        for f in c.filhos:
            rec(f)
    for c in e.filhos:
        rec(c)
    return res


def todos_controlos(e):
    res = []

    def rec(c):
        res.append(c)
        for f in c.filhos:
            rec(f)
    for c in e.filhos:
        rec(c)
    return res
