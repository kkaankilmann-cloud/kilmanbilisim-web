# -*- coding: utf-8 -*-
"""
TUM yazi sayfalarinin sayfa ici tarihlerini JSON-LD referansiyla kontrol et
Sadece 4 hedef yazi degil, 34 yazinin hepsini tara
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

ay_isimleri_tr = {1:'Ocak',2:'Şubat',3:'Mart',4:'Nisan',5:'Mayıs',6:'Haziran',
     7:'Temmuz',8:'Ağustos',9:'Eylül',10:'Ekim',11:'Kasım',12:'Aralık'}

sorun = 0
# TR sayfalarini tara
for dosya in sorted(os.listdir(bd)):
    if not dosya.endswith('.html') or dosya == 'index.html':
        continue
    f = os.path.join(bd, dosya)
    c = open(f, 'r', encoding='utf-8').read()
    
    # JSON-LD tarih
    m = re.search(r'datePublished.*?(20\d{2})-(\d{2})-(\d{2})', c)
    if not m:
        continue
    yil, ay, gun = int(m.group(1)), int(m.group(2)), int(m.group(3))
    hedef = f"{gun} {ay_isimleri_tr[ay]} {yil}"
    
    # Sayfa ici tarih (&#128197; veya UTF-8 emoji)
    tarih_m = re.search(r'(?:&#128197;|\U0001F4C5)\s*([^<]+)', c)
    if tarih_m:
        mevcut = tarih_m.group(1).strip()
        # Entity'leri decode et
        mevcut_decoded = mevcut.replace('&#287;', 'ğ').replace('&#305;', 'ı').replace('&#246;', 'ö').replace('&#252;', 'ü').replace('&#231;', 'ç').replace('&#350;', 'Ş').replace('&#351;', 'ş')
        hedef_decoded = hedef
        if mevcut_decoded != hedef_decoded:
            print(f"YANLIS: {dosya[:50]:50} sayfa='{mevcut_decoded}' beklenen='{hedef_decoded}'")
            sorun += 1

print(f"\nToplam sorun: {sorun}")
