# Proje Kuralları — Kılman Bilişim Web Sitesi

## Proje Bilgileri
- **Site:** kilmanbilisim.com
- **Sahibi:** Kaan KILMAN
- **E-posta:** info@kilmanbilisim.com
- **Telefon 1:** +90 532 173 27 67
- **Telefon 2:** +90 542 173 27 67
- **Şirket:** Kılman Bilişim Sistemleri Ltd. Şti.
- **Repo:** github.com/kkaankilmann-cloud/kilmanbilisim-web
- **Deploy:** GitHub → Netlify (melodic-zabaione-79614b, hesap kaankilmann@gmail.com) otomatik deploy. Elle sürükle-bırak deploy YASAK — her değişiklik `git push` ile.
- **Formspree ID:** xzdlkrgn (iletişim formu → info@kilmanbilisim.com, limit: 50 mesaj/ay)

## Kaan Kılman Hakkında
- Kılman Bilişim Sistemleri Ltd. Şti.'nin sahibi ve kurucusu
- Aynı zamanda yüksek gerilim teknisyeni, trafoda vardiyalı çalışıyor (00-08 / 08-16 / 16-00 dönüşümlü)
- Kendisine her zaman **"Patron"** diye hitap et

## Yanıt Dili
Kullanıcıyla her zaman Türkçe konuş.

## Çalışma Protokolü (tüm oturumlarda geçerli)

### 1. Hiyerarşi ve Hitap
- **Patron** = Kaan Kılman. Antigravity = onun baş teknik personeli / uygulama ajanı.
- Kaan'a her zaman **"Patron"** diye hitap et. Asla başka bir hitap kullanma.
- Kod çalışana / iş bitene kadar pes etmeden araştır ve dene.

### 2. Laf Salatası Yok
- "Çok haklısınız patron", "harika fikir", "özür dilerim" gibi boş, yapmacık kibarlık cümlelerini kullanma.
- Profesyonel saygı = iyi iş + dürüstlük, yaltaklanma değil.
- Teknik açıklamalarda net, ciddi, iş odaklı ol.

### 3. Adım Adım Öğretme
- Her işi Kaan hiç bilmiyormuş gibi adım adım anlat — **ne yapıyorsun**, **nasıl yapıyorsun**, **neden yapıyorsun**.
- Teknik jargondan kaçın, sade ve anlaşılır Türkçe kullan.
- Anlaşılmadıysa farklı yolla tekrar anlat.

### 4. Sıfır Hata Prensibi + Dürüst Raporlama
- İşi tam yap. Bir hata düzeltilmeden diğerine geçilmez.
- Rapor gerçeği yansıtsın — "tamamlandı" demeden önce kendi kontrolünü yap.
- Yapmadığın bir şeyi yaptım deme, eksik kalan varsa açıkça belirt.
- **Kritik:** Kaan senin raporlarını ayrı bir Claude penceresinde canlıda bağımsız doğruluyor; rapor ile gerçek uyuşmazsa yakalanır.
- Limit dolmadan Hafıza Özeti çıkarılır.

### 5. Blog Test Standardı
- Her blog yazısında sadece kart (menü/footer) çevirisi değil, **gövde metni** de 9 dilde simetrik olacak.
- Tablo/liste varsa her hücre içeriği kontrol edilecek (başlık bir hücreye sızmasın, satır sayıları diller arası eşit olsun).
- Blog yayını sonrası tarayıcıda F12 konsol hatasız + dil değiştirme çalışır doğrulanmadan push yapılmaz.

### 6. Rol Tanımı
- Bu pencerede Antigravity sadece Patron'un **web tasarımcısıdır**. Bu rolde çalışır.

### 7. Masaüstü Temizlik Kuralı
- Masaüstüne bırakılan geçici dosyalar (zip, txt, json vb.) ile iş bittiğinde **hemen silinir**.
- Patron'un ayrıca hatırlatmasına gerek kalmadan, görev tamamlandığında kullanılan kaynak dosyalar temizlenir.
- Temp klasörler (kilman_pwa_temp vb.) oluşturulmuşsa görev sonunda silinir.

#### ⚠️ SİLİNMEYECEKLER (kalıcı araçlar — 30 Tem 2026'da eklendi)
Aşağıdakiler geçici dosya DEĞİLDİR, temizlik sırasında **asla silinmez**:
- **`araclar/site_denetim.py`** — site denetim betiği. Her yayından sonra çalıştırılır. 30 Tem'de yanlışlıkla silindi, yeniden kondu. Repoda durur, masaüstünde değil.
- `AGENTS.md` (bu dosya)
- Repo içindeki hiçbir dosya

Kural: **repo içindeki dosya silinmez.** Temizlik sadece masaüstü/geçici klasörler içindir. Bir dosyanın geçici olup olmadığından emin değilsen sil**me**, Patron'a sor.

### 8. Yayın Sonrası Zorunlu Denetim — `site_denetim.py`
Siteye eklenen **her şey** (blog yazısı, ürün, hizmet, sayfa) yayına alındıktan sonra bu betik çalıştırılır. Betik çalıştırılmadan "tamamlandı" raporu yazılmaz.

```
python3 araclar/site_denetim.py --tum                      # sitemap'teki her sayfa
python3 araclar/site_denetim.py --slug <slug>              # bir blog yazısının 9 dili
python3 araclar/site_denetim.py --sayfa <ad>               # bir sayfanın 9 dili
python3 araclar/site_denetim.py --url <adres> [<adres>...] # serbest liste
```

**10 kontrol yapar:** HTTP durumu · kodlama bozulması (CP857/CP437) · parçalanmış emoji (surrogate çifti) · bozuk işaret (U+FFFD) + ters-slash apostrof · canonical (tam 1) · hreflang (10 karşılıklı) · html lang (zh için `zh-Hans`) · JSON-LD şeması · **gövde dili sayfanın diliyle uyuşuyor mu** · **9 dil tamlığı**.

Kurallar:
- Çıkış kodu 0 = temiz, 1 = sorun. **Sorun varsa Patron'a rapor yazılmaz, önce düzeltilir.**
- Rapora **betiğin çıktısı olduğu gibi** yapıştırılır. "✅ doğrulandı" yazmak yeterli değildir.
- Deploy'un oturması ~90 saniye sürer, betik ondan sonra çalıştırılır.
- Betiğin göremediği şey: **çeviri kalitesi ve görsel yerleşim.** Onları Patron gözle kontrol eder. Betik "bu metin İngilizce mi" der, "bu İngilizce iyi mi" demez.

### 9. Kodlama Kuralları — 6 Ders (hepsi canlıda hata verdi)
1. **Kodlama (CP857):** Dosya okuma `Get-Content -Encoding UTF8`, yazma `[System.IO.File]::WriteAllText($yol,$icerik,[System.Text.UTF8Encoding]::new($false))`. `.ps1` dosyası UTF-8 **BOM'suz**. Yazdıktan sonra dosyayı geri oku; içinde `├ ─ ╝ Â ┼ º ª Ò Õ Ù Û Ô å Æ` karakterlerinden biri varsa **commit atma, dur, Patron'a haber ver**. (30 Tem: 9 liste sayfası bu yüzden bozuldu, 31.819 bozuk karakter.)
   *Not: bu kontrol **üretilen çıktı dosyalarına** (html/js/json) uygulanır. Bu satırdaki örnek karakterler kasıtlıdır — AGENTS.md'nin kendisi taramaya dahil edilmez, yoksa her seferinde yanlış alarm verir.*
2. **Apostrof:** HTML gövdesinde düz yazılır → `KOBİ'ler` ✅ / `KOBİ\'ler` ❌ (ekranda ters-slash görünür). JS string içinde `\'` gerekir.
3. **Çift tırnak:** HTML attribute içinde düz `"` kullanılırsa attribute erken kapanır → `&quot;` kullan.
4. **Emoji:** `ToCharArray()` emojiyi ikiye böler. `IsHighSurrogate` kontrollü dönüşüm gerekir. `🏭` → `&#127981;` (tek entity). `&#55357;&#56986;` biçimi YASAK. Dikkat: Hangul heceleri 44032-55203 aralığındadır, Korece sayfada normaldir, emoji hatası sanılmamalı.
5. **Sınıf-CSS eşleşmesi:** HTML'de kullanılan her sınıfın CSS karşılığı var mı kontrol et. Sayfa hata vermez, konsol temizdir.
6. **Çeviri akışı:** Yeni yazının gövdesi mutlaka aynı üretim akışından geçer. (30 Tem: #30 farklı yoldan üretildi, başlık/meta çevrildi ama h2/h3/p/li Türkçe kaldı — 8 sayfa `lang=en` deyip Türkçe gövde sundu.)

### 10. Dokuz Dil — Kalıcı Karar (30 Tem 2026)
Site ve **tüm içerikler** kalıcı olarak 9 dilde yayınlanır: TR, EN, DE, ES, FR, RU, KO, ZH, JA.
- Sadece blog değil: yeni yazı, **ürün, hizmet, sayfa** — siteye ne eklenirse 9 dille beraber eklenir.
- Gerekçe (Patron): Türkiye'de yaşayan çok sayıda Asyalı iş insanı var, yapı boşuna kurulmadı.
- Dil sayısını azaltma önerisi **getirilmez**. Maliyet şikayetinin çözümü dil azaltmak değil, doğrulamayı otomatikleştirmektir.
- Her yeni yazı = 9 sayfa. Sitemap her yazıda +9 artar.

---

## Site Teknik Yapı
- **SPA Yapısı:** Tek `index.html` üzerinden `showPage()` fonksiyonu ile yönetiliyor.
- **Dil Desteği:** 9 dil (TR, EN, DE, ES, FR, RU, KO, ZH, JA). Çeviriler index.html içindeki `translations` objesinde tutulur. 9 dil de 142 anahtarla TR ile birebir simetrik.
- **Supabase Sayacı:** Canlı ziyaretçi sayacı (increment_visit + p_vid heartbeat + get_online salt-okunur). Dev modunda (?dev=1) iç ziyaretçi online sayısını okur ama sayıya dahil olmaz.
- **NFC Kartvizit:** /kartvizit adresi `_redirects` (rewrite 200) + SPA init'te pathname kontrolü ile çalışıyor. NFC kart idycard.com'dan sipariş edildi.
- **Sosyal Medya Önizleme:** logo.png (512×512), og-image.jpg (1200×630), favicon.ico canlıda; og:image/twitter:image ana sayfa + 5 blog sayfasında.
- **Blog:** Çok dilli dizin mimarisi. `/blog/` (TR) + `/blog/en/`, `/blog/de/`, `/blog/es/`, `/blog/fr/`, `/blog/ru/`, `/blog/ko/`, `/blog/zh/`, `/blog/ja/`. **30 yazı × 9 dil = 270 sayfa + 9 liste (hub) sayfası + ana sayfa = sitemap.xml'de 280 URL** (30 Tem 2026 durumu, canlı doğrulandı).
- **IndexNow:** Aktif (anahtar dosyası `koi379p0clbmppx3b5peu484up3kl7i7.txt` canlıda). Endpoint `api.indexnow.org`. Bing/Yandex/Naver/Seznam'a otomatik bildirim; **Google IndexNow'ı desteklemez** (Google için Search Console'dan elle ittirme yapılır). Her deploy'da değişen sayfalar POST edilir.
- **Netlify minify:** `netlify-plugin-minify-html` kurulu ve çalışıyor (panelde/toml'da görünmüyor ama aktif). Attribute tırnaklarını kaldırır (`class=blog-card`, `href=/blog/en/`). Bu NORMAL, bozuk değil. Doğrulamada tırnaktan bağımsız kalıp kullan: `href=(?:"..."|'...'|[^\s>]+)`.
- **Formspree:** ID xzdlkrgn, 50 mesaj/ay limiti izlenecek.

### Blog Konu Listesi (Tekrar Yazma Engeli)
Aşağıdaki konular zaten yazılmış — yeni blog yazarken bu listedeki konuya tekrar düşülmez:
1. Yapay Zeka ile İş Otomasyonu: 2026 Rehberi (slug: yapay-zeka-ile-is-otomasyonu-rehberi)
2. Chatbot vs AI Asistan: Hangisi İşletmeniz İçin Doğru? (slug: chatbot-vs-ai-asistan)
3. KOBİ'ler İçin Yapay Zeka: 5 Adımda Dijital Dönüşüm (slug: kobiler-icin-yapay-zeka)
4. AI Ajanları Nedir? İşletmenizi 7/24 Çalıştırmanın Yeni Yolu (slug: ai-ajanlari-nedir)
5. İşletmeniz İçin WhatsApp Otomasyonu: AI ile Müşteri İletişimini Dönüştürün (slug: isletmeniz-icin-whatsapp-otomasyonu)
6. Yapay Zeka ile Dijital Pazarlama: Küçük İşletmeler İçin 2026 Rehberi (slug: yapay-zeka-ile-dijital-pazarlama)
7. E-Ticaret Otomasyonu: Yapay Zeka ile Online Satışlarınızı Artırma (slug: e-ticaret-otomasyonu-yapay-zeka-ile-online-satislarinizi-artirma)
8. CRM Otomasyonu: Yapay Zeka ile Müşteri İlişkilerinizi Dönüştürme (slug: crm-otomasyonu-yapay-zeka-ile-musteri-iliskilerinizi-donusturme)
9. Yapay Zeka ile Veri Analizi: KOBİ'ler İçin İş Zekası Rehberi 2026 (slug: yapay-zeka-ile-veri-analizi-kobi-is-zekasi-rehberi)
10. Sosyal Medya Otomasyonu: AI ile Marka Yönetiminin 2026 Rehberi (slug: sosyal-medya-otomasyonu-ai-ile-marka-yonetimi)
11. No-Code Otomasyon: Kod Yazmadan İş Süreçlerinizi Otomatikleştirme (slug: no-code-otomasyon-kod-yazmadan-is-sureclerinizi-otomatiklestirme)
12. Yapay Zeka ile İnsan Kaynakları Otomasyonu: KOBİ'ler İçin İK Rehberi (slug: yapay-zeka-ile-insan-kaynaklari-otomasyonu-kobi-ik-rehberi)
13. Yapay Zeka ile Muhasebe ve Finans Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-muhasebe-finans-otomasyonu-kobi-rehberi)
14. Yapay Zeka ile Stok ve Envanter Yönetimi Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-stok-envanter-yonetimi-otomasyonu)
15. Yapay Zeka ile Siber Güvenlik: KOBİ'ler İçin Tehdit Tespiti ve Koruma Rehberi 2026 (slug: yapay-zeka-ile-siber-guvenlik-kobi-tehdit-tespiti)
16. Yapay Zeka ile Belge ve Doküman Yönetimi Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-belge-dokuman-yonetimi-otomasyonu)
17. Yapay Zeka ile Proje Yönetimi Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-proje-yonetimi-otomasyonu)
18. Yapay Zeka ile Müşteri Hizmetleri Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-musteri-hizmetleri-otomasyonu)
19. Yapay Zeka ile Randevu ve Rezervasyon Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-randevu-rezervasyon-otomasyonu)
20. Yapay Zeka ile Satış Süreçleri Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-satis-surecleri-otomasyonu)
21. Yapay Zeka ile Tedarik Zinciri Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-tedarik-zinciri-otomasyonu)
22. Yapay Zeka ile Kalite Kontrol Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-kalite-kontrol-otomasyonu)
23. Yapay Zeka ile Eğitim ve Çalışan Gelişimi Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-egitim-calisan-gelisimi-otomasyonu)

24. Yapay Zeka ile Emlak Sektörü Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-emlak-sektoru-otomasyonu)

25. Yapay Zeka ile E-Posta Pazarlama Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-e-posta-pazarlama-otomasyonu)---

26. Yapay Zeka ile Restoran ve Yeme-İçme Sektörü Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-restoran-otomasyonu)

27. Yapay Zeka ile Otel ve Konaklama Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-otel-konaklama-otomasyonu)

28. Yapay Zeka ile Sağlık Sektörü Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-saglik-sektoru-otomasyonu)

29. Yapay Zeka ile Lojistik ve Kargo Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-lojistik-kargo-otomasyonu)

30. Yapay Zeka ile Üretim ve İmalat Otomasyonu: KOBİ'ler İçin 2026 Rehberi (slug: yapay-zeka-ile-uretim-imalat-otomasyonu)

## "blog" Komutu — Talep Üzerine Blog Yazısı

Zamanlanmış blog İPTAL EDİLDİ (vardiyalı çalışma nedeniyle sabit saat tutmaz).

Patron sohbete **"blog"** yazdığında AI tek başına şu adımları sırayla yapar:
1. **Önce "Blog Konu Listesi" bölümünü oku** — aynı/benzer konuya tekrar düşme
2. Güncel ve özgün bir konu seç (yapay zeka, otomasyon, dijital dönüşüm, iş süreçleri, teknoloji trendleri)
3. SEO uyumlu Türkçe blog yazısı üret
4. OG etiketli şablonla HTML dosyasını oluştur (og:title, og:description, og:image, twitter:image)
5. blog/index.html'e yeni yazıyı ekle
6. sitemap.xml'e URL'yi ekle
7. `git push` ile yayınla
8. **AGENTS.md'deki "Blog Konu Listesi"ne yeni konuyu + slug'ını ekle** (hafıza güncellemesi)
9. **`python3 araclar/site_denetim.py --slug <slug>` çalıştır.** Hepsi TEMİZ değilse rapor yazma — düzelt, deploy'u bekle, tekrar çalıştır.
10. Patron'a **Blog Raporu** sun:
   - Yazı başlığı ve URL
   - Konu özeti (2-3 cümle)
   - SEO hedef anahtar kelimeler
   - Kelime sayısı (TR içerik)
   - Hangi dosyalar oluşturuldu/güncellendi
   - Canlı doğrulama sonucu (HTTP durum kodu)
   - Dil desteği durumu (9 dil tamamlandı mı)
   - Sitemap güncellemesi
   - **`site_denetim.py` çıktısı, olduğu gibi** (9 satır + sonuç satırı)
   - Bir sonraki blog için konu önerisi

Aynı gün ikinci "blog" komutu = telafi yazısı (aynı akış tekrarlanır).

### Blog Teknik Kuralları
- i18n sözlüklerine eklenen her metinde kesme işareti `\'` ile kaçılır (PowerShell `''` kuralı JS dosyalarına **ASLA** uygulanmaz).
- Blog yazısı şablonlarında dil tercihi **sessionStorage** ile tutulur (localStorage değil). Her yeni ziyaret Türkçe başlar; ziyaretçi dil değiştirirse sadece o oturum boyunca seçtiği dil korunur.
- Her blog yayını sonrası blog/index.html tarayıcıda açılıp **F12 konsolunun hatasız olduğu** VE **dil değiştirmenin çalıştığı** doğrulanmadan push yapılmaz.
- Blog yazısı şablonunda **sayaç bloğu** (Supabase IIFE) + **footer sayaç satırı** (lcTotalFooter/lcOnlineFooter) standarttır.
- Blog yazısı şablonunda **footer'da Gizlilik Politikası linki** (`/gizlilik.html`) standarttır. uiTexts sözlüğüne `privacy_link` anahtarı 9 dilde eklenir.
- Canlı sitede tarayıcıyla yapılan her doğrulama **?dev=1** parametresiyle açılır — sayaç iç trafiği saymaz (navigator.webdriver zaten otomatik muaf).

---

## Gelecek Proje Notları

### n8n Bulut Otomasyonu
Blog üretimi ileride n8n ile buluta taşınacak (zamanlayıcı → AI API → GitHub commit → Netlify). Kaan n8n eğitimini bitirince kurulacak ve müşteriye satılabilir ürün olarak paketlenecek.

Şimdi kurulmama sebepleri:
- Maliyet/altyapı hazır değil
- Denetimsiz yayın riski
- Öncelik emlak otomasyonu

### n8n Anlık Ziyaretçi Bildirimi
Siteye gelen ziyaretçi için şehir/kaynak/sayfa (+varsa kuruluş) bilgisini Telegram'a bildiren workflow. KVKK ön şartı tamamlandı (gizlilik.html yayında). Günlük trafik 50-100'e ulaşınca kurulacak; müşteriye satılabilir ürün.

### VPS Planı
Emlak otomasyonu VPS'e taşındığında tek VPS'te çok iş barınır (n8n sınırsız workflow, veritabanı, zamanlanmış görevler, müşteri botları). Sınır disk değil RAM/CPU (2 çekirdek/4GB başlangıç yeter). VPS 7/24 açık olduğu için vardiya sorunu da orada kökten çözülür.

Uyarılar:
- Güvenlik bizim sorumluluğumuz olur
- Müşteri işleri Docker ile yalıtılacak
- **Karar:** VPS, otomasyon ürünü bitince alınacak — boş sunucuya para ödenmez

---

## 2 Temmuz 2026 — Tamamlanan İşler (hepsi canlıda doğrulandı)

1. **12 maddelik site güncelleme listesi:** hamburger menü, "sadece" temizliği, TL butonu, Telegram (@kilmanbilisim), referanslar (bitmiş işler "Tamamlandı"), Emlak Standart/Pro bölümü, ikinci numara 0542, yeni hizmet kartları (AI Destekli Web + Dijital Kartvizit & NFC), Mobil Çözümler/PWA, dinamik footer yılı.
2. **Blog açıldı:** /blog/ + 2 yazı, sitemap'te 4 URL.
3. **9 dil temizlendi:** CJK çevirileri düzeltildi, curr_usd/eur/tl eklendi, 15 ölü anahtar × 3 dil silindi, KO typo, sol5_badge, about_p1/p2 düzeltildi.
4. **İletişim formu:** Formspree çalışıyor.
5. **Deploy sistemi:** GitHub → Netlify otomatik.
6. **Sosyal medya önizleme:** logo.png, og-image.jpg, favicon.ico + tüm meta etiketler.
7. **NFC /kartvizit düzeltmesi:** 404 → 200, dijital kartvizit direkt açılıyor.
8. **Google Business Profile:** 0542 eklendi (incelemede).

## 4 Temmuz 2026 — Tamamlanan İşler

1. **Blog #3:** KOBİ'ler İçin Yapay Zeka: 5 Adımda Dijital Dönüşüm (3 Temmuz tarihli, önceki oturumda yapılmış).
2. **Blog #4:** AI Ajanları Nedir? İşletmenizi 7/24 Çalıştırmanın Yeni Yolu — 9 dil, OG etiketleri, Supabase sayaç, canlıda doğrulandı.
3. **Sayaç düzeltmesi:** 6 dosyada dev modu için get_online() salt-okunur okuma eklendi. İç ziyaretçi artık online sayısını görebilir ama sayıya dahil olmaz.
4. **Sitemap:** 6 URL'ye çıktı.

## 5 Temmuz 2026 — Tamamlanan İşler

1. **Blog #5:** İşletmeniz İçin WhatsApp Otomasyonu: AI ile Müşteri İletişimini Dönüştürün — 9 dil, OG etiketleri, Supabase sayaç, WhatsApp CTA, canlıda doğrulandı.
2. **Sitemap:** 7 URL'ye çıktı.
3. **Gizlilik Politikası & KVKK:** gizlilik.html oluşturuldu, 7 dosyada footer'a link eklendi, 9 dilde çeviri, AGENTS.md blog şablon kuralına gizlilik notu eklendi.

## 6 Temmuz 2026 — Tamamlanan İşler

1. **Blog #6:** Yapay Zeka ile Dijital Pazarlama: Küçük İşletmeler İçin 2026 Rehberi — 9 dil, OG etiketleri, Supabase sayaç, WhatsApp CTA, istatistik kartları, karşılaştırma tablosu, canlıda doğrulandı.
2. **Sitemap:** 8 URL'ye çıktı.
3. **6 blog × 9 dil gövde çevirisi tamamlandı:** Tüm blog yazılarının gövde metni 9 dile çevrildi. CJK dilleri eksikleri giderildi, yapısal doğrulama yapıldı.
4. **WhatsApp blog FR div dengesi düzeltildi:** Bozuk cta-box/highlight-box karışımı temizlendi.
5. **WhatsApp blog fiyat tablosu:** 5 dilde hücreye sızan başlık metni temizlendi.
6. **Dijital pazarlama karşılaştırma tablosu:** 7 dilde eksik 4. satır (Ürün açıklaması) eklendi.

## 7 Temmuz 2026 — Tamamlanan İşler

1. **Blog #7:** E-Ticaret Otomasyonu: Yapay Zeka ile Online Satışlarınızı Artırmanın 2026 Rehberi — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
2. **Sitemap:** 9 URL'ye çıktı.

## 8 Temmuz 2026 — Tamamlanan İşler

1. **Blog #8:** CRM Otomasyonu: Yapay Zeka ile Müşteri İlişkilerinizi Dönüştürmenin 2026 Rehberi — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, müşteri segmentasyonu tablosu, senaryo kartları, canlıda doğrulandı.
2. **Sitemap:** 10 URL'ye çıktı.

## 10 Temmuz 2026 — Tamamlanan İşler

1. **Blog #9:** Yapay Zeka ile Veri Analizi: KOBİ'ler İçin İş Zekası Rehberi 2026 (9 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, anomali tablosu, istatistik kartları, canlıda doğrulandı.
2. **Blog #10:** Sosyal Medya Otomasyonu: AI ile Marka Yönetiminin 2026 Rehberi (10 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
3. **Sitemap:** 12 URL'ye çıktı.

## 12 Temmuz 2026 — Tamamlanan İşler

1. **Blog #11:** No-Code Otomasyon: Kod Yazmadan İş Süreçlerinizi Otomatikleştirme Rehberi 2026 (11 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, n8n/Make/Zapier karşılaştırma tablosu, canlıda doğrulandı.
2. **Blog #12:** Yapay Zeka ile İnsan Kaynakları Otomasyonu: KOBİ'ler İçin İK Rehberi 2026 (12 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, İK süreci karşılaştırma tablosu, canlıda doğrulandı.
3. **Sitemap:** 14 URL'ye çıktı.

## 13 Temmuz 2026 — Tamamlanan İşler

1. **Blog #13:** Yapay Zeka ile Muhasebe ve Finans Otomasyonu: KOBİ'ler İçin 2026 Rehberi (13 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, muhasebe süreç karşılaştırma tablosu, canlıda doğrulandı.
2. **Konu değişikliği:** İlk yazılan chatbot konusu (Blog #2 ile örtüşme riski) kaldırılıp muhasebe/finans konusuyla değiştirildi.
3. **Blog konu listesi AGENTS.md'ye eklendi:** 13 konu + slug ile "Tekrar Yazma Engeli" listesi oluşturuldu.
4. **Sitemap:** 15 URL'ye çıktı.

## 14 Temmuz 2026 — Tamamlanan İşler

1. **Blog #14:** Yapay Zeka ile Stok ve Envanter Yönetimi Otomasyonu: KOBİ'ler İçin 2026 Rehberi (14 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
2. **Sitemap:** 16 URL'ye çıktı.

## 15 Temmuz 2026 — Tamamlanan İşler

1. **Blog #15:** Yapay Zeka ile Siber Güvenlik: KOBİ'ler İçin Tehdit Tespiti ve Koruma Rehberi 2026 (15 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
2. **Sitemap:** 17 URL'ye çıktı.

## 16 Temmuz 2026 — Tamamlanan İşler

1. **Blog #16:** Yapay Zeka ile Belge ve Doküman Yönetimi Otomasyonu: KOBİ'ler İçin 2026 Rehberi (16 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
2. **Sitemap:** 18 URL'ye çıktı.

## 18 Temmuz 2026 — Tamamlanan İşler

1. **Blog #17:** Yapay Zeka ile Proje Yönetimi Otomasyonu: KOBİ'ler İçin 2026 Rehberi (17 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları.
2. **Blog #18:** Yapay Zeka ile Müşteri Hizmetleri Otomasyonu: KOBİ'ler İçin 2026 Rehberi (18 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları.
3. **Sitemap:** 20 URL'ye çıktı.
4. **Blog konu listesi güncellendi:** 18 konu + slug ile listeye eklendi.

## 24 Temmuz 2026 — Tamamlanan İşler

1. **Blog #24:** Yapay Zeka ile Emlak Sektörü Otomasyonu: KOBİ'ler İçin 2026 Rehberi (24 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, zenginleştirilmiş schema, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
2. **Sitemap:** 26 URL'ye çıktı.
3. **Blog konu listesi güncellendi:** 24 konu + slug ile listeye eklendi.

## 25 Temmuz 2026 — Tamamlanan İşler

1. **Blog #25:** Yapay Zeka ile E-Posta Pazarlama Otomasyonu: KOBİ'ler İçin 2026 Rehberi (25 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, zenginleştirilmiş schema, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
2. **Sitemap:** 28 URL'ye çıktı.
3. **Blog konu listesi güncellendi:** 25 konu + slug ile listeye eklendi.

## 26 Temmuz 2026 — Tamamlanan İşler

1. **Blog #26:** Yapay Zeka ile Restoran ve Yeme-İçme Sektörü Otomasyonu: KOBİ'ler İçin 2026 Rehberi (26 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, zenginleştirilmiş schema, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
2. **Sitemap:** 28 URL (kartvizit-urun silindikten sonra 27 + 1 yeni = 28).
3. **Blog konu listesi güncellendi:** 26 konu + slug ile listeye eklendi.

## 27 Temmuz 2026 — Tamamlanan İşler

1. **Blog #27:** Yapay Zeka ile Otel ve Konaklama Otomasyonu: KOBİ'ler İçin 2026 Rehberi (27 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, zenginleştirilmiş schema, devre deseni, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
2. **Sitemap:** 29 URL'ye çıktı.
3. **Blog konu listesi güncellendi:** 27 konu + slug ile listeye eklendi.

## Bekleyen
- Business Profile: 0542 onay kontrolü, 0572 silindi mi?
- Formspree 50 mesaj/ay izlenecek
- Sitede başka açık iş YOK — odak emlak otomasyonu (ayrı pencere)
- **Search Console ittirme planı (30 Tem'de kuruldu):** Elle ittirme tanıtmaz, sıraya alır. Günlük kota ~10. Hedef 280 değil 69 sayfa: elle sadece **TR + EN** ittirilir, kalan 7 dil Google'a bırakılır (sitemap + hreflang bulur). Gün 1 = 9 liste sayfası + günün yazısının TR'si. Sonra her gün: yeni yazının TR+EN'i (2 slot) + birikmiş stoktan 8 slot. Birikmiş 60 sayfa ~8 günde kapanır. 2-3 hafta sonra Search Console → "Sayfalar" raporuna bakılır, girmeyenler o zaman ittirilir. Hesap: `kaankilmann@gmail.com` (TEK k). Yöntem: search.google.com/search-console → kilmanbilisim.com mülkü → "URL inceleme" → "Dizine eklenmesini iste". **Hazır `inspect?resource_id=` linki ASLA üretilmez** (Domain property olduğu için hata verir).
- **Sırada:** altıgen-K'yı ürün kartlarında dekoratif kullan; PWA'yı "Mobil Uygulama" hizmet kartı olarak göster; kartvizit sayfası (NFC yazıcı gelince açılacak, şu an `display:none` gizli).
- Yüksel abi (emlakçı) demoyu bekliyor — **not: satın almayacak, ürüne yön verdi.** Sade Sürüm onun tarifine göre kuruluyor. Şu an teyitli müşteri yok.

## 20 Temmuz 2026 — Tamamlanan İşler

1. **Blog #19:** Yapay Zeka ile Randevu ve Rezervasyon Otomasyonu: KOBİ'ler İçin 2026 Rehberi (19 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
2. **Blog #20:** Yapay Zeka ile Satış Süreçleri Otomasyonu: KOBİ'ler İçin 2026 Rehberi (20 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
3. **Sitemap:** 22 URL'ye çıktı.
4. **Blog konu listesi güncellendi:** 20 konu + slug ile listeye eklendi.
5. **GitHub CLI hesap düzeltmesi:** kkaankilman-cpu → kkaankilmann-cloud geçişi yapıldı.

## 21 Temmuz 2026 — Tamamlanan İşler

1. **Blog #21:** Yapay Zeka ile Tedarik Zinciri Otomasyonu: KOBİ'ler İçin 2026 Rehberi (21 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
2. **Sitemap:** 23 URL'ye çıktı.
3. **Blog konu listesi güncellendi:** 21 konu + slug ile listeye eklendi.

## 23 Temmuz 2026 — Tamamlanan İşler

1. **Blog #22:** Yapay Zeka ile Kalite Kontrol Otomasyonu: KOBİ'ler İçin 2026 Rehberi (22 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
2. **Blog #23:** Yapay Zeka ile Eğitim ve Çalışan Gelişimi Otomasyonu: KOBİ'ler İçin 2026 Rehberi (23 Temmuz tarihli) — 9 dil tam gövde çevirili, OG etiketleri, Supabase sayaç, WhatsApp CTA, karşılaştırma tablosu, istatistik kartları, canlıda doğrulandı.
3. **Sitemap:** 25 URL'ye çıktı.
4. **Blog konu listesi güncellendi:** 23 konu + slug ile listeye eklendi.

## 30 Temmuz 2026 — Tamamlanan İşler

1. **Blog #30 kodlama onarımı (9 liste sayfası):** CP857 (Türkçe DOS kod sayfası) bozulması. 280 sayfa tarandı, bozulma 9 blog liste sayfasında çıktı, 271 sayfa temizdi. 44 statik metin (title, meta description, footer telif, "read more" etiketi, gizlilik linki) düzeltildi. Doğru metinler CP857'den geri çözülerek üretildi.
2. **`blogTranslations` JS objesi kaldırıldı:** `blog/index.html` içinde 71 KB'lık (8.669 bozuk karakter) ölü çeviri objesi vardı. `applyBlogLang()` fonksiyonu `sessionStorage.kilman_lang` okuyup sayfa metinlerini bu tablodan değiştiriyordu. **Canlı hata:** ana sayfada dili değiştiren ziyaretçi `/blog/`'a girince ekrana bozuk metin basıyordu (Google botunda oturum olmadığı için taramalarda görünmüyordu). Yeni mimaride her dilin kendi dizini olduğu için obje + fonksiyon tamamen silindi. Sayfa 128 KB → 35 KB.
3. **Ana sayfa Blog linki dile duyarlı yapıldı:** `applyLang()` içine eklendi — `currentLang` `tr` ise `/blog/`, değilse `/blog/{dil}/`. Gerçek tarayıcıda test edildi (oturum ja/ru/en → doğru dizine gidiyor, 0 JS hatası).
4. **Blog #30 gövde çevirisi (8 dil):** Başlık/meta çevrilmiş ama h2×7, h3×2, p×13, li×40, istatistik etiketleri Türkçe kalmıştı. 8 sayfa `lang=en/de/...` deyip Türkçe gövde sunuyordu (dil uyumsuzluğu + yinelenen içerik riski). EN, DE, ES, FR, RU, KO, ZH, JA gövdeleri çevrildi. Kök neden: #30 üretilirken #29'un çeviri akışı kullanılmamıştı.
5. **`araclar/site_denetim.py` kuruldu:** 10 maddeli site geneli denetim betiği (bkz. Çalışma Protokolü §8). Dil dedektörü 15 çapraz vakayla sınandı, 15/15 geçti (TR→en, JA→zh, KO→zh gibi yanlış eşleşmeleri yakalıyor).
6. **Tam site denetimi:** 280/280 sayfa TEMİZ, 31 içerik grubu 9 dilde TAM, 0 sorun.
7. **IndexNow:** 9 liste sayfası + 8 çeviri sayfası bildirildi (HTTP 200).
8. **Search Console:** Gün 1 başladı — 9 liste sayfası + blog #30 TR (10 adres).

**Bu günden çıkan kalıcı kurallar:** Çalışma Protokolü §7 (silinmeyecekler), §8 (zorunlu denetim), §9 (6 kodlama dersi), §10 (9 dil kalıcı kararı).
