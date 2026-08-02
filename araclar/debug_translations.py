# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
f = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\index.html"
c = open(f, 'r', encoding='utf-8').read()

# translations objesini bul
m = re.search(r'const translations\s*=\s*\{', c)
if m:
    print(f"translations objesi satirda: {c[:m.start()].count(chr(10))+1}")
    # Her dil blogu icin faq_ anahtarlarini say
    blok = c[m.start():]
    diller = re.findall(r"(\w{2}):\s*\{", blok[:500])
    print(f"Diller: {diller}")
    
    for dil in ['tr', 'en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']:
        faq_q = len(re.findall(r"faq_q\d+", blok))
        break
    
    # TR blogunun faq anahtarlarini listele
    tr_match = re.search(r"tr:\s*\{(.*?)\n\s{4}\}", blok, re.DOTALL)
    if tr_match:
        tr_block = tr_match.group(1)
        faq_keys = sorted(set(re.findall(r"(faq_[qa]\d+)", tr_block)))
        print(f"\nTR faq anahtarlari ({len(faq_keys)}):")
        for k in faq_keys:
            print(f"  {k}")
        
        sol_keys = sorted(set(re.findall(r"(sol\d+_\w+)", tr_block)))
        print(f"\nTR sol anahtarlari ({len(sol_keys)}):")
        for k in sol_keys:
            print(f"  {k}")
    
    # translations satir numarasini bul
    lines = c.split('\n')
    for i, line in enumerate(lines):
        if 'const translations' in line:
            print(f"\ntranslations satiri: {i+1}")
            break
else:
    print("translations bulunamadi")
