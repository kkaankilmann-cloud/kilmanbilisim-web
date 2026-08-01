# -*- coding: utf-8 -*-
"""
Glow CSS duzeltme - tum HTML dosyalarinda:
1. box-shadow: inset 0 0 130px ... -> 24px/8px
2. opacity: .55 -> 0 (tam sonme)
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files"

# Eski ve yeni degerler
eski_shadow_patterns = [
    r'box-shadow:\s*inset\s+0\s+0\s+130px\s+rgba\(0,\s*212,\s*255,\s*\.?\d+\),\s*inset\s+0\s+0\s+40px\s+rgba\(0,\s*212,\s*255,\s*\.?\d+\);',
]
yeni_shadow = 'box-shadow: inset 0 0 24px rgba(0,212,255,.55), inset 0 0 8px rgba(0,212,255,.35);'

eski_opacity_patterns = [
    r"0%,\s*100%\s*\{\s*opacity:\s*\.55\s*\}",
]
yeni_opacity = "0%,100% { opacity: 0 }"

dosya_sayisi = 0
degisiklik = 0

for root, dirs, files in os.walk(bd):
    for fn in files:
        if not fn.endswith('.html'):
            continue
        f = os.path.join(root, fn)
        c = open(f, 'r', encoding='utf-8').read()
        
        yeni_c = c
        
        # box-shadow degistir
        for pattern in eski_shadow_patterns:
            yeni_c = re.sub(pattern, yeni_shadow, yeni_c)
        
        # opacity degistir
        for pattern in eski_opacity_patterns:
            yeni_c = re.sub(pattern, yeni_opacity, yeni_c)
        
        if yeni_c != c:
            with open(f, 'w', encoding='utf-8', newline='') as fw:
                fw.write(yeni_c)
            degisiklik += 1
            rel = os.path.relpath(f, bd)
        
        dosya_sayisi += 1

print(f"Taranan: {dosya_sayisi} dosya")
print(f"Degisiklik: {degisiklik} dosya")

# Dogrulama: index.html'deki yeni degerleri goster
idx = os.path.join(bd, 'index.html')
c = open(idx, 'r', encoding='utf-8').read()
m1 = re.search(r'box-shadow:[^;]+;', c)
m2 = re.search(r'0%.*?opacity:[^}]+', c)
if m1:
    print(f"\nindex.html box-shadow: {m1.group()}")
if m2:
    print(f"index.html opacity: {m2.group()}")
