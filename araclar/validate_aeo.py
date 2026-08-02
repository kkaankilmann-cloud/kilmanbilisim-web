# -*- coding: utf-8 -*-
"""Commit oncesi dogrulama: JSON-LD parse + sayim + kodlama kontrolu"""
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

f = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\index.html"
c = open(f, 'r', encoding='utf-8').read()

sorun = 0

# 1. JSON-LD blokları parse
print("=== JSON-LD PARSE ===")
bloklar = re.findall(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', c, re.DOTALL | re.IGNORECASE)
print(f"  Blok sayisi: {len(bloklar)}")
for i, b in enumerate(bloklar):
    try:
        d = json.loads(b)
        if isinstance(d, list):
            t = f"Array({len(d)} eleman)"
        else:
            t = d.get('@type', '?')
        print(f"  Blok {i+1}: {t} — OK")
    except json.JSONDecodeError as e:
        print(f"  Blok {i+1}: JSON PARSE HATASI! {e}")
        sorun += 1

# 2. knowsAbout sayimi
print("\n=== knowsAbout ===")
knows_count = c.count('"knowsAbout"')
print(f"  knowsAbout gecme: {knows_count} (beklenen: 2 — Organization + LocalBusiness)")
if knows_count != 2:
    sorun += 1

# 3. Service sayimi
print("\n=== Service ===")
service_count = c.count('"serviceType"')
print(f"  serviceType gecme: {service_count} (beklenen: 11)")
if service_count != 11:
    sorun += 1

# 4. FAQPage mainEntity sayimi
print("\n=== FAQPage ===")
faq_schema = [b for b in bloklar if 'FAQPage' in b]
if faq_schema:
    d = json.loads(faq_schema[0])
    q_count = len(d.get('mainEntity', []))
    print(f"  mainEntity soru sayisi: {q_count} (beklenen: 11)")
    if q_count != 11:
        sorun += 1
else:
    print("  FAQPage BULUNAMADI!")
    sorun += 1

# 5. Gorünen FAQ sayisi
print("\n=== Gorunen FAQ ===")
faq_items = re.findall(r'class="faq-item"', c)
print(f"  faq-item sayisi: {len(faq_items)} (beklenen: 11)")
if len(faq_items) != 11:
    sorun += 1

# 6. Hizmet karti sayisi (gorunen + gizli)
print("\n=== Hizmet Kartlari ===")
sol_titles = re.findall(r'data-i18n="sol\d+_title"', c)
print(f"  Kart sayisi: {len(sol_titles)} (beklenen: 12 — 8 eski + 4 yeni)")
if len(sol_titles) != 12:
    sorun += 1

# 7. Translations dogrulamasi
print("\n=== Translations ===")
for key in ['faq_q7', 'faq_a11', 'sol9_title', 'sol12_desc']:
    count = c.count(key + ':')
    print(f"  {key}: {count}x (beklenen: 9)")
    if count != 9:
        sorun += 1

# 8. Kodlama kontrolu (CP857 bozuk karakter)
print("\n=== Kodlama ===")
bozuk = ['├', '─', '╝', 'º', 'ª', 'Ò', 'Õ', 'Ù', 'Ô']
bozuk_bulundu = []
for ch in bozuk:
    if ch in c:
        bozuk_bulundu.append(ch)
if bozuk_bulundu:
    print(f"  BOZUK KARAKTER: {bozuk_bulundu}")
    sorun += 1
else:
    print("  Bozuk karakter YOK — OK")

# 9. Surrogate pair kontrolu
print("\n=== Surrogate Pair ===")
surrogates = re.findall(r'&#5535[0-9];', c)
if surrogates:
    print(f"  SURROGATE PAIR BULUNDU: {surrogates[:5]}")
    sorun += 1
else:
    print("  Surrogate pair YOK — OK")

print(f"\n{'='*50}")
print(f"SONUC: {'TEMIZ — commit atilabilir' if sorun == 0 else f'{sorun} SORUN VAR — duzelt!'}")
