# -*- coding: utf-8 -*-
"""
WhatsApp butonlarindaki numarayi degistir:
  wa.me/905321732767 -> wa.me/905421732767
Sadece wa.me/ icindeki numara. tel:, schema, gorunen metin DOKUNULMAZ.
"""
import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')

root = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files"
eski = "wa.me/905321732767"
yeni = "wa.me/905421732767"

# Tum HTML dosyalarini tara
dosyalar = glob.glob(os.path.join(root, "**", "*.html"), recursive=True)
dosyalar.append(os.path.join(root, "index.html"))  # kok
dosyalar = list(set(dosyalar))  # tekrar onle

toplam_degisim = 0
etkilenen_dosya = 0
detay = []

for dosya in sorted(dosyalar):
    try:
        c = open(dosya, 'r', encoding='utf-8').read()
    except:
        continue
    
    sayi = c.count(eski)
    if sayi > 0:
        yeni_icerik = c.replace(eski, yeni)
        
        # Dogrulama: eski numara kalmadi mi
        assert yeni_icerik.count(eski) == 0, f"HATA: {dosya} icinde eski numara kaldi!"
        
        # Yaz
        with open(dosya, 'w', encoding='utf-8', newline='') as fw:
            fw.write(yeni_icerik)
        
        toplam_degisim += sayi
        etkilenen_dosya += 1
        rel = os.path.relpath(dosya, root)
        detay.append(f"  {rel}: {sayi} degisim")

print(f"=== SONUC ===")
print(f"Toplam degisim: {toplam_degisim}")
print(f"Etkilenen dosya: {etkilenen_dosya}")
print(f"\nDetay:")
for d in detay:
    print(d)

# Dogrulama: hicbir dosyada eski numara kalmadi mi
print(f"\n=== DOGRULAMA ===")
kalan = 0
for dosya in sorted(dosyalar):
    try:
        c = open(dosya, 'r', encoding='utf-8').read()
    except:
        continue
    if eski in c:
        rel = os.path.relpath(dosya, root)
        print(f"  UYARI: {rel} icinde eski numara KALDI!")
        kalan += 1

if kalan == 0:
    print(f"  wa.me/905321732767 → SIFIR (temiz)")

# Yeni numara sayisi
yeni_sayi = 0
for dosya in sorted(dosyalar):
    try:
        c = open(dosya, 'r', encoding='utf-8').read()
    except:
        continue
    yeni_sayi += c.count(yeni)
print(f"  wa.me/905421732767 → {yeni_sayi} baglanti")

# tel: kontrolu
tel_532 = 0
for dosya in sorted(dosyalar):
    try:
        c = open(dosya, 'r', encoding='utf-8').read()
    except:
        continue
    tel_532 += c.count("tel:+905321732767")
print(f"  tel:+905321732767 → {tel_532} (korundu)")
