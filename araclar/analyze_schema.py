# -*- coding: utf-8 -*-
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')

f = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\index.html"
c = open(f, 'r', encoding='utf-8').read()

# JSON-LD blokları bul
bloklar = re.findall(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', c, re.DOTALL | re.IGNORECASE)
print(f"JSON-LD blok sayisi: {len(bloklar)}")
for i, b in enumerate(bloklar):
    try:
        d = json.loads(b)
        t = d.get('@type', '?')
        print(f"\n  Blok {i+1}: @type={t}")
        if isinstance(d, dict):
            for k in d.keys():
                print(f"    {k}")
    except:
        print(f"\n  Blok {i+1}: JSON parse hatasi! ilk 200: {b[:200]}")

# FAQPage arama
faq_count = len(re.findall(r'FAQPage', c))
print(f"\nFAQPage gecme: {faq_count}")

# Service arama
serv = re.findall(r'serviceType', c)
print(f"serviceType gecme: {len(serv)}")

# page-solutions arama
sols = re.findall(r'page-solutions', c)
print(f"page-solutions gecme: {len(sols)}")

# SSS / FAQ section
sss = re.findall(r'faq|sss|page-faq', c, re.IGNORECASE)
print(f"faq/sss gecme: {len(sss)}")

# translations objesi
trans = re.findall(r'translations\s*=', c)
print(f"translations= gecme: {len(trans)}")
