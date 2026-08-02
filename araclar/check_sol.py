# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
f = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\index.html"
c = open(f, 'r', encoding='utf-8').read()
m = re.findall(r'data-i18n="(sol\d+_title)"', c)
print(f"Toplam: {len(m)}")
for x in m:
    print(f"  {x}")
