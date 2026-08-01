# -*- coding: utf-8 -*-
import requests, sys, time
sys.stdout.reconfigure(encoding='utf-8')
urls = [
    'https://kilmanbilisim.com/',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-is-otomasyonu-rehberi.html',
    'https://kilmanbilisim.com/blog/chatbot-vs-ai-asistan-isletmeniz-icin-dogru-secim.html',
    'https://kilmanbilisim.com/blog/ai-ajanlari-nedir-isletmenizi-7-24-calistirmanin-yeni-yolu.html',
    'https://kilmanbilisim.com/blog/isletmeniz-icin-whatsapp-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-dijital-pazarlama.html',
    'https://kilmanbilisim.com/blog/e-ticaret-otomasyonu-yapay-zeka-ile-online-satislarinizi-artirma.html',
    'https://kilmanbilisim.com/blog/crm-otomasyonu-yapay-zeka-ile-musteri-iliskilerinizi-donusturme.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-veri-analizi-kobi-is-zekasi-rehberi.html',
    'https://kilmanbilisim.com/blog/sosyal-medya-otomasyonu-ai-ile-marka-yonetimi.html',
    'https://kilmanbilisim.com/blog/no-code-otomasyon-kod-yazmadan-is-sureclerinizi-otomatiklestirme.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-insan-kaynaklari-otomasyonu-kobi-ik-rehberi.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-muhasebe-finans-otomasyonu-kobi-rehberi.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-stok-envanter-yonetimi-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-siber-guvenlik-kobi-tehdit-tespiti.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-belge-dokuman-yonetimi-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-proje-yonetimi-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-musteri-hizmetleri-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-randevu-rezervasyon-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-satis-surecleri-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-tedarik-zinciri-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-egitim-calisan-gelisimi-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-emlak-sektoru-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-e-posta-pazarlama-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-otel-konaklama-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-saglik-sektoru-otomasyonu.html',
    'https://kilmanbilisim.com/blog/yapay-zeka-ile-lojistik-kargo-otomasyonu.html',
    'https://kilmanbilisim.com/blog/de/yapay-zeka-ile-lojistik-kargo-otomasyonu.html',
    'https://kilmanbilisim.com/blog/es/yapay-zeka-ile-lojistik-kargo-otomasyonu.html',
    'https://kilmanbilisim.com/blog/fr/yapay-zeka-ile-restoran-otomasyonu.html',
    'https://kilmanbilisim.com/blog/ko/chatbot-vs-ai-asistan-isletmeniz-icin-dogru-secim.html',
    'https://kilmanbilisim.com/blog/zh/chatbot-vs-ai-asistan-isletmeniz-icin-dogru-secim.html',
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
    time.sleep(0.3)

print(f'\nSonuc: {ok} OK / {fail} HATA (toplam {ok+fail})')
