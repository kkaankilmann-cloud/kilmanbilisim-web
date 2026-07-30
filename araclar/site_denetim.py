#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KILMAN BILISIM — SITE ICERIK DENETIM BETIGI  (v2, site geneli)
==============================================================
Siteye eklenen HER SEY icin (blog yazisi, urun, hizmet, sayfa) 9 dil kontrolu yapar.

KULLANIM
  python3 site_denetim.py --tum                      # sitemap'teki her sayfa (tam tarama)
  python3 site_denetim.py --slug <slug>              # bir blog yazisinin 9 dili
  python3 site_denetim.py --sayfa <ad>               # bir sayfanin 9 dili (orn: urun-panel)
  python3 site_denetim.py --url <adres> [<adres>...] # serbest adres listesi
  python3 site_denetim.py --yeni                     # sitemap'te olup dizinde olmayanlari bul

NE KONTROL EDER (10 madde)
  1. HTTP durumu (200 mu)
  2. Kodlama bozulmasi  — CP857/CP437 geri-cevrim testi (30 Tem: 9 sayfa bu yuzden bozuktu)
  3. Parcalanmis emoji  — &#55357;&#56986; gibi surrogate ciftleri
  4. Ekranda bozuk isaret (U+FFFD) ve ters-slash apostrof (\\')
  5. canonical (tam 1 adet)
  6. hreflang (10 karsilikli baglanti)
  7. html lang dogru mu (zh icin zh-Hans)
  8. JSON-LD semasi var mi
  9. GOVDE DILI sayfanin diliyle uyusuyor mu  (30 Tem: baslik EN, govde TR cikti)
 10. 9 dil tamligi — her icerigin 9 dil karsiligi var mi

CIKIS KODU: 0 = hepsi temiz, 1 = sorun var  (CI/otomasyona baglanabilir)
"""

import sys, re, html, argparse, unicodedata
import requests
from concurrent.futures import ThreadPoolExecutor

BASE = "https://kilmanbilisim.com"
DILLER = ["tr", "en", "de", "es", "fr", "ru", "ko", "zh", "ja"]
BEKLENEN_HTML_LANG = {"zh": "zh-Hans"}

# ----------------------------------------------------------------------
# 1) KODLAMA BOZULMASI TESPITI  (CP857 / CP437 geri-cevrim)
# ----------------------------------------------------------------------
def _cevir(run, kod):
    bs = bytearray()
    for ch in run:
        if ch == "\uf8bc":
            bs.append(0xE7)          # cp857'de tanimsiz slot
        else:
            try: bs += ch.encode(kod)
            except Exception: return None
    try:
        r = bs.decode("utf-8")
        return r if r != run else None
    except Exception:
        return None

def kodlama_bozuk(metin):
    """Bozuk karakter sayisi ve ilk ornek."""
    n, ornek, i = 0, "", 0
    while i < len(metin):
        if ord(metin[i]) < 128:
            i += 1; continue
        j = i
        while j < len(metin) and ord(metin[j]) >= 128:
            j += 1
        run = metin[i:j]
        for kod in ("cp857", "cp437"):
            d = _cevir(run, kod)
            if d:
                n += (j - i)
                if not ornek:
                    ornek = f"{run[:24]} -> {d[:24]}"
                break
        i = j
    return n, ornek

# ----------------------------------------------------------------------
# 2) DIL TESPITI  (yazi sistemi + durak kelime)
# ----------------------------------------------------------------------
DURAK = {
    "tr": [" ve ", " için ", " bir ", " ile ", " olarak ", " gibi ", " bu ", " daha ", " ancak ", " veya "],
    "en": [" the ", " and ", " for ", " with ", " that ", " your ", " this ", " from ", " can ", " are "],
    "de": [" und ", " der ", " die ", " das ", " für ", " mit ", " ist ", " ein ", " von ", " nicht "],
    "es": [" el ", " la ", " de ", " que ", " para ", " con ", " los ", " una ", " por ", " del "],
    "fr": [" le ", " la ", " les ", " des ", " pour ", " avec ", " que ", " une ", " est ", " dans "],
}
YAZI_ARALIK = {
    "ru": [(0x0400, 0x04FF)],                                   # Kiril
    "ko": [(0xAC00, 0xD7AF), (0x1100, 0x11FF)],                 # Hangul
    "ja": [(0x3040, 0x309F), (0x30A0, 0x30FF)],                 # Hiragana + Katakana
    "zh": [(0x4E00, 0x9FFF)],                                   # Han
}

def yazi_orani(metin, dil):
    araliklar = YAZI_ARALIK.get(dil)
    if not araliklar: return None
    say = sum(1 for ch in metin if any(a <= ord(ch) <= b for a, b in araliklar))
    harf = sum(1 for ch in metin if ch.isalpha()) or 1
    return say / harf

def durak_skor(metin, dil):
    m = " " + re.sub(r"\s+", " ", metin.lower()) + " "
    kelimeler = DURAK.get(dil)
    if not kelimeler: return None
    return sum(m.count(k) for k in kelimeler)

def govde_dili_uyumlu(govde, dil):
    """(uyumlu_mu, aciklama)"""
    if len(govde.strip()) < 200:
        return None, "govde cok kisa"
    if dil in YAZI_ARALIK:                       # ru/ko/zh/ja: yazi sistemi bakilir
        oran = yazi_orani(govde, dil)
        tr = durak_skor(govde, "tr") or 0
        kana = sum(1 for ch in govde if 0x3040 <= ord(ch) <= 0x30FF)
        harf = sum(1 for ch in govde if ch.isalpha()) or 1
        kana_orani = kana / harf
        # zh ile ja ayrimi: Japonca kanji icerir, bu yuzden Han orani zh'yi kanitlamaz.
        # zh olmasi icin kana YOK olmali; ja olmasi icin kana VAR olmali.
        if dil == "zh" and kana_orani > 0.02:
            return False, f"kana orani %{kana_orani*100:.0f} — bu Japonca, Cince degil"
        if dil == "ja" and kana_orani < 0.05:
            return False, f"kana orani %{kana_orani*100:.0f} — Japonca kana yok"
        if oran < 0.15:
            return False, f"{dil} yazi orani %{oran*100:.0f} (dusuk)" + (f", TR skor {tr}" if tr >= 8 else "")
        return True, f"yazi orani %{oran*100:.0f}"
    # tr/en/de/es/fr: durak kelime yarismasi
    skorlar = {d: (durak_skor(govde, d) or 0) for d in DURAK}
    kazanan = max(skorlar, key=skorlar.get)
    if skorlar[dil] == 0:
        return False, f"{dil} durak kelimesi yok (govde: {kazanan})"
    if kazanan != dil and skorlar[kazanan] > skorlar[dil] * 1.8:
        return False, f"govde {kazanan} gibi ({kazanan}={skorlar[kazanan]}, {dil}={skorlar[dil]})"
    return True, f"{dil}={skorlar[dil]}"

# ----------------------------------------------------------------------
# 3) SAYFA DENETIMI
# ----------------------------------------------------------------------
def dil_bul(url):
    """Adresten dili cikar. /blog/en/... -> en ; /blog/... -> tr"""
    y = url.replace(BASE, "")
    m = re.match(r"^/blog/([a-z]{2})(?:/|$)", y)
    if m and m.group(1) in DILLER: return m.group(1)
    m = re.match(r"^/([a-z]{2})(?:/|$)", y)
    if m and m.group(1) in DILLER and m.group(1) != "tr": return m.group(1)
    return "tr"

def govde_al(dcoz):
    m = re.search(r"<article[^>]*>(.*?)</article>", dcoz, re.S)
    ic = m.group(1) if m else dcoz
    m2 = re.search(r"<main[^>]*>(.*?)</main>", ic, re.S)
    if m2: ic = m2.group(1)
    ic = re.sub(r"<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<footer.*?</footer>|<header.*?</header>",
                "", ic, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", ic))

def denetle(url, ana_sayfa_mi=False):
    dil = dil_bul(url)
    try:
        r = requests.get(url, timeout=45)
    except Exception as e:
        return dict(url=url, dil=dil, bayrak=[f"ERISILEMEDI ({type(e).__name__})"])
    ham = r.text
    dcoz = html.unescape(ham)
    bayrak, notlar = [], {}

    if r.status_code != 200:
        bayrak.append(f"HTTP{r.status_code}")

    n, ornek = kodlama_bozuk(dcoz)
    if n:
        bayrak.append(f"kodlama({n})"); notlar["kodlama"] = ornek

    # Parcalanmis emoji: SADECE gercek surrogate cifti (yuksek 55296-56319 + alcak 56320-57343).
    # DIKKAT: Hangul heceleri 44032-55203 araligindadir; genis regex Korece sayfada yanlis alarm verir.
    if re.search(r"&#(?:5529[6-9]|55[3-9]\d{2}|56[0-2]\d{2}|563(?:0\d|1\d));\s*&#(?:56(?:3[2-9]\d|[4-9]\d{2})|57[0-2]\d{2}|573[0-3]\d|5734[0-3]);", ham):
        bayrak.append("parcali-emoji")
    # ham UTF-8 metinde de yalniz kalmis surrogate olabilir
    if any(0xD800 <= ord(c) <= 0xDFFF for c in dcoz):
        bayrak.append("yalniz-surrogate")
    if "\ufffd" in dcoz:
        bayrak.append("bozuk-isaret")
    if re.search(r"\\'", dcoz):
        bayrak.append("ters-slash-apostrof")

    if len(re.findall(r"rel=(?:\"canonical\"|'canonical'|canonical)", ham)) != 1:
        bayrak.append("canonical")
    hre = len(re.findall(r"hreflang=", ham))
    if not ana_sayfa_mi and hre != 10:
        bayrak.append(f"hreflang({hre})")
    if ham.count("application/ld+json") < 1:
        bayrak.append("jsonld-yok")

    m = re.search(r"<html[^>]*\blang=(?:\"([^\"]+)\"|'([^']+)'|([^\s>]+))", ham)
    la = (m.group(1) or m.group(2) or m.group(3)) if m else "YOK"
    if la != BEKLENEN_HTML_LANG.get(dil, dil):
        bayrak.append(f"lang={la}")

    govde = govde_al(dcoz)
    uyum, acik = govde_dili_uyumlu(govde, dil)
    notlar["dil"] = acik
    if uyum is False:
        bayrak.append("GOVDE-YANLIS-DIL")

    return dict(url=url, dil=dil, kod=r.status_code, kb=len(ham.encode()) // 1024,
                bayrak=bayrak, notlar=notlar)

# ----------------------------------------------------------------------
# 4) ADRES TOPLAMA
# ----------------------------------------------------------------------
def sitemap_urlleri():
    t = requests.get(f"{BASE}/sitemap.xml", timeout=30).text
    return re.findall(r"<loc>(.*?)</loc>", t)

def slug_urlleri(slug):
    return [f"{BASE}/blog/{slug}.html" if d == "tr" else f"{BASE}/blog/{d}/{slug}.html" for d in DILLER]

def sayfa_urlleri(ad):
    ad = ad.strip("/")
    return [f"{BASE}/{ad}" if d == "tr" else f"{BASE}/{d}/{ad}" for d in DILLER]

# ----------------------------------------------------------------------
# 5) 9 DIL TAMLIK KONTROLU
# ----------------------------------------------------------------------
def dil_tamligi(urller):
    """Ayni icerigin 9 dil karsiligi var mi."""
    gruplar = {}
    for u in urller:
        y = u.replace(BASE, "")
        m = re.match(r"^/blog/(?:([a-z]{2})/)?(.*)$", y)
        if not m: continue
        d = m.group(1) if (m.group(1) in DILLER) else "tr"
        kalan = m.group(2) or ""
        if m.group(1) and m.group(1) not in DILLER:
            kalan = m.group(1) + "/" + kalan
        # liste (hub) sayfalari: /blog/ ve /blog/xx/ -> tek grup
        anahtar = "[blog liste sayfasi]" if kalan in ("", "/") else kalan
        gruplar.setdefault(anahtar, set()).add(d)
    eksikler = {k: sorted(set(DILLER) - v) for k, v in gruplar.items() if len(v) < 9}
    return gruplar, eksikler

# ----------------------------------------------------------------------
# 6) RAPOR
# ----------------------------------------------------------------------
def rapor(sonuclar, baslik):
    print(f"\n{'='*78}\n{baslik}\n{'='*78}")
    print(f"{'dil':4}{'HTTP':>5}{'KB':>5}  {'adres':50} sonuc")
    sorunlu = []
    for s in sonuclar:
        ad = s["url"].replace(BASE, "")
        if len(ad) > 48: ad = ad[:22] + "..." + ad[-23:]
        durum = "TEMIZ" if not s["bayrak"] else ",".join(s["bayrak"])
        print(f"{s['dil']:4}{s.get('kod','-'):>5}{s.get('kb','-'):>5}  {ad:50} {durum}")
        if s["bayrak"]: sorunlu.append(s)
    print(f"\ntoplam {len(sonuclar)} sayfa | temiz {len(sonuclar)-len(sorunlu)} | SORUNLU {len(sorunlu)}")
    if sorunlu:
        print("\n--- SORUN DETAYI ---")
        for s in sorunlu:
            print(f"  {s['url']}")
            print(f"     {', '.join(s['bayrak'])}")
            for k, v in s.get("notlar", {}).items():
                if v: print(f"     {k}: {v}")
    return sorunlu

def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--tum", action="store_true")
    ap.add_argument("--slug")
    ap.add_argument("--sayfa")
    ap.add_argument("--url", nargs="+")
    ap.add_argument("--yeni", action="store_true")
    ap.add_argument("-h", "--help", action="store_true")
    a = ap.parse_args()
    if a.help or not any([a.tum, a.slug, a.sayfa, a.url, a.yeni]):
        print(__doc__); return 2

    if a.tum or a.yeni:
        urller = sitemap_urlleri(); baslik = f"TAM SITE TARAMASI — {len(urller)} adres"
    elif a.slug:
        urller = slug_urlleri(a.slug); baslik = f"BLOG YAZISI — {a.slug} (9 dil)"
    elif a.sayfa:
        urller = sayfa_urlleri(a.sayfa); baslik = f"SAYFA — {a.sayfa} (9 dil)"
    else:
        urller = a.url; baslik = "SERBEST ADRES LISTESI"

    with ThreadPoolExecutor(max_workers=12) as ex:
        sonuclar = list(ex.map(lambda u: denetle(u, ana_sayfa_mi=(u.rstrip("/") == BASE)), urller))

    sorunlu = rapor(sonuclar, baslik)

    if a.tum or a.yeni:
        gruplar, eksikler = dil_tamligi(urller)
        print(f"\n--- 9 DIL TAMLIK ---\n{len(gruplar)} icerik grubu")
        if eksikler:
            print(f"EKSIK DILI OLAN {len(eksikler)} icerik:")
            for k, v in list(eksikler.items())[:15]: print(f"  {k}  eksik: {v}")
        else:
            print("hepsi 9 dilde TAM")

    print("\n" + "="*78)
    if sorunlu:
        print("SONUC: SORUN VAR — Search Console'a adres EKLENMEZ, patrona bildirilir")
        return 1
    print("SONUC: HEPSI TEMIZ")
    return 0

if __name__ == "__main__":
    sys.exit(main())
