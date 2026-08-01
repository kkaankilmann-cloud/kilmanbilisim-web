# -*- coding: utf-8 -*-
"""
8 dil liste sayfalarini duzelt:
1. Article arasi metin artiklarini temizle
2. Kart tarihlerini JSON-LD referansiyla duzelt
3. Kartlari yeniden eskiye sirala
"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

ay_isimleri = {
    'en': {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
           7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'},
    'de': {1:'Januar',2:'Februar',3:'M\u00e4rz',4:'April',5:'Mai',6:'Juni',
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
    'ko': {},
    'zh': {},
    'ja': {},
}

def format_tarih(yil, ay, gun, dil):
    if dil == 'en':
        return f"{ay_isimleri['en'][ay]} {gun}, {yil}"
    elif dil == 'de':
        return f"{gun}. {ay_isimleri['de'][ay]} {yil}"
    elif dil == 'es':
        return f"{gun} de {ay_isimleri['es'][ay]} de {yil}"
    elif dil == 'fr':
        return f"{gun} {ay_isimleri['fr'][ay]} {yil}"
    elif dil == 'ru':
        return f"{gun} {ay_isimleri['ru'][ay]} {yil}"
    elif dil == 'ko':
        return f"{yil}\ub144 {ay}\uc6d4 {gun}\uc77c"
    elif dil == 'zh':
        return f"{yil}\u5e74{ay}\u6708{gun}\u65e5"
    elif dil == 'ja':
        return f"{yil}\u5e74{ay}\u6708{gun}\u65e5"

def get_jsonld_tarih(slug_dosya):
    f = os.path.join(bd, slug_dosya)
    if not os.path.exists(f):
        return None
    c = open(f, 'r', encoding='utf-8').read()
    m = re.search(r'datePublished.*?(20\d{2})-(\d{2})-(\d{2})', c)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None

def fix_liste(dil):
    f = os.path.join(bd, dil, 'index.html')
    if not os.path.exists(f):
        print(f"  {dil}: dosya yok!")
        return
    
    c = open(f, 'r', encoding='utf-8').read()
    
    # Metin artiklarini temizle
    c = re.sub(r'(</article>\s*)\n\s*[^<\n]+(<article)', r'\1\n  \2', c)
    c = re.sub(r'(<div class="blog-grid">\s*)\n\s*[^<\n]+(<article)', r'\1\n  \2', c)
    
    # Kartlari bul
    kartlar = re.findall(r'(<article\s+class="blog-card">.*?</article>)', c, re.DOTALL)
    print(f"  {dil}: {len(kartlar)} kart")
    
    duzeltilmis = []
    duzeltme_sayisi = 0
    for kart in kartlar:
        slug_m = re.search(r'href="/blog/' + re.escape(dil) + r'/([\w-]+\.html)"', kart)
        if not slug_m:
            duzeltilmis.append((kart, (0,0,0)))
            continue
        slug = slug_m.group(1)
        
        tarih_data = get_jsonld_tarih(slug)
        if not tarih_data:
            duzeltilmis.append((kart, (0,0,0)))
            continue
        yil, ay, gun = tarih_data
        hedef = format_tarih(yil, ay, gun, dil)
        
        # Tarihi duzelt
        tarih_pattern = r'(&#128197;\s*)([^<]+?)(\s*</span>)'
        m = re.search(tarih_pattern, kart)
        if m:
            mevcut = m.group(2).strip()
            if mevcut != hedef:
                kart = kart[:m.start(2)] + hedef + kart[m.end(2):]
                duzeltme_sayisi += 1
        
        duzeltilmis.append((kart, tarih_data))
    
    # Sirala (yeniden eskiye)
    duzeltilmis.sort(key=lambda x: -(x[1][0]*10000 + x[1][1]*100 + x[1][2]))
    
    # Dosyayi guncelle
    grid_pattern = r'(<div class="blog-grid">\s*\n).*?(</div>\s*\n\s*<footer)'
    yeni_kartlar = "\n  ".join([k[0] for k in duzeltilmis])
    
    m = re.search(grid_pattern, c, re.DOTALL)
    if m:
        c = c[:m.start(1)] + m.group(1) + "  " + yeni_kartlar + "\n" + m.group(2) + c[m.end():]
    
    with open(f, 'w', encoding='utf-8', newline='') as fw:
        fw.write(c)
    
    print(f"    {duzeltme_sayisi} tarih duzeltildi")

for dil in ['en', 'de', 'es', 'fr', 'ru', 'ko', 'zh', 'ja']:
    fix_liste(dil)
