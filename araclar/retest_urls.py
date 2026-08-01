# -*- coding: utf-8 -*-
import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
urls = [
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-emlak-sektoru-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-otel-konaklama-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-saglik-sektoru-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-lojistik-kargo-otomasyonu.html',
    'https://kilmanbilisim.com/blog/de/yapay-zeka-ile-lojistik-kargo-otomasyonu.html',
    'https://kilmanbilisim.com/blog/es/yapay-zeka-ile-lojistik-kargo-otomasyonu.html',
    'https://kilmanbilisim.com/blog/ru/yapay-zeka-ile-lojistik-kargo-otomasyonu.html',
    'https://kilmanbilisim.com/blog/ru/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/ko/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/zh/yapay-zeka-ile-restoran-otomasyonu.html',
]
for u in urls:
    try:
        r = requests.get(u, timeout=15)
        kisa = u.split('/')[-1][:50]
        print(f'{r.status_code} {kisa}')
    except Exception as e:
        kisa = u.split('/')[-1][:50]
        print(f'HATA {type(e).__name__} {kisa}')
