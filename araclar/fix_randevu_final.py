# -*- coding: utf-8 -*-
"""
Randevu karti duzeltme — 8 dil (TR zaten elle duzeltildi)
1. Kartlar arasindaki basiboş metni temizle
2. blog-card-meta div'ini komple yeniden yaz
3. Dogrula: </article> ile <article arasinda metin yok
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

slug = 'yapay-zeka-ile-randevu-rezervasyon-otomasyonu'

# Dogru meta blogu — her dil icin
dil_meta = {
    'en': {
        'tag': '&#128197;&#65039; Appointment Management',
        'tarih': '&#128197; July 19, 2026',
    },
    'de': {
        'tag': '&#128197;&#65039; Terminverwaltung',
        'tarih': '&#128197; 19. Juli 2026',
    },
    'es': {
        'tag': '&#128197;&#65039; Gesti&#243;n de Citas',
        'tarih': '&#128197; 19 de julio de 2026',
    },
    'fr': {
        'tag': '&#128197;&#65039; Gestion de Rendez-vous',
        'tarih': '&#128197; 19 juillet 2026',
    },
    'ru': {
        'tag': '&#128197;&#65039; &#1059;&#1087;&#1088;&#1072;&#1074;&#1083;&#1077;&#1085;&#1080;&#1077; &#1079;&#1072;&#1087;&#1080;&#1089;&#1103;&#1084;&#1080;',
        'tarih': '&#128197; 19 &#1080;&#1102;&#1083;&#1103; 2026',
    },
    'ko': {
        'tag': '&#128197;&#65039; &#50696;&#50557; &#44288;&#47532;',
        'tarih': '&#128197; 2026&#45380; 7&#50900; 19&#51068;',
    },
    'zh': {
        'tag': '&#128197;&#65039; &#39044;&#32422;&#31649;&#29702;',
        'tarih': '&#128197; 2026&#24180;7&#26376;19&#26085;',
    },
    'ja': {
        'tag': '&#128197;&#65039; &#20104;&#32004;&#31649;&#29702;',
        'tarih': '&#128197; 2026&#24180;7&#26376;19&#26085;',
    },
}

for dil, meta in dil_meta.items():
    f = os.path.join(bd, dil, 'index.html')
    if not os.path.exists(f):
        print(f"  {dil}: dosya yok!")
        continue
    
    c = open(f, 'r', encoding='utf-8').read()
    
    # 1. Basiboş metin temizle: </article> ile <article arasinda
    # Tum basibos metinleri temizle (sadece randevu degil, hepsini)
    c_temiz = re.sub(r'(</article>)\s*\n?\s*([^<\s][^<]*?)(<article)', r'\1\n  \3', c)
    if c_temiz != c:
        print(f"  {dil}: basiboş metin temizlendi")
    c = c_temiz
    
    # 2. Randevu kartinin blog-card-meta div'ini bul ve komple degistir
    # Randevu kartini slug ile bul
    slug_pattern = re.escape(slug)
    kart_pattern = r'(<article\s+class="blog-card">\s*\n\s*<div class="blog-card-meta">\s*\n\s*<span class="blog-card-tag">)(.*?)(</span>\s*\n\s*<span>)(.*?)(</span>\s*\n\s*<span>.*?</span>\s*\n\s*</div>\s*\n\s*<h2><a href="/blog/' + re.escape(dil) + '/' + slug_pattern + r'\.html")'
    
    m = re.search(kart_pattern, c, re.DOTALL)
    if m:
        eski_tag = m.group(2)
        eski_tarih = m.group(4)
        print(f"  {dil}: MEVCUT tag=[{eski_tag[:40]}] tarih=[{eski_tarih[:40]}]")
        
        # Komple degistir
        c = c[:m.start(2)] + meta['tag'] + c[m.end(2):m.start(4)] + meta['tarih'] + c[m.end(4):]
        print(f"  {dil}: YENİ   tag=[{meta['tag'][:40]}] tarih=[{meta['tarih'][:40]}]")
    else:
        print(f"  {dil}: RANDEVU KARTI BULUNAMADI — elle kontrol gerekli!")
    
    with open(f, 'w', encoding='utf-8', newline='') as fw:
        fw.write(c)

# 3. Dogrulama: hicbir liste sayfasinda basibos metin kalmamali
print("\n=== DOGRULAMA: basibos metin kontrolu ===")
sorun = 0
for dil in ['', 'en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']:
    if dil:
        f = os.path.join(bd, dil, 'index.html')
    else:
        f = os.path.join(bd, 'index.html')
    c = open(f, 'r', encoding='utf-8').read()
    basibos = re.findall(r'</article>\s*([^<\s][^<]{2,140}?)\s*<article', c)
    dl = dil or 'tr'
    if basibos:
        for b in basibos:
            print(f"  {dl}: BASIBOS METIN: [{b[:60]}]")
            sorun += 1
    else:
        print(f"  {dl}: temiz")

print(f"\nToplam basibos metin sorun: {sorun}")
