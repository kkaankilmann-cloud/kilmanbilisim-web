# -*- coding: utf-8 -*-
"""
Randevu karti kategori simgesi degistir:
U+1F4C5 (&#128197;) -> U+1F5D3 (&#128467;) — sadece blog-card-tag ve post-tag icinde
Slug bazli eslestirme. Tarih simgesi degismeyecek.
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"
slug = 'yapay-zeka-ile-randevu-rezervasyon-otomasyonu'

degisiklik = 0

# 1. Liste sayfalari — blog-card-tag icindeki simge
for dil in ['', 'en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']:
    if dil:
        f = os.path.join(bd, dil, 'index.html')
    else:
        f = os.path.join(bd, 'index.html')
    dl = dil or 'tr'
    
    if not os.path.exists(f):
        print(f"  {dl}: dosya yok!")
        continue
    
    c = open(f, 'r', encoding='utf-8').read()
    
    # Randevu kartini slug ile bul
    if dil:
        href = f'/blog/{dil}/{slug}.html'
    else:
        href = f'/blog/{slug}.html'
    
    # article blogu icinde blog-card-tag bul
    pattern = r'(<span class="blog-card-tag">)(&#128197;&#65039;)(.*?</span>.*?' + re.escape(href) + r')'
    m = re.search(pattern, c, re.DOTALL)
    if m:
        # Sadece bu kartın tag simgesini degistir
        c = c[:m.start(2)] + '&#128467;&#65039;' + c[m.end(2):]
        print(f"  {dl} liste: &#128197; -> &#128467; (blog-card-tag)")
        degisiklik += 1
    else:
        # UTF-8 emoji olabilir
        pattern2 = r'(<span class="blog-card-tag">)(\U0001F4C5\uFE0F|\U0001F4C5)(.*?' + re.escape(href) + r')'
        m2 = re.search(pattern2, c, re.DOTALL)
        if m2:
            c = c[:m2.start(2)] + '\U0001F5D3\uFE0F' + c[m2.end(2):]
            print(f"  {dl} liste: UTF8 1F4C5 -> 1F5D3 (blog-card-tag)")
            degisiklik += 1
        else:
            print(f"  {dl} liste: BULUNAMADI")
    
    with open(f, 'w', encoding='utf-8', newline='') as fw:
        fw.write(c)

# 2. Yazi sayfalari — post-tag icindeki simge
for dil in ['', 'en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']:
    if dil:
        f = os.path.join(bd, dil, f'{slug}.html')
    else:
        f = os.path.join(bd, f'{slug}.html')
    dl = dil or 'tr'
    
    if not os.path.exists(f):
        continue
    
    c = open(f, 'r', encoding='utf-8').read()
    
    # post-tag span icindeki simge
    pattern = r'(<span class="post-tag">)(&#128197;&#65039;|&#128197;)'
    m = re.search(pattern, c)
    if m:
        c = c[:m.start(2)] + '&#128467;&#65039;' + c[m.end(2):]
        print(f"  {dl} yazi:  &#128197; -> &#128467; (post-tag)")
        degisiklik += 1
    else:
        # UTF-8
        pattern2 = r'(<span class="post-tag">)(\U0001F4C5\uFE0F|\U0001F4C5)'
        m2 = re.search(pattern2, c)
        if m2:
            c = c[:m2.start(2)] + '\U0001F5D3\uFE0F' + c[m2.end(2):]
            print(f"  {dl} yazi:  UTF8 1F4C5 -> 1F5D3 (post-tag)")
            degisiklik += 1
    
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
    dl = dil or 'tr'
    c = open(f, 'r', encoding='utf-8').read()
    
    if dil:
        href = f'/blog/{dil}/{slug}.html'
    else:
        href = f'/blog/{slug}.html'
    
    # Randevu kartinin tag simgesi
    p = r'<span class="blog-card-tag">(.*?)</span>.*?' + re.escape(href)
    m = re.search(p, c, re.DOTALL)
    if m:
        tag = m.group(1)[:60]
        if '&#128467;' in tag or '\U0001F5D3' in tag:
            print(f"  {dl}: OK (U+1F5D3) [{tag[:40]}]")
        elif '&#128197;' in tag or '\U0001F4C5' in tag:
            print(f"  {dl}: HATA — hala U+1F4C5! [{tag[:40]}]")
            sorun += 1
        else:
            print(f"  {dl}: BELIRSIZ [{tag[:40]}]")

# Basibos metin kontrolu
for dil in ['', 'en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']:
    if dil:
        f = os.path.join(bd, dil, 'index.html')
    else:
        f = os.path.join(bd, 'index.html')
    dl = dil or 'tr'
    c = open(f, 'r', encoding='utf-8').read()
    basibos = re.findall(r'</article>\s*([^<\s][^<]{2,140}?)\s*<article', c)
    if basibos:
        for b in basibos:
            print(f"  {dl}: BASIBOS: [{b[:60]}]")
            sorun += 1

print(f"\nToplam sorun: {sorun}")
