#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KILMAN BILISIM — ETKILESIM DENETIMI  (03.08.2026)
==================================================
site_denetim.py HTML YAPISINI ve ICERIGI kontrol eder.
Bu betik TARAYICIDA CALISAN DAVRANISI kontrol eder.

NEDEN VAR:
03.08'de netlify.toml'daki preventAttributesEscaping ayari
  onclick="showPage('about')"  ->  onclick="showPage("about")"
donusumune yol acti. Attribute erken kapandi, ana sayfada HICBIR menu
linki calismadi. Konsol temizdi, HTML gecerliydi, site_denetim.py
UC KEZ "316/316 TEMIZ" dedi. Hatayi Patron gozle buldu.

Ders: gecerli HTML != calisan site.

KULLANIM
  python3 etkilesim.py                 # ana sayfa + yeni sayfalar
  python3 etkilesim.py --url <adres>   # tek adres

CIKIS KODU: 0 = temiz, 1 = sorun
"""
import sys, re, argparse
from playwright.sync_api import sync_playwright

BASE = "https://kilmanbilisim.com"

# ----------------------------------------------------------------------
def gorunur_bolumler(pg):
    return pg.evaluate(
        "()=>[...document.querySelectorAll('.page')]"
        ".filter(e=>getComputedStyle(e).display!=='none').map(e=>e.id)")

def onclick_bicimi(pg):
    """onclick degeri gecerli bir showPage cagrisi mi.

    ⚠️ 03.08 DERSI: ic tirnagin tek mi cift mi oldugu ONEMSIZ.
    onclick='showPage("about")' de onclick="showPage('about')" de GECERLI.
    Onemli olan attribute'un ERKEN KAPANMAMASI — yani deger icinde
    hedef adin tam okunabilmesi. Kirik hal: showPage( ile bitmesi.
    """
    return pg.evaluate("""()=>{
      const a=[...document.querySelectorAll('[onclick]')]
        .map(e=>e.getAttribute('onclick')||'')
        .filter(s=>s.includes('showPage'));
      const gecerli=a.filter(s=>/showPage\\(\\s*['"][a-z0-9-]+['"]\\s*\\)/i.test(s));
      const kirik=a.filter(s=>!/showPage\\(\\s*['"][a-z0-9-]+['"]\\s*\\)/i.test(s));
      return {toplam:a.length, kirik:kirik.length, gecerli:gecerli.length,
              ornek:(kirik[0]||a[0]||'')};
    }""")

def menu_testi(pg):
    """Her showPage linkine tiklanip HEDEF bolum aciliyor mu.

    Dogru olcut: tiklamadan sonra onclick'teki hedef bolum gorunur olmali.
    "Bolum degisti mi" yanlis olcut — zaten acik olan bolume tiklamak
    degisiklik yaratmaz ama HATA DEGILDIR (logo, Ana Sayfa).
    """
    linkler = pg.evaluate("""()=>[...document.querySelectorAll('nav a')]
        .map((a,i)=>({i:i, t:(a.innerText.trim()||'(logo)').slice(0,22),
                      oc:a.getAttribute('onclick')||''}))
        .filter(x=>x.oc.includes('showPage'))""")
    sonuc = []
    for L in linkler:
        m = re.search(r"showPage\(\s*['\"]([a-z0-9-]+)['\"]", L["oc"])
        hedef = f"page-{m.group(1)}" if m else None
        if not hedef:
            sonuc.append((L["t"], ["hedef okunamadi"], False)); continue
        try:
            pg.evaluate(f"()=>document.querySelectorAll('nav a')[{L['i']}].click()")
            pg.wait_for_timeout(420)
            gor = gorunur_bolumler(pg)
            sonuc.append((L["t"], gor, hedef in gor))
        except Exception as e:
            sonuc.append((L["t"], [f"TIKLANAMADI:{type(e).__name__}"], False))
    return sonuc

def gercek_linkler(pg):
    """Gercek adrese giden navbar linkleri (kademeli gecis takibi)."""
    return pg.evaluate("""()=>[...document.querySelectorAll('nav a')]
        .map(a=>({t:(a.innerText.trim()||'(logo)').slice(0,20), h:a.getAttribute('href')||''}))
        .filter(x=>x.h && x.h!=='#')""")

def sayac_ve_glow(pg):
    return pg.evaluate("""()=>{
      const g=i=>{const e=document.getElementById(i);return e?e.textContent.trim():null};
      const s=getComputedStyle(document.body,'::after');
      return {sayac: g('lcTotalFooter')||g('lcTotal'),
              glow: s.animationName, tiklama_engeli: s.pointerEvents};
    }""")

# ----------------------------------------------------------------------
def denetle(pg, url, ana_sayfa):
    bayrak, notlar = [], {}
    hata = []
    pg.on("console", lambda m: hata.append(m.text[:90]) if m.type == "error" else None)
    pg.goto(url, wait_until="load")
    pg.wait_for_timeout(1800)

    oc = onclick_bicimi(pg)
    notlar["onclick"] = f"{oc['gecerli']} gecerli / {oc['kirik']} kirik (toplam {oc['toplam']})"
    if oc["kirik"]:
        bayrak.append(f"ONCLICK-KIRIK({oc['kirik']})")
        notlar["onclick_ornek"] = oc["ornek"][:70]

    if ana_sayfa:
        m = menu_testi(pg)
        calismayan = [ad for ad, _, ok in m if not ok]
        notlar["menu"] = f"{len(m)-len(calismayan)}/{len(m)} calisiyor"
        if calismayan:
            bayrak.append(f"MENU-CALISMIYOR({len(calismayan)})")
            notlar["menu_kotu"] = ", ".join(calismayan[:5])
        gl = gercek_linkler(pg)
        notlar["gercek_link"] = ", ".join(f"{x['t']}→{x['h']}" for x in gl[:6]) or "yok"

    sg = sayac_ve_glow(pg)
    notlar["sayac"] = sg["sayac"] or "eleman yok"
    notlar["glow"] = f"{sg['glow']} · pointer-events:{sg['tiklama_engeli']}"
    if sg["sayac"] in ("—", "-", None):
        bayrak.append("SAYAC-BOS")
    if sg["glow"] == "none":
        bayrak.append("GLOW-YOK")
    if sg["tiklama_engeli"] != "none":
        bayrak.append("GLOW-TIKLAMA-ENGELLIYOR")

    if hata:
        bayrak.append(f"KONSOL-HATASI({len(hata)})")
        notlar["konsol"] = hata[0]

    return bayrak, notlar

def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--url", nargs="+")
    ap.add_argument("-h", "--help", action="store_true")
    a = ap.parse_args()
    if a.help:
        print(__doc__); return 2

    hedefler = a.url if a.url else [
        BASE + "/",
        BASE + "/hakkimizda.html",
        BASE + "/en/hakkimizda.html",
    ]
    sorunlu = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for u in hedefler:
            c = b.new_context(viewport={"width": 1280, "height": 900})
            pg = c.new_page()
            ana = u.rstrip("/") == BASE
            try:
                bayrak, notlar = denetle(pg, u, ana)
            except Exception as e:
                bayrak, notlar = [f"ACILAMADI:{type(e).__name__}"], {}
            print(f"\n{'='*70}\n{u.replace(BASE,'') or '/'}")
            for k, v in notlar.items():
                print(f"   {k:16}: {v}")
            print(f"   {'SONUC':16}: {'TEMIZ' if not bayrak else ' | '.join(bayrak)}")
            if bayrak: sorunlu += 1
            c.close()
        b.close()
    print(f"\n{'='*70}")
    print(f"toplam {len(hedefler)} sayfa | sorunlu {sorunlu}")
    print("SONUC: " + ("HEPSI TEMIZ" if not sorunlu else "SORUN VAR — patrona bildirilir"))
    return 1 if sorunlu else 0

if __name__ == "__main__":
    sys.exit(main())
