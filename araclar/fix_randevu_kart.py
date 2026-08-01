# -*- coding: utf-8 -*-
"""
Randevu kartinda etiket ve tarih yer degistirmesi:
- blog-card-tag icindeki tarih -> kategori adi
- ikinci span icindeki kategori adi -> tarih
- Kategori simgesi 📅 -> 🗓️
9 dilde.
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

# Randevu kartinin slug'i
slug = 'yapay-zeka-ile-randevu-rezervasyon-otomasyonu'

# Her dildeki etiket ve tarih degerleri
dil_verileri = {
    '': {'etiket': 'Randevu Y\u00f6netimi', 'tarih': '19 Temmuz 2026'},
    'en': {'etiket': 'Appointment Management', 'tarih': 'July 19, 2026'},
    'de': {'etiket': 'Terminverwaltung', 'tarih': '19. Juli 2026'},
    'es': {'etiket': 'Gesti\u00f3n de Citas', 'tarih': '19 de julio de 2026'},
    'fr': {'etiket': 'Gestion de Rendez-vous', 'tarih': '19 juillet 2026'},
    'ru': {'etiket': '\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0437\u0430\u043f\u0438\u0441\u044f\u043c\u0438', 'tarih': '19 \u0438\u044e\u043b\u044f 2026'},
    'ko': {'etiket': '\uc608\uc57d \uad00\ub9ac', 'tarih': '2026\ub144 7\uc6d4 19\uc77c'},
    'zh': {'etiket': '\u9884\u7ea6\u7ba1\u7406', 'tarih': '2026\u5e747\u670819\u65e5'},
    'ja': {'etiket': '\u4e88\u7d04\u7ba1\u7406', 'tarih': '2026\u5e747\u670819\u65e5'},
}

degisiklik = 0

for dil, veri in dil_verileri.items():
    if dil == '':
        f = os.path.join(bd, 'index.html')
    else:
        f = os.path.join(bd, dil, 'index.html')
    
    if not os.path.exists(f):
        print(f"  {dil or 'tr'}: dosya yok!")
        continue
    
    c = open(f, 'r', encoding='utf-8').read()
    
    # Randevu kartini bul (slug iceren article)
    pattern = r'(<article\s+class="blog-card">.*?</article>)'
    kartlar = list(re.finditer(pattern, c, re.DOTALL))
    
    for kart_m in kartlar:
        kart = kart_m.group(1)
        if slug not in kart:
            continue
        
        # Mevcut durumu kontrol et: blog-card-tag icinde tarih mi var?
        # Pattern: <span class="blog-card-tag">EMOJI ICERIK</span>
        #          <span>EMOJI ICERIK</span>
        meta_pattern = r'(<span\s+class="blog-card-tag">)(.*?)(</span>\s*<span>)(.*?)(</span>\s*<span>)'
        meta_m = re.search(meta_pattern, kart, re.DOTALL)
        
        if not meta_m:
            # Entity formatli da olabilir
            meta_pattern2 = r'(<span\s+class="blog-card-tag">)(.*?)(</span>\s*\n\s*<span>)(.*?)(</span>\s*\n\s*<span>)'
            meta_m = re.search(meta_pattern2, kart, re.DOTALL)
        
        if meta_m:
            etiket_icerik = meta_m.group(2).strip()
            tarih_icerik = meta_m.group(4).strip()
            
            dl = dil or 'tr'
            print(f"  {dl:3} MEVCUT etiket: [{etiket_icerik[:40]}] tarih: [{tarih_icerik[:40]}]")
            
            # Dogru degerler: etiket = 🗓️ KategoriAdi, tarih = 📅 Tarih
            # Simge: kategori icin 🗓️ (veya entity), tarih icin 📅 (veya entity &#128197;)
            
            # Etiket icerigi (blog-card-tag): 🗓️ + kategori adi
            yeni_etiket = '\U0001F5D3\uFE0F ' + veri['etiket']
            # Tarih icerigi: &#128197; + tarih veya 📅 + tarih
            # Mevcut dosyada hangi format kullaniliyor kontrol et
            if '&#128197;' in kart:
                yeni_tarih = '&#128197; ' + veri['tarih']
            else:
                yeni_tarih = '\U0001F4C5 ' + veri['tarih']
            
            # Kartta degistir
            yeni_kart = kart[:meta_m.start(2) - kart_m.start()] + yeni_etiket + kart[meta_m.end(2) - kart_m.start():meta_m.start(4) - kart_m.start()] + yeni_tarih + kart[meta_m.end(4) - kart_m.start():]
            
            # Ana dosyada degistir
            c = c[:kart_m.start()] + yeni_kart + c[kart_m.end():]
            print(f"       YENİ    etiket: [{yeni_etiket[:40]}] tarih: [{yeni_tarih[:40]}]")
            degisiklik += 1
        else:
            print(f"  {dil or 'tr'}: meta pattern bulunamadi!")
    
    with open(f, 'w', encoding='utf-8', newline='') as fw:
        fw.write(c)

print(f"\nToplam degisiklik: {degisiklik}")
