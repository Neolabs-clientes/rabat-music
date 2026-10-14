#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estructura el texto extraido de cada ficha en datos.json."""
import json, re, unicodedata

GEN = {"trap": "Trap", "drill": "Drill", "reggaeton": "Reggaetón", "regueton": "Reggaetón",
       "rap": "Rap", "hip hop": "Hip-Hop", "hip-hop": "Hip-Hop", "pop": "Pop",
       "electronica": "Electrónica", "afrobeat": "Afrobeat", "dembow": "Dembow",
       "r&b": "R&B", "punk": "Punk", "flamenco": "Flamenco", "rock": "Rock"}
MARCA = ("ARTISTAS", "QUIÉNES SOMOS", "CONTACTO", "¡PÁSATE", "DON'T BE SHY", "¿NOS SIGUES")


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def limpio(s):
    return re.sub(r"\s+", " ", s).strip()


def parte(t, a, b=None):
    """Texto entre el marcador a y el marcador b."""
    i = t.find(a)
    if i < 0:
        return ""
    i += len(a)
    j = t.find(b, i) if b else len(t)
    return t[i:j if j > 0 else len(t)]


def parsea(reg):
    t = reg["texto"]
    lineas = [limpio(x) for x in t.split("\n")]
    lineas = [x for x in lineas if x]
    nombre = lineas[0] if lineas else reg["slug"]
    # sello/colectivo: linea corta inmediatamente despues del nombre
    sello = ""
    if len(lineas) > 1 and 0 < len(lineas[1]) <= 22 and len(lineas[1].split()) <= 2:
        sello = lineas[1]
    bio = limpio(parte(t, sello or nombre, "MOOD") or parte(t, nombre, "MOOD"))
    bio = re.sub(r"^" + re.escape(nombre) + r"\s*", "", bio)
    moods = [limpio(x) for x in parte(t, "MOOD", "LOGROS").split("\n") if limpio(x)]
    logros = [limpio(x) for x in parte(t, "LOGROS", "TÍTULOS POPULARES").split("\n") if limpio(x)]
    temas = []
    resta = parte(t, "TÍTULOS POPULARES")
    filas = [limpio(x) for x in resta.split("\n") if limpio(x)]
    yt = [h for h in reg["links"] if "youtube.com/watch" in h]
    k = 0
    for i in range(0, len(filas) - 1, 2):
        titulo, meta = filas[i], filas[i + 1]
        if titulo in MARCA:
            break
        temas.append({"titulo": titulo, "meta": meta, "url": yt[k] if k < len(yt) else ""})
        k += 1
    redes = {}
    for h in reg["links"]:
        for clave, patron in (("instagram", r"instagram\.com"), ("tiktok", r"tiktok\.com"),
                              ("youtube", r"youtube\.com"), ("spotify", r"open\.spotify\.com")):
            if re.search(patron, h) and clave not in redes and "rabatmusicgroup" not in h:
                redes[clave] = h
    texto_gen = sin_tildes((bio + " " + " ".join(moods)).lower())
    generos = sorted({v for k2, v in GEN.items() if k2 in texto_gen})
    return {"slug": reg["slug"], "nombre": nombre.upper(), "sello": sello, "bio": bio,
            "mood": moods, "logros": logros, "temas": temas, "redes": redes,
            "generos": generos or ["Urbano"], "fuente": "%s/%s" % ("https://www.rabatmusicgroup.com", reg["slug"])}


def main():
    regs = json.load(open("crudo_artistas.json"))
    datos = [parsea(r) for r in regs]
    json.dump(datos, open("datos.json", "w"), ensure_ascii=False, indent=1)
    print("artistas:", len(datos))
    print("con bio:", sum(1 for d in datos if len(d["bio"]) > 80))
    print("con logros:", sum(1 for d in datos if d["logros"]))
    print("con temas:", sum(1 for d in datos if d["temas"]))
    print("con redes:", sum(1 for d in datos if d["redes"]))
    gen = {}
    for d in datos:
        for g in d["generos"]:
            gen[g] = gen.get(g, 0) + 1
    print("generos:", dict(sorted(gen.items(), key=lambda x: -x[1])))
    print("\nMuestra:", json.dumps(datos[20], ensure_ascii=False)[:900])


main()
