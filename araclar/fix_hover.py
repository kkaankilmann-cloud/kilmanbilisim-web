# -*- coding: utf-8 -*-
"""
Hover beyaz parlama duzeltme:
.btn-primary:hover  background: #fff -> #66E5FF, glow kucultme
.nav-wa-btn:hover   background: #fff -> #66E5FF, glow kucultme
Tum HTML dosyalarinda.
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files"

degisiklik = 0
dosya_sayisi = 0

for root, dirs, files in os.walk(bd):
    for fn in files:
        if not fn.endswith('.html'):
            continue
        f = os.path.join(root, fn)
        c = open(f, 'r', encoding='utf-8').read()
        yeni = c
        
        # .btn-primary:hover { background: #fff; ... }
        # Cesitli formatlar olabilir
        yeni = re.sub(
            r'(\.btn-primary:hover\s*\{[^}]*?)background:\s*#fff\s*;',
            r'\1background: #66E5FF;',
            yeni
        )
        yeni = re.sub(
            r'(\.btn-primary:hover\s*\{[^}]*?)box-shadow:\s*var\(--neon-glow\)\s*;',
            r'\1box-shadow: 0 0 12px rgba(0,212,255,.45);',
            yeni
        )
        
        # .nav-wa-btn:hover { background: #fff; ... }
        yeni = re.sub(
            r'(\.nav-wa-btn:hover\s*\{[^}]*?)background:\s*#fff\s*;',
            r'\1background: #66E5FF;',
            yeni
        )
        yeni = re.sub(
            r'(\.nav-wa-btn:hover\s*\{[^}]*?)box-shadow:\s*var\(--neon-glow\)\s*;',
            r'\1box-shadow: 0 0 12px rgba(0,212,255,.45);',
            yeni
        )
        
        if yeni != c:
            with open(f, 'w', encoding='utf-8', newline='') as fw:
                fw.write(yeni)
            degisiklik += 1
        
        dosya_sayisi += 1

print(f"Taranan: {dosya_sayisi} dosya")
print(f"Degisiklik: {degisiklik} dosya")

# Dogrulama
idx = os.path.join(bd, 'index.html')
c = open(idx, 'r', encoding='utf-8').read()
m1 = re.search(r'\.btn-primary:hover\s*\{[^}]+\}', c)
m2 = re.search(r'\.nav-wa-btn:hover\s*\{[^}]+\}', c)
if m1: print(f"\nindex.html: {m1.group()}")
if m2: print(f"index.html: {m2.group()}")
