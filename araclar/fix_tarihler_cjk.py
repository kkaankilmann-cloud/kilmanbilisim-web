# -*- coding: utf-8 -*-
"""
GOREV C - CJK dilleri tarih duzeltme - HTML entity versiyonu
RU tarihleri de entity olarak yazilmis, onlari da duzeltelim
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

bd = r"c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"
toplam = 0

def do_replace(dosya, eski, yeni):
    global toplam
    if not os.path.exists(dosya):
        return False
    with open(dosya, 'r', encoding='utf-8') as f:
        c = f.read()
    if eski in c:
        c = c.replace(eski, yeni)
        with open(dosya, 'w', encoding='utf-8', newline='') as f:
            f.write(c)
        toplam += 1
        return True
    return False

# HTML entity tarihleri
# RU: июля=&#1080;&#1102;&#1083;&#1103;  августа=&#1072;&#1074;&#1075;&#1091;&#1089;&#1090;&#1072;
RU_IYULYA = "&#1080;&#1102;&#1083;&#1103;"
RU_AVGUSTA = "&#1072;&#1074;&#1075;&#1091;&#1089;&#1090;&#1072;"

# KO: 년=&#45380; 월=&#50900; 일=&#51068;
KO_NYON = "&#45380;"
KO_WOL = "&#50900;"
KO_IL = "&#51068;"

# ZH/JA: 年=&#24180; 月=&#26376; 日=&#26085;
CJK_NIAN = "&#24180;"
CJK_YUE = "&#26376;"
CJK_RI = "&#26085;"

yazilar = [
    {
        'slug': 'chatbot-vs-ai-asistan-isletmeniz-icin-dogru-secim',
        'ad': 'chatbot',
        'ru': {
            'eski': [f"2 {RU_IYULYA} 2026", "2 июля 2026"],
            'yeni': f"1 {RU_IYULYA} 2026"
        },
        'ko': {
            'eski': [f"2026{KO_NYON} 7{KO_WOL} 2{KO_IL}", "2026년 7월 2일"],
            'yeni': f"2026{KO_NYON} 7{KO_WOL} 1{KO_IL}"
        },
        'zh': {
            'eski': [f"2026{CJK_NIAN}7{CJK_YUE}2{CJK_RI}", "2026年7月2日"],
            'yeni': f"2026{CJK_NIAN}7{CJK_YUE}1{CJK_RI}"
        },
        'ja': {
            'eski': [f"2026{CJK_NIAN}7{CJK_YUE}2{CJK_RI}", "2026年7月2日"],
            'yeni': f"2026{CJK_NIAN}7{CJK_YUE}1{CJK_RI}"
        },
    },
    {
        'slug': 'yapay-zeka-ile-hukuk-sozlesme-yonetimi-otomasyonu',
        'ad': 'hukuk',
        'ru': {
            'eski': [f"31 {RU_IYULYA} 2026", "31 июля 2026", f"1 {RU_IYULYA} 2026"],
            'yeni': f"1 {RU_AVGUSTA} 2026"
        },
        'ko': {
            'eski': [f"2026{KO_NYON} 7{KO_WOL} 31{KO_IL}", "2026년 7월 31일"],
            'yeni': f"2026{KO_NYON} 8{KO_WOL} 1{KO_IL}"
        },
        'zh': {
            'eski': [f"2026{CJK_NIAN}7{CJK_YUE}31{CJK_RI}", "2026年7月31日"],
            'yeni': f"2026{CJK_NIAN}8{CJK_YUE}1{CJK_RI}"
        },
        'ja': {
            'eski': [f"2026{CJK_NIAN}7{CJK_YUE}31{CJK_RI}", "2026年7月31日"],
            'yeni': f"2026{CJK_NIAN}8{CJK_YUE}1{CJK_RI}"
        },
    },
    {
        'slug': 'yapay-zeka-ile-perakende-sektoru-otomasyonu',
        'ad': 'perakende',
        'ru': {
            'eski': [f"31 {RU_IYULYA} 2026", "31 июля 2026",
                     f"1 {RU_AVGUSTA} 2026", "1 августа 2026"],
            'yeni': f"2 {RU_AVGUSTA} 2026"
        },
        'ko': {
            'eski': [f"2026{KO_NYON} 7{KO_WOL} 31{KO_IL}", "2026년 7월 31일",
                     f"2026{KO_NYON} 8{KO_WOL} 1{KO_IL}", "2026년 8월 1일"],
            'yeni': f"2026{KO_NYON} 8{KO_WOL} 2{KO_IL}"
        },
        'zh': {
            'eski': [f"2026{CJK_NIAN}7{CJK_YUE}31{CJK_RI}", "2026年7月31日",
                     f"2026{CJK_NIAN}8{CJK_YUE}1{CJK_RI}", "2026年8月1日"],
            'yeni': f"2026{CJK_NIAN}8{CJK_YUE}2{CJK_RI}"
        },
        'ja': {
            'eski': [f"2026{CJK_NIAN}7{CJK_YUE}31{CJK_RI}", "2026年7月31日",
                     f"2026{CJK_NIAN}8{CJK_YUE}1{CJK_RI}", "2026年8月1日"],
            'yeni': f"2026{CJK_NIAN}8{CJK_YUE}2{CJK_RI}"
        },
    },
    {
        'slug': 'yapay-zeka-ile-tarim-sera-otomasyonu',
        'ad': 'tarim',
        'ru': {
            'eski': [f"31 {RU_IYULYA} 2026", "31 июля 2026",
                     f"1 {RU_AVGUSTA} 2026", "1 августа 2026"],
            'yeni': f"3 {RU_AVGUSTA} 2026"
        },
        'ko': {
            'eski': [f"2026{KO_NYON} 7{KO_WOL} 31{KO_IL}", "2026년 7월 31일",
                     f"2026{KO_NYON} 8{KO_WOL} 1{KO_IL}", "2026년 8월 1일"],
            'yeni': f"2026{KO_NYON} 8{KO_WOL} 3{KO_IL}"
        },
        'zh': {
            'eski': [f"2026{CJK_NIAN}7{CJK_YUE}31{CJK_RI}", "2026年7月31日",
                     f"2026{CJK_NIAN}8{CJK_YUE}1{CJK_RI}", "2026年8月1日"],
            'yeni': f"2026{CJK_NIAN}8{CJK_YUE}3{CJK_RI}"
        },
        'ja': {
            'eski': [f"2026{CJK_NIAN}7{CJK_YUE}31{CJK_RI}", "2026年7月31日",
                     f"2026{CJK_NIAN}8{CJK_YUE}1{CJK_RI}", "2026年8月1日"],
            'yeni': f"2026{CJK_NIAN}8{CJK_YUE}3{CJK_RI}"
        },
    },
]

for yazi in yazilar:
    slug = yazi['slug']
    ad = yazi['ad']
    for dil in ['ru', 'ko', 'zh', 'ja']:
        eskiler = yazi[dil]['eski']
        yeni = yazi[dil]['yeni']
        
        # Yazi sayfasi
        yazi_dosya = os.path.join(bd, dil, f"{slug}.html")
        for eski in eskiler:
            if do_replace(yazi_dosya, eski, yeni):
                print(f"SAYFA {dil} {ad}: OK")
        
        # Liste sayfasi (kart)
        liste_dosya = os.path.join(bd, dil, "index.html")
        for eski in eskiler:
            if do_replace(liste_dosya, eski, yeni):
                print(f"KART  {dil} {ad}: OK")

print(f"\nToplam CJK degisiklik: {toplam}")
