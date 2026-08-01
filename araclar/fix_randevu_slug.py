# -*- coding: utf-8 -*-
"""
Randevu karti duzeltme — SLUG BAZLI
Her dilde:
1. randevu-rezervasyon slug'ini iceren article blogu bul
2. O article icindeki blog-card-meta div'ini komple degistir
3. Kartlar arasindaki basibos metni temizle
4. Dogrula
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"
slug = 'yapay-zeka-ile-randevu-rezervasyon-otomasyonu'

# Her dil icin DOGRU meta
meta_dogru = {
    '':   ('&#128197;&#65039; Randevu Y&#246;netimi',            '&#128197; 19 Temmuz 2026'),
    'en': ('&#128197;&#65039; Appointment Management',           '&#128197; July 19, 2026'),
    'de': ('&#128197;&#65039; Terminverwaltung',                 '&#128197; 19. Juli 2026'),
    'es': ('&#128197;&#65039; Gesti&#243;n de Citas',            '&#128197; 19 de julio de 2026'),
    'fr': ('&#128197;&#65039; Gestion de Rendez-vous',           '&#128197; 19 juillet 2026'),
    'ru': ('&#128197;&#65039; &#1059;&#1087;&#1088;&#1072;&#1074;&#1083;&#1077;&#1085;&#1080;&#1077; &#1079;&#1072;&#1087;&#1080;&#1089;&#1103;&#1084;&#1080;', '&#128197; 19 &#1080;&#1102;&#1083;&#1103; 2026'),
    'ko': ('&#128197;&#65039; &#50696;&#50557; &#44288;&#47532;', '&#128197; 2026&#45380; 7&#50900; 19&#51068;'),
    'zh': ('&#128197;&#65039; &#39044;&#32422;&#31649;&#29702;',  '&#128197; 2026&#24180;7&#26376;19&#26085;'),
    'ja': ('&#128197;&#65039; &#20104;&#32004;&#31649;&#29702;',  '&#128197; 2026&#24180;7&#26376;19&#26085;'),
}

# Okuma bilgisi icin
okuma_suresi = {
    '':   '&#9201;&#65039; 9 dk okuma',
    'en': '&#9201;&#65039; 9 min read',
    'de': '&#9201;&#65039; 9 Min. Lesezeit',
    'es': '&#9201;&#65039; 9 min de lectura',
    'fr': '&#9201;&#65039; 9 min de lecture',
    'ru': '&#9201;&#65039; 9 &#1084;&#1080;&#1085; &#1095;&#1090;&#1077;&#1085;&#1080;&#1103;',
    'ko': '&#9201;&#65039; 9&#48516; &#51069;&#44592;',
    'zh': '&#9201;&#65039; 9&#20998;&#38047;&#38405;&#35835;',
    'ja': '&#9201;&#65039; 9&#20998;&#38291;&#35501;&#12415;',
}

degisiklik = 0

for dil, (dogru_tag, dogru_tarih) in meta_dogru.items():
    if dil:
        f = os.path.join(bd, dil, 'index.html')
    else:
        f = os.path.join(bd, 'index.html')
    
    dl = dil or 'tr'
    
    if not os.path.exists(f):
        print(f"  {dl}: dosya yok!")
        continue
    
    c = open(f, 'r', encoding='utf-8').read()
    
    # 1. Basibos metin temizle: </article> ve <article arasinda metin
    c = re.sub(r'(</article>)\s*([^<\s][^<]{2,200}?)\s*(<article)', r'\1\n  \3', c)
    
    # 2. Randevu article blogunu slug ile bul
    # Slug iceren href'i arayalim
    if dil:
        href_pattern = f'/blog/{dil}/{slug}.html'
    else:
        href_pattern = f'/blog/{slug}.html'
    
    # Article blogunu bul — slug'i iceren tum article'i yakala
    article_pattern = r'(<article class="blog-card">\s*\n\s*<div class="blog-card-meta">\s*\n\s*)<span class="blog-card-tag">(.*?)</span>\s*\n\s*<span>(.*?)</span>\s*\n\s*<span>(.*?)</span>(\s*\n\s*</div>\s*\n\s*<h2><a href="' + re.escape(href_pattern) + r'")'
    
    m = re.search(article_pattern, c)
    if m:
        eski_tag = m.group(2)
        eski_tarih = m.group(3)
        eski_okuma = m.group(4)
        
        print(f"  {dl}: MEVCUT tag=[{eski_tag[:50]}]")
        print(f"       MEVCUT tarih=[{eski_tarih[:40]}]")
        
        # Okuma suresi kalsin ama biz de dogru olanini koyalim
        okuma = eski_okuma  # mevcut okuma suresini koru
        
        # Yeni meta bloku
        yeni = (f'<span class="blog-card-tag">{dogru_tag}</span>\n'
                f'      <span>{dogru_tarih}</span>\n'
                f'      <span>{okuma}</span>')
        
        # Eski meta blogunu degistir
        eski = f'<span class="blog-card-tag">{eski_tag}</span>\n      <span>{eski_tarih}</span>\n      <span>{eski_okuma}</span>'
        
        # Replace: m.group(1) + yeni + m.group(5)
        yeni_article = m.group(1) + yeni + m.group(5)
        c = c[:m.start()] + yeni_article + c[m.end():]
        
        print(f"  {dl}: DUZELTILDI tag=[{dogru_tag[:50]}]")
        print(f"       tarih=[{dogru_tarih[:40]}]")
        degisiklik += 1
    else:
        print(f"  {dl}: RANDEVU KARTI BULUNAMADI — elle kontrol!")
    
    with open(f, 'w', encoding='utf-8', newline='') as fw:
        fw.write(c)

print(f"\nToplam degisiklik: {degisiklik}")

# 3. Dogrulama
print("\n=== DOGRULAMA ===")
sorun = 0
for dil in ['', 'en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']:
    if dil:
        f = os.path.join(bd, dil, 'index.html')
    else:
        f = os.path.join(bd, 'index.html')
    c = open(f, 'r', encoding='utf-8').read()
    dl = dil or 'tr'
    
    # Basibos metin
    basibos = re.findall(r'</article>\s*([^<\s][^<]{2,140}?)\s*<article', c)
    if basibos:
        for b in basibos:
            print(f"  {dl}: BASIBOS: [{b[:60]}]")
            sorun += 1
    
    # Randevu kartinin tagi
    if dil:
        href = f'/blog/{dil}/{slug}.html'
    else:
        href = f'/blog/{slug}.html'
    
    kart_p = r'<span class="blog-card-tag">(.*?)</span>\s*<span>(.*?)</span>.*?' + re.escape(href)
    km = re.search(kart_p, c, re.DOTALL)
    if km:
        tag = km.group(1)[:50]
        tarih = km.group(2)[:40]
        # Tag'da tarih var mi kontrol (YANLIS)
        if '2026' in tag:
            print(f"  {dl}: HATA — TAG'da tarih var: [{tag}]")
            sorun += 1
        else:
            print(f"  {dl}: OK tag=[{tag[:30]}] tarih=[{tarih[:30]}]")

print(f"\nToplam sorun: {sorun}")
