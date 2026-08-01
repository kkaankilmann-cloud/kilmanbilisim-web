# -*- coding: utf-8 -*-
"""Kart sirasini kontrol et ve yeniden eskiye sirala"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

# TR liste sayfasi
f = os.path.join(bd, 'index.html')
c = open(f, 'r', encoding='utf-8').read()

# Tum article blog-card bloklarini bul
pattern = r'<article\s+class=["\']blog-card["\'].*?</article>'
kartlar = re.findall(pattern, c, re.DOTALL)
print(f'Toplam kart: {len(kartlar)}')

# Ilk 8 kartin slug ve tarihini goster
for i, kart in enumerate(kartlar[:8]):
    slug_m = re.search(r'href=["\'](.*?\.html)', kart)
    tarih_m = re.search(r'&#128197;\s*([^<]+)', kart)
    slug = slug_m.group(1) if slug_m else '?'
    tarih = tarih_m.group(1).strip() if tarih_m else '?'
    print(f'{i+1}. {tarih:25} {slug[:60]}')
