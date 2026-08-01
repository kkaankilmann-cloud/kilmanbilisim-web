# -*- coding: utf-8 -*-
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

for dil in ['', 'en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']:
    if dil:
        f = os.path.join(bd, dil, 'index.html')
    else:
        f = os.path.join(bd, 'index.html')
    c = open(f, 'r', encoding='utf-8').read()
    dl = dil or 'tr'
    
    kartlar = list(re.finditer(
        r'<span class="blog-card-tag">(.*?)</span>\s*<span>(.*?)</span>',
        c, re.DOTALL
    ))
    print(f"\n--- {dl} ({len(kartlar)} kart) ---")
    for i, m in enumerate(kartlar):
        tag = m.group(1)[:50]
        date = m.group(2)[:35]
        print(f'  {i+1:2}. TAG=[{tag}]  DATE=[{date}]')
