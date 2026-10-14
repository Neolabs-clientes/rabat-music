#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Punto de entrada: genera todas las paginas de la web de Rabat Music Group."""
import os
from construye import A, DOM, MAIL, IG, TT, MAPS, esc, head, nav, pie, servicios, valores
from construye import pagina_index, pagina_artistas
from paginas import pagina_artista


def pagina_nosotros():
    return (head("Quiénes somos · Rabat Music Group",
                 "Sello discográfico, agencia de management y booking en Madrid. Una nueva forma de hacer "
                 "industria musical que pone al artista en el centro.", DOM + "/quienes-somos.html")
            + nav("Nosotros")
            + '<section class="seccion" style="padding-top:clamp(120px,16vh,180px)"><div class="envoltura">'
            + '<span class="num">Quiénes somos</span><h1 style="font-size:clamp(40px,7.4vw,104px)">¿Quiénes<br>somos?</h1>'
            + '<div class="rejilla-2" style="margin-top:clamp(30px,4vw,54px);align-items:start">'
            + '<div><p class="bio" style="font-size:17px;color:var(--crema)">Un sello discográfico, agencia de '
            + 'management y booking que se dedica a desarrollar la carrera de artistas desde cero hasta su máximo '
            + 'potencial. Una nueva forma de hacer industria musical que pone al artista en el centro.</p>'
            + '<p class="bio">Trabajamos desde Madrid, en Martín de los Heros, con un roster de %d artistas de ' % len(A)
            + 'trap, rap, reggaetón, pop y electrónica. Del primer single al cierre de gira, con las cuentas claras '
            + 'y el artista en la toma de decisiones.</p>'
            + '<div class="redes"><a href="%s" target="_blank" rel="noopener">Instagram</a>' % IG
            + '<a href="%s" target="_blank" rel="noopener">TikTok</a>' % TT
            + '<a href="mailto:%s">Escríbenos</a></div></div>' % MAIL
            + '<div><img src="assets/equipo.jpg" alt="Equipo de Rabat Music Group" loading="lazy" '
            + 'style="border:1px solid var(--linea);width:100%">'
            + '<p class="mini" style="margin-top:12px">Equipo y artistas · Best Content Creators</p></div>'
            + '</div><div class="salto"></div><span class="num">Cómo trabajamos</span>'
            + '<h2>Del primer tema<br>a la gira</h2>' + servicios()
            + '<div class="salto"></div><span class="num">Nuestros valores</span><h2>Lo que nos<br>define</h2>'
            + valores()
            + '<div class="salto"></div><p><a class="boton amarillo" href="artistas.html">Ver el roster</a> '
            + '<a class="boton" href="contacto.html">Contactar</a></p>'
            + '</div></section>' + pie())


def pagina_contacto():
    opciones = "".join("<option>%s</option>" % o for o in
                       ("Contratación de un artista (booking)", "Management", "Prensa y entrevistas",
                        "Marcas, festivales y eventos", "Demos y nuevos artistas", "Otro"))
    form = """<form id="formulario" novalidate>
<div class="campo"><label for="mot">Motivo</label><select id="mot">%s</select></div>
<div class="campo"><label for="nom">Nombre y empresa</label><input id="nom" required autocomplete="name"></div>
<div class="campo"><label for="eml">Email</label><input id="eml" type="email" required autocomplete="email"></div>
<div class="campo"><label for="ciu">Ciudad y fecha (si es contratación)</label><input id="ciu"></div>
<div class="campo"><label for="msg">Cuéntanos</label><textarea id="msg" rows="5"></textarea></div>
<button class="boton amarillo" type="submit">Abrir email y enviar</button>
<p class="mini" id="respuesta" style="margin-top:14px">Se abrirá tu programa de correo con el mensaje listo.</p>
</form>""" % opciones
    return (head("Contacto · Rabat Music Group",
                 "Contacta con Rabat Music Group: contratación de artistas, management, prensa y marcas. "
                 "C. de Martín de los Heros, 24, 28008 Madrid.", DOM + "/contacto.html")
            + nav("Contacto")
            + '<section class="seccion" style="padding-top:clamp(120px,16vh,180px)"><div class="envoltura">'
            + '<span class="num">Contacto</span><h1 style="font-size:clamp(42px,8vw,116px)">¿Dónde<br>estamos?</h1>'
            + '<div class="contacto-rejilla"><div>'
            + '<div class="dato"><span>Oficina y dirección</span><b>Martín de los Heros, 24<br>28008 Madrid</b>'
            + '<p style="margin-top:12px"><a class="mini" href="%s" target="_blank" rel="noopener" ' % MAPS
            + 'style="color:var(--amarillo)">Ver en el mapa →</a></p></div>'
            + '<div class="dato"><span>Email general</span><b><a href="mailto:%s">%s</a></b></div>' % (MAIL, MAIL)
            + '<div class="dato"><span>Redes</span><b><a href="%s" target="_blank" rel="noopener">' % IG
            + '@rabatmusicgroup</a></b><p style="margin-top:10px"><a class="mini" href="%s" ' % TT
            + 'target="_blank" rel="noopener" style="color:var(--amarillo)">TikTok →</a></p></div>'
            + '<div class="dato"><span>Prensa y presskits</span>'
            + '<b>Cada artista tiene su material de prensa en su propia ficha</b>'
            + '<p style="margin-top:12px"><a class="mini" href="artistas.html" '
            + 'style="color:var(--amarillo)">Ir al roster →</a></p></div>'
            + '</div><div><span class="num">Escríbenos</span>'
            + '<h3 style="margin-bottom:18px">¡Pásate a decir hola!</h3>' + form
            + '</div></div></div></section>' + pie())


def escribe(ruta, texto):
    os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    return len(texto)


def main():
    total = 0
    total += escribe("index.html", pagina_index())
    total += escribe("artistas.html", pagina_artistas())
    total += escribe("quienes-somos.html", pagina_nosotros())
    total += escribe("contacto.html", pagina_contacto())
    for a in A:
        total += escribe("artistas/%s.html" % a["slug"], pagina_artista(a))
    # 404
    total += escribe("404.html", head("Página no encontrada · Rabat Music Group", "404", DOM + "/404.html")
                     + nav() + '<section class="seccion" style="padding-top:clamp(140px,20vh,220px)">'
                     + '<div class="envoltura centrado"><span class="num">Error 404</span>'
                     + '<h1 style="font-size:clamp(48px,10vw,140px)">Te has<br>perdido</h1>'
                     + '<p class="entrada" style="margin:24px auto 30px">Esa página no existe. '
                     + 'Pero el roster sí.</p><a class="boton amarillo" href="artistas.html">'
                     + 'Ver los artistas</a></div></section>' + pie())
    # robots + sitemap (lo que su web no tiene)
    urls = ["", "artistas.html", "quienes-somos.html", "contacto.html"] + \
           ["artistas/%s.html" % a["slug"] for a in A]
    total += escribe("sitemap.xml",
                     '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                     + "".join("<url><loc>%s/%s</loc><changefreq>weekly</changefreq><priority>%s</priority></url>\n"
                               % (DOM, u, "1.0" if u == "" else "0.8") for u in urls)
                     + "</urlset>\n")
    total += escribe("robots.txt", "User-agent: *\nDisallow: /\n\nSitemap: %s/sitemap.xml\n" % DOM)
    print("paginas escritas:", 4 + len(A) + 2, "| bytes:", total)
    print("equipo.jpg:", "OK" if os.path.exists("assets/equipo.jpg") else "FALTA (descargar de su web)")


if __name__ == "__main__":
    main()
