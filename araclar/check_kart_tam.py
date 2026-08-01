# -*- coding: utf-8 -*-
"""Tum 34 kartin slug + tarih + JSON-LD tarihini kontrol et"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

f = os.path.join(bd, 'index.html')
c = open(f, 'r', encoding='utf-8').read()

# Tum article blog-card bloklarini bul
pattern = r'<article\s+class=["\']blog-card["\'].*?</article>'
kartlar = re.findall(pattern, c, re.DOTALL)

print(f"Toplam kart: {len(kartlar)}")
print(f"{'#':>3} {'KART_TARIH':25} {'SLUG':60}")
print("-" * 90)

for i, kart in enumerate(kartlar):
    slug_m = re.search(r'href=["\']([^"\']+\.html)', kart)
    tarih_m = re.search(r'&#128197;\s*([^<]+)', kart)
    slug = slug_m.group(1).strip() if slug_m else '?'
    tarih = tarih_m.group(1).strip() if tarih_m else '?'
    
    # JSON-LD tarihini de kontrol et (yazi sayfasindan)
    slug_dosya = slug.replace('/blog/', '')
    yazi_f = os.path.join(bd, slug_dosya)
    jsonld_tarih = '?'
    if os.path.exists(yazi_f):
        yazi_c = open(yazi_f, 'r', encoding='utf-8').read()
        m = re.search(r'datePublished.*?(20\d{2}-\d{2}-\d{2})', yazi_c)
        if m:
            jsonld_tarih = m.group(1)
    
    uyumsuz = ""
    # Basit karsilastirma: JSON-LD tarihi ile kart tarihindeki gun/ay eslessin
    print(f"{i+1:>3} {tarih:25} {slug[:55]:55} JLD:{jsonld_tarih}")

# Ayrica: enerji kartinin tarihini detayli kontrol
print("\n=== ENERJI KART DETAY ===")
for kart in kartlar:
    if 'enerji-yonetimi' in kart:
        tarih_m = re.search(r'&#128197;\s*([^<]+)', kart)
        print(f"Enerji kart tarih: {tarih_m.group(1).strip() if tarih_m else '?'}")
        break
