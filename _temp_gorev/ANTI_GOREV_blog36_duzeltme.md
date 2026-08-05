# ANTI GOREV — blog #36 uc duzeltme

Tarih: 05.08.2026
Etkilenen: 9 dosya — `yapay-zeka-ile-is-guvenligi-isg-otomasyonu.html` (TR + 8 dil)

Anti raporu "TEMIZ" dedi. Betik yapiyi denetliyor, YAZIM STANDARDINI denetlemiyor.
Uc ihlal canlidan olculdu.

---

# HATA 1 — h2'ler soru bicimli degil

Kalici blog standardi, kural 1: **h2'ler SORU bicimli olacak (en az 5 + SSS)**

Mevcut h2'ler:
```
İSG otomasyonunun temel bileşenleri          ← duz baslik
Sektörlere göre İSG otomasyon uygulamaları   ← duz baslik
Uygulama adımları                            ← duz baslik
Yatırım maliyeti ve geri dönüş               ← duz baslik
Sık Sorulan Sorular
```
Soru bicimli h2: **0/5** — dokuz dilde de ayni.

## Yapilacak

Ilk dort h2 soru bicimine cevrilecek. Icerik AYNEN kalir, sadece baslik degisir:

```
İSG otomasyonunun temel bileşenleri
  -> İSG otomasyonu hangi bileşenlerden oluşur?

Sektörlere göre İSG otomasyon uygulamaları
  -> Hangi sektörde nasıl uygulanır?

Uygulama adımları
  -> Kurulum nasıl ilerler?

Yatırım maliyeti ve geri dönüş
  -> Maliyeti nedir, ne kadar sürede geri döner?

Sık Sorulan Sorular    -> AYNEN KALIR
```

**Kural 2:** her h2'nin altindaki ilk cumle DOGRUDAN cevap olacak.
Mevcut ilk cumleler giris cumlesiyse cevap cumlesine cevrilecek.
YASAK giris kaliplari: "gunumuzde" · "teknolojinin gelismesiyle" · "bilindigi uzere"

8 dilde ayni islem, o dilin dogal soru kaliplariyla. Ceviri degil, dogal cumle.

---

# HATA 2 — FAQPage schema yok

Kalici standart, kural 6: **FAQPage schema zorunlu (4-5 soru, alici diliyle)**

Mevcut schema: sadece `BlogPosting`. Dokuz dilde de FAQPage YOK.

## Yapilacak

Sayfadaki SSS bolumunde zaten 4 soru var:
```
Küçük bir atölyede İSG otomasyonu gerekli mi?
Mevcut güvenlik kameralarım yeterli mi?
Çalışanlar gözetim hissi duyar mı?
Yasal uyumluluk nasıl sağlanır?
```

Bu dort soru-cevap `FAQPage` schema'sina eklenecek.

**Schema metni sayfadaki metinle BIREBIR ayni olacak.** Farkli olursa Google
uyumsuzluk sayar. Kopyala, elden yazma.

Referans: `/sss.html` dosyasindaki FAQPage yapisi.

---

# HATA 3 — footer Turkce kalmis

Dokuz dilin hepsinde footer TURKCE:
```
Navigasyon · Ana Sayfa · Hakkımızda · Toplam Ziyaretçi · Şu An Online
```

Eski yazilarda DOGRU (Japonca yazida `ナビゲーション ホーム 会社概要`, sayac `総訪問者`).
Yeni yazi uretilirken Turkce sablondan kopyalanmis.

## Yapilacak

Footer, o dilin MEVCUT bir blog yazisindan kopyalanacak:
```
/blog/ja/<S>  -> footer'i /blog/ja/yapay-zeka-ile-restoran-otomasyonu.html'den al
/blog/de/<S>  -> /blog/de/yapay-zeka-ile-restoran-otomasyonu.html
... 8 dil icin ayni
```

Sayac etiketleri (`lc-label`) de o dosyadan gelecek.
**Yeni ceviri YAPMA** — metinler zaten var, kopyala.

TR dosyasinin footer'i dogru, dokunma.

---

## Yasaklar

- Yazi ICERIGINE dokunma (paragraflar, tablolar, sayilar)
- h3 basliklarina dokunma
- Slug, tarih, kategori degistirme
- Navbar'a, dil butonlarina dokunma
- Sitemap'e dokunma (379)
- UYDURMA rakam ekleme

---

## Teslim raporu — OLCMEDEN YAZMA

```
[ ] 9 dosyada soru bicimli h2 sayisi        -> her dil icin sayi (>=4 olmali)
[ ] h2 basliklari                            -> 3 dil icin liste
[ ] her h2'nin ilk cumlesi dogrudan cevap    -> 2 ornek
[ ] FAQPage schema gecerli JSON              -> json.loads, 9/9
[ ] schema metni sayfa metniyle ayni         -> 2 soru icin karsilastirma
[ ] footer dogru dilde                       -> 3 dil ornegi
[ ] sayac etiketleri dogru dilde             -> 3 dil ornegi
[ ] kelime sayilari degismedi                -> once/sonra
[ ] sitemap 379
```
