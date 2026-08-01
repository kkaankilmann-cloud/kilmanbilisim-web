# -*- coding: utf-8 -*-
"""
2. tur duzeltme - kalan sorunlar
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"
toplam = 0

def do_replace(dosya, eski, yeni, context=""):
    global toplam
    if not os.path.exists(dosya):
        return False
    with open(dosya, 'r', encoding='utf-8') as f:
        c = f.read()
    if eski in c:
        c = c.replace(eski, yeni)
        with open(dosya, 'w', encoding='utf-8', newline='') as f:
            f.write(c)
        toplam += 1
        print(f"  DUZELTILDI: {context}")
        return True
    return False

# ============================================================
# 1. TR HUKUK: "Ğustos" -> "Ağustos"
# ============================================================
print("=== TR hukuk Gustos duzeltme ===")
f = os.path.join(bd, "yapay-zeka-ile-hukuk-sozlesme-yonetimi-otomasyonu.html")
c = open(f, 'r', encoding='utf-8').read()
# "1 Ğustos" -> "1 Ağustos"
if "Ğustos" in c:
    c = c.replace("Ğustos", "Ağustos")
    with open(f, 'w', encoding='utf-8', newline='') as fw:
        fw.write(c)
    print("  Gustos->Agustos duzeltildi")
    toplam += 1

# ============================================================
# 2. TR PERAKENDE sayfa: "1 Ağustos" -> "2 Ağustos"
# ============================================================
print("=== TR perakende sayfa ===")
do_replace(
    os.path.join(bd, "yapay-zeka-ile-perakende-sektoru-otomasyonu.html"),
    "1 Ağustos 2026", "2 Ağustos 2026", "TR perakende sayfa"
)

# ============================================================
# 3. TR TARIM sayfa: "1 Ağustos" -> "3 Ağustos"
# ============================================================
print("=== TR tarim sayfa ===")
do_replace(
    os.path.join(bd, "yapay-zeka-ile-tarim-sera-otomasyonu.html"),
    "1 Ağustos 2026", "3 Ağustos 2026", "TR tarim sayfa"
)

# ============================================================
# 4. FR PERAKENDE sayfa: "1 août" -> "2 août"
# ============================================================
print("=== FR perakende sayfa ===")
do_replace(
    os.path.join(bd, "fr", "yapay-zeka-ile-perakende-sektoru-otomasyonu.html"),
    "1 ao\u00fbt 2026", "2 ao\u00fbt 2026", "FR perakende sayfa"
)
do_replace(
    os.path.join(bd, "fr", "yapay-zeka-ile-perakende-sektoru-otomasyonu.html"),
    "1 ao&#251;t 2026", "2 ao&#251;t 2026", "FR perakende sayfa entity"
)

# ============================================================
# 5. FR TARIM sayfa: "1 août" -> "3 août"
# ============================================================
print("=== FR tarim sayfa ===")
do_replace(
    os.path.join(bd, "fr", "yapay-zeka-ile-tarim-sera-otomasyonu.html"),
    "1 ao\u00fbt 2026", "3 ao\u00fbt 2026", "FR tarim sayfa"
)
do_replace(
    os.path.join(bd, "fr", "yapay-zeka-ile-tarim-sera-otomasyonu.html"),
    "1 ao&#251;t 2026", "3 ao&#251;t 2026", "FR tarim sayfa entity"
)

# ============================================================
# 6. KART TARIHLERI - hukuk=1, perakende=2, tarim=3
# Sorun: replace cascade - once hukuk'u duzeltip sonra perakende/tarim
# Kartlarda hepsi ayni tarih olmus - bu demek ki onceki replace'ler
# hukuk kartinin tarihini de perakende/tarim ile birlikte degistirmis
# ============================================================
# Kart tarihlerini SLUG bazli duzeltmem lazim. Slug'u iceren article
# blogundaki tarihi bulmam lazim.
print("\n=== KART TARIHLERI DUZELTME ===")

import re

beklenen_kartlar = {
    'hukuk-sozlesme': {
        '': '1 Ağustos 2026',
        'en': 'August 1, 2026',
        'de': '1. August 2026',
        'es': '1 de agosto de 2026',
        'fr': '1 ao\u00fbt 2026',
    },
    'tarim-sera': {
        '': '3 Ağustos 2026',
        'en': 'August 3, 2026',
        'de': '3. August 2026',
        'es': '3 de agosto de 2026',
        'fr': '3 ao\u00fbt 2026',
    },
}

# RU kartlar entity: hukuk=1, tarim=3
RU_AVGUSTA = "&#1072;&#1074;&#1075;&#1091;&#1089;&#1090;&#1072;"
KO_NYON = "&#45380;"
KO_WOL = "&#50900;"
KO_IL = "&#51068;"
CJK_NIAN = "&#24180;"
CJK_YUE = "&#26376;"
CJK_RI = "&#26085;"

beklenen_kartlar_cjk = {
    'hukuk-sozlesme': {
        'ru': f"1 {RU_AVGUSTA} 2026",
        'ko': f"2026{KO_NYON} 8{KO_WOL} 1{KO_IL}",
        'zh': f"2026{CJK_NIAN}8{CJK_YUE}1{CJK_RI}",
        'ja': f"2026{CJK_NIAN}8{CJK_YUE}1{CJK_RI}",
    },
    'tarim-sera': {
        'ru': f"3 {RU_AVGUSTA} 2026",
        'ko': f"2026{KO_NYON} 8{KO_WOL} 3{KO_IL}",
        'zh': f"2026{CJK_NIAN}8{CJK_YUE}3{CJK_RI}",
        'ja': f"2026{CJK_NIAN}8{CJK_YUE}3{CJK_RI}",
    },
}

# Kartlari slug bazli duzelt
# Her liste sayfasinda ilgili slug'in article blogunu bul,
# icindeki tarihi hedef tarihle degistir
diller_batili = ['', 'en', 'de', 'es', 'fr']
diller_cjk = ['ru', 'ko', 'zh', 'ja']

for slug_kismi, tarihler in beklenen_kartlar.items():
    for dil, hedef in tarihler.items():
        liste = os.path.join(bd, dil, 'index.html') if dil else os.path.join(bd, 'index.html')
        if not os.path.exists(liste):
            continue
        c = open(liste, 'r', encoding='utf-8').read()
        
        # slug'i iceren article blogunu bul
        # <article class="blog-card">...slug...&#128197; TARIH</span>...
        pattern = f'({slug_kismi}[^{{}}]*?&#128197;\\s*)([^<]+?)(<)'
        m = re.search(pattern, c, re.DOTALL)
        if m:
            mevcut = m.group(2).strip()
            if mevcut != hedef:
                c = c[:m.start(2)] + hedef + c[m.end(2):]
                with open(liste, 'w', encoding='utf-8', newline='') as fw:
                    fw.write(c)
                dl = dil if dil else 'tr'
                print(f"  KART {dl} {slug_kismi}: '{mevcut}' -> '{hedef}'")
                toplam += 1

for slug_kismi, tarihler in beklenen_kartlar_cjk.items():
    for dil, hedef in tarihler.items():
        liste = os.path.join(bd, dil, 'index.html')
        if not os.path.exists(liste):
            continue
        c = open(liste, 'r', encoding='utf-8').read()
        
        pattern = f'({slug_kismi}[^{{}}]*?&#128197;\\s*)([^<]+?)(<)'
        m = re.search(pattern, c, re.DOTALL)
        if m:
            mevcut = m.group(2).strip()
            if mevcut != hedef:
                c = c[:m.start(2)] + hedef + c[m.end(2):]
                with open(liste, 'w', encoding='utf-8', newline='') as fw:
                    fw.write(c)
                print(f"  KART {dil} {slug_kismi}: DUZELTILDI")
                toplam += 1

print(f"\nToplam 2. tur duzeltme: {toplam}")
