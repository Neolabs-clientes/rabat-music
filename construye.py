#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la web de Rabat Music Group a partir de datos.json (contenido real)."""
import json, re, os, html

DOM = "https://neolabs-clientes.github.io/rabat-music"
A = json.load(open("datos.json"))
POR = {a["slug"]: a for a in A}
FOTO = lambda s: "assets/artistas/%s.webp" % s
WEB = "https://www.rabatmusicgroup.com/%s"
DIR = "C. de Martín de los Heros, 24 · 28008 Madrid"
MAIL = "hola@rabatmusicgroup.com"
IG = "https://www.instagram.com/rabatmusicgroup"
TT = "https://www.tiktok.com/@rabatmusicgroup"
MAPS = "https://www.google.com/maps/search/?api=1&query=C.+de+Mart%C3%ADn+de+los+Heros+24,+28008+Madrid"
NAV = [("Artistas", "artistas.html"), ("Servicios", "index.html#servicios"),
       ("Nosotros", "quienes-somos.html"), ("Contacto", "contacto.html")]
SERVICIOS = [
    ("01", "Management", "Desarrollo de carrera a largo plazo: estrategia, imagen, "
     "planificación de lanzamientos y acompañamiento diario del artista."),
    ("02", "Booking", "Colocación de shows en salas, festivales y giras. Negociación de "
     "caché, contratos y logística de cada fecha."),
    ("03", "Sello discográfico", "Edición y distribución de la obra, gestión de derechos "
     "y publicación en plataformas. El artista en el centro de la industria."),
]
VALORES = [("Superación", "Ningún techo de cristal"), ("Cercanía", "Un equipo, no un despacho"),
           ("Constancia", "Carreras, no canciones"), ("Transparencia", "Cuentas claras, siempre")]


def esc(s):
    return html.escape(str(s or ""), quote=True)


def prefija(s, pre="../"):
    """Reescribe rutas relativas para las paginas que viven en subcarpeta."""
    return re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/|data:)',
                  lambda m: '%s="%s' % (m.group(1), pre), s)


def head(titulo, desc, canon, extra=""):
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta name="robots" content="noindex,follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Rabat Music Group">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s/assets/portada.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#000000">
<link rel="icon" href="assets/logo-rabat.svg">
<link rel="preload" href="assets/fuentes/rabat-display.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="assets/estilo.css">
%s
</head>
<body>
<div class="progreso" id="progreso"></div>
<div class="grano"></div>
""" % (esc(titulo), esc(desc), canon, esc(titulo), esc(desc), canon, DOM, extra)


def nav(activo=""):
    enl = []
    for t, u in NAV:
        marca = ' aria-current="page"' if t == activo else ""
        enl.append('<a href="%s"%s>%s</a>' % (u, marca, t))
    return """<header class="barra">
<a class="marca" href="index.html"><img src="assets/logo-rabat.svg" alt="Rabat Music Group" width="132" height="26"><span>Sello · Management · Booking</span></a>
<button class="hamburguesa" id="hamb" aria-expanded="false" aria-controls="menu">Menú</button>
<nav class="enlaces" id="menu" aria-label="Principal">%s
<a class="cta-nav" href="contacto.html">Contratar artista</a></nav>
</header>
""" % "".join(enl)


def pie():
    return """<footer class="pie"><div class="envoltura">
<div class="pie-arriba">
  <div>
    <img src="assets/logo-rabat.svg" alt="Rabat Music Group" width="152" height="30">
    <p>Sello discográfico, agencia de management y booking. Desarrollamos la carrera de nuestros artistas desde cero hasta su máximo potencial.</p>
    <p><b style="color:var(--amarillo);font-family:var(--mono);font-size:11px;letter-spacing:.2em">MADRID</b></p>
  </div>
  <div><h4>Navegación</h4>
    <a href="index.html">Inicio</a><a href="artistas.html">Artistas</a>
    <a href="index.html#servicios">Servicios</a><a href="quienes-somos.html">Quiénes somos</a>
    <a href="contacto.html">Contacto</a></div>
  <div><h4>Contacto</h4>
    <a href="mailto:%s">%s</a>
    <p>%s</p>
    <a href="%s" target="_blank" rel="noopener">Instagram</a>
    <a href="%s" target="_blank" rel="noopener">TikTok</a></div>
</div>
<div class="pie-abajo">
  <span>© <span id="aaa"></span> Rabat Music Group</span>
  <span>Sitio web: rediseño y desarrollo de Neo Labs · neolabs.me</span>
</div>
</div></footer>
<script src="assets/app.js"></script>
</body>
</html>""" % (MAIL, MAIL, DIR, IG, TT)


def marquesina():
    tira = "".join("<span>%s</span>" % esc(a["nombre"]) for a in A)
    return ('<div class="marquesina" aria-hidden="true"><div class="tira">%s</div>'
            '<div class="tira">%s</div></div>') % (tira, tira)


def ficha(a, retardo=0):
    """Ficha circular del roster, con genero y nombre para filtrar."""
    return ('<a class="ficha rev retardo-%d" href="artistas/%s.html" data-gen="%s" data-busca="%s">'
            '<span class="aro"><img src="%s" alt="%s" loading="lazy" width="512" height="512"></span>'
            '<b>%s</b><i>%s</i></a>') % (retardo % 3 + 1, a["slug"], esc(" ".join(a["generos"])),
                                         esc(a["nombre"].lower()), FOTO(a["slug"]), esc(a["nombre"]),
                                         esc(a["nombre"]), esc(a["generos"][0]))


def rejilla(artistas, ident="roster"):
    return '<div class="roster" id="%s">%s</div>' % (ident, "".join(ficha(a, i) for i, a in enumerate(artistas)))


def destacados():
    tarjetas = []
    for a in A[:4]:
        tarjetas.append("""<a class="dest rev" href="artistas/%s.html">
<img src="%s" alt="%s" loading="lazy" width="512" height="512">
<span class="flecha">Ver ficha →</span>
<span class="dest-txt"><span>%s</span><h3>%s</h3></span></a>""" % (a["slug"], FOTO(a["slug"]),
                                                                    esc(a["nombre"]), esc(", ".join(a["generos"])), esc(a["nombre"])))
    return '<div class="destacados">%s</div>' % "".join(tarjetas)


def servicios():
    t = "".join('<article class="tj rev retardo-%d"><span class="eti">%s</span><h3>%s</h3><p>%s</p></article>'
                % (i % 3 + 1, n, esc(t2), esc(d)) for i, (n, t2, d) in enumerate(SERVICIOS))
    if len(SERVICIOS) == 3:
        t += ('<article class="tj rev"><span class="eti">+</span><h3>¿Marcas y eventos?</h3>'
              '<p>Activaciones de marca, colaboraciones y eventos privados con nuestros artistas. '
              'Cuéntanos qué tienes en mente y te proponemos el formato.</p>'
              '<p style="margin-top:14px"><a href="contacto.html" style="color:var(--amarillo);'
              'font-family:var(--mono);font-size:10.5px;letter-spacing:.18em">ESCRÍBENOS →</a></p></article>')
    return '<div class="tres">%s</div>' % t


def valores():
    return '<div class="valores">%s</div>' % "".join(
        '<div class="valor rev retardo-%d"><b>%s</b><span>%s</span></div>' % (i % 3 + 1, esc(n), esc(d))
        for i, (n, d) in enumerate(VALORES))


def jsonld():
    org = {"@context": "https://schema.org", "@type": "MusicGroup", "name": "Rabat Music Group",
           "description": "Sello discográfico, agencia de management y booking. Madrid.",
           "address": {"@type": "PostalAddress", "streetAddress": "C. de Martín de los Heros, 24",
                       "postalCode": "28008", "addressLocality": "Madrid", "addressCountry": "ES"},
           "email": MAIL, "url": DOM, "sameAs": [IG, TT],
           "member": [{"@type": "MusicGroup", "name": a["nombre"], "genre": a["generos"],
                       "url": "%s/artistas/%s.html" % (DOM, a["slug"])} for a in A]}
    return '<script type="application/ld+json">%s</script>' % json.dumps(org, ensure_ascii=False)


def pagina_index():
    hero = """<section class="hero"><div class="envoltura">
<img class="hero-logo" src="assets/logo-rabat.svg" alt="Rabat Music Group" width="1080" height="113">
<h1>DONDE FIRMAS<br>Y NO TE <em>F*LLAN</em></h1>
<p class="hero-sub">Management · Booking · Sello discográfico</p>
<div class="hero-datos">
  <div><b>%d</b>artistas en el roster</div>
  <div><b>3</b>líneas de negocio</div>
  <div><b>MAD</b>Martín de los Heros 24</div>
</div>
<div class="hero-acciones">
  <a class="boton amarillo" href="artistas.html">Ver los %d artistas</a>
  <a class="boton" href="contacto.html">Contratación y booking</a>
</div>
</div><span class="sello-madrid">MADRID · 28008</span></section>""" % (len(A), len(A))
    cta = """<section class="seccion"><div class="envoltura centrado">
<span class="num">— Booking abierto —</span>
<h2>¿Quieres a uno de<br>nuestros artistas<br>en tu <em>cartel</em>?</h2>
<p class="entrada" style="margin:26px auto 30px">Dinos la ciudad, la fecha y el formato. Te pasamos
disponibilidad, caché y condiciones en menos de 24 horas.</p>
<a class="boton amarillo" href="contacto.html">Solicitar fecha</a>
</div></section>"""
    return (head("Rabat Music Group · Management, booking y sello discográfico en Madrid",
                 "Sello discográfico, agencia de management y booking en Madrid. %d artistas: "
                 "contratación, giras y desarrollo de carrera." % len(A), DOM + "/", jsonld())
            + nav()
            + hero + marquesina()
            + '<section class="seccion" id="servicios"><div class="envoltura"><span class="num">01 — Servicios</span>'
            + '<h2>Tres formas de<br>trabajar contigo</h2><p class="entrada">Representamos al artista de principio a fin: '
            + 'de la primera maqueta al último bolo de la gira. Y si eres marca, festival o sala, hablamos tu idioma.</p>'
            + servicios() + '</div></section>'
            + '<section class="seccion" id="portada" style="background:var(--negro-2)"><div class="envoltura">'
            + '<span class="num">02 — En portada</span><h2>Los que más<br>suenan ahora</h2>'
            + destacados()
            + '<div style="margin-top:34px"><a class="boton" href="artistas.html">Ver el roster completo →</a></div>'
            + '</div></section>'
            + '<section class="seccion" id="nosotros"><div class="envoltura"><span class="num">03 — Nosotros</span>'
            + '<div class="rejilla-2"><div><h2>Un sello, una agencia<br>y un equipo</h2>'
            + '<p class="entrada">Un sello discográfico, agencia de management y booking que se dedica a '
            + 'desarrollar la carrera de artistas desde cero hasta su máximo potencial. Una nueva forma de hacer '
            + 'industria musical que pone al artista en el centro.</p>'
            + '<p><a class="boton" href="quienes-somos.html" style="margin-top:14px">Quiénes somos</a></p></div>'
            + '<div><img src="assets/equipo.jpg" alt="Equipo de Rabat Music Group" loading="lazy" '
            + 'style="border:1px solid var(--linea);width:100%"></div></div>'
            + valores() + '</div></section>'
            + cta + pie())


def pagina_artistas():
    gens = {}
    for a in A:
        for g in a["generos"]:
            gens[g] = gens.get(g, 0) + 1
    chips = ['<button class="chip activo" data-f="todos">Todos <span style="opacity:.6">%d</span></button>' % len(A)]
    for g, n in sorted(gens.items(), key=lambda x: (-x[1], x[0])):
        chips.append('<button class="chip" data-f="%s">%s <span style="opacity:.6">%d</span></button>' % (esc(g), esc(g), n))
    return (head("Artistas · Rabat Music Group",
                 "Roster completo de Rabat Music Group: %d artistas de trap, rap, reggaetón, pop y "
                 "electrónica. Disponibles para contratación." % len(A), DOM + "/artistas.html")
            + nav("Artistas")
            + '<section class="seccion" style="padding-top:clamp(120px,16vh,180px)"><div class="envoltura">'
            + '<span class="num">Roster %d/%d</span><h1 style="font-size:clamp(44px,9vw,124px)">Elige<br>tu artista</h1>'
            + '<p class="entrada" style="margin-top:22px">Filtra por género o busca por nombre. Cada ficha trae '
            + 'biografía, logros, temas y contacto directo de contratación.</p>'
            + '<div class="filtros" id="filtros">' + "".join(chips)
            + '<input id="busca" type="search" placeholder="Buscar artista…" aria-label="Buscar artista" '
            + 'style="background:var(--negro-2);border:1px solid var(--linea);color:var(--crema);'
            + 'font-family:var(--mono);font-size:12px;padding:12px 14px;min-width:190px">'
            + '<span class="cuenta" id="cuenta">%d artistas</span></div>' % len(A)
            + rejilla(A)
            + '<p class="nota">Todos los artistas del roster son representados por Rabat Music Group. '
            + 'Para contratación de cualquiera de ellos, <a href="contacto.html" style="color:var(--amarillo)">'
            + 'escríbenos</a> con ciudad y fecha.</p>'
            + '</div></section>' + pie())
