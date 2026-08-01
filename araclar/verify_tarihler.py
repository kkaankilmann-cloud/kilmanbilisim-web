# -*- coding: utf-8 -*-
"""Tum sayfa ici ve kart tarihlerini dogrula"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"
slugs = [
    ('chatbot-vs-ai-asistan-isletmeniz-icin-dogru-secim', 'chatbot'),
    ('yapay-zeka-ile-hukuk-sozlesme-yonetimi-otomasyonu', 'hukuk'),
    ('yapay-zeka-ile-perakende-sektoru-otomasyonu', 'perakende'),
    ('yapay-zeka-ile-tarim-sera-otomasyonu', 'tarim'),
]
diller = ['', 'en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']

print("=== SAYFA ICI TARIHLER ===")
for slug, ad in slugs:
    for dil in diller:
        dl = dil if dil else 'tr'
        f = os.path.join(bd, dil, slug+'.html') if dil else os.path.join(bd, slug+'.html')
        if os.path.exists(f):
            c = open(f, 'r', encoding='utf-8').read()
            m = re.findall(r'&#128197;\s*([^<]{5,50})', c)
            tarih = m[0].strip() if m else 'BULUNAMADI'
            print(f"  {dl:3} {ad:12} {tarih}")

print("\n=== KART TARIHLER ===")
for dil in diller:
    dl = dil if dil else 'tr'
    f = os.path.join(bd, dil, 'index.html') if dil else os.path.join(bd, 'index.html')
    if os.path.exists(f):
        c = open(f, 'r', encoding='utf-8').read()
        for slug, ad in slugs:
            # Slug'a yakin olan 128197 tarihini bul
            # Karttaki tarih slug'dan sonra gelir
            idx = c.find(slug[:20])
            if idx >= 0:
                # slug'dan sonraki 128197'yi bul
                after = c[idx:idx+2000]
                m = re.findall(r'&#128197;\s*([^<]{5,50})', after)
                tarih = m[0].strip() if m else 'BULUNAMADI'
                print(f"  {dl:3} {ad:12} {tarih}")

print("\n=== AGUSTOS (g'siz) KONTROLU ===")
for root, dirs, files in os.walk(bd):
    for fn in files:
        if fn.endswith('.html'):
            f = os.path.join(root, fn)
            c = open(f, 'r', encoding='utf-8').read()
            # Agustos ama Ağustos degil
            if 'Agustos' in c and 'Ağustos' not in c:
                print(f"  SORUN: {os.path.relpath(f, bd)}")
            elif 'Agustos' in c:
                # Hem Agustos hem Agustos var mi?
                # Entity olarak da kontrol
                pass
