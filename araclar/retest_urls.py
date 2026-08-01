# -*- coding: utf-8 -*-
import requests, sys, time
sys.stdout.reconfigure(encoding='utf-8')
urls = [
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-otel-konaklama-otomasyonu.html',
    'https://kilmanbilisim.com/blog/es/yapay-zeka-ile-lojistik-kargo-otomasyonu.html',
    'https://kilmanbilisim.com/blog/ru/yapay-zeka-ile-lojistik-kargo-otomasyonu.html',
    'https://kilmanbilisim.com/blog/zh/yapay-zeka-ile-lojistik-kargo-otomasyonu.html',
    'https://kilmanbilisim.com/blog/ja/yapay-zeka-ile-lojistik-kargo-otomasyonu.html',
    'https://kilmanbilisim.com/blog/en/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/de/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/es/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/fr/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/ru/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/ko/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/zh/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/ja/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/en/yapay-zeka-ile-is-otomasyonu-rehberi.html',
    'https://kilmanbilisim.com/blog/es/yapay-zeka-ile-is-otomasyonu-rehberi.html',
]
ok = 0
fail = 0
for u in urls:
    try:
        r = requests.get(u, timeout=15)
        ok += 1
    except Exception as e:
        kisa = u.replace('https://kilmanbilisim.com','')
        print(f'HATA {type(e).__name__}: {kisa}')
        fail += 1
    time.sleep(0.5)
print(f'\nSonuc: {ok} OK / {fail} HATA (toplam {ok+fail})')
