"""Utilitários para fórmulas Power Fx.

As fórmulas são escritas no formato *invariante* (o formato exigido nos ficheiros
.pa.yaml): ponto decimal, vírgula como separador de argumentos e ponto e vírgula
para encadear instruções.

`para_pt_pt` converte uma fórmula para a sintaxe que um autor com região pt-PT vê
e escreve na barra de fórmulas do Power Apps Studio:

    invariante      pt-PT
    ----------      -----
    1.5             1,5      (separador decimal)
    ,               ;        (separador de argumentos, campos e registos)
    ;               ;;       (encadeamento de instruções)

O conteúdo de cadeias de texto ("..."), identificadores entre plicas ('...') e
comentários (// e /* */) nunca é alterado.
"""
import re

_IDENT = re.compile(r"[^\W\d]\w*")
_NUM = re.compile(r"[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?")


def _tokens(f):
    """Divide a fórmula em pedaços (tipo, texto)."""
    i, n = 0, len(f)
    while i < n:
        c = f[i]
        if c == '"':
            j = i + 1
            while j < n:
                if f[j] == '"':
                    if j + 1 < n and f[j + 1] == '"':
                        j += 2
                        continue
                    break
                j += 1
            if j >= n:
                raise ValueError("Cadeia de texto sem aspas de fecho: " + f[i:i + 40])
            yield "texto", f[i:j + 1]
            i = j + 1
        elif c == "'":
            j = i + 1
            while j < n:
                if f[j] == "'":
                    if j + 1 < n and f[j + 1] == "'":
                        j += 2
                        continue
                    break
                j += 1
            yield "ident", f[i:j + 1]
            i = j + 1
        elif f.startswith("//", i):
            j = f.find("\n", i)
            j = n if j < 0 else j
            yield "comentario", f[i:j]
            i = j
        elif f.startswith("/*", i):
            j = f.find("*/", i + 2)
            if j < 0:
                raise ValueError("Comentário /* sem fecho")
            yield "comentario", f[i:j + 2]
            i = j + 2
        elif c == "$" and i + 1 < n and f[i + 1] == '"':
            raise ValueError("Interpolação de texto ($\"...\") não suportada pelo conversor")
        elif c.isalpha() or c == "_":
            m = _IDENT.match(f, i)
            yield "ident", m.group(0)
            i = m.end()
        elif c.isdigit():
            m = _NUM.match(f, i)
            yield "numero", m.group(0)
            i = m.end()
        else:
            yield "simbolo", c
            i += 1


def para_pt_pt(f):
    """Converte uma fórmula do formato invariante para a sintaxe pt-PT da barra de fórmulas."""
    out = []
    for tipo, t in _tokens(f):
        if tipo == "numero":
            out.append(t.replace(".", ","))
        elif tipo == "simbolo" and t == ",":
            out.append(";")
        elif tipo == "simbolo" and t == ";":
            out.append(";;")
        else:
            out.append(t)
    return "".join(out)


def sem_comentarios(f):
    """Remove comentários (útil para medir o tamanho efetivo das fórmulas)."""
    return "".join(t for tipo, t in _tokens(f) if tipo != "comentario")


def texto(s):
    """Literal de texto Power Fx (aspas duplicadas no interior)."""
    return '"' + s.replace('"', '""') + '"'


def recuar(f, n):
    """Acrescenta n espaços a todas as linhas exceto a primeira (para encaixar subfórmulas)."""
    pad = " " * n
    return f.replace("\n", "\n" + pad)
