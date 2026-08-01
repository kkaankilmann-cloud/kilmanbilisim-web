# -*- coding: utf-8 -*-
"""
TR index.html tam duzeltme:
1. Article arasi metin artiklarini temizle
2. Kart tarihlerini JSON-LD referansiyla duzelt
3. Kartlari yeniden eskiye sirala
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

# Ay isimleri
ay_isimleri_tr = {1:'Ocak',2:'Şubat',3:'Mart',4:'Nisan',5:'Mayıs',6:'Haziran',
     7:'Temmuz',8:'Ağustos',9:'Eylül',10:'Ekim',11:'Kasım',12:'Aralık'}

def get_jsonld_tarih(slug_dosya):
    f = os.path.join(bd, slug_dosya)
    if not os.path.exists(f):
        return None
    c = open(f, 'r', encoding='utf-8').read()
    m = re.search(r'datePublished.*?(20\d{2})-(\d{2})-(\d{2})', c)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None

def fix_liste_sayfasi(liste_dosya, dil=''):
    c = open(liste_dosya, 'r', encoding='utf-8').read()
    
    # 1. Article arasi metin artiklarini temizle
    # Pattern: </article>\n  METIN<article veya </article>\nMETIN<article
    c_temiz = re.sub(r'(</article>\s*)\n\s*[^<\n]+(<article)', r'\1\n  \2', c)
    # Ayrica: blog-grid sonrasi metin artigi
    c_temiz = re.sub(r'(<div class="blog-grid">\s*)\n\s*[^<\n]+(<article)', r'\1\n  \2', c_temiz)
    
    if c_temiz != c:
        print(f"  Metin artiklari temizlendi")
    c = c_temiz
    
    # 2. Tum article bloklarini cikar
    pattern = r'(<article\s+class="blog-card">.*?</article>)'
    kartlar = re.findall(pattern, c, re.DOTALL)
    print(f"  {len(kartlar)} kart bulundu")
    
    # 3. Her kartin tarihini duzelt
    duzeltilmis_kartlar = []
    for kart in kartlar:
        # Slug bul
        slug_m = re.search(r'href="/blog/(?:' + re.escape(dil) + r'/)?([\w-]+\.html)"', kart) if dil else re.search(r'href="/blog/([\w-]+\.html)"', kart)
        if not slug_m:
            duzeltilmis_kartlar.append(kart)
            continue
        slug = slug_m.group(1)
        
        # JSON-LD tarihini al
        tarih_data = get_jsonld_tarih(slug)
        if not tarih_data:
            duzeltilmis_kartlar.append(kart)
            continue
        yil, ay, gun = tarih_data
        
        if dil == '' or dil == 'tr':
            hedef = f"{gun} {ay_isimleri_tr[ay]} {yil}"
        else:
            hedef = None  # Baska diller icin ayri format
        
        if hedef:
            # Karttaki tarihi degistir
            tarih_pattern = r'(&#128197;\s*)([^<]+?)(\s*</span>)'
            m = re.search(tarih_pattern, kart)
            if m:
                mevcut = m.group(2).strip()
                if mevcut != hedef:
                    kart = kart[:m.start(2)] + hedef + kart[m.end(2):]
                    print(f"    {slug[:45]:45} '{mevcut}' -> '{hedef}'")
        
        duzeltilmis_kartlar.append((kart, tarih_data))
    
    # 4. Tarihe gore sirala (yeniden eskiye)
    def sort_key(item):
        if isinstance(item, tuple):
            kart, (yil, ay, gun) = item
            return -(yil * 10000 + ay * 100 + gun)
        return 0
    
    duzeltilmis_kartlar.sort(key=sort_key)
    
    # 5. Dosyayi yeniden yaz
    # Blog-grid icindeki kartlari degistir
    grid_pattern = r'(<div class="blog-grid">\s*\n).*?(</div>\s*\n\s*<footer)'
    
    yeni_kartlar = "\n  ".join([k[0] if isinstance(k, tuple) else k for k in duzeltilmis_kartlar])
    
    m = re.search(grid_pattern, c, re.DOTALL)
    if m:
        c = c[:m.start(1)] + m.group(1) + "  " + yeni_kartlar + "\n" + m.group(2) + c[m.end():]
    
    with open(liste_dosya, 'w', encoding='utf-8', newline='') as fw:
        fw.write(c)
    
    # Dogrulama
    c2 = open(liste_dosya, 'r', encoding='utf-8').read()
    kartlar2 = re.findall(r'<article\s+class="blog-card">.*?</article>', c2, re.DOTALL)
    print(f"  Sonuc: {len(kartlar2)} kart")
    
    for i, kart in enumerate(kartlar2[:5]):
        slug_m = re.search(r'href="/blog/[\w/]*([\w-]+\.html)"', kart)
        tarih_m = re.search(r'&#128197;\s*([^<]+)', kart)
        slug = slug_m.group(1) if slug_m else '?'
        tarih = tarih_m.group(1).strip() if tarih_m else '?'
        print(f"    {i+1}. {tarih:25} {slug[:45]}")

print("=== TR LISTE SAYFASI ===")
fix_liste_sayfasi(os.path.join(bd, 'index.html'), '')
