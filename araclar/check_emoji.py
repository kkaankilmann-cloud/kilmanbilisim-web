# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

f = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog\index.html"
c = open(f, 'r', encoding='utf-8').read()

e1 = c.count('&#128197;')
e2 = c.count('\U0001F4C5')
print(f"Entity &#128197;: {e1}")
print(f"UTF-8 \U0001F4C5: {e2}")

# blog-card pattern
pattern = r'<article\s+class=["\']blog-card["\']'
kartlar = re.findall(pattern, c)
print(f"blog-card sayisi: {len(kartlar)}")

# Baska card pattern var mi?
pattern2 = r'<article'
kartlar2 = re.findall(pattern2, c)
print(f"article sayisi: {len(kartlar2)}")

# Ilk 200 karakteri goster
idx = c.find('<article')
if idx >= 0:
    print(f"\nIlk article: {repr(c[idx:idx+200])}")
