# -*- coding: utf-8 -*-
"""
TUM kart tarihlerini JSON-LD referansiyla duzelten script.
Her karttaki tarihi, o yazinin JSON-LD datePublished degerinden turetir.
9 dilde calisir.
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

# JSON-LD'den tarih -> dile gore formatla
ay_isimleri = {
    '': {1:'Ocak',2:'Şubat',3:'Mart',4:'Nisan',5:'Mayıs',6:'Haziran',
         7:'Temmuz',8:'Ağustos',9:'Eylül',10:'Ekim',11:'Kasım',12:'Aralık'},
    'en': {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
           7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'},
    'de': {1:'Januar',2:'Februar',3:'März',4:'April',5:'Mai',6:'Juni',
           7:'Juli',8:'August',9:'September',10:'Oktober',11:'November',12:'Dezember'},
    'es': {1:'enero',2:'febrero',3:'marzo',4:'abril',5:'mayo',6:'junio',
           7:'julio',8:'agosto',9:'septiembre',10:'octubre',11:'noviembre',12:'diciembre'},
    'fr': {1:'janvier',2:'f\u00e9vrier',3:'mars',4:'avril',5:'mai',6:'juin',
           7:'juillet',8:'ao\u00fbt',9:'septembre',10:'octobre',11:'novembre',12:'d\u00e9cembre'},
    'ru': {1:'\u0438\u043d\u0432\u0430\u0440\u044f',2:'\u0444\u0435\u0432\u0440\u0430\u043b\u044f',
           3:'\u043c\u0430\u0440\u0442\u0430',4:'\u0430\u043f\u0440\u0435\u043b\u044f',
           5:'\u043c\u0430\u044f',6:'\u0438\u044e\u043d\u044f',
           7:'\u0438\u044e\u043b\u044f',8:'\u0430\u0432\u0433\u0443\u0441\u0442\u0430',
           9:'\u0441\u0435\u043d\u0442\u044f\u0431\u0440\u044f',10:'\u043e\u043a\u0442\u044f\u0431\u0440\u044f',
           11:'\u043d\u043e\u044f\u0431\u0440\u044f',12:'\u0434\u0435\u043a\u0430\u0431\u0440\u044f'},
}

def format_tarih(yil, ay, gun, dil):
    """JSON-LD tarihini dile gore formatla"""
    if dil == '':  # TR
        ay_ismi = ay_isimleri[''].get(ay, '?')
        return f"{gun} {ay_ismi} {yil}"
    elif dil == 'en':
        ay_ismi = ay_isimleri['en'].get(ay, '?')
        return f"{ay_ismi} {gun}, {yil}"
    elif dil == 'de':
        ay_ismi = ay_isimleri['de'].get(ay, '?')
        return f"{gun}. {ay_ismi} {yil}"
    elif dil == 'es':
        ay_ismi = ay_isimleri['es'].get(ay, '?')
        return f"{gun} de {ay_ismi} de {yil}"
    elif dil == 'fr':
        ay_ismi = ay_isimleri['fr'].get(ay, '?')
        return f"{gun} {ay_ismi} {yil}"
    elif dil == 'ru':
        ay_ismi = ay_isimleri['ru'].get(ay, '?')
        return f"{gun} {ay_ismi} {yil}"
    elif dil == 'ko':
        return f"{yil}\ub144 {ay}\uc6d4 {gun}\uc77c"
    elif dil == 'zh':
        return f"{yil}\u5e74{ay}\u6708{gun}\u65e5"
    elif dil == 'ja':
        return f"{yil}\u5e74{ay}\u6708{gun}\u65e5"

def get_jsonld_tarih(slug):
    """Yazi sayfasindan JSON-LD datePublished oku"""
    f = os.path.join(bd, slug + '.html') if os.path.exists(os.path.join(bd, slug + '.html')) else None
    if not f:
        f = os.path.join(bd, slug)
    if not os.path.exists(f):
        return None
    c = open(f, 'r', encoding='utf-8').read()
    m = re.search(r'datePublished.*?(20\d{2})-(\d{2})-(\d{2})', c)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None

def fix_liste_sayfa(dil):
    """Bir liste sayfasindaki tum kart tarihlerini duzelt"""
    if dil == '':
        f = os.path.join(bd, 'index.html')
    else:
        f = os.path.join(bd, dil, 'index.html')
    
    if not os.path.exists(f):
        return 0
    
    c = open(f, 'r', encoding='utf-8').read()
    degisiklik = 0
    
    # Tum article blog-card bloklarini bul
    pattern = r'(<article\s+class=["\']blog-card["\'].*?</article>)'
    kartlar = list(re.finditer(pattern, c, re.DOTALL))
    
    for kart_m in reversed(kartlar):  # Sondan basa git ki index kaymasin
        kart = kart_m.group(1)
        
        # Slug'i bul
        slug_m = re.search(r'href=["\'](?:/blog/(?:' + re.escape(dil) + r'/)?)?([\w-]+\.html)', kart)
        if not slug_m:
            continue
        slug = slug_m.group(1)
        if slug == 'index.html':
            continue
        
        # JSON-LD tarihini al (TR sayfasindan)
        tarih_data = get_jsonld_tarih(slug)
        if not tarih_data:
            continue
        yil, ay, gun = tarih_data
        
        # Hedef tarih metni
        hedef = format_tarih(yil, ay, gun, dil)
        
        # Karttaki mevcut tarihi bul ve degistir
        tarih_pattern = r'(&#128197;\s*)([^<]+?)(\s*<)'
        tarih_m = re.search(tarih_pattern, kart)
        if tarih_m:
            mevcut = tarih_m.group(2).strip()
            if mevcut != hedef:
                # Kart icindeki tarihi degistir
                yeni_kart = kart[:tarih_m.start(2) - kart_m.start()] + hedef + kart[tarih_m.end(2) - kart_m.start():]
                # Ana dosyada degistir
                c = c[:kart_m.start()] + yeni_kart + c[kart_m.end():]
                dl = dil if dil else 'tr'
                print(f"  KART {dl:3} {slug[:45]:45} '{mevcut[:25]}' -> '{hedef}'")
                degisiklik += 1
    
    if degisiklik > 0:
        with open(f, 'w', encoding='utf-8', newline='') as fw:
            fw.write(c)
    
    return degisiklik

toplam = 0
for dil in ['', 'en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']:
    dl = dil if dil else 'tr'
    print(f"\n=== {dl.upper()} LISTE SAYFASI ===")
    n = fix_liste_sayfa(dil)
    toplam += n
    if n == 0:
        print("  Degisiklik yok")

print(f"\nTOPLAM kart duzeltme: {toplam}")
