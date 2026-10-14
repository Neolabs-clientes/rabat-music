#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrae el contenido real de cada ficha de artista de rabatmusicgroup.com."""
import json, re, time
from playwright.sync_api import sync_playwright

B = "https://www.rabatmusicgroup.com"
roster = json.load(open("roster.json"))["roster"]
vistos, artistas = set(), []
with sync_playwright() as pw:
    nav = pw.chromium.launch()
    pg = nav.new_context(viewport={"width": 1440, "height": 1000}).new_page()
    for href, alt, src in roster:
        slug = href.rstrip("/").split("/")[-1]
        if not slug or slug in vistos:
            continue
        vistos.add(slug)
        try:
            pg.goto(B + "/" + slug, wait_until="load", timeout=60000)
            pg.wait_for_timeout(2200)
            if "PULSA" in pg.inner_text("body").upper():
                pg.mouse.click(720, 450); pg.wait_for_timeout(3500)
            t = pg.inner_text("body")
            links = pg.eval_on_selector_all("a", "e=>e.map(x=>x.href)")
            imgs = pg.eval_on_selector_all("img", "e=>e.map(x=>x.currentSrc||x.src)")
            artistas.append({"slug": slug, "texto": t, "links": links, "imgs": imgs})
            print("[%d] %s %d chars" % (len(artistas), slug, len(t)), flush=True)
        except Exception as e:
            print("fallo", slug, e, flush=True)
    nav.close()
json.dump(artistas, open("crudo_artistas.json", "w"), ensure_ascii=False)
print("guardados:", len(artistas))
