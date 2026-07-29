# gen_list_pages.ps1 — Blog liste sayfası üreteç
# 8 yeni dil liste sayfası üretir, TR sayfasını günceller
# Çalıştır: powershell -File gen_list_pages.ps1

$blogDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$srcFile = Join-Path $blogDir "index.html"
$srcContent = [System.IO.File]::ReadAllText($srcFile, [System.Text.Encoding]::UTF8)

# i18n sözlüğünü dosyadan çıkar
$jsMatch = [regex]::Match($srcContent, 'const blogTranslations = \{(.*?)\};', [System.Text.RegularExpressions.RegexOptions]::Singleline)
if(-not $jsMatch.Success) { Write-Error "blogTranslations bulunamadı!"; exit 1 }

# Dil yapılandırması
$langs = @{
    'en' = @{ locale='en_US'; title='Blog — Kılman Bilişim | AI & Automation Content'; desc='Latest articles, guides and industry insights on artificial intelligence, automation and digital transformation.'; titleKey='blog_title'; subKey='blog_sub' }
    'de' = @{ locale='de_DE'; title='Blog — Kılman Bilişim | KI & Automatisierung'; desc='Aktuelle Artikel, Leitfäden und Branchenanalysen zu künstlicher Intelligenz, Automatisierung und digitaler Transformation.'; titleKey='blog_title'; subKey='blog_sub' }
    'es' = @{ locale='es_ES'; title='Blog — Kılman Bilişim | IA y Automatización'; desc='Artículos actuales, guías y análisis del sector sobre inteligencia artificial, automatización y transformación digital.'; titleKey='blog_title'; subKey='blog_sub' }
    'fr' = @{ locale='fr_FR'; title='Blog — Kılman Bilişim | IA et Automatisation'; desc="Articles actuels, guides et analyses sectorielles sur l'intelligence artificielle, l'automatisation et la transformation numérique."; titleKey='blog_title'; subKey='blog_sub' }
    'ru' = @{ locale='ru_RU'; title='Blog — Kılman Bilişim | ИИ и автоматизация'; desc='Актуальные статьи, руководства и отраслевые обзоры по искусственному интеллекту, автоматизации и цифровой трансформации.'; titleKey='blog_title'; subKey='blog_sub' }
    'ko' = @{ locale='ko_KR'; title='Blog — Kılman Bilişim | AI 및 자동화'; desc='인공지능, 자동화 및 디지털 전환에 관한 최신 기사, 가이드 및 업계 분석.'; titleKey='blog_title'; subKey='blog_sub' }
    'zh' = @{ locale='zh_CN'; title='Blog — Kılman Bilişim | AI与自动化'; desc='关于人工智能、自动化和数字化转型的最新文章、指南和行业分析。'; titleKey='blog_title'; subKey='blog_sub' }
    'ja' = @{ locale='ja_JP'; title='Blog — Kılman Bilişim | AIと自動化'; desc='人工知能、自動化、デジタルトランスフォーメーションに関する最新記事、ガイド、業界分析。'; titleKey='blog_title'; subKey='blog_sub' }
}

# Çeviri sözlüğünü JS'ten çıkar — her dil için post başlıkları ve açıklamaları
# blogTranslations objesinden her dilin key-value çiftlerini parse et
function Get-TranslationForLang($lang, $jsContent) {
    $pattern = "(?<=$lang\s*:\s*\{)(.*?)(?=\}(\s*,\s*\w|\s*\}))"
    $m = [regex]::Match($jsContent, $pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
    if($m.Success) {
        $block = $m.Groups[1].Value
        $result = @{}
        $kvMatches = [regex]::Matches($block, "(\w+):\s*'((?:[^'\\]|\\.)*)'")
        foreach($kv in $kvMatches) {
            $result[$kv.Groups[1].Value] = $kv.Groups[2].Value -replace "\\'","'"
        }
        return $result
    }
    return @{}
}

$jsContent = $jsMatch.Groups[1].Value
$allTranslations = @{}
foreach($lang in @('tr','en','de','es','fr','ru','ko','zh','ja')) {
    $allTranslations[$lang] = Get-TranslationForLang $lang $jsContent
}

# 29 blog yazısının slug ve post numaraları (en yeni en üstte)
$posts = @(
    @{n=29; slug='yapay-zeka-ile-lojistik-kargo-otomasyonu'; date='29 Temmuz 2026'; tagKey='tag_logistics'}
    @{n=28; slug='yapay-zeka-ile-saglik-sektoru-otomasyonu'; date='28 Temmuz 2026'; tagKey='tag_health'}
    @{n=27; slug='yapay-zeka-ile-otel-konaklama-otomasyonu'; date='27 Temmuz 2026'; tagKey='tag_hotel'}
    @{n=26; slug='yapay-zeka-ile-restoran-otomasyonu'; date='26 Temmuz 2026'; tagKey='tag_restaurant'}
    @{n=25; slug='yapay-zeka-ile-e-posta-pazarlama-otomasyonu'; date='25 Temmuz 2026'; tagKey='tag_email'}
    @{n=24; slug='yapay-zeka-ile-emlak-sektoru-otomasyonu'; date='24 Temmuz 2026'; tagKey='tag_realestate'}
    @{n=23; slug='yapay-zeka-ile-egitim-calisan-gelisimi-otomasyonu'; date='23 Temmuz 2026'; tagKey='tag_training'}
    @{n=22; slug='yapay-zeka-ile-kalite-kontrol-otomasyonu'; date='22 Temmuz 2026'; tagKey='tag_quality'}
    @{n=21; slug='yapay-zeka-ile-tedarik-zinciri-otomasyonu'; date='21 Temmuz 2026'; tagKey='tag_supply'}
    @{n=20; slug='yapay-zeka-ile-satis-surecleri-otomasyonu'; date='20 Temmuz 2026'; tagKey='tag_sales'}
    @{n=19; slug='yapay-zeka-ile-randevu-rezervasyon-otomasyonu'; date='19 Temmuz 2026'; tagKey='tag_appointment'}
    @{n=18; slug='yapay-zeka-ile-musteri-hizmetleri-otomasyonu'; date='18 Temmuz 2026'; tagKey='tag_customer_service'}
    @{n=17; slug='yapay-zeka-ile-proje-yonetimi-otomasyonu'; date='17 Temmuz 2026'; tagKey='tag_project'}
    @{n=16; slug='yapay-zeka-ile-belge-dokuman-yonetimi-otomasyonu'; date='16 Temmuz 2026'; tagKey='tag_document'}
    @{n=15; slug='yapay-zeka-ile-siber-guvenlik-kobi-tehdit-tespiti'; date='15 Temmuz 2026'; tagKey='tag_cybersecurity'}
    @{n=14; slug='yapay-zeka-ile-stok-envanter-yonetimi-otomasyonu'; date='14 Temmuz 2026'; tagKey='tag_inventory'}
    @{n=13; slug='yapay-zeka-ile-muhasebe-finans-otomasyonu-kobi-rehberi'; date='13 Temmuz 2026'; tagKey='tag_accounting'}
    @{n=12; slug='yapay-zeka-ile-insan-kaynaklari-otomasyonu-kobi-ik-rehberi'; date='12 Temmuz 2026'; tagKey='tag_hr'}
    @{n=11; slug='no-code-otomasyon-kod-yazmadan-is-sureclerinizi-otomatiklestirme'; date='11 Temmuz 2026'; tagKey='tag_nocode'}
    @{n=10; slug='sosyal-medya-otomasyonu-ai-ile-marka-yonetimi'; date='10 Temmuz 2026'; tagKey='tag_social'}
    @{n=9; slug='yapay-zeka-ile-veri-analizi-kobi-is-zekasi-rehberi'; date='9 Temmuz 2026'; tagKey='tag_data'}
    @{n=8; slug='crm-otomasyonu-yapay-zeka-ile-musteri-iliskilerinizi-donusturme'; date='8 Temmuz 2026'; tagKey='tag_crm'}
    @{n=7; slug='e-ticaret-otomasyonu-yapay-zeka-ile-online-satislarinizi-artirma'; date='7 Temmuz 2026'; tagKey='tag_ecommerce'}
    @{n=6; slug='yapay-zeka-ile-dijital-pazarlama'; date='6 Temmuz 2026'; tagKey='tag_marketing'}
    @{n=5; slug='isletmeniz-icin-whatsapp-otomasyonu'; date='5 Temmuz 2026'; tagKey='tag_wa'}
    @{n=4; slug='ai-ajanlari-nedir-isletmenizi-7-24-calistirmanin-yeni-yolu'; date='4 Temmuz 2026'; tagKey='tag_ai'}
    @{n=3; slug='kobiler-icin-yapay-zeka-5-adimda-dijital-donusum'; date='3 Temmuz 2026'; tagKey='tag_dt'}
    @{n=2; slug='chatbot-vs-ai-asistan-isletmeniz-icin-dogru-secim'; date='3 Temmuz 2026'; tagKey='tag_ai'}
    @{n=1; slug='yapay-zeka-ile-is-otomasyonu-rehberi'; date='2 Temmuz 2026'; tagKey='tag_ai'}
)

# Tarih çevirileri (ay isimleri)
$months = @{
    'en' = @{ 'Temmuz'='July' }
    'de' = @{ 'Temmuz'='Juli' }
    'es' = @{ 'Temmuz'='Julio' }
    'fr' = @{ 'Temmuz'='Juillet' }
    'ru' = @{ 'Temmuz'='Июль' }
    'ko' = @{ 'Temmuz'='7월' }
    'zh' = @{ 'Temmuz'='7月' }
    'ja' = @{ 'Temmuz'='7月' }
}

# Okuma süresi çevirileri  
$readTimeLabels = @{
    'en' = @{ '5'='5 min read'; '6'='6 min read'; '7'='7 min read'; '8'='8 min read'; '9'='9 min read'; '10'='10 min read'; '12'='12 min read' }
    'de' = @{ '5'='5 Min.'; '6'='6 Min.'; '7'='7 Min.'; '8'='8 Min.'; '9'='9 Min.'; '10'='10 Min.'; '12'='12 Min.' }
    'es' = @{ '5'='5 min'; '6'='6 min'; '7'='7 min'; '8'='8 min'; '9'='9 min'; '10'='10 min'; '12'='12 min' }
    'fr' = @{ '5'='5 min'; '6'='6 min'; '7'='7 min'; '8'='8 min'; '9'='9 min'; '10'='10 min'; '12'='12 min' }
    'ru' = @{ '5'='5 мин'; '6'='6 мин'; '7'='7 мин'; '8'='8 мин'; '9'='9 мин'; '10'='10 мин'; '12'='12 мин' }
    'ko' = @{ '5'='5분'; '6'='6분'; '7'='7분'; '8'='8분'; '9'='9분'; '10'='10분'; '12'='12분' }
    'zh' = @{ '5'='5分钟'; '6'='6分钟'; '7'='7分钟'; '8'='8分钟'; '9'='9分钟'; '10'='10分钟'; '12'='12分钟' }
    'ja' = @{ '5'='5分'; '6'='6分'; '7'='7分'; '8'='8分'; '9'='9分'; '10'='10分'; '12'='12分' }
}

# readMore çevirileri
$readMoreTexts = @{
    'tr'='Devamını Oku →'; 'en'='Read More →'; 'de'='Weiterlesen →'; 'es'='Leer Más →';
    'fr'='Lire la Suite →'; 'ru'='Читать Далее →'; 'ko'='더 읽기 →'; 'zh'='阅读更多 →'; 'ja'='続きを読む →'
}

# Nav label çevirileri
$navHome = @{ 'tr'='Ana Sayfa'; 'en'='Home'; 'de'='Startseite'; 'es'='Inicio'; 'fr'='Accueil'; 'ru'='Главная'; 'ko'='홈'; 'zh'='首页'; 'ja'='ホーム' }
$privacyTexts = @{ 'tr'='Gizlilik Politikası'; 'en'='Privacy Policy'; 'de'='Datenschutz'; 'es'='Política de Privacidad'; 'fr'='Politique de Confidentialité'; 'ru'='Политика конфиденциальности'; 'ko'='개인정보 처리방침'; 'zh'='隐私政策'; 'ja'='プライバシーポリシー' }
$footerRights = @{ 'tr'='Tüm hakları saklıdır.'; 'en'='All rights reserved.'; 'de'='Alle Rechte vorbehalten.'; 'es'='Todos los derechos reservados.'; 'fr'='Tous droits réservés.'; 'ru'='Все права защищены.'; 'ko'='모든 권리 보유.'; 'zh'='版权所有。'; 'ja'='全著作権所有。' }

# Blog hero alt yazı
$heroSub = @{
    'tr'='Yapay zeka, otomasyon ve dijital dönüşüm hakkında güncel yazılar, rehberler ve sektör analizleri.'
    'en'='Articles, guides and industry insights on artificial intelligence, automation and digital transformation.'
    'de'='Aktuelle Artikel, Leitfäden und Branchenanalysen zu KI, Automatisierung und digitaler Transformation.'
    'es'='Artículos actuales, guías y análisis del sector sobre IA, automatización y transformación digital.'
    'fr'="Articles, guides et analyses sectorielles sur l'IA, l'automatisation et la transformation numérique."
    'ru'='Статьи, руководства и обзоры по ИИ, автоматизации и цифровой трансформации.'
    'ko'='인공지능, 자동화 및 디지털 전환에 관한 최신 기사, 가이드 및 업계 분석.'
    'zh'='关于人工智能、自动化和数字化转型的最新文章、指南和行业分析。'
    'ja'='AI、自動化、デジタルトランスフォーメーションに関する最新記事、ガイド、業界分析。'
}

# hreflang bloğu (9 sayfa için aynı)
$hreflangBlock = @"
<link rel="alternate" hreflang="tr" href="https://kilmanbilisim.com/blog/"/>
<link rel="alternate" hreflang="en" href="https://kilmanbilisim.com/blog/en/"/>
<link rel="alternate" hreflang="de" href="https://kilmanbilisim.com/blog/de/"/>
<link rel="alternate" hreflang="es" href="https://kilmanbilisim.com/blog/es/"/>
<link rel="alternate" hreflang="fr" href="https://kilmanbilisim.com/blog/fr/"/>
<link rel="alternate" hreflang="ru" href="https://kilmanbilisim.com/blog/ru/"/>
<link rel="alternate" hreflang="ko" href="https://kilmanbilisim.com/blog/ko/"/>
<link rel="alternate" hreflang="zh" href="https://kilmanbilisim.com/blog/zh/"/>
<link rel="alternate" hreflang="ja" href="https://kilmanbilisim.com/blog/ja/"/>
<link rel="alternate" hreflang="x-default" href="https://kilmanbilisim.com/blog/"/>
"@

# Okuma süresi mapping (post numarasina gore)
$readTimes = @{}
foreach($p in $posts) {
    $n = $p.n
    if($n -ge 27) { $readTimes[$n] = '10' }
    elseif($n -ge 24) { $readTimes[$n] = '10' }
    elseif($n -ge 7) { $readTimes[$n] = '9' }
    elseif($n -ge 5) { $readTimes[$n] = '8' }
    else { $readTimes[$n] = '5' }
}
# Özel override'lar
$readTimes[28] = '12'; $readTimes[29] = '12'

# CSS bloğu — index.html'den aynen al (button -> a.lang-btn)
$cssMatch = [regex]::Match($srcContent, '<style>(.*?)</style>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
$css = $cssMatch.Groups[1].Value
# button stillerini a.lang-btn'e çevir
$css = $css -replace '\.blog-lang button\b', '.blog-lang a.lang-btn'
$css = $css -replace '\.blog-lang button:', '.blog-lang a.lang-btn:'

# Supabase sayaç bloğu
$supabaseMatch = [regex]::Match($srcContent, '<!-- CANLI ZIYARETCI SAYACI.*?</script>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
$supabaseBlock = $supabaseMatch.Value

function Build-LangButtons($activeLang) {
    $allLangs = @('tr','en','de','es','fr','ru','ko','zh','ja')
    $buttons = @()
    foreach($l in $allLangs) {
        $activeClass = if($l -eq $activeLang) { ' active' } else { '' }
        $href = if($l -eq 'tr') { '/blog/' } else { "/blog/$l/" }
        $buttons += "<a href=`"$href`" class=`"lang-btn$activeClass`">$($l.ToUpper())</a>"
    }
    return $buttons -join ''
}

function Build-Cards($lang) {
    $t = $allTranslations[$lang]
    $cards = @()
    foreach($p in $posts) {
        $n = $p.n
        $slug = $p.slug
        $titleKey = "post${n}_title"
        $descKey = "post${n}_desc"
        $tagKey = $p.tagKey
        
        $title = if($t[$titleKey]) { $t[$titleKey] } else { "Post $n" }
        $desc = if($t[$descKey]) { $t[$descKey] } else { '' }
        $tag = if($t[$tagKey]) { $t[$tagKey] } else { '' }
        $readMore = $readMoreTexts[$lang]
        
        # Tarih çevirisi
        $date = $p.date
        if($lang -ne 'tr' -and $months[$lang]) {
            foreach($trMonth in $months[$lang].Keys) {
                $date = $date -replace $trMonth, $months[$lang][$trMonth]
            }
        }
        
        # Okuma süresi
        $rt = $readTimes[$n]
        $readTimeText = "⏱️ $rt dk okuma"
        if($lang -ne 'tr' -and $readTimeLabels[$lang] -and $readTimeLabels[$lang][$rt]) {
            $readTimeText = "⏱️ $($readTimeLabels[$lang][$rt])"
        }
        
        # Kart linki — kendi diline!
        $cardHref = if($lang -eq 'tr') { "/blog/$slug.html" } else { "/blog/$lang/$slug.html" }
        
        $card = @"

  <article class="blog-card">
    <div class="blog-card-meta">
      <span class="blog-card-tag">$tag</span>
      <span>📅 $date</span>
      <span>$readTimeText</span>
    </div>
    <h2><a href="$cardHref">$title</a></h2>
    <p>$desc</p>
    <a href="$cardHref" class="read-more">$readMore</a>
  </article>
"@
        $cards += $card
    }
    return $cards -join "`n"
}

# ========== 8 DİL SAYFASI ÜRET ==========
$created = 0
foreach($lang in $langs.Keys) {
    $cfg = $langs[$lang]
    $t = $allTranslations[$lang]
    $canonical = "https://kilmanbilisim.com/blog/$lang/"
    $blogTitle = if($t['blog_title']) { $t['blog_title'] } else { 'Blog' }
    $blogSub = if($heroSub[$lang]) { $heroSub[$lang] } else { $heroSub['en'] }
    $homeLabel = $navHome[$lang]
    $footerR = $footerRights[$lang]
    $privacyL = $privacyTexts[$lang]
    $langButtons = Build-LangButtons $lang
    $cards = Build-Cards $lang

    $html = @"
<!DOCTYPE html>
<html lang="$lang">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>$($cfg.title)</title>
<meta name="description" content="$($cfg.desc)"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="$canonical"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="$canonical"/>
<meta property="og:title" content="$($cfg.title)"/>
<meta property="og:description" content="$($cfg.desc)"/>
<meta property="og:locale" content="$($cfg.locale)"/>
<meta property="og:image" content="https://kilmanbilisim.com/og-image.jpg"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="$($cfg.title)"/>
<meta name="twitter:description" content="$($cfg.desc)"/>
<meta name="twitter:image" content="https://kilmanbilisim.com/og-image.jpg"/>
$hreflangBlock
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
<style>
$css
</style>
</head>
<body>

<nav class="blog-nav">
  <div class="blog-nav-inner">
    <div class="blog-nav-left">
      <a href="/" class="blog-nav-logo">KILMAN<span style="display:block;font-size:0.75rem;color:var(--text-muted);letter-spacing:0.08em;">BİLİŞİM</span></a>
    </div>
    <ul class="blog-nav-links">
      <li style="list-style:none;"><a href="/">$homeLabel</a></li>
      <li style="list-style:none;"><a href="/blog/$lang/" class="active">Blog</a></li>
    </ul>
    <div class="blog-nav-right">
      <div class="blog-lang">
        $langButtons
      </div>
      <button class="blog-hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</nav>

<div class="blog-hero">
  <h1>$blogTitle</h1>
  <p>$blogSub</p>
</div>

<div class="blog-grid">
$cards
</div>

<footer class="blog-footer">
<div style="text-align:center; margin-bottom:12px; font-size:0.9rem; color:#00D4FF;">
  👥 <span id="lcTotalFooter">—</span> &nbsp;·&nbsp; <span style="color:#22c55e;">●</span> <span id="lcOnlineFooter">—</span>
</div>
  <p>© <script>document.write(new Date().getFullYear())</script> Kılman Bilişim Sistemleri Ltd. Şti. $footerR</p>
  <p style="margin-top:8px;"><a href="/gizlilik.html" style="color:#8B949E;font-size:0.82rem;">$privacyL</a></p>
</footer>

<script>
// Hamburger toggle
const blogHamburger = document.querySelector('.blog-hamburger');
const blogNavLinks = document.querySelector('.blog-nav-links');
const blogLang = document.querySelector('.blog-lang');
if (blogHamburger) {
  blogHamburger.addEventListener('click', () => {
    const isOpen = !blogNavLinks.classList.contains('open');
    blogNavLinks.classList.toggle('open', isOpen);
    blogLang && blogLang.classList.toggle('open', isOpen);
    const spans = blogHamburger.querySelectorAll('span');
    blogHamburger.classList.toggle('active', isOpen);
    if (isOpen) {
      spans[0].style.transform = 'rotate(45deg) translate(5px,5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px,-5px)';
      requestAnimationFrame(() => {
        if (blogLang) { blogNavLinks.style.top = (70 + blogLang.offsetHeight) + 'px'; }
        else { blogNavLinks.style.top = '70px'; }
      });
    } else {
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
      blogNavLinks.style.top = '';
    }
  });
  window.addEventListener('scroll', () => {
    if (blogNavLinks.classList.contains('open')) {
      blogNavLinks.classList.remove('open');
      blogLang && blogLang.classList.remove('open');
      blogHamburger.classList.remove('active');
      blogHamburger.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }
  });
}
</script>

$supabaseBlock
</body>
</html>
"@

    $outDir = Join-Path $blogDir $lang
    if(-not (Test-Path $outDir)) { New-Item -Path $outDir -ItemType Directory -Force | Out-Null }
    $outFile = Join-Path $outDir "index.html"
    [System.IO.File]::WriteAllText($outFile, $html, [System.Text.Encoding]::UTF8)
    $created++
    Write-Output "URETILDI: /blog/$lang/index.html"
}

Write-Output "`n$created dil liste sayfasi uretildi."
