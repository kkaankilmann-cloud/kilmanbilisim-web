#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOREV A: 32 dosya govde cevirisi - index bazli degistirme.
Her dosyadaki <main class="post-content"> icerisindeki h2, li, p ogelerini 
sirayla bulur ve hedef dildeki cevirileriyle degistirir.

Strateji: TR dosyasindaki ogelerin sira numaralarini kullanarak
hedef dosyadaki ayni siradaki ogeleri hedef dildeki cevirilerle degistirir.
"""
import re, os, sys

BD = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"
LANGS = ["en", "de", "es", "fr", "ru", "ko", "zh", "ja"]

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

def get_main_content(html):
    """<main class="post-content"> ile </main> arasindaki icerigi dondur"""
    m = re.search(r'<main\s+class="post-content">(.*?)</main>', html, re.DOTALL)
    if m:
        return m.group(1), m.start(1), m.end(1)
    return None, 0, 0

def replace_elements_by_index(html, tag_pattern, translations, main_start, main_end):
    """main icerisindeki tag_pattern ile eslesen ogeleri sirayla degistirir"""
    main_content = html[main_start:main_end]
    matches = list(re.finditer(tag_pattern, main_content, re.DOTALL))
    
    if len(matches) != len(translations):
        return html, False, len(matches)
    
    # Sondan basa degistir
    for m, t in reversed(list(zip(matches, translations))):
        abs_start = main_start + m.start(1)
        abs_end = main_start + m.end(1)
        html = html[:abs_start] + t + html[abs_end:]
        # main_end'i guncelle
        main_end += len(t) - (abs_end - abs_start)
    
    return html, True, len(matches)

# Ceviriler dosyadan yuklenecek - burada inline tanimliyorum
# Her slug icin ayri fonksiyon

def process_slug(slug, h2_trans, li_trans, p_trans, hb_trans=None):
    """Bir slug'in 8 dilini isle"""
    print(f"\n{'='*60}")
    print(f"SLUG: {slug}")
    
    tr_path = os.path.join(BD, f"{slug}.html")
    tr_html = read_file(tr_path)
    
    tr_main, tr_ms, tr_me = get_main_content(tr_html)
    if not tr_main:
        print("  HATA: TR dosyasinda <main> bulunamadi!")
        return
    
    # TR h2, li, p sayilarini kontrol et
    tr_h2_count = len(re.findall(r'<h2>(.+?)</h2>', tr_main, re.DOTALL))
    tr_li_count = len(re.findall(r'<li>(.+?)</li>', tr_main, re.DOTALL))
    # p: highlight-box icindekiler dahil
    tr_p_raw = re.findall(r'<p>(.+?)</p>', tr_main, re.DOTALL)
    # p icinden class'li olanlari da say
    tr_p_cls = re.findall(r'<p [^>]*>(.+?)</p>', tr_main, re.DOTALL)
    
    print(f"  TR: h2={tr_h2_count}, li={tr_li_count}, p_raw={len(tr_p_raw)}, p_cls={len(tr_p_cls)}")
    
    for lang in LANGS:
        if lang not in h2_trans:
            print(f"  {lang}: CEVIRI YOK, atlanıyor")
            continue
            
        lang_path = os.path.join(BD, lang, f"{slug}.html")
        if not os.path.exists(lang_path):
            print(f"  {lang}: DOSYA YOK!")
            continue
        
        html = read_file(lang_path)
        main_content, ms, me = get_main_content(html)
        if not main_content:
            print(f"  {lang}: <main> bulunamadi!")
            continue
        
        # H2 degistir
        h2s = h2_trans[lang]
        html, ok, count = replace_elements_by_index(html, r'<h2>(.+?)</h2>', h2s, ms, me)
        if not ok:
            print(f"  {lang}: H2 SAYISI UYUSMUYOR (dosyada {count}, ceviride {len(h2s)})")
        
        # main_content guncelle
        main_content, ms, me = get_main_content(html)
        
        # LI degistir
        lis = li_trans[lang]
        html, ok, count = replace_elements_by_index(html, r'<li>(.+?)</li>', lis, ms, me)
        if not ok:
            print(f"  {lang}: LI SAYISI UYUSMUYOR (dosyada {count}, ceviride {len(lis)})")
        
        # main_content guncelle
        main_content, ms, me = get_main_content(html)
        
        # P degistir - sadece <p> (class'siz)
        ps = p_trans[lang]
        html, ok, count = replace_elements_by_index(html, r'<p>(.+?)</p>', ps, ms, me)
        if not ok:
            print(f"  {lang}: P SAYISI UYUSMUYOR (dosyada {count}, ceviride {len(ps)})")
        
        write_file(lang_path, html)
        
        # Dogrulama: Turkce karakter iceren h2 kaldi mi?
        new_main, _, _ = get_main_content(html)
        remaining_tr = 0
        tr_entities = ['&#305;', '&#246;', '&#252;', '&#231;', '&#351;', '&#287;']
        for h2 in re.findall(r'<h2>(.+?)</h2>', new_main):
            if any(e in h2 for e in tr_entities):
                remaining_tr += 1
        
        print(f"  {lang}: OK (kalan TR h2: {remaining_tr})")

# Test: sadece h2 ile perakende
print("PERAKENDE H2 TEST")
print("Script calistirildi - simdi cevirileri yukle ve isle")
