#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fichas de artista + paginas institucionales + escritura de ficheros."""
import json, re, os
from construye import (A, DOM, MAIL, WEB, IG, TT, MAPS, FOTO, esc, head, nav, pie, prefija, rejilla,
                       servicios, valores, pagina_index, pagina_artistas)


def hitos(a):
    """Cifras sacadas de sus propios logros. No se inventa ninguna."""
    nums = []
    for l in a["logros"]:
        for m in re.finditer(r"(?<![\d.,])(?:X|\+)?\s?(\d{1,3})\s+([A-ZÁÉÍÓÚÑ]{3,})", l.upper()):
            etq = m.group(2).strip().capitalize()
            if etq in ("Mas", "Con", "Que", "Sus", "Del", "Las", "Los", "Para", "Desde",
                       "Ciudades", "Plataformas", "Una"):
                continue
            if m.group(1) != "0" and etq not in [n[1] for n in nums]:
                nums.append((m.group(1), etq))
    if len(nums) < 2 and a["temas"]:
        nums.append((str(len(a["temas"])), "Temas"))
    if a["redes"]:
        nums.append((str(len(a["redes"])), "Plataformas"))
    return nums[:3]


def pagina_artista(a):
    h = "".join('<div class="hito rev"><b>%s</b><span>%s</span></div>' % (esc(n), esc(e)) for n, e in hitos(a))
    logros = "".join('<div class="logro rev">%s</div>' % esc(l) for l in a["logros"])
    temas = ""
    for t in a["temas"]:
        if not t.get("url"):
            continue
        vid = (re.search(r"[?&]v=([\w-]{6,})", t["url"]) or [None, ""])[1]
        temas += ('<a class="tema rev" href="%s" target="_blank" rel="noopener">'
                  '<img src="https://i.ytimg.com/vi/%s/mqdefault.jpg" alt="%s" loading="lazy" width="132" height="74">'
                  '<span><b>%s</b><span>%s</span></span><span style="color:var(--amarillo)">Play</span></a>'
                  % (esc(t["url"]), vid, esc(t["titulo"]), esc(t["titulo"]), esc(t["meta"])))
    redes = "".join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(u), k.capitalize())
                    for k, u in a["redes"].items())
    asunto = esc("Contratación %s" % a["nombre"]).replace(" ", "%20")
    cuerpo = ("Hola%2C%20quiero%20contratar%20a%20" + esc(a["nombre"]).replace(" ", "%20")
              + ".%0AFecha%3A%0ACiudad%3A%0AFormato%3A%0APresupuesto%3A")
    enlace = "mailto:%s?subject=%s&body=%s" % (MAIL, asunto, cuerpo)
    sello = ('<span style="border-color:var(--amarillo);color:var(--amarillo)">%s</span>' % esc(a["sello"])
             if a["sello"] else "")
    mismos = [x for x in A if x["slug"] != a["slug"] and set(x["generos"]) & set(a["generos"])][:6]
    cola = ""
    if mismos:
        cola = ('<section class="seccion" style="background:var(--negro-2)"><div class="envoltura">'
                '<span class="num">Mismo género</span><h2>Si te gusta %s</h2>%s'
                '<p style="margin-top:30px"><a class="boton" href="artistas.html">Ver el roster completo →</a></p>'
                '</div></section>') % (esc(a["nombre"]), rejilla(mismos, "rel"))
    return prefija(head("%s · Rabat Music Group" % a["nombre"],
                 "%s — %s. Biografía, logros y contratación con Rabat Music Group."
                 % (a["nombre"], ", ".join(a["generos"])), "%s/artistas/%s.html" % (DOM, a["slug"]))
            + nav("Artistas")
            + '<section class="art-hero"><div class="envoltura" style="display:contents">'
            + '<div class="rev"><span class="num">Roster / ficha</span><h1>%s</h1>' % esc(a["nombre"])
            + '<div class="etiquetas"><span>%s</span>%s</div>' % (esc(", ".join(a["generos"])), sello)
            + '<p class="mini" style="margin-top:24px"><a href="artistas.html" style="color:var(--amarillo)">'
            + '← Ver todo el roster</a></p></div>'
            + '<div class="foto rev retardo-2"><img src="%s" alt="%s" width="512" height="512"></div>'
            % (FOTO(a["slug"]), esc(a["nombre"]))
            + '</div></section><div class="salto"></div>'
            + '<section><div class="envoltura"><div class="rejilla-2" style="align-items:start">'
            + '<div><span class="num">Biografía</span><p class="bio">%s</p>' % esc(a["bio"])
            + '<div class="redes">%s<a href="%s">Contratación</a></div></div>' % (redes, enlace)
            + '<div><span class="num">En cifras</span><div class="hitos">%s</div>' % h
            + (('<span class="num">Logros</span>%s' % logros) if logros else "")
            + '<p style="margin-top:22px"><a class="boton amarillo" href="%s">Solicitar fecha</a> ' % enlace
            + ('<a class="boton" href="%s" target="_blank" rel="noopener">Presskit</a>' % a["presskit"] if a.get("presskit") else "") + '</p>'
            + '</div></div>'
            + (('<div class="salto"></div><span class="num">Temas</span><div class="temas">%s</div>' % temas)
               if temas else "")
            + '</div></section>' + cola + pie())
