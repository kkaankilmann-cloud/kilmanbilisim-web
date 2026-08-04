#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KILMAN BILISIM — SITE ICERIK DENETIM BETIGI  (v3, catch-all kalkani)
====================================================================
Siteye eklenen HER SEY icin (blog yazisi, urun, hizmet, sayfa) 9 dil kontrolu yapar.

KULLANIM
  python3 site_denetim.py --tum                      # sitemap'teki her sayfa (tam tarama)
  python3 site_denetim.py --slug <slug>              # bir blog yazisinin 9 dili
  python3 site_denetim.py --sayfa <ad>               # bir sayfanin 9 dili (orn: urun-panel)
  python3 site_denetim.py --url <adres> [<adres>...] # serbest adres listesi
  python3 site_denetim.py --yeni                     # sitemap'te olup dizinde olmayanlari bul
  python3 site_denetim.py --kalkan-testi             # catch-all kalkanini kendi kendine test et

NE KONTROL EDER (12 madde)
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
 11. CATCH-ALL KALKANI — sayfa gercekten var mi (soft-404 parmak izi)  [04.08.2026]
 12. CANONICAL UYUSMAZLIGI — sayfa kendini baska adres mi saniyor    [04.08.2026]

CIKIS KODU: 0 = hepsi temiz, 1 = sorun var  (CI/otomasyona baglanabilir)
"""

import sys, re, html, argparse, unicodedata, hashlib, random, string
import requests
from concurrent.futures import ThreadPoolExecutor

BASE = "https://kilmanbilisim.com"

# ----------------------------------------------------------------------
# 0) CATCH-ALL KALKANI  (04.08.2026)
# Site olmayan sayfalar icin 404 vermiyor, ana sayfayi 200 ile donduruyor.
# Bu kalkan program basinda bir kez sahte adres cekip parmak izini saklar.
# Her sayfa denetiminde parmak izi eslesmesi kontrol edilir.
# ----------------------------------------------------------------------
SOFT404 = {"hash": None, "boyut": None}

def soft404_parmak_izi(base=None):
    """Kesin olmayan bir adres cekilir, cevabinin parmak izi saklanir."""
    if base is None: base = BASE
    rnd = "".join(random.choices(string.ascii_lowercase, k=12))
    url = f"{base}/__yok-{rnd}.html"
    try:
        r = requests.get(url, timeout=30)
        govde = r.content  # bytes
        SOFT404["hash"] = hashlib.sha256(govde).hexdigest()
        SOFT404["boyut"] = len(govde)
        print(f"[kalkan] soft-404 parmak izi alindi: {SOFT404['boyut']} bayt")
    except Exception as e:
        print(f"[kalkan] UYARI: parmak izi alinamadi ({e})")
    return SOFT404

def sayfa_var_mi(govde_bytes):
    """Sayfa gercekten var mi yoksa catch-all ana sayfa mi donuyor?"""
    if SOFT404["hash"] is None:
        return True, ""
    if hashlib.sha256(govde_bytes).hexdigest() == SOFT404["hash"]:
        return False, "SAYFA YOK (catch-all: ana sayfa donuyor)"
    return True, ""

def canonical_uyusmazligi(ham, istenen_url):
    """Canonical adresin istenen URL ile eslesip eslesmedigini kontrol et."""
    # Tirnaksiz kalibi da yakala (netlify minify tirnak kaldirabilir)
    m = (re.search(r'<link[^>]+rel=["\']?canonical["\']?[^>]+href=["\']?([^"\'>\s]+)', ham)
         or re.search(r'<link[^>]+href=["\']?([^"\'>\s]+)["\']?[^>]+rel=["\']?canonical', ham))
    if not m:
        return ""  # canonical yoklugu mevcut kontrol #5 tarafindan zaten yakalaniyor
    bulunan = m.group(1).rstrip("/")
    istenen = istenen_url.rstrip("/")
    if bulunan != istenen:
        return f"CANONICAL UYUSMAZ (sayfa kendini {bulunan} saniyor)"
    return ""
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

# ----------------------------------------------------------------------
# 2b) TURKCE KALINTI TESPITI  (paragraf bazli)
# 01.08.2026'da eklendi. Sebep: govde_dili_uyumlu() sayfanin TAMAMINA bakip
# "hangi dil kazaniyor" diye olcuyordu ve %80 tolerans birakiyordu. Yari
# cevrilmis sayfada (giris Ingilizce, govde Turkce) tr=29 en=17 cikti,
# tolerans icinde kaldigi icin TEMIZ dedi. 32 sayfa bu yuzden kacti.
# Cozum: her paragrafi/basligi AYRI degerlendir, Turkce'ye OZGU harfleri kullan.
# ----------------------------------------------------------------------
TR_OZGU = set("ğşıİĞŞ")          # de/fr/es/en'de bulunmaz
TR_KELIME = [" ve ", " ile ", " için ", " bir ", " olarak ", " gibi ", " bu ", " daha ",
             " her ", " olan ", " göre ", " kadar ", " ancak ", " veya ",
             " akıllı", " yönetim", " otomasyon", " tahmin", " analiz", " takip",
             " sistem", " planlama", " kontrol", " süreç", " işletme", " müşteri",
             " maliyet", " rapor", " yapay", " zeka", " üretim", " tüketim"]
MARKA = ["Kılman Bilişim", "Kılman", "KOBİ", "İstanbul", "Türkiye", "Türk"]

def _marka_at(s):
    for m in MARKA: s = s.replace(m, " ")
    return s

def turkce_kalinti_mi(s, kisa=False, hedef_dil=None):
    """Bu metin parcasi Turkce mi? Marka adlari ve yazar satirlari sayilmaz."""
    s = _marka_at(s)
    m = " " + s.lower() + " "
    ozgu = sum(1 for c in s if c in TR_OZGU)
    kel  = sum(m.count(k) for k in TR_KELIME)

    # 04.08.2026 EK: KESIN TURKCE IMZASI
    # Asagidaki ekler yalnizca Turkce'de bulunur (iyelik + cogul + bildirme).
    # Bunlar varsa hedef-dil korumasi DEVRE DISI kalir — cunku 04.08'de
    # "Kendi gelistirdigimiz urunler somut referanslarimizdir:" cumlesi
    # 8 dilde kaldi ve koruma yuzunden GORULMEDI.
    KESIN_TR = ("ımızdır", "imizdir", "umuzdur", "ümüzdür",
                "diğimiz", "dığımız", "duğumuz", "düğümüz",
                "larımız", "lerimiz", "ıyoruz", "iyoruz", "uyoruz", "üyoruz")
    if any(k in s for k in KESIN_TR):
        return True

    # 03.08.2026 YANLIS ALARM DUZELTMESI:
    # Netlify minify tirnaklari geri getirince metin ayristirmasi degisti;
    # baslik + yazar satiri ("Kaan Kilman", "Kilman Bilisim") tek parca olarak
    # yakalaniyordu ve Ispanyolca sayfalar Turkce sanildi.
    # Koruma: parca hedef dilin durak kelimelerince BASKINSA Turkce sayilmaz.
    if hedef_dil and hedef_dil in DURAK:
        hedef_skor = durak_skor(s, hedef_dil) or 0
        if hedef_skor >= 3 and hedef_skor > kel:
            return False
    if hedef_dil in YAZI_ARALIK:
        oran = yazi_orani(s, hedef_dil)
        if oran is not None and oran >= 0.30:
            return False

    if kisa:                       # basliklar kisa olur, esik dusuk
        return ozgu >= 1 and kel >= 1
    return (ozgu >= 3 and kel >= 2) or kel >= 5

def turkce_kalinti_say(dcoz, dil):
    """Yabanci dil sayfasinda Turkce kalmis baslik/paragraf sayisi."""
    if dil == "tr": return 0, 0, []
    m = re.search(r"<article[^>]*>(.*?)</article>", dcoz, re.S)
    ic = m.group(1) if m else dcoz
    ic = re.sub(r"<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<footer.*?</footer>", "", ic, flags=re.S)
    basliklar = [re.sub(r"<[^>]+>", "", x).strip()
                 for x in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", ic, re.S)]
    paragraflar = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
                   for x in re.findall(r"<(?:p|li)[^>]*>(.*?)</(?:p|li)>", ic, re.S)]
    paragraflar = [p for p in paragraflar if len(p) >= 40]
    kb = [x for x in basliklar if turkce_kalinti_mi(x, kisa=True, hedef_dil=dil)]
    kp = [x for x in paragraflar if turkce_kalinti_mi(x, hedef_dil=dil)]
    return len(kb), len(kp), (kb + kp)[:2]

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
# 5) IC LINK BICIMI  (03.08.2026 eklendi)
# Sitede standart: sayfa adresleri .html uzantili. Uzantisiz surum de
# acilir ama Google icin AYRI URL sayilir; canonical ile catisir.
# ⚠️ Tirnak bicimi karisik olabilir (href="..." ve href='...'), o yuzden
# ikisini de yakalayan kalip kullanilir. 03.08'de tek tirnakli 10 link
# tam bu yuzden gozden kacti.
# ----------------------------------------------------------------------
LINK_KALIP = re.compile(r"""href\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s>]+))""")
# uzanti almayacak adresler: kok, klasor adresleri, ozel dosyalar
LINK_MUAF = ("/", "/blog/")

def ic_link_bicimi(ham):
    """(uzantisiz_link_listesi) — tirnak bicimi ne olursa olsun."""
    kotu = []
    for m in LINK_KALIP.finditer(ham):
        h = (m.group(1) or m.group(2) or m.group(3) or "").strip()
        if not h.startswith("/"):            # dis link, mailto, tel, wa.me
            continue
        if h in LINK_MUAF or h.endswith("/"):  # klasor adresi
            continue
        if re.match(r"^/blog/[a-z]{2}/?$", h):  # /blog/en/ gibi
            continue
        if "." in h.rsplit("/", 1)[-1]:      # uzantisi var (.html .png .xml ...)
            continue
        if h.startswith("#") or h.startswith("?"):
            continue
        kotu.append(h)
    return sorted(set(kotu))

# ----------------------------------------------------------------------
# 6) ICERIK DERINLIGI  (03.08.2026 eklendi, 04.08.2026 guncellendi)
# 80 kelimelik sayfa Google'da "ince icerik" sayilir, siralanmaz.
# CJK dillerinde bosluk olmadigi icin kelime degil KARAKTER sayilir.
#
# 04.08.2026 EK A: display:none icindeki metin Google'un saymadigi
# gizli icerik — kelime sayimindan cikarilacak. Div derinligi sayilir.
# 04.08.2026 EK B: Esik sayfa tipine gore ayrildi.
# ----------------------------------------------------------------------
CJK_ARALIK = [(0x4E00, 0x9FFF), (0x3040, 0x30FF), (0xAC00, 0xD7AF)]

ESIKLER = {
    "blog":    {"latin": 700, "cjk": 1200},
    "urun":    {"latin": 300, "cjk": 550},
    "hizmet":  {"latin": 300, "cjk": 550},
    "kurumsal":{"latin": 300, "cjk": 550},
    "diger":   {"latin": 200, "cjk": 280},
}

def sayfa_tipi_bul(url):
    """URL'den sayfa tipini cikar."""
    y = url.replace(BASE, "")
    if "/blog/" in y or y.startswith("/blog"):
        # /blog/ liste sayfalari icin diger, blog yazilari icin blog
        if y.rstrip("/").endswith("/blog") or re.match(r"^/blog/[a-z]{2}/?$", y):
            return "diger"  # liste sayfasi
        return "blog"
    if "urunler" in y:
        return "urun"
    if "hizmetler" in y:
        return "hizmet"
    if any(k in y for k in ("hakkimizda", "sss", "iletisim", "referanslar")):
        return "kurumsal"
    return "diger"

def _gizli_blok_kes(h, baslangic):
    """baslangic'taki acilis etiketinden itibaren div derinligi sayarak
    tum blogu (ic ice div'ler dahil) keser ve span olarak dondurur."""
    derinlik = 0
    for m in re.finditer(r'<(/?)div\b', h[baslangic:]):
        if m.group(1) == "":
            derinlik += 1
        else:
            derinlik -= 1
            if derinlik == 0:
                # </div> etiketinin sonuna kadar kes
                bitis = baslangic + m.end()
                # </div>'in > isaretini bul
                kapa = h.find(">", bitis)
                if kapa == -1: kapa = bitis
                return baslangic, kapa + 1
    return baslangic, len(h)

def _gizli_bloklari_cikar(h):
    """style='...display:none...' tasiyan tum elemanlari (ve icindeki her seyi) cikarir."""
    sonuc = h
    # Tekrar tekrar bul ve kes (her seferinde indeksler degisir)
    for _ in range(20):  # en fazla 20 gizli blok
        m = re.search(r'<div[^>]+style=["\'][^"]*display\s*:\s*none[^"]*["\']', sonuc, re.I)
        if not m:
            # tirnaksiz hali de kontrol et (netlify minify)
            m = re.search(r'<div[^>]+style=[^>]*display\s*:\s*none', sonuc, re.I)
            if not m:
                break
        bas, son = _gizli_blok_kes(sonuc, m.start())
        sonuc = sonuc[:bas] + sonuc[son:]
    return sonuc

def icerik_derinligi(dcoz, dil, url=""):
    """(kelime, cjk_karakter, h2_sayisi, yetersiz_mi, detay_str)"""
    gov = dcoz
    # 1) head, script, style, nav, footer cikar
    gov = re.sub(r"<head.*?</head>", "", gov, flags=re.S)
    gov = re.sub(r"<nav.*?</nav>|<footer.*?</footer>|<script.*?</script>|<style.*?</style>",
                 "", gov, flags=re.S)
    # 2) display:none gizli bloklari cikar (div derinligi sayarak)
    gov = _gizli_bloklari_cikar(gov)
    h2 = len(re.findall(r"<h2[^>]*>", gov))
    metin = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", gov)).strip()
    cjk_dar = sum(1 for c in metin if any(a <= ord(c) <= b for a, b in CJK_ARALIK))
    # CJK dillerde bosluklari cikarip TUM karakterleri say (Latin kelimeler, rakamlar dahil)
    cjk_genis = len(metin.replace(" ", ""))
    kelime = len([w for w in metin.split(" ") if w])
    # Sayfa tipine gore esik
    tip = sayfa_tipi_bul(url)
    esik = ESIKLER.get(tip, ESIKLER["diger"])
    if dil in ("zh", "ja", "ko"):
        yetersiz = cjk_genis < esik["cjk"]
        detay = f"{cjk_genis} kar (gorunur) · esik {esik['cjk']} · tip {tip}"
    else:
        yetersiz = kelime < esik["latin"]
        detay = f"{kelime} kel (gorunur) · esik {esik['latin']} · tip {tip}"
    return kelime, cjk_genis, h2, yetersiz, detay

# ----------------------------------------------------------------------
# 3) SAYFA DENETIMI
# ----------------------------------------------------------------------
# Site bolum klasorleri. Dil segmenti bunlardan SONRA, dosya adindan ONCE gelir.
# Turkce'de dil segmenti YOKTUR.
#   /blog/en/x.html · /hizmetler/en/x.html · /urunler/en/x.html · /en/hakkimizda.html
BOLUMLER = ("blog", "hizmetler", "urunler")

def dil_bul(url):
    """Adresten dili cikar (03.08.2026 yeni sayfa mimarisi dahil)."""
    y = url.replace(BASE, "")
    # bolum klasoru + dil:  /blog/en/...  /hizmetler/en/...  /urunler/en/...
    m = re.match(r"^/(" + "|".join(BOLUMLER) + r")/([a-z]{2})(?:/|$)", y)
    if m and m.group(2) in DILLER: return m.group(2)
    # kok seviyesinde dil:  /en/hakkimizda.html
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

    # --- CATCH-ALL KALKANI (madde 11) ---
    # Ana sayfa catch-all'in dondurudugunun TA KENDISI — hash ayni cikar, atla.
    if not ana_sayfa_mi:
        var, acik = sayfa_var_mi(r.content)
        if not var:
            bayrak.append("SAYFA-YOK")
            notlar["kalkan"] = acik
            # Diger kontrollere girilmez — ana sayfanin hreflang'ini olcup
            # "temiz" demek en tehlikeli hata.
            return dict(url=url, dil=dil, kod=r.status_code, kb=len(ham.encode()) // 1024,
                        bayrak=bayrak, notlar=notlar)

    # --- CANONICAL UYUSMAZLIGI (madde 12) ---
    if not ana_sayfa_mi:
        cu = canonical_uyusmazligi(ham, url)
        if cu:
            bayrak.append("CANONICAL-UYUSMAZ")
            notlar["canonical"] = cu

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

    # --- ic link bicimi (tirnaktan bagimsiz) ---
    kotu_link = ic_link_bicimi(ham)
    if kotu_link:
        bayrak.append(f"UZANTISIZ-LINK({len(kotu_link)})")
        notlar["link"] = ", ".join(kotu_link[:5])

    # --- icerik derinligi ---
    kel, cjk, h2, yetersiz, detay = icerik_derinligi(dcoz, dil, url)
    notlar["icerik"] = detay
    if yetersiz:
        bayrak.append("INCE-ICERIK")


    kb, kp, ornekler = turkce_kalinti_say(dcoz, dil)
    if kb or kp:
        bayrak.append(f"TURKCE-KALINTI(baslik:{kb},paragraf:{kp})")
        if ornekler: notlar["kalinti"] = ornekler[0][:110]

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
        if y in ("", "/"):
            continue                      # ana sayfa tek dilli degil, SPA — haric
        d, anahtar = None, None

        # 1) bolum klasoru:  /blog/[dil/]dosya  ·  /hizmetler/[dil/]dosya  ·  /urunler/[dil/]dosya
        m = re.match(r"^/(" + "|".join(BOLUMLER) + r")/(?:([a-z]{2})/)?(.*)$", y)
        if m:
            bolum, dil, kalan = m.group(1), m.group(2), m.group(3) or ""
            if dil in DILLER:
                d = dil
            else:                          # /blog/slug.html -> dil yok, TR
                d = "tr"
                if dil: kalan = dil + "/" + kalan
            anahtar = f"[{bolum} liste]" if kalan in ("", "/") else f"{bolum}/{kalan}"

        # 2) kok seviyesi:  /hakkimizda.html  ·  /en/hakkimizda.html
        if d is None:
            m = re.match(r"^/(?:([a-z]{2})/)?([^/]+)$", y)
            if not m: continue
            dil, dosya = m.group(1), m.group(2)
            if dil in DILLER and dil != "tr":
                d, anahtar = dil, dosya
            elif dil is None:
                d, anahtar = "tr", dosya
            else:
                continue

        if anahtar: gruplar.setdefault(anahtar, set()).add(d)

    eksikler = {k: sorted(set(DILLER) - v) for k, v in gruplar.items() if len(v) < 9}
    return gruplar, eksikler

# ----------------------------------------------------------------------
# 6) RAPOR
# ----------------------------------------------------------------------
def rapor(sonuclar, baslik):
    print(f"\n{'='*78}\n{baslik}\n{'='*78}")
    print(f"{'dil':4}{'HTTP':>5}{'KB':>5}  {'adres':50} sonuc")
    sorunlu = []
    sayfa_yok_sayisi = 0
    canonical_sayisi = 0
    for s in sonuclar:
        ad = s["url"].replace(BASE, "")
        if len(ad) > 48: ad = ad[:22] + "..." + ad[-23:]
        durum = "TEMIZ" if not s["bayrak"] else ",".join(s["bayrak"])
        print(f"{s['dil']:4}{s.get('kod','-'):>5}{s.get('kb','-'):>5}  {ad:50} {durum}")
        if s["bayrak"]:
            sorunlu.append(s)
            if "SAYFA-YOK" in s["bayrak"]: sayfa_yok_sayisi += 1
            if "CANONICAL-UYUSMAZ" in s["bayrak"]: canonical_sayisi += 1
    temiz = len(sonuclar) - len(sorunlu)
    ozet = f"\ntoplam {len(sonuclar)} sayfa | temiz {temiz}"
    if sayfa_yok_sayisi: ozet += f" | SAYFA YOK {sayfa_yok_sayisi}"
    if canonical_sayisi: ozet += f" | canonical {canonical_sayisi}"
    diger = len(sorunlu) - sayfa_yok_sayisi - canonical_sayisi
    if diger > 0: ozet += f" | sorunlu {diger}"
    if not sorunlu: ozet += " | SORUNLU 0"
    print(ozet)
    if sorunlu:
        print("\n--- SORUN DETAYI ---")
        for s in sorunlu:
            print(f"  {s['url']}")
            print(f"     {', '.join(s['bayrak'])}")
            for k, v in s.get("notlar", {}).items():
                if v: print(f"     {k}: {v}")
    return sorunlu

def kalkan_testi():
    """Catch-all kalkanini kendi kendine test eder."""
    print("=" * 78)
    print("KALKAN TESTI")
    print("=" * 78)
    soft404_parmak_izi()
    hata = 0

    # Test 1: Kesin var olan sayfa
    var_url = f"{BASE}/hizmetler.html"
    try:
        r = requests.get(var_url, timeout=30)
        var, _ = sayfa_var_mi(r.content)
        if var:
            print(f"  OK: {var_url} -> SAYFA VAR (dogru)")
        else:
            print(f"  HATA: {var_url} -> SAYFA YOK dedi (yanlis!)")
            hata += 1
    except Exception as e:
        print(f"  HATA: {var_url} -> erisilemedi ({e})")
        hata += 1

    # Test 2: Kesin olmayan sayfa
    yok_url = f"{BASE}/__test-yok-99999.html"
    try:
        r = requests.get(yok_url, timeout=30)
        var, acik = sayfa_var_mi(r.content)
        if not var:
            print(f"  OK: {yok_url} -> SAYFA YOK (dogru)")
        else:
            print(f"  HATA: {yok_url} -> SAYFA VAR dedi (yanlis!)")
            hata += 1
    except Exception as e:
        print(f"  HATA: {yok_url} -> erisilemedi ({e})")
        hata += 1

    # Test 3: Canonical uyusmazligi
    try:
        r = requests.get(f"{BASE}/hizmetler.html", timeout=30)
        cu = canonical_uyusmazligi(r.text, f"{BASE}/hizmetler.html")
        if not cu:
            print(f"  OK: canonical uyumlu (hizmetler.html)")
        else:
            print(f"  UYARI: {cu}")
    except Exception as e:
        print(f"  HATA: canonical testi erisilemedi ({e})")

    print("=" * 78)
    if hata:
        print(f"KALKAN BOZUK — {hata} test basarisiz")
        return 1
    print("KALKAN CALISIYOR — tum testler basarili")
    return 0

def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--tum", action="store_true")
    ap.add_argument("--slug")
    ap.add_argument("--sayfa")
    ap.add_argument("--url", nargs="+")
    ap.add_argument("--yeni", action="store_true")
    ap.add_argument("--kalkan-testi", action="store_true")
    ap.add_argument("-h", "--help", action="store_true")
    a = ap.parse_args()

    if a.kalkan_testi:
        return kalkan_testi()

    if a.help or not any([a.tum, a.slug, a.sayfa, a.url, a.yeni]):
        print(__doc__); return 2

    # --- PARMAK IZI (her modda ilk is) ---
    soft404_parmak_izi()

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
