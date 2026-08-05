# ANTI_KALICI — yeni blog yazisi uretim kontrol listesi (EK)

Tarih: 05.08.2026
Bu dosya `ANTI_KALICI_blog_yazim_standardi.md` dosyasina EKLENECEK, hafizada kalacak.

---

## Neden bu ek yazildi

Blog #36 uretildi ve "TEMIZ" raporlandi. Gercekte uc ihlal vardi:
soru bicimli h2 yok · FAQPage schema yok · footer 9 dilde Turkce.

Sebep: yeni yazi uretilirken **sablon Turkce dosyadan kopyalanmis**, dil
eslesmesi yapilmamis; ve yazim standardinin 9 kurali uretim sirasinda
kontrol edilmemis.

---

## Her yeni blog yazisinda ZORUNLU kontrol

Yaziyi push etmeden ONCE, dokuz dilin her biri icin:

```
[ ] h2'lerin en az 4'u SORU bicimli (SSS basligi haric)
[ ] her h2'nin altindaki ilk cumle DOGRUDAN cevap
[ ] FAQPage schema VAR ve icindeki metin sayfadaki metinle BIREBIR ayni
[ ] BlogPosting schema VAR
[ ] footer O DILIN mevcut bir yazisindan kopyalandi
[ ] sayac etiketleri (lc-label) o dilde
[ ] navbar o dilde, dil butonlari AYNI yazinin dil surumlerine bakiyor
[ ] 3 ic link, hepsi kendi dil surumune
[ ] uzunluk: latin 700-900 kelime · CJK 1200+ karakter · diller arasi fark <%20
[ ] uydurma rakam YOK (musteri sayisi, yuzde, yil, sure garantisi)
```

## Footer ve navbar KOPYALANIR, yazilmaz

```
/blog/ja/<yeni-slug>.html
  -> footer ve navbar'i /blog/ja/ altindaki MEVCUT bir yazidan kopyala
  -> Turkce dosyadan kopyalama
```

Turkce sablondan kopyalanan footer, 8 dilde Turkce kalir. Blog #36'da olan budur.

## Ticari unvan istisnasi

`KILMAN BİLİŞİM SİSTEMLERİ` ticari unvandir, **her dilde Turkce yazilir.**
Bu bir ceviri hatasi degildir, duzeltilmeyecektir.

## Push sonrasi

```
python3 araclar/site_denetim.py --standart --slug <yeni-slug>
```

Cikti "9 temiz" degilse yazi BITMIS SAYILMAZ. Rapor yazilmadan once duzeltilir.

## Rapor kurali

"TEMIZ" yazmadan once hangi betigin neyi olctugunu belirt.
`site_denetim.py` yapiyi olcer; yazim standardini `--standart` modu olcer.
Ikisi ayri. Sadece birini calistirip "TEMIZ" demek eksik rapordur.
