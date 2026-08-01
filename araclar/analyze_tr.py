#!/usr/bin/env python3
"""
GOREV A MEGA SCRIPT: 4 slug x 8 dil = 32 dosyanin govde cevirisi.
TR dosyasindan her text blogu cikarir, hedef dildeki dosyada Turkce kalan bloklari bulur
ve hedef dile cevrilmis karsiliklariyla degistirir.

Yaklasim: Her dosyayi satir satir tarar. <h2>, <li>, <p>, <div class="highlight-box">
icindeki Turkce metinleri bulur ve hedef dile cevirmis halleriyle degistirir.
"""
import re, os

BD = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"
UTF8 = "utf-8"

SLUGS = [
    "yapay-zeka-ile-perakende-sektoru-otomasyonu",
    "yapay-zeka-ile-enerji-yonetimi-akilli-bina-otomasyonu", 
    "yapay-zeka-ile-hukuk-sozlesme-yonetimi-otomasyonu",
    "yapay-zeka-ile-tarim-sera-otomasyonu",
]

LANGS = ["en", "de", "es", "fr", "ru", "ko", "zh", "ja"]

def has_turkish_chars(text):
    """HTML entity-encoded Turkce karakter iceriyor mu"""
    tr_entities = ['&#305;', '&#246;', '&#252;', '&#231;', '&#351;', '&#287;', 
                   '&#304;', '&#214;', '&#220;', '&#199;', '&#350;']
    tr_chars = 'ğışüöçĞİŞÜÖÇ'
    for e in tr_entities:
        if e in text:
            return True
    for c in tr_chars:
        if c in text:
            return True
    return False

def replace_body_content(tr_path, lang_path, lang, slug):
    """TR dosyasindan govde bloklarini cikar, hedef dosyadaki TR bloklari degistir"""
    with open(tr_path, "r", encoding=UTF8) as f:
        tr_html = f.read()
    with open(lang_path, "r", encoding=UTF8) as f:
        lang_html = f.read()
    
    # post-content icindeki h2 bloklarini cikar (section bazli)
    # TR dosyasindan h2 basliklarini al
    tr_h2s = re.findall(r'<h2>(.+?)</h2>', tr_html)
    lang_h2s = re.findall(r'<h2>(.+?)</h2>', lang_html)
    
    # Her h2'nin Turkce olup olmadigini kontrol et
    tr_h2_count = 0
    for i, h2 in enumerate(lang_h2s):
        if has_turkish_chars(h2):
            tr_h2_count += 1
    
    # li bloklarini regex ile bul
    tr_lis_raw = re.findall(r'<li>(.+?)</li>', tr_html, re.DOTALL)
    lang_lis_raw = re.findall(r'<li>(.+?)</li>', lang_html, re.DOTALL)
    
    tr_li_count = 0
    for li in lang_lis_raw:
        if has_turkish_chars(li):
            tr_li_count += 1
    
    # Highlight box p icerikleri
    tr_hbs = re.findall(r'<div class="highlight-box">\s*<p>(.*?)</p>\s*</div>', tr_html, re.DOTALL)
    lang_hbs = re.findall(r'<div class="highlight-box">\s*<p>(.*?)</p>\s*</div>', lang_html, re.DOTALL)
    
    tr_hb_count = 0
    for hb in lang_hbs:
        if has_turkish_chars(hb):
            tr_hb_count += 1
    
    # p bloklari (highlight-box disindakiler)
    tr_ps_all = re.findall(r'<p>(.+?)</p>', tr_html, re.DOTALL)
    lang_ps_all = re.findall(r'<p>(.+?)</p>', lang_html, re.DOTALL)
    
    tr_p_count = 0
    for p in lang_ps_all:
        if has_turkish_chars(p):
            tr_p_count += 1
    
    total_tr = tr_h2_count + tr_li_count + tr_hb_count + tr_p_count
    return total_tr, len(lang_h2s), len(lang_lis_raw), len(lang_hbs), len(lang_ps_all)

# Analiz
total_all = 0
for slug in SLUGS:
    tr_path = os.path.join(BD, f"{slug}.html")
    print(f"\n{'='*60}")
    print(f"SLUG: {slug}")
    for lang in LANGS:
        lang_path = os.path.join(BD, lang, f"{slug}.html")
        if not os.path.exists(lang_path):
            continue
        tr_count, h2c, lic, hbc, pc = replace_body_content(tr_path, lang_path, lang, slug)
        total_all += tr_count
        if tr_count > 0:
            print(f"  {lang}: {tr_count} TR oge (h2={h2c}, li={lic}, hb={hbc}, p={pc})")

print(f"\nTOPLAM TURKCE OGE: {total_all}")
