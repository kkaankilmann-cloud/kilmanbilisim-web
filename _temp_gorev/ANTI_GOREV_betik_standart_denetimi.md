# ANTI GOREV — betige BLOG YAZIM STANDARDI denetimi eklenecek

Tarih: 05.08.2026
Dosya: `araclar/site_denetim.py`
Sayfa uretimi YOK, sadece betik guclendirmesi.

---

## Neden

Blog #36 betikten "TEMIZ" gecti. Gercekte uc standart ihlali vardi:
```
soru bicimli h2   : 0/5   (standart: en az 5)
FAQPage schema    : YOK   (standart: zorunlu)
footer dili       : TURKCE (9 dilde birden)
```

Betik yapiyi denetliyor (HTTP, canonical, hreflang, uzunluk) ama
**yazim standardini denetlemiyor.** Her yeni yazida bu kor nokta tekrarlanacak.

Gunde 1 yazi x 9 dil = ayda 270 sayfa. Elle kontrol surdurulebilir degil.

---

## Yeni mod: `--standart`

```
python3 araclar/site_denetim.py --standart              # tum blog yazilari
python3 araclar/site_denetim.py --standart --slug <slug>  # tek yazi, 9 dil
```

Sadece **blog yazilarina** uygulanir. Sayfalar (hakkimizda, hizmetler...) ve
blog dizinleri bu denetimin disinda.

Arsivdeki 34 eski yazi bu denetimden MUAF (arsiv listesi zaten var).

---

## Denetlenecek 6 madde

### 1. Soru bicimli h2

```python
h2ler = re.findall(r'<h2[^>]*>(.*?)</h2>', h, re.S)
temiz = [re.sub(r'<[^>]+>','',x).strip() for x in h2ler]
soru  = sum(1 for x in temiz if any(q in x for q in "?？؟"))
# soru < 4  -> SORU-BICIMI-EKSIK (soru/toplam yazilacak)
```

Esik 4 (SSS basligi soru degil, o yuzden 5 degil 4).

### 2. FAQPage schema

```python
tipler = []
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
    try: tipler.append(json.loads(b).get("@type"))
    except: -> BOZUK-JSONLD
# "FAQPage" tipler icinde yoksa -> FAQPAGE-YOK
```

### 3. FAQPage metni sayfa metniyle ayni mi

FAQPage icindeki her `name` degeri, sayfa govdesinde AYNEN geciyor mu?
Gecmiyorsa -> `SCHEMA-METIN-UYUSMAZ` (hangi soru oldugu yazilacak)

### 4. Footer dili

Dosyanin dili adresten belirlenir (`/blog/ja/...` -> ja).
Footer metninde o dile ait BEKLENEN kelime var mi:

```python
BEKLENEN = {
 "tr":"Navigasyon", "en":"Navigation", "de":"Navigation", "es":"Navegación",
 "fr":"Navigation", "ru":"Навигация", "ko":"내비게이션", "zh":"导航", "ja":"ナビゲーション"
}
```

Ayrica non-TR dosyalarda Turkce imza aranir:
`Toplam Ziyaretçi` · `Şu An Online` · `Ana Sayfa` · `Hakkımızda`
Bulunursa -> `FOOTER-TURKCE`

⚠️ `KILMAN BİLİŞİM SİSTEMLERİ` ticari unvandir, HER DILDE Turkce yazilir.
Kalinti sayilmayacak, YANLIS ALARM URETME.

### 5. Yasak giris kaliplari

Her h2'nin ALTINDAKI ilk paragrafta su kaliplar aranir:
```
gunumuzde · günümüzde · teknolojinin gelismesiyle · bilindigi uzere · son yillarda
yukarida bahsettigimiz gibi · bir onceki bolumde
```
Bulunursa -> `YASAK-KALIP` (hangi kalip, hangi h2 altinda)

### 6. Ic link sayisi

Standart: en az 3 ic link (1 hizmet + 2 blog), her dil kendi surumune.
```
ic link < 3 -> IC-LINK-AZ (sayi yazilacak)
```
Dil uyusmazligi da yakalanacak: `/blog/ja/` icindeki link `/blog/en/`'e
bakiyorsa -> `IC-LINK-DIL-HATASI`

---

## Rapor ciktisi

```
=== BLOG YAZIM STANDARDI ===
slug: yapay-zeka-ile-is-guvenligi-isg-otomasyonu
dil  soru-h2  FAQPage  schema-metin  footer-dil  yasak-kalip  ic-link
tr     0/5      YOK        -           ok            0          4
ja     0/5      YOK        -           TURKCE        0          4
...
SONUC: 9 yazidan 9'u standart disi
```

Ihlal varsa cikis kodu 1.

---

## Yasaklar

- Mevcut kontrolleri (catch-all kalkani, ince-icerik, arsiv, canonical) DEGISTIRME
- Sayfalara ve blog dizinlerine bu denetimi UYGULAMA
- Arsivdeki 34 yaziya uygulama
- `etkilesim.py`'ye dokunma

---

## Kabul testi — bilinen dogru degerler

Blog #36 (henuz duzeltilmedi) icin betik sunu bulmali:

```
soru bicimli h2  : 0/5    -> SORU-BICIMI-EKSIK
FAQPage          : YOK    -> FAQPAGE-YOK
footer (8 dil)   : TURKCE -> FOOTER-TURKCE
footer (tr)      : ok
```

Blog #35 (`isletmeniz-icin-ozel-yazilim-mi-hazir-paket-mi`) icin:
```
soru bicimli h2  : 5/6    -> TEMIZ
FAQPage          : VAR    -> TEMIZ
footer           : ok     -> TEMIZ
```

Betik bu iki yaziyi dogru ayirt edemiyorsa mantik hatalidir.

---

## Teslim raporu

```
[ ] --standart modu 2 sekilde calisiyor    -> ciktilar
[ ] kabul testi: blog #36 -> 3 ihlal       -> cikti aynen
[ ] kabul testi: blog #35 -> temiz          -> cikti aynen
[ ] ticari unvan yanlis alarm URETMIYOR    -> blog #35 ja surumu ciktisi
[ ] mevcut kontroller bozulmadi            -> --tum ozet satiri once/sonra
```

Olcmeden yazma. Kabul testi tutmuyorsa mantik hatalidir, rapor etme, duzelt.
