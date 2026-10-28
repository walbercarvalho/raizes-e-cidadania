#!/usr/bin/env python3
"""Ferramenta do núcleo documental da família (só biblioteca padrão do Python 3.8+).

Uso:
  python arvore.py iniciar <pasta>            cria a estrutura de um projeto novo
  python arvore.py validar <pessoas.json>     confere ids, vínculos, fontes e datas
  python arvore.py html <pessoas.json> [-o arvore.html]
  python arvore.py gedcom <pessoas.json> [-o arvore.ged]
  python arvore.py fichas <pessoas.json> [-d fichas]
  python arvore.py documentos <pessoas.json> [-o documentos-organizados/indice-dos-documentos.csv]
  python arvore.py pendencias <pessoas.json> [-o pendencias.md]
  python arvore.py tudo <pessoas.json>        valida e gera html, gedcom, fichas, índice e pendências

O formato do pessoas.json está em references/formato-pessoas-json.md.
"""
import argparse
import csv
import datetime
import html
import json
import os
import re
import sys

STATUS = ("confirmado", "relato", "hipotese")
TIPOS_EVENTO = ("nascimento", "batismo", "casamento", "obito", "sepultamento",
                "imigracao", "emigracao", "naturalizacao", "residencia", "outro")
MESES_GED = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
BOM_CSV = "utf-8-sig"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------- leitura

def carregar(caminho):
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    for chave in ("pessoas", "unioes", "documentos", "divergencias", "cadeias"):
        dados.setdefault(chave, [])
    return dados


def indice(lista):
    return {item["id"]: item for item in lista if "id" in item}


def evento(pessoa, tipo):
    for ev in pessoa.get("eventos", []):
        if ev.get("tipo") == tipo:
            return ev
    return None


def ano(ev):
    if not ev:
        return ""
    m = re.search(r"\d{4}", str(ev.get("data", "")))
    return m.group(0) if m else ""


def ano_txt(ev):
    a = ano(ev)
    if a and not re.match(r"^\d{4}", str(ev.get("data", ""))):
        return "c. " + a
    return a


def anos_vida(p):
    n = ano_txt(evento(p, "nascimento") or evento(p, "batismo"))
    o = ano_txt(evento(p, "obito"))
    if n or o:
        return "%s–%s" % (n or "?", o or ("" if not evento(p, "obito") else "?"))
    return ""


def gravar(caminho, texto):
    pasta = os.path.dirname(os.path.abspath(caminho))
    os.makedirs(pasta, exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


# ---------------------------------------------------------------- validação

# ---------------------------------------------------------------- origem (país, reino ou povo)

# Ícones simplificados (SVG 30x20) do Estado de cada época. Não são reproduções
# oficiais exatas; servem para reconhecer a origem de relance.
BANDEIRAS = {
    "br": '<rect width="30" height="20" fill="#009c3b"/><path d="M15 2.6 27.4 10 15 17.4 2.6 10z" fill="#ffdf00"/><circle cx="15" cy="10" r="4.3" fill="#002776"/><path d="M10.9 9.2q4.3-1 8.3 1.5" stroke="#fff" stroke-width=".7" fill="none"/>',
    "br-imperio": '<rect width="30" height="20" fill="#00953e"/><path d="M15 2.6 27.4 10 15 17.4 2.6 10z" fill="#fcd116"/><path d="M12.4 7.6h5.2v3.4q0 2.6-2.6 3.2-2.6-.6-2.6-3.2z" fill="#00953e" stroke="#fff" stroke-width=".5"/><path d="M12.8 6.9l.6-1.6 1.6.9 1.6-.9.6 1.6z" fill="#fcd116" stroke="#8a6d00" stroke-width=".2"/>',
    "pt": '<rect width="30" height="20" fill="#da291c"/><rect width="12" height="20" fill="#046a38"/><circle cx="12" cy="10" r="4.4" fill="none" stroke="#ffe900" stroke-width="1.2"/><path d="M10 7.7h4v3.2q0 1.9-2 2.4-2-.5-2-2.4z" fill="#fff" stroke="#da291c" stroke-width=".6"/>',
    "pt-reino": '<rect width="15" height="20" fill="#0038a8"/><rect x="15" width="15" height="20" fill="#fff"/><path d="M12 7.5h6v4q0 3-3 3.6-3-.6-3-3.6z" fill="#fff" stroke="#c8102e" stroke-width="1"/><circle cx="15" cy="10.5" r="1" fill="#0038a8"/><path d="M12.3 6.8l.7-2 2 1 2-1 .7 2z" fill="#f2c200"/>',
    "it": '<rect width="10" height="20" fill="#009246"/><rect x="10" width="10" height="20" fill="#fff"/><rect x="20" width="10" height="20" fill="#ce2b37"/>',
    "it-reino": '<rect width="10" height="20" fill="#009246"/><rect x="10" width="10" height="20" fill="#fff"/><rect x="20" width="10" height="20" fill="#ce2b37"/><path d="M12.6 6.5h4.8v4.3q0 2.4-2.4 3-2.4-.6-2.4-3z" fill="#ce2b37" stroke="#1f5fbf" stroke-width=".5"/><path d="M15 7.3v6M13.3 9.6h3.4" stroke="#fff" stroke-width="1"/>',
    "es": '<rect width="30" height="20" fill="#aa151b"/><rect y="5" width="30" height="10" fill="#f1bf00"/>',
    "es-rep": '<rect width="30" height="6.67" fill="#da121a"/><rect y="6.67" width="30" height="6.67" fill="#fcdd09"/><rect y="13.33" width="30" height="6.67" fill="#6d2c84"/>',
    "jp": '<rect width="30" height="20" fill="#fff"/><circle cx="15" cy="10" r="6" fill="#bc002d"/>',
    "ar": '<rect width="30" height="20" fill="#74acdf"/><rect y="6.67" width="30" height="6.67" fill="#fff"/><circle cx="15" cy="10" r="2" fill="#f6b40e"/>',
    "fr": '<rect width="10" height="20" fill="#002395"/><rect x="10" width="10" height="20" fill="#fff"/><rect x="20" width="10" height="20" fill="#ed2939"/>',
    "de": '<rect width="30" height="6.67"/><rect y="6.67" width="30" height="6.67" fill="#dd0000"/><rect y="13.33" width="30" height="6.67" fill="#ffce00"/>',
    "de-imperio": '<rect width="30" height="6.67"/><rect y="6.67" width="30" height="6.67" fill="#fff"/><rect y="13.33" width="30" height="6.67" fill="#dd0000"/>',
    "at": '<rect width="30" height="20" fill="#ed2939"/><rect y="6.67" width="30" height="6.67" fill="#fff"/>',
    "at-hu": '<rect width="30" height="10"/><rect y="10" width="30" height="10" fill="#fcd116"/>',
    "pl": '<rect width="30" height="10" fill="#fff"/><rect y="10" width="30" height="10" fill="#dc143c"/>',
    "lb": '<rect width="30" height="20" fill="#ed1c24"/><rect y="5" width="30" height="10" fill="#fff"/><path d="M15 6.2l3.2 6.6h-6.4z" fill="#00a651"/>',
    "otomano": '<rect width="30" height="20" fill="#e30a17"/><circle cx="13" cy="10" r="5" fill="#fff"/><circle cx="14.3" cy="10" r="4" fill="#e30a17"/><path d="M19.6 10l-3 1 1.8-2.5v3l-1.8-2.5z" fill="#fff"/>',
    "us": '<rect width="30" height="20" fill="#fff"/><path d="M0 0h30v1.54H0zm0 3.08h30v1.54H0zm0 3.08h30v1.54H0zm0 3.08h30v1.54H0zm0 3.08h30v1.54H0zm0 3.08h30v1.54H0zm0 3.08h30v1.54H0z" fill="#b22234"/><rect width="12" height="10.77" fill="#3c3b6e"/>',
}

PAISES = {
    "BR": ("Brasil", ("brasil", "brazil")), "PT": ("Portugal", ("portugal",)),
    "IT": ("Itália", ("itália", "italia", "italy")), "ES": ("Espanha", ("espanha", "españa", "spain")),
    "JP": ("Japão", ("japão", "japao", "japan")), "AR": ("Argentina", ("argentina",)),
    "FR": ("França", ("frança", "franca", "france")), "DE": ("Alemanha", ("alemanha", "germany", "deutschland")),
    "AT": ("Áustria", ("áustria", "austria")), "PL": ("Polônia", ("polônia", "polonia", "poland")),
    "LB": ("Líbano", ("líbano", "libano", "lebanon")), "SY": ("Síria", ("síria", "siria", "syria")),
    "US": ("Estados Unidos", ("estados unidos", "eua", "usa")),
}
UFS = set("AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split())

# Estado de cada época: (início, fim, ícone, nome). Início incluído, fim excluído; None = sem limite.
PERIODOS = {
    "BR": [(None, "1815-12-16", "pt-reino", "Estado do Brasil, colônia do Reino de Portugal"),
           ("1815-12-16", "1822-09-07", "pt-reino", "Reino Unido de Portugal, Brasil e Algarves"),
           ("1822-09-07", "1889-11-15", "br-imperio", "Império do Brasil"),
           ("1889-11-15", None, "br", "República do Brasil")],
    "PT": [(None, "1910-10-05", "pt-reino", "Reino de Portugal"), ("1910-10-05", None, "pt", "República Portuguesa")],
    "IT": [(None, "1861-03-17", "", "Estados italianos antes da unificação"),
           ("1861-03-17", "1946-06-02", "it-reino", "Reino de Itália"), ("1946-06-02", None, "it", "República Italiana")],
    "ES": [(None, "1873-02-11", "es", "Reino de Espanha"), ("1873-02-11", "1874-12-29", "es", "Primeira República Espanhola"),
           ("1874-12-29", "1931-04-14", "es", "Reino de Espanha"), ("1931-04-14", "1939-04-01", "es-rep", "Segunda República Espanhola"),
           ("1939-04-01", "1975-11-22", "es", "Espanha (regime de Franco)"), ("1975-11-22", None, "es", "Reino de Espanha")],
    "JP": [(None, "1868-01-03", "jp", "Japão (xogunato Tokugawa)"), ("1868-01-03", "1947-05-03", "jp", "Império do Japão"),
           ("1947-05-03", None, "jp", "Japão")],
    "DE": [(None, "1871-01-18", "", "Estados alemães antes da unificação"), ("1871-01-18", "1918-11-09", "de-imperio", "Império Alemão"),
           ("1918-11-09", None, "de", "Alemanha")],
    "AT": [(None, "1867-03-30", "at", "Império Austríaco"), ("1867-03-30", "1918-11-12", "at-hu", "Áustria-Hungria"),
           ("1918-11-12", None, "at", "Áustria")],
    "PL": [(None, "1918-11-11", "", "Polônia dividida entre Rússia, Prússia e Áustria"), ("1918-11-11", None, "pl", "Polônia")],
    "LB": [(None, "1918-10-01", "otomano", "Império Otomano"), ("1918-10-01", "1943-11-22", "lb", "Líbano sob mandato francês"),
           ("1943-11-22", None, "lb", "Líbano")],
    "SY": [(None, "1918-10-01", "otomano", "Império Otomano"), ("1918-10-01", None, "", "Síria")],
    "AR": [(None, None, "ar", "Argentina")], "FR": [(None, None, "fr", "França")], "US": [(None, None, "us", "Estados Unidos")],
}


def intervalo(data):
    """Primeiro e último dia possíveis de uma data do pessoas.json; None quando não há data legível."""
    v = str(data or "").strip()

    def lim(s, fim):
        m = re.match(r"^(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?$", s.strip())
        if not m:
            return None
        a, me, d = m.groups()
        if d:
            return "%s-%s-%s" % (a, me, d)
        if me:
            return "%s-%s-%s" % (a, me, "31" if fim else "01")
        return "%s-%s" % (a, "12-31" if fim else "01-01")

    if not v:
        return None
    if v.startswith("c. "):
        m = re.match(r"\d{4}", v[3:])
        return ("%d-01-01" % (int(m.group()) - 2), "%d-12-31" % (int(m.group()) + 2)) if m else None
    if v.startswith("antes de "):
        f = lim(v[9:], False)
        return (None, f) if f else None
    if v.startswith("depois de "):
        i = lim(v[10:], True)
        return (i, None) if i else None
    m = re.match(r"^entre (\S+) e (\S+)$", v)
    if m:
        i, f = lim(m.group(1), False), lim(m.group(2), True)
        return (i, f) if i and f else None
    i = lim(v, False)
    return (i, lim(v, True)) if i else None


def pais_do_local(local):
    partes = [re.sub(r"\[\?\]", "", x).strip() for x in str(local or "").split(",")]
    for parte in reversed(partes):
        if parte.upper() in UFS and len(parte) == 2:
            return "BR"
        baixo = parte.lower()
        for cod, (_, chaves) in PAISES.items():
            if any(c in baixo for c in chaves):
                return cod
    return None


def origem_pessoa(p):
    """Origem da pessoa: a declarada em 'origem' ou a deduzida do local e da data de nascimento."""
    if p.get("origem"):
        o = p["origem"]
        return {"icone": o.get("icone", ""), "nome": o.get("nome", ""), "nota": o.get("nota", ""), "derivado": False}
    ev = evento(p, "nascimento") or evento(p, "batismo")
    cod = pais_do_local((ev or {}).get("local"))
    if not cod:
        return None
    lista = PERIODOS.get(cod, [(None, None, "", PAISES[cod][0])])
    inter = intervalo((ev or {}).get("data"))
    if inter:
        ini, fim = inter
        lista = [x for x in lista if (x[1] is None or ini is None or ini < x[1]) and (x[0] is None or fim is None or fim >= x[0])]
    icones = {x[2] for x in lista}
    nome = " ou ".join(dict.fromkeys(x[3] for x in lista)) or PAISES[cod][0]
    if len(lista) > 1:
        nome = nome + " (época incerta)" if inter else PAISES[cod][0] + " (época não informada)"
    return {"icone": icones.pop() if len(icones) == 1 else "", "nome": nome, "sigla": cod, "derivado": True}


def destaque_links(p):
    return [l for l in (p.get("destaque") or {}).get("links", []) if l.get("url")]


RE_DATA = re.compile(r"^(c\. |antes de |depois de )?\d{4}(-\d{2}(-\d{2})?)?$|^entre \d{4}(-\d{2}(-\d{2})?)? e \d{4}(-\d{2}(-\d{2})?)?$")


def validar(dados, base):
    erros, avisos = [], []
    pessoas = indice(dados["pessoas"])
    docs = indice(dados["documentos"])

    vistos = set()
    for colecao in ("pessoas", "unioes", "documentos"):
        for item in dados[colecao]:
            i = item.get("id")
            if not i:
                erros.append("%s sem id: %s" % (colecao, json.dumps(item, ensure_ascii=False)[:80]))
            elif i in vistos:
                erros.append("id repetido: %s" % i)
            vistos.add(i)

    def conferir_fato(dono, fato, rotulo):
        st = fato.get("status")
        if st not in STATUS:
            erros.append("%s, %s: status '%s' inválido (use %s)" % (dono, rotulo, st, ", ".join(STATUS)))
        fontes = fato.get("fontes", [])
        for d in fontes:
            if d not in docs:
                erros.append("%s, %s: fonte '%s' não existe em documentos" % (dono, rotulo, d))
        if st == "confirmado" and not fontes:
            erros.append("%s, %s: marcado como confirmado sem documento em fontes" % (dono, rotulo))
        if st == "relato" and not fato.get("nota"):
            avisos.append("%s, %s: relato sem nota dizendo quem contou e quando" % (dono, rotulo))
        data = fato.get("data")
        if data and not RE_DATA.match(str(data)):
            avisos.append("%s, %s: data '%s' fora do padrão (AAAA-MM-DD, AAAA-MM, AAAA, 'c. AAAA', 'entre AAAA e AAAA')" % (dono, rotulo, data))

    for p in dados["pessoas"]:
        pid = p.get("id", "?")
        if not p.get("nome"):
            erros.append("%s: sem nome" % pid)
        if p.get("sexo") not in ("M", "F", "?", None):
            avisos.append("%s: sexo '%s' (use M, F ou ?)" % (pid, p.get("sexo")))
        for pai in p.get("pais", []):
            if pai not in pessoas:
                erros.append("%s: pai/mãe '%s' não existe" % (pid, pai))
        if len(p.get("pais", [])) > 2:
            erros.append("%s: mais de dois pais" % pid)
        if p.get("filiacao"):
            conferir_fato(pid, p["filiacao"], "filiação")
        for ev in p.get("eventos", []):
            if ev.get("tipo") not in TIPOS_EVENTO:
                avisos.append("%s: evento '%s' desconhecido" % (pid, ev.get("tipo")))
            conferir_fato(pid, ev, ev.get("tipo", "evento"))
        o = p.get("origem")
        if o is not None:
            if not isinstance(o, dict) or not o.get("nome"):
                erros.append("%s: origem precisa de 'nome' (e, se houver, 'icone')" % pid)
            elif o.get("icone") and o["icone"] not in BANDEIRAS:
                avisos.append("%s: ícone de origem '%s' desconhecido; a árvore mostra a sigla" % (pid, o["icone"]))
        dq = p.get("destaque")
        if dq is not None:
            if not dq.get("resumo"):
                erros.append("%s: destaque sem resumo" % pid)
            if not destaque_links(p):
                erros.append("%s: destaque sem link para a fonte" % pid)
            for l in dq.get("links", []):
                if not str(l.get("url", "")).startswith(("http://", "https://")):
                    erros.append("%s: link do destaque sem endereço http(s): %s" % (pid, l.get("titulo", "")))
            conferir_fato(pid, dq, "destaque")
            if dq.get("status") == "confirmado" and not dq.get("nota"):
                avisos.append("%s, destaque: diga na nota o que prova que a figura conhecida é esta pessoa" % pid)
            if not dq.get("consultado"):
                avisos.append("%s, destaque: falta a data de consulta das fontes ('consultado')" % pid)

    for u in dados["unioes"]:
        for x in u.get("pessoas", []):
            if x not in pessoas:
                erros.append("união %s: pessoa '%s' não existe" % (u.get("id"), x))
        if "status" in u or u.get("fontes"):
            conferir_fato("união " + u.get("id", "?"), u, "união")

    for d in dados["documentos"]:
        for x in d.get("pessoas", []):
            if x not in pessoas:
                erros.append("documento %s: pessoa '%s' não existe" % (d.get("id"), x))
        for campo in ("arquivo", "transcricao"):
            if d.get(campo) and not os.path.exists(os.path.join(base, d[campo])):
                avisos.append("documento %s: %s '%s' não encontrado" % (d.get("id"), campo, d[campo]))

    for dv in dados["divergencias"]:
        if dv.get("pessoa") not in pessoas:
            erros.append("divergência: pessoa '%s' não existe" % dv.get("pessoa"))
        for v in dv.get("valores", []):
            if not v.get("fonte") and not v.get("relato"):
                avisos.append("divergência de %s: valor '%s' sem fonte nem relato" % (dv.get("pessoa"), v.get("valor")))
            if v.get("fonte") and v["fonte"] not in docs:
                erros.append("divergência de %s: fonte '%s' não existe" % (dv.get("pessoa"), v["fonte"]))

    for c in dados["cadeias"]:
        if "pais" in c and "nacionalidade" not in c:
            avisos.append("cadeia '%s': use 'nacionalidade' em vez de 'pais' para o código do país" % c.get("nome"))
        elos = c.get("elos", [])
        for i, x in enumerate(elos):
            if x not in pessoas:
                erros.append("cadeia '%s': elo '%s' não existe" % (c.get("nome"), x))
            elif i > 0 and elos[i - 1] not in pessoas[x].get("pais", []):
                erros.append("cadeia '%s': '%s' não tem '%s' em pais" % (c.get("nome"), x, elos[i - 1]))

    # ciclos de ascendência
    def sobe(pid, caminho):
        if pid in caminho:
            erros.append("ciclo de ascendência: %s" % " > ".join(caminho + [pid]))
            return
        for pai in pessoas.get(pid, {}).get("pais", []):
            if pai in pessoas:
                sobe(pai, caminho + [pid])
    for pid in pessoas:
        sobe(pid, [])
        if len(erros) > 200:
            break

    central = dados.get("pessoa_central")
    if not central and pessoas:
        avisos.append("pessoa_central vazia: a árvore abre na primeira pessoa da lista")
    if central and central not in pessoas:
        erros.append("pessoa_central '%s' não existe" % central)
    return sorted(set(erros)), sorted(set(avisos))


# ---------------------------------------------------------------- HTML

HTML_MODELO = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITULO__</title>
<style>
:root{--bg:#f7f5f0;--card:#fff;--tx:#1f1d1a;--mut:#6b665e;--bd:#ddd6c8;--ac:#2f5d8a;--ok:#2e7d4f;--rel:#a86b00;--hip:#8a3b8f;--sel:#fff3d6}
@media (prefers-color-scheme:dark){:root{--bg:#171614;--card:#22201d;--tx:#eee9e0;--mut:#a39d92;--bd:#3a3631;--ac:#7fb0e0;--ok:#6fcf97;--rel:#f2b84b;--hip:#d59bdb;--sel:#3a3220}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}
header{padding:16px;border-bottom:1px solid var(--bd);display:flex;gap:12px;flex-wrap:wrap;align-items:center}
h1{font-size:20px;margin:0;flex:1 1 240px}input{font:inherit;padding:8px 10px;border:1px solid var(--bd);border-radius:8px;background:var(--card);color:var(--tx);width:min(320px,100%)}
main{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:16px;padding:16px}
@media (max-width:860px){main{grid-template-columns:1fr}}
.arv{overflow-x:auto;background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px}
.gens{display:flex;gap:10px;min-width:max-content;min-height:420px}.gen{display:flex;flex-direction:column;min-width:170px}.col{flex:1;display:flex;flex-direction:column;justify-content:space-around;gap:8px}
.gen h3{font-size:12px;color:var(--mut);margin:0 0 4px;font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.p{border:1px solid var(--bd);border-left:4px solid var(--mut);border-radius:8px;padding:6px 8px;cursor:pointer;background:var(--card);max-width:220px}
.p.M{border-left-color:#4a7ab0}.p.F{border-left-color:#b0567a}.p:hover{background:var(--sel)}.p.vazio{opacity:.45;cursor:default;border-style:dashed}
.p b{display:block;font-size:13px}.p small{color:var(--mut)}.p .cad{font-size:11px;color:var(--ac)}
.org{display:inline-flex;vertical-align:-2px;margin-left:5px}.org svg{width:18px;height:12px;border-radius:2px;box-shadow:0 0 0 .6px rgba(0,0,0,.4)}
.org.sig{font-size:9px;font-weight:700;line-height:12px;padding:0 3px;border:1px solid var(--bd);border-radius:3px;color:var(--mut);vertical-align:0}
.estrela{color:#c9970c;margin-right:3px}.estrela.talvez{color:var(--mut)}.dq{border:1px solid #c9970c55;background:#c9970c12;border-radius:10px;padding:8px 10px;margin:10px 0}
.painel{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:14px 16px}
.painel h2{margin:0 0 4px;font-size:19px}.mut{color:var(--mut)}
table{border-collapse:collapse;width:100%;font-size:14px;margin:8px 0}td,th{border-bottom:1px solid var(--bd);padding:6px 4px;text-align:left;vertical-align:top}
.st{font-size:11px;padding:1px 6px;border-radius:10px;border:1px solid currentColor;white-space:nowrap}
.st.confirmado{color:var(--ok)}.st.relato{color:var(--rel)}.st.hipotese{color:var(--hip)}
.lk{color:var(--ac);cursor:pointer;text-decoration:underline}a{color:var(--ac)}
.leg{font-size:13px;color:var(--mut);padding:0 16px 16px}
ul{padding-left:18px;margin:6px 0}#res{display:flex;flex-wrap:wrap;gap:6px;padding:0 16px}
</style>
</head>
<body>
<header><h1>__TITULO__</h1><input id="busca" placeholder="Buscar pessoa…" aria-label="Buscar pessoa"></header>
<div id="res"></div>
<main><section class="arv"><div class="gens" id="gens"></div></section><section class="painel" id="painel"></section></main>
<p class="leg"><span class="estrela">★</span>figura conhecida na história, com fonte; <span class="estrela talvez">☆</span>possível, ainda não confirmada. O ícone ao lado do nome mostra o país, reino ou povo de nascimento (passe o mouse para ver o nome). Status de cada dado: <span class="st confirmado">confirmado</span> por documento, <span class="st relato">relato</span> da família, <span class="st hipotese">hipótese</span>. Gerado em __GERADO__ a partir de pessoas.json.</p>
<script>
const D = __DADOS__;
const P = Object.fromEntries(D.pessoas.map(p => [p.id, p]));
const DOC = Object.fromEntries(D.documentos.map(d => [d.id, d]));
const BANDEIRAS = __BANDEIRAS__;
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const ROT = {nascimento:"Nascimento",batismo:"Batismo",casamento:"Casamento",obito:"Óbito",sepultamento:"Sepultamento",imigracao:"Imigração",emigracao:"Emigração",naturalizacao:"Naturalização",residencia:"Residência",outro:"Outro"};
const ev = (p,t) => (p.eventos||[]).find(e => e.tipo === t);
const ano = e => {const a=((e && String(e.data||"").match(/\d{4}/)) || [""])[0]; return a && !/^\d{4}/.test(String(e.data)) ? "c. "+a : a;};
function vida(p){const n=ano(ev(p,"nascimento")||ev(p,"batismo")),o=ano(ev(p,"obito"));return (n||o)?`${n||"?"}–${o||(ev(p,"obito")?"?":"")}`:"";}
function cadeias(id){return D.cadeias.filter(c => (c.elos||[]).includes(id)).map(c => c.nome);}
const sigla = s => String(s||"?").split(/\s+/).filter(w=>!/^(d[aoe]s?|of|e)$/i.test(w)).slice(0,2).map(w=>w[0]).join("").toUpperCase();
function icone(o){if(!o)return "";const t=esc(o.nome+(o.derivado?" · deduzido do local e da data de nascimento":""));const s=BANDEIRAS[o.icone];
  return s?`<span class="org" title="${t}"><svg viewBox="0 0 30 20" role="img" aria-label="${t}">${s}</svg></span>`:`<span class="org sig" title="${t}">${esc(o.sigla||sigla(o.nome))}</span>`;}
function estrela(p){const d=p.destaque;if(!d)return "";const ok=d.status==="confirmado";
  return `<span class="estrela${ok?"":" talvez"}" title="${ok?"Figura conhecida na história":"Possível figura conhecida (ainda não confirmada)"}">${ok?"★":"☆"}</span>`;}
function caixa(id){
  const p = P[id];
  if(!p) return `<div class="p vazio"><b>desconhecido</b></div>`;
  const cad = cadeias(id);
  return `<div class="p ${esc(p.sexo||"")}" data-id="${esc(id)}"><b>${estrela(p)}${esc(p.nome)}${icone(p._origem)}</b><small>${esc(vida(p))}</small>${cad.length?`<div class="cad">${esc(cad.join(" · "))}</div>`:""}</div>`;
}
function pais(id){const p=P[id];if(!p)return [null,null];const ps=(p.pais||[]).map(x=>P[x]).filter(Boolean);
  const pai=ps.find(x=>x.sexo==="M"),mae=ps.find(x=>x.sexo==="F");const resto=ps.filter(x=>x!==pai&&x!==mae);
  return [(pai||resto.shift()||{}).id||null,(mae||resto.shift()||{}).id||null];}
const NOMES=["Pessoa","Pais","Avós","Bisavós","Trisavós","4º avós","5º avós"];
function arvore(id){
  let nivel=[id],html="";
  for(let g=0;g<6;g++){
    if(g>0 && nivel.every(x=>!x)) break;
    html += `<div class="gen"><h3>${NOMES[g]}</h3><div class="col">${nivel.map(x=>x?caixa(x):`<div class="p vazio"><b>—</b></div>`).join("")}</div></div>`;
    nivel = nivel.flatMap(x => x ? pais(x) : [null,null]);
  }
  document.getElementById("gens").innerHTML = html;
}
function fontes(lst){return (lst||[]).map(d=>{const x=DOC[d];if(!x)return esc(d);
  const alvo=x.arquivo||x.transcricao||x.url;const t=esc(x.titulo||d);return alvo?`<a href="${esc(alvo)}" target="_blank" rel="noopener">${t}</a>`:t;}).join("<br>")||'<span class="mut">sem documento</span>';}
function st(s){return s?`<span class="st ${esc(s)}">${esc(s==="hipotese"?"hipótese":s)}</span>`:"";}
function painel(id){
  const p=P[id];if(!p)return;
  const filhos=D.pessoas.filter(x=>(x.pais||[]).includes(id));
  const unioes=D.unioes.filter(u=>(u.pessoas||[]).includes(id));
  const div=D.divergencias.filter(x=>x.pessoa===id);
  let h=`<h2>${estrela(p)}${esc(p.nome)}${icone(p._origem)}</h2><div class="mut">${esc(vida(p))}${p.profissao?" · "+esc(p.profissao):""}</div>`;
  if(p._origem) h+=`<p class="mut">Origem: ${esc(p._origem.nome)}${p._origem.derivado?" (deduzida do local e da data de nascimento)":""}${p._origem.nota?". "+esc(p._origem.nota):""}</p>`;
  const dq=p.destaque;
  if(dq) h+=`<div class="dq"><b>${estrela(p)}${dq.status==="confirmado"?"Figura conhecida na história":"Possível figura conhecida"}</b> ${st(dq.status)}<p>${esc(dq.resumo)}</p>${dq.nota?`<p class="mut"><small>${esc(dq.nota)}</small></p>`:""}<p><small>Fontes: ${(dq.links||[]).filter(l=>l.url).map(l=>`<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.titulo||l.url)}</a>`).join(" · ")}${dq.consultado?` <span class="mut">(consultadas em ${esc(dq.consultado)})</span>`:""}</small></p></div>`;
  if((p.variantes||[]).length) h+=`<p class="mut">Também aparece como: ${p.variantes.map(esc).join("; ")}</p>`;
  h+=`<table><tr><th>Fato</th><th>Data e lugar</th><th>Fonte</th></tr>`;
  for(const e of (p.eventos||[])) h+=`<tr><td>${esc(ROT[e.tipo]||e.tipo)} ${st(e.status)}</td><td>${esc(e.data||"")}<br><span class="mut">${esc(e.local||"")}</span>${e.nota?`<br><small class="mut">${esc(e.nota)}</small>`:""}</td><td>${fontes(e.fontes)}</td></tr>`;
  if(p.filiacao) h+=`<tr><td>Filiação ${st(p.filiacao.status)}</td><td>${(p.pais||[]).map(x=>P[x]?`<span class="lk" data-id="${esc(x)}">${esc(P[x].nome)}</span>`:esc(x)).join("<br>")}${p.filiacao.nota?`<br><small class="mut">${esc(p.filiacao.nota)}</small>`:""}</td><td>${fontes(p.filiacao.fontes)}</td></tr>`;
  for(const u of unioes){const o=(u.pessoas||[]).filter(x=>x!==id)[0];
    h+=`<tr><td>${esc(u.tipo||"União")} ${st(u.status)}</td><td>${o&&P[o]?`<span class="lk" data-id="${esc(o)}">${esc(P[o].nome)}</span><br>`:""}${esc(u.data||"")} <span class="mut">${esc(u.local||"")}</span>${u.nota?`<br><small class="mut">${esc(u.nota)}</small>`:""}</td><td>${fontes(u.fontes)}</td></tr>`;}
  h+=`</table>`;
  if(filhos.length) h+=`<p><b>Filhos:</b> ${filhos.map(f=>`<span class="lk" data-id="${esc(f.id)}">${esc(f.nome)}</span>`).join(", ")}</p>`;
  if(div.length){h+=`<p><b>Divergências entre documentos</b></p><ul>`;for(const d of div)h+=`<li>${esc(d.campo)}: ${(d.valores||[]).map(v=>`${esc(v.valor)} (${esc(v.fonte?(DOC[v.fonte]?.titulo||v.fonte):(v.relato?"relato: "+v.relato:"sem fonte"))})`).join(" × ")}${d.nota?` <span class="mut">${esc(d.nota)}</span>`:""}</li>`;h+=`</ul>`;}
  if(p.notas) h+=`<p>${esc(p.notas)}</p>`;
  const cad=cadeias(id); if(cad.length) h+=`<p class="mut">Faz parte da cadeia: ${esc(cad.join("; "))}</p>`;
  document.getElementById("painel").innerHTML=h;
}
function foco(id){if(!P[id])return;arvore(id);painel(id);history.replaceState(null,"","#"+encodeURIComponent(id));}
document.addEventListener("click",e=>{const t=e.target.closest("[data-id]");if(t)foco(t.dataset.id);});
document.getElementById("busca").addEventListener("input",e=>{const q=e.target.value.trim().toLowerCase();const r=document.getElementById("res");
  if(q.length<2){r.innerHTML="";return;}
  r.innerHTML=D.pessoas.filter(p=>(p.nome+" "+(p.variantes||[]).join(" ")).toLowerCase().includes(q)).slice(0,20).map(p=>caixa(p.id)).join("");});
const ini=decodeURIComponent(location.hash.slice(1));
foco(P[ini]?ini:(D.pessoa_central&&P[D.pessoa_central]?D.pessoa_central:(D.pessoas[0]||{}).id));
</script>
</body>
</html>
"""


def gerar_html(dados, saida):
    titulo = html.escape(dados.get("familia") or "Árvore da família")
    copia = dict(dados, pessoas=[dict(p, _origem=origem_pessoa(p)) for p in dados["pessoas"]])
    corpo = json.dumps(copia, ensure_ascii=False).replace("</", "<\\/")
    texto = (HTML_MODELO.replace("__TITULO__", titulo)
             .replace("__BANDEIRAS__", json.dumps(BANDEIRAS))
             .replace("__GERADO__", datetime.date.today().strftime("%d/%m/%Y"))
             .replace("__DADOS__", corpo))
    gravar(saida, texto)


# ---------------------------------------------------------------- GEDCOM

def data_ged(valor):
    if not valor:
        return None, None
    v = str(valor).strip()

    def simples(s):
        m = re.match(r"^(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?$", s)
        if not m:
            return None
        a, me, d = m.groups()
        partes = []
        if d:
            partes.append(str(int(d)))
        if me:
            partes.append(MESES_GED[int(me) - 1])
        partes.append(a)
        return " ".join(partes)

    s = simples(v)
    if s:
        return s, None
    for prefixo, ged in (("c. ", "ABT "), ("antes de ", "BEF "), ("depois de ", "AFT ")):
        if v.startswith(prefixo) and simples(v[len(prefixo):]):
            return ged + simples(v[len(prefixo):]), None
    m = re.match(r"^entre (\S+) e (\S+)$", v)
    if m and simples(m.group(1)) and simples(m.group(2)):
        return "BET %s AND %s" % (simples(m.group(1)), simples(m.group(2))), None
    return None, v


def nome_ged(p):
    nome = p.get("nome", "").strip()
    sobrenome = p.get("sobrenome")
    if sobrenome and nome.endswith(sobrenome):
        return "%s /%s/" % (nome[: -len(sobrenome)].strip(), sobrenome)
    partes = nome.split()
    if len(partes) < 2:
        return nome
    return "%s /%s/" % (" ".join(partes[:-1]), partes[-1])


def provavelmente_vivo(p):
    if evento(p, "obito") or evento(p, "sepultamento"):
        return False
    a = ano(evento(p, "nascimento") or evento(p, "batismo"))
    return not a or int(a) > datetime.date.today().year - 100


def gerar_gedcom(dados, saida):
    pessoas = dados["pessoas"]
    xi = {p["id"]: "@I%d@" % (n + 1) for n, p in enumerate(pessoas)}
    xs = {d["id"]: "@S%d@" % (n + 1) for n, d in enumerate(dados["documentos"])}
    tag = {"nascimento": "BIRT", "batismo": "BAPM", "obito": "DEAT", "sepultamento": "BURI",
           "imigracao": "IMMI", "emigracao": "EMIG", "naturalizacao": "NATU", "residencia": "RESI",
           "casamento": "MARR", "outro": "EVEN"}

    familias = {}
    for u in dados["unioes"]:
        chave = tuple(sorted(u.get("pessoas", [])))
        familias.setdefault(chave, {"uniao": u, "filhos": []})
    for p in pessoas:
        if p.get("pais"):
            chave = tuple(sorted(p["pais"]))
            familias.setdefault(chave, {"uniao": None, "filhos": []})["filhos"].append(p["id"])
    xf = {chave: "@F%d@" % (n + 1) for n, chave in enumerate(familias)}

    L = ["0 HEAD", "1 SOUR RAIZES_E_CIDADANIA", "2 NAME raizes-e-cidadania", "1 GEDC", "2 VERS 5.5.1",
         "2 FORM LINEAGE-LINKED", "1 CHAR UTF-8", "1 LANG Portuguese",
         "1 DATE %s" % data_ged(datetime.date.today().isoformat())[0]]

    def fato(nivel, t, f):
        L.append("%d %s" % (nivel, t))
        d, livre = data_ged(f.get("data"))
        if d:
            L.append("%d DATE %s" % (nivel + 1, d))
        if f.get("local"):
            L.append("%d PLAC %s" % (nivel + 1, f["local"]))
        for s in f.get("fontes", []):
            if s in xs:
                L.append("%d SOUR %s" % (nivel + 1, xs[s]))
        nota = "; ".join(x for x in (
            "status: %s" % f["status"] if f.get("status") else "",
            "data no documento: %s" % livre if livre else "",
            f.get("nota", "")) if x)
        if nota:
            L.append("%d NOTE %s" % (nivel + 1, nota))

    for p in pessoas:
        L.append("0 %s INDI" % xi[p["id"]])
        L.append("1 NAME %s" % nome_ged(p))
        for v in p.get("variantes", []):
            L.append("1 NAME %s" % v)
            L.append("2 TYPE aka")
        if p.get("sexo") in ("M", "F"):
            L.append("1 SEX %s" % p["sexo"])
        if provavelmente_vivo(p):
            L.append("1 RESN privacy")
        if p.get("profissao"):
            L.append("1 OCCU %s" % p["profissao"])
        for ev in p.get("eventos", []):
            if ev.get("tipo") == "casamento":
                continue
            fato(1, tag.get(ev.get("tipo"), "EVEN"), ev)
            if tag.get(ev.get("tipo")) == "EVEN":
                L.append("2 TYPE %s" % ev.get("tipo"))
        for chave, x in xf.items():
            if p["id"] in chave:
                L.append("1 FAMS %s" % x)
            if p["id"] in familias[chave]["filhos"]:
                L.append("1 FAMC %s" % x)
        if p.get("notas"):
            L.append("1 NOTE %s" % p["notas"].replace("\n", " "))
        if p.get("destaque"):
            dq = p["destaque"]
            L.append("1 NOTE Figura conhecida (%s): %s Fontes: %s" % (dq.get("status", "sem status"), dq.get("resumo", ""),
                     "; ".join("%s <%s>" % (l.get("titulo", ""), l["url"]) for l in destaque_links(p))))
        L.append("1 REFN %s" % p["id"])

    for chave, f in familias.items():
        L.append("0 %s FAM" % xf[chave])
        for pid in chave:
            sexo = next((p.get("sexo") for p in pessoas if p["id"] == pid), None)
            L.append("1 %s %s" % ("WIFE" if sexo == "F" else "HUSB", xi[pid]))
        for c in f["filhos"]:
            L.append("1 CHIL %s" % xi[c])
        u = f["uniao"]
        if u and (u.get("data") or u.get("local") or u.get("fontes") or u.get("status")):
            fato(1, "MARR", u)

    for d in dados["documentos"]:
        L.append("0 %s SOUR" % xs[d["id"]])
        L.append("1 TITL %s" % (d.get("titulo") or d["id"]))
        if d.get("acervo"):
            L.append("1 PUBL %s" % d["acervo"])
        if d.get("cota"):
            L.append("1 NOTE cota: %s" % d["cota"])
    L.append("0 TRLR")
    gravar(saida, "\n".join(L) + "\n")


# ---------------------------------------------------------------- fichas

INI, FIM = "<!-- dados:inicio (gerado pelo arvore.py; edite o pessoas.json) -->", "<!-- dados:fim -->"


def origem(v, docs):
    if v.get("fonte"):
        return docs.get(v["fonte"], {}).get("titulo", v["fonte"])
    if v.get("relato"):
        return "relato: %s" % v["relato"]
    return "sem fonte"


def bloco_ficha(dados, p):
    pessoas = indice(dados["pessoas"])
    docs = indice(dados["documentos"])
    L = [INI, "", "| Fato | Data | Lugar | Status | Fonte |", "| --- | --- | --- | --- | --- |"]
    for ev in p.get("eventos", []):
        fontes = ", ".join(docs[d].get("titulo", d) if d in docs else d for d in ev.get("fontes", [])) or "sem documento"
        L.append("| %s | %s | %s | %s | %s |" % (ev.get("tipo", ""), ev.get("data", ""), ev.get("local", ""),
                                               ev.get("status", ""), fontes))
    L.append("")
    if p.get("pais"):
        L.append("Pais: " + "; ".join("[[%s]]" % x if x in pessoas else x for x in p["pais"])
                 + (" (%s)" % p["filiacao"].get("status") if p.get("filiacao") else ""))
    filhos = [x["id"] for x in dados["pessoas"] if p["id"] in x.get("pais", [])]
    if filhos:
        L.append("Filhos: " + "; ".join("[[%s]]" % x for x in filhos))
    if p.get("variantes"):
        L.append("Também aparece como: " + "; ".join(p["variantes"]))
    o = origem_pessoa(p)
    if o:
        L.append("Origem: %s%s%s" % (o["nome"], " (deduzida do local e da data de nascimento)" if o["derivado"] else "",
                                     ". " + o["nota"] if o.get("nota") else ""))
    if p.get("destaque"):
        dq = p["destaque"]
        L.append("")
        L.append("⭐ %s (%s): %s" % ("Figura conhecida na história" if dq.get("status") == "confirmado" else "Possível figura conhecida",
                                     dq.get("status", "sem status"), dq.get("resumo", "")))
        if dq.get("nota"):
            L.append("Identificação: %s" % dq["nota"])
        L.append("Fontes: %s%s" % (" · ".join("[%s](%s)" % (l.get("titulo") or l["url"], l["url"]) for l in destaque_links(p)),
                                   " (consultadas em %s)" % dq["consultado"] if dq.get("consultado") else ""))
    for dv in dados["divergencias"]:
        if dv.get("pessoa") == p["id"]:
            L.append("Divergência em %s: %s" % (dv.get("campo"), " x ".join(
                "%s (%s)" % (v.get("valor"), origem(v, docs)) for v in dv.get("valores", []))))
    L += ["", FIM]
    return "\n".join(L)


def gerar_fichas(dados, pasta):
    criadas = atualizadas = 0
    for p in dados["pessoas"]:
        caminho = os.path.join(pasta, "%s.md" % p["id"])
        bloco = bloco_ficha(dados, p)
        if os.path.exists(caminho):
            with open(caminho, encoding="utf-8") as f:
                texto = f.read()
            if INI in texto and FIM in texto:
                antes = texto.split(INI)[0]
                depois = texto.split(FIM, 1)[1]
                texto = antes + bloco + depois
            else:
                texto = texto.rstrip() + "\n\n## Dados\n\n" + bloco + "\n"
            atualizadas += 1
        else:
            texto = ("# %s\n\n%s\n\n## Dados\n\n%s\n\n## História\n\n"
                     "Escreva aqui a narrativa da vida da pessoa. Cada afirmação cita o documento "
                     "e diz se é confirmado, relato da família ou hipótese.\n\n## Pendências\n\n- \n"
                     % (p.get("nome", p["id"]), anos_vida(p), bloco))
            criadas += 1
        gravar(caminho, texto)
    return criadas, atualizadas


# ---------------------------------------------------------------- índice e pendências

def gerar_indice(dados, saida):
    pessoas = indice(dados["pessoas"])
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    with open(saida, "w", encoding=BOM_CSV, newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["id", "tipo", "titulo", "data", "local", "pessoas", "acervo", "cota", "arquivo", "original", "transcricao", "observacoes"])
        for d in dados["documentos"]:
            w.writerow([d.get("id", ""), d.get("tipo", ""), d.get("titulo", ""), d.get("data", ""), d.get("local", ""),
                        ", ".join(pessoas.get(x, {}).get("nome", x) for x in d.get("pessoas", [])),
                        d.get("acervo", ""), d.get("cota", ""), d.get("arquivo", ""), d.get("original", ""),
                        d.get("transcricao", ""), d.get("observacoes", "")])


def gerar_pendencias(dados, saida):
    pessoas = indice(dados["pessoas"])
    docs = indice(dados["documentos"])
    L = ["# Pendências", "", "Gerado em %s. Lista o que falta documentar em cada cadeia de cidadania e em cada pessoa."
         % datetime.date.today().strftime("%d/%m/%Y"), ""]

    def situacao(f):
        if not f or not f.get("status"):
            return "falta"
        if f.get("status") == "confirmado":
            return "ok (%s)" % ", ".join(docs.get(d, {}).get("titulo", d) for d in f.get("fontes", []))
        return "só %s" % ("hipótese" if f.get("status") == "hipotese" else f.get("status", "sem status"))

    for c in dados["cadeias"]:
        L += ["## Cadeia: %s" % c.get("nome", ""), "", "País: %s. Do ascendente ao requerente." % c.get("nacionalidade", c.get("pais", "?")), "",
              "| Elo | Nascimento | Filiação | Casamento | Óbito |", "| --- | --- | --- | --- | --- |"]
        elos = c.get("elos", [])
        for i, pid in enumerate(elos):
            p = pessoas.get(pid, {"nome": pid})
            nasc = evento(p, "nascimento") or evento(p, "batismo")
            fil = p.get("filiacao")
            if i > 0 and elos[i - 1] not in p.get("pais", []):
                fil_txt = "ERRO: %s não está em pais" % elos[i - 1]
            else:
                fil_txt = situacao(fil) if i > 0 else "(ascendente)"
            uniao = next((u for u in dados["unioes"] if pid in u.get("pessoas", [])), None)
            L.append("| %s | %s | %s | %s | %s |" % (p.get("nome"), situacao(nasc), fil_txt,
                                                     situacao(uniao) if uniao else "sem união registrada",
                                                     situacao(evento(p, "obito")) if evento(p, "obito") else "vivo ou sem dado"))
        L.append("")

    L += ["## Fatos sem documento", ""]
    n = 0
    for p in dados["pessoas"]:
        for ev in p.get("eventos", []):
            if ev.get("status") != "confirmado":
                L.append("- %s: %s %s (%s)" % (p.get("nome"), ev.get("tipo"), ev.get("data", ""), ev.get("status", "sem status")))
                n += 1
        if p.get("pais") and (p.get("filiacao") or {}).get("status") != "confirmado":
            L.append("- %s: filiação (%s)" % (p.get("nome"), (p.get("filiacao") or {}).get("status", "sem status")))
            n += 1
    for u in dados["unioes"]:
        if u.get("status") != "confirmado":
            nomes = " e ".join(pessoas.get(x, {}).get("nome", x) for x in u.get("pessoas", []))
            L.append("- %s: %s %s (%s)" % (nomes, u.get("tipo", "união"), u.get("data", ""), u.get("status", "sem status")))
            n += 1
    if not n:
        L.append("Nenhum.")
    a_conferir = [p for p in dados["pessoas"] if p.get("destaque") and p["destaque"].get("status") != "confirmado"]
    if a_conferir:
        L += ["", "## Figuras conhecidas a confirmar", ""]
        for p in a_conferir:
            L.append("- %s: %s (%s)" % (p.get("nome"), p["destaque"].get("resumo", ""), p["destaque"].get("status", "sem status")))
    L += ["", "## Divergências registradas", ""]
    for dv in dados["divergencias"]:
        L.append("- %s, %s: %s" % (pessoas.get(dv.get("pessoa"), {}).get("nome", dv.get("pessoa")), dv.get("campo"),
                                   " x ".join("%s (%s)" % (v.get("valor"), origem(v, docs)) for v in dv.get("valores", []))))
    if not dados["divergencias"]:
        L.append("Nenhuma.")
    gravar(saida, "\n".join(L) + "\n")


# ---------------------------------------------------------------- iniciar

PASTAS = ["documentos-originais", "documentos-organizados", "transcricoes", "fichas", "cidadania", "pesquisas", "saidas"]

LEIAME = """# Núcleo documental da família

Pastas:

- `documentos-originais/`: os arquivos como chegaram (fotos, PDFs, scans). Nunca são alterados nem renomeados.
- `documentos-organizados/`: cópias renomeadas como `AAAA-MM-DD Tipo - Pessoa - lugar.ext`, com o índice `indice-dos-documentos.csv`.
- `transcricoes/`: uma transcrição por documento antigo.
- `fichas/`: uma nota por pessoa (a parte entre os marcadores é gerada a partir do pessoas.json).
- `cidadania/`: matriz de prova, checklist e rascunhos de pedidos.
- `pesquisas/`: registro das buscas feitas (onde, quando, termos, resultado, inclusive as sem resultado).
- `saidas/`: GEDCOM e pendências gerados pelo `arvore.py`. A árvore (`arvore.html`) fica na raiz e abre em qualquer navegador.

`pessoas.json` é a fonte dos dados. `pedidos-de-certidoes.csv` controla certidões pedidas, custos e prazos.

Regra de ouro: todo dado cita o documento e diz se é confirmado, relato da família ou hipótese.
Divergências entre documentos são registradas, nunca corrigidas em silêncio.
"""

GITIGNORE = """# Esta pasta tem dados pessoais da família, inclusive de pessoas vivas.
# Não a publique. Se usar git, use um repositório privado; mesmo assim,
# estes itens ficam de fora por padrão.
documentos-originais/
documentos-organizados/
transcricoes/
fichas/
cidadania/
saidas/
pessoas.json
arvore.html
pedidos-de-certidoes.csv
*.jpg
*.jpeg
*.png
*.pdf
*.tif
*.tiff
"""


def iniciar(pasta, familia):
    for p in PASTAS:
        os.makedirs(os.path.join(pasta, p), exist_ok=True)
    pj = os.path.join(pasta, "pessoas.json")
    if not os.path.exists(pj):
        gravar(pj, json.dumps({
            "familia": familia, "pessoa_central": "", "atualizado": datetime.date.today().isoformat(),
            "pessoas": [], "unioes": [], "documentos": [], "divergencias": [], "cadeias": []
        }, ensure_ascii=False, indent=2) + "\n")
    for nome, texto in (("LEIAME.md", LEIAME), (".gitignore", GITIGNORE)):
        if not os.path.exists(os.path.join(pasta, nome)):
            gravar(os.path.join(pasta, nome), texto)
    pedidos = os.path.join(pasta, "pedidos-de-certidoes.csv")
    if not os.path.exists(pedidos):
        with open(pedidos, "w", encoding=BOM_CSV, newline="") as f:
            csv.writer(f, delimiter=";").writerow(
                ["documento", "pessoa", "orgao_ou_cartorio", "contato", "tipo_de_certidao", "finalidade",
                 "pedido_em", "custo_estimado", "custo_pago", "prazo", "status", "recebido_em", "observacoes"])
    indice_csv = os.path.join(pasta, "documentos-organizados", "indice-dos-documentos.csv")
    if not os.path.exists(indice_csv):
        gerar_indice({"documentos": [], "pessoas": []}, indice_csv)
    print("Projeto criado em %s" % os.path.abspath(pasta))


# ---------------------------------------------------------------- linha de comando

def main():
    ap = argparse.ArgumentParser(description="Núcleo documental da família")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("iniciar"); s.add_argument("pasta"); s.add_argument("--familia", default="Família")
    for nome in ("validar", "html", "gedcom", "fichas", "documentos", "pendencias", "tudo"):
        s = sub.add_parser(nome); s.add_argument("json")
        s.add_argument("-o", "--saida"); s.add_argument("-d", "--pasta")
    a = ap.parse_args()

    if a.cmd == "iniciar":
        iniciar(a.pasta, a.familia)
        return 0

    base = os.path.dirname(os.path.abspath(a.json))
    dados = carregar(a.json)
    erros, avisos = validar(dados, base)
    for x in avisos:
        print("aviso: " + x)
    for x in erros:
        print("ERRO: " + x)
    if a.cmd == "validar":
        print("%d pessoas, %d documentos, %d erros, %d avisos" % (len(dados["pessoas"]), len(dados["documentos"]), len(erros), len(avisos)))
        return 1 if erros else 0
    if erros:
        print("Corrija os erros antes de gerar.")
        return 1

    saidas = os.path.join(base, "saidas")
    if a.cmd in ("html", "tudo"):
        destino = a.saida if a.cmd == "html" and a.saida else os.path.join(base, "arvore.html")
        gerar_html(dados, destino); print("árvore: " + destino)
    if a.cmd in ("gedcom", "tudo"):
        destino = a.saida if a.cmd == "gedcom" and a.saida else os.path.join(saidas, "arvore.ged")
        gerar_gedcom(dados, destino); print("gedcom: " + destino)
    if a.cmd in ("fichas", "tudo"):
        c, u = gerar_fichas(dados, a.pasta or os.path.join(base, "fichas")); print("fichas: %d criadas, %d atualizadas" % (c, u))
    if a.cmd in ("documentos", "tudo"):
        destino = a.saida if a.cmd == "documentos" and a.saida else os.path.join(base, "documentos-organizados", "indice-dos-documentos.csv")
        gerar_indice(dados, destino); print("índice: " + destino)
    if a.cmd in ("pendencias", "tudo"):
        destino = a.saida if a.cmd == "pendencias" and a.saida else os.path.join(saidas, "pendencias.md")
        gerar_pendencias(dados, destino); print("pendências: " + destino)
    return 0


if __name__ == "__main__":
    sys.exit(main())
