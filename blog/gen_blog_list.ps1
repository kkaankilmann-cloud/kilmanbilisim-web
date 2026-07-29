#!/usr/bin/env pwsh
# gen_blog_list.ps1 — Blog liste sayfasi ureteci
# Kullanim: powershell -ExecutionPolicy Bypass -File gen_blog_list.ps1
# TR index.html'den okur, 8 dil sayfasi uretir, TR'yi gunceller

$ErrorActionPreference = 'Stop'
$blogDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# ─── TR INDEX.HTML OKU ───
$trFile = Join-Path $blogDir 'index.html'
$trContent = [System.IO.File]::ReadAllText($trFile, [System.Text.Encoding]::UTF8)

# ─── i18n SOZLUGUNU CIKAR ───
# blogTranslations objesini regex ile parse et
$langs = @('tr','en','de','es','fr','ru','ko','zh','ja')
$i18n = @{}

foreach ($lang in $langs) {
    $pattern = "(?s)$lang\s*:\s*\{(.*?)\n\s*\},"
    if ($lang -eq 'ja') { $pattern = "(?s)$lang\s*:\s*\{(.*?)\n\s*\}" }
    $m = [regex]::Match($trContent, $pattern)
    if ($m.Success) {
        $block = $m.Groups[1].Value
        $dict = @{}
        # Her satirdaki key: 'value' cifti
        $entries = [regex]::Matches($block, "(\w+)\s*:\s*'((?:[^'\\]|\\.)*)'")
        foreach ($e in $entries) {
            $key = $e.Groups[1].Value
            $val = $e.Groups[2].Value -replace "\\'", "'"
            $dict[$key] = $val
        }
        $i18n[$lang] = $dict
        Write-Host "  $lang : $($dict.Count) anahtar"
    } else {
        Write-Host "  UYARI: $lang sozlugu bulunamadi!" -ForegroundColor Red
    }
}

# ─── KART BILGILERI — TR KARTLARINDAN CIKAR ───
$cardPattern = '(?s)<article class="blog-card">(.*?)</article>'
$cardMatches = [regex]::Matches($trContent, $cardPattern)
Write-Host "`nKart sayisi: $($cardMatches.Count)"

$cards = @()
foreach ($cm in $cardMatches) {
    $cardHtml = $cm.Value
    # Slug
    $slugMatch = [regex]::Match($cardHtml, 'href="/blog/([^"]+)\.html"')
    $slug = if ($slugMatch.Success) { $slugMatch.Groups[1].Value } else { '' }
    # Tag i18n key
    $tagMatch = [regex]::Match($cardHtml, 'data-i18n="(tag_\w+)"')
    $tagKey = if ($tagMatch.Success) { $tagMatch.Groups[1].Value } else { '' }
    # Post number from title key
    $titleMatch = [regex]::Match($cardHtml, 'data-i18n="(post\d+_title)"')
    $titleKey = if ($titleMatch.Success) { $titleMatch.Groups[1].Value } else { '' }
    $descMatch = [regex]::Match($cardHtml, 'data-i18n="(post\d+_desc)"')
    $descKey = if ($descMatch.Success) { $descMatch.Groups[1].Value } else { '' }
    # Date
    $dateMatch = [regex]::Match($cardHtml, [regex]::Escape('📅') + '\s*(.+?)</span>')
    $dateStr = if ($dateMatch.Success) { $dateMatch.Groups[1].Value.Trim() } else { '' }
    # Read time key
    $readMatch = [regex]::Match($cardHtml, 'data-i18n="(read_\d+)"')
    $readKey = if ($readMatch.Success) { $readMatch.Groups[1].Value } else { '' }
    # Read more key
    $rmKey = 'read_more'

    $cards += [PSCustomObject]@{
        Slug     = $slug
        TagKey   = $tagKey
        TitleKey = $titleKey
        DescKey  = $descKey
        Date     = $dateStr
        ReadKey  = $readKey
        RmKey    = $rmKey
    }
}

# ─── CSS CIKAR (style tag arasi) ───
$cssMatch = [regex]::Match($trContent, '(?s)<style>(.*?)</style>')
$cssBlock = if ($cssMatch.Success) { $cssMatch.Groups[1].Value } else { '' }

# lang-btn CSS'i ekle (button yerine a icin)
$langBtnCss = @"
.blog-lang a.lang-btn{display:inline-block;background:transparent;border:1px solid var(--border);color:var(--text-muted);padding:4px 10px;border-radius:6px;font-size:0.75rem;font-weight:600;font-family:'Inter',sans-serif;text-decoration:none;transition:all 0.2s;}
.blog-lang a.lang-btn:hover{border-color:var(--neon);color:var(--neon);opacity:1;}
.blog-lang a.lang-btn.active{background:var(--neon);color:var(--bg-main);border-color:var(--neon);}
"@

# ─── SUPABASE SAYAC KODU ───
$supabaseJs = @'
<script>
(function(){
  const SUPABASE_URL = 'https://glpwxyaqcaqyiupesyay.supabase.co';
  const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdscHd4eWFxY2FxeWl1cGVzeWF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE3NDU1NDIsImV4cCI6MjA5NzMyMTU0Mn0.iuK71d5caVQzpRWAA0rfMy24Ne5KGsie9T7F6Ku5M5g';
  function rpc(fn, body){
    return fetch(SUPABASE_URL + '/rest/v1/rpc/' + fn, {
      method: 'POST', headers: { 'apikey': SUPABASE_KEY, 'Authorization': 'Bearer ' + SUPABASE_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify(body || {})
    }).then(r => r.ok ? r.json() : null);
  }
  function fmt(n){ return (typeof n === 'number') ? n.toLocaleString('tr-TR') : n; }
  let vid = sessionStorage.getItem('kb_vid');
  if(!vid){ vid = 'v_' + Date.now() + '_' + Math.random().toString(36).slice(2,9); sessionStorage.setItem('kb_vid', vid); }
  const _p = new URLSearchParams(location.search);
  if (_p.get('dev') === '1') localStorage.setItem('kb_ignore', '1');
  const isInternal = navigator.webdriver || localStorage.getItem('kb_ignore') === '1';
  const elTotalF = document.getElementById('lcTotalFooter');
  const elOnlineF = document.getElementById('lcOnlineFooter');
  function setTotal(v){ const t = fmt(v); if(elTotalF) elTotalF.textContent = t; }
  function setOnline(v){ const t = fmt(v); if(elOnlineF) elOnlineF.textContent = t; }
  if (isInternal) {
    rpc('get_total').then(total => { if (total != null) setTotal(total); }).catch(()=>{});
  } else if (!sessionStorage.getItem('kb_counted')) {
    rpc('increment_visit').then(total => { sessionStorage.setItem('kb_counted', '1'); if (total != null) setTotal(total); }).catch(()=>{});
  } else {
    rpc('get_total').then(total => { if (total != null) setTotal(total); }).catch(()=>{});
  }
  function beat(){ rpc('heartbeat', { p_vid: vid }).then(online => { if(online != null) setOnline(online); }).catch(()=>{}); }
  if (!isInternal) { beat(); setInterval(beat, 20000); }
  else { const readOnline = () => rpc('get_online').then(online => { if (online != null) setOnline(online); }).catch(()=>{}); readOnline(); setInterval(readOnline, 20000); }
})();
</script>
'@

# ─── HREFLANG BLOGU ───
$baseUrl = 'https://kilmanbilisim.com'
function Get-HreflangBlock {
    $lines = @()
    $lines += "<link rel=`"alternate`" hreflang=`"tr`" href=`"$baseUrl/blog/`"/>"
    foreach ($l in @('en','de','es','fr','ru','ko','zh','ja')) {
        $lines += "<link rel=`"alternate`" hreflang=`"$l`" href=`"$baseUrl/blog/$l/`"/>"
    }
    $lines += "<link rel=`"alternate`" hreflang=`"x-default`" href=`"$baseUrl/blog/`"/>"
    return $lines -join "`n"
}

# ─── OG:LOCALE MAP ───
$localeMap = @{
    'tr' = 'tr_TR'; 'en' = 'en_US'; 'de' = 'de_DE'; 'es' = 'es_ES'
    'fr' = 'fr_FR'; 'ru' = 'ru_RU'; 'ko' = 'ko_KR'; 'zh' = 'zh_CN'; 'ja' = 'ja_JP'
}

# ─── LANG-BTN NAV ───
function Get-LangNav($activeLang) {
    $btns = @()
    foreach ($l in $langs) {
        $cls = if ($l -eq $activeLang) { ' active' } else { '' }
        $href = if ($l -eq 'tr') { '/blog/' } else { "/blog/$l/" }
        $btns += "<a href=`"$href`" class=`"lang-btn$cls`">$($l.ToUpper())</a>"
    }
    return $btns -join ''
}

# ─── KART HTML URET ───
function Get-CardHtml($lang, $card) {
    $dict = $i18n[$lang]
    if (-not $dict) { return '' }

    $tag = if ($dict[$card.TagKey]) { $dict[$card.TagKey] } else { $card.TagKey }
    $title = if ($dict[$card.TitleKey]) { $dict[$card.TitleKey] } else { $card.TitleKey }
    $desc = if ($dict[$card.DescKey]) { $dict[$card.DescKey] } else { $card.DescKey }
    $readTime = if ($dict[$card.ReadKey]) { $dict[$card.ReadKey] } else { $card.ReadKey }
    $readMore = if ($dict[$card.RmKey]) { $dict[$card.RmKey] } else { 'Read More' }

    # Kart linki: kendi diline
    $href = if ($lang -eq 'tr') { "/blog/$($card.Slug).html" } else { "/blog/$lang/$($card.Slug).html" }

    return @"
  <article class="blog-card">
    <div class="blog-card-meta">
      <span class="blog-card-tag">$tag</span>
      <span>📅 $($card.Date)</span>
      <span>$readTime</span>
    </div>
    <h2><a href="$href">$title</a></h2>
    <p>$desc</p>
    <a href="$href" class="read-more">$readMore</a>
  </article>
"@
}

# ─── SAYFA SABLONU ───
function Build-ListPage($lang) {
    $dict = $i18n[$lang]
    $isAlt = $lang -ne 'tr'
    $canonical = if ($isAlt) { "$baseUrl/blog/$lang/" } else { "$baseUrl/blog/" }
    $blogTitle = if ($dict['blog_title']) { $dict['blog_title'] } else { 'Blog' }
    $blogSub = if ($dict['blog_sub']) { $dict['blog_sub'] } else { '' }
    $footerRights = if ($dict['footer_rights']) { $dict['footer_rights'] } else { 'All rights reserved.' }
    $privacyLink = if ($dict['privacy_link']) { $dict['privacy_link'] } else { 'Privacy Policy' }
    $ogLocale = $localeMap[$lang]
    $navHome = if ($dict['back_home']) { ($dict['back_home'] -replace '.*\s', '') } else { 'Home' }
    $blogLinkText = 'Blog'

    # Kartlar
    $cardHtmlParts = @()
    foreach ($c in $cards) {
        $cardHtmlParts += Get-CardHtml $lang $c
    }
    $allCards = $cardHtmlParts -join "`n"

    $hreflang = Get-HreflangBlock
    $langNav = Get-LangNav $lang

    # Blog menü linki
    $blogMenuHref = if ($isAlt) { "/blog/$lang/" } else { '/blog/' }

    $html = @"
<!DOCTYPE html>
<html lang="$lang">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>$blogTitle &#8212; K&#305;lman Bili&#351;im</title>
<meta name="description" content="$blogSub"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="$canonical"/>
$hreflang
<meta property="og:type" content="website"/>
<meta property="og:url" content="$canonical"/>
<meta property="og:title" content="$blogTitle &#8212; K&#305;lman Bili&#351;im"/>
<meta property="og:description" content="$blogSub"/>
<meta property="og:locale" content="$ogLocale"/>
<meta property="og:image" content="$baseUrl/og-image.jpg"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="$blogTitle &#8212; K&#305;lman Bili&#351;im"/>
<meta name="twitter:description" content="$blogSub"/>
<meta name="twitter:image" content="$baseUrl/og-image.jpg"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
<style>
$cssBlock
$langBtnCss
</style>
</head>
<body>

<nav class="blog-nav">
  <div class="blog-nav-inner">
    <div class="blog-nav-left">
      <a href="/" class="blog-nav-logo">KILMAN<span style="display:block;font-size:0.75rem;color:var(--text-muted);letter-spacing:0.08em;">B&#304;L&#304;&#350;&#304;M</span></a>
    </div>
    <ul class="blog-nav-links">
      <li style="list-style:none;"><a href="/">$navHome</a></li>
      <li style="list-style:none;"><a href="$blogMenuHref" class="active">Blog</a></li>
    </ul>
    <div class="blog-nav-right">
      <div class="blog-lang">$langNav</div>
      <button class="blog-hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</nav>

<div class="blog-hero">
  <h1>$blogTitle</h1>
  <p>$blogSub</p>
</div>

<div class="blog-grid">
$allCards
</div>

<footer class="blog-footer">
<div style="text-align:center; margin-bottom:12px; font-size:0.9rem; color:#00D4FF;">
  <span id="lcTotalFooter">&#8212;</span> &nbsp;&#183;&nbsp; <span style="color:#22c55e;">&#9679;</span> <span id="lcOnlineFooter">&#8212;</span>
</div>
  <p>&copy; <script>document.write(new Date().getFullYear())</script> K&#305;lman Bili&#351;im Sistemleri Ltd. &#350;ti. $footerRights</p>
  <p style="margin-top:8px;"><a href="/gizlilik.html" style="color:#8B949E;font-size:0.82rem;">$privacyLink</a></p>
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
    } else {
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
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

$supabaseJs
</body>
</html>
"@
    return $html
}

# ═══════════════════════════════════════════════
# ADIM 1 — 8 dil sayfasi uret
# ═══════════════════════════════════════════════
Write-Host "`n=== ADIM 1: 8 dil liste sayfasi ===" -ForegroundColor Cyan
$altLangs = @('en','de','es','fr','ru','ko','zh','ja')
foreach ($lang in $altLangs) {
    $dir = Join-Path $blogDir $lang
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $outFile = Join-Path $dir 'index.html'
    $html = Build-ListPage $lang
    [System.IO.File]::WriteAllText($outFile, $html, [System.Text.Encoding]::UTF8)
    Write-Host "  [OK] /blog/$lang/index.html ($($html.Length) char)" -ForegroundColor Green
}

# ═══════════════════════════════════════════════
# ADIM 2 — TR liste sayfasini guncelle
# ═══════════════════════════════════════════════
Write-Host "`n=== ADIM 2: TR liste sayfasi guncelle ===" -ForegroundColor Cyan

# TR'yi yeniden uret (tum JS temizlenip basit haliyle)
$trHtml = Build-ListPage 'tr'
[System.IO.File]::WriteAllText($trFile, $trHtml, [System.Text.Encoding]::UTF8)
Write-Host "  [OK] /blog/index.html ($($trHtml.Length) char)" -ForegroundColor Green

# ═══════════════════════════════════════════════
# ADIM 3 — 232 yazi sayfasinda Blog menu linki
# ═══════════════════════════════════════════════
Write-Host "`n=== ADIM 3: 232 yazi sayfasinda Blog menu linki ===" -ForegroundColor Cyan
$fixedMenuLinks = 0
foreach ($lang in $altLangs) {
    $dir = Join-Path $blogDir $lang
    $files = Get-ChildItem $dir -Filter "*.html" | Where-Object { $_.Name -ne 'index.html' }
    foreach ($f in $files) {
        $c = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
        $newBlogHref = "/blog/$lang/"
        # Pattern: <a href="/blog/" ... >Blog</a> veya <a href="/blog/xx/" ...>Blog</a>
        $updated = $c -replace '(<a\s+href=")(/blog/(?:[a-z]{2}/)?)("\s*(?:class="[^"]*")?\s*>Blog</a>)', "`${1}$newBlogHref`${3}"
        if ($updated -ne $c) {
            [System.IO.File]::WriteAllText($f.FullName, $updated, [System.Text.Encoding]::UTF8)
            $fixedMenuLinks++
        }
    }
}
Write-Host "  [OK] $fixedMenuLinks dosyada Blog menu linki duzeltildi" -ForegroundColor Green

# ═══════════════════════════════════════════════
# ADIM 4 — Sitemap
# ═══════════════════════════════════════════════
Write-Host "`n=== ADIM 4: Sitemap ===" -ForegroundColor Cyan
$sitemapFile = Join-Path (Split-Path $blogDir) 'sitemap.xml'
$sitemapContent = [System.IO.File]::ReadAllText($sitemapFile, [System.Text.Encoding]::UTF8)
$today = Get-Date -Format 'yyyy-MM-dd'
$newEntries = ""
foreach ($lang in $altLangs) {
    $url = "$baseUrl/blog/$lang/"
    if ($sitemapContent -notmatch [regex]::Escape($url)) {
        $newEntries += @"
  <url>
    <loc>$url</loc>
    <lastmod>$today</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
"@
    }
}

if ($newEntries) {
    $sitemapContent = $sitemapContent -replace '</urlset>', "$newEntries`n</urlset>"
    [System.IO.File]::WriteAllText($sitemapFile, $sitemapContent, [System.Text.Encoding]::UTF8)
    Write-Host "  [OK] Sitemap guncellendi" -ForegroundColor Green
} else {
    Write-Host "  [SKIP] Sitemap zaten guncel" -ForegroundColor Yellow
}

# URL sayisi
$urlCount = ([regex]::Matches($sitemapContent, '<loc>')).Count
Write-Host "  Sitemap URL sayisi: $urlCount"

Write-Host "`n=== TAMAMLANDI ===" -ForegroundColor Green
Write-Host "  8 dil sayfasi + TR guncelleme + $fixedMenuLinks menu linki + sitemap"
