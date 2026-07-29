# gen_lang_pages.ps1 — Faz 2 Dil Sayfası Üreteci
# Kullanım: .\gen_lang_pages.ps1 -Slug "yapay-zeka-ile-restoran-otomasyonu"
# Her çağrıda 1 yazı için 8 dil sayfası üretir + TR dosyasını temizler

param(
    [Parameter(Mandatory=$true)]
    [string]$Slug
)

$ErrorActionPreference = 'Stop'
$blogDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$srcFile = Join-Path $blogDir "$Slug.html"

if(-not (Test-Path $srcFile)) { Write-Error "Kaynak dosya bulunamadi: $srcFile"; exit 1 }

$src = [System.IO.File]::ReadAllText($srcFile, [System.Text.Encoding]::UTF8)
$langs = @('tr','en','de','es','fr','ru','ko','zh','ja')
$otherLangs = @('en','de','es','fr','ru','ko','zh','ja')

# og:locale map
$localeMap = @{
    'tr'='tr_TR'; 'en'='en_US'; 'de'='de_DE'; 'es'='es_ES';
    'fr'='fr_FR'; 'ru'='ru_RU'; 'ko'='ko_KR'; 'zh'='zh_CN'; 'ja'='ja_JP'
}

# Footer rights translations
$footerRights = @{
    'tr'='Tüm hakları saklıdır.'; 'en'='All rights reserved.'; 'de'='Alle Rechte vorbehalten.';
    'es'='Todos los derechos reservados.'; 'fr'='Tous droits réservés.';
    'ru'='Все права защищены.'; 'ko'='모든 권리 보유.'; 'zh'='版权所有。'; 'ja'='全著作権所有。'
}
$privacyText = @{
    'tr'='Gizlilik Politikası'; 'en'='Privacy Policy'; 'de'='Datenschutz';
    'es'='Política de Privacidad'; 'fr'='Politique de Confidentialité';
    'ru'='Политика конфиденциальности'; 'ko'='개인정보 처리방침'; 'zh'='隐私政策'; 'ja'='プライバシーポリシー'
}
$navHome = @{
    'tr'='Ana Sayfa'; 'en'='Home'; 'de'='Startseite'; 'es'='Inicio';
    'fr'='Accueil'; 'ru'='Главная'; 'ko'='홈'; 'zh'='首页'; 'ja'='ホーム'
}

# ====== STEP 1: Parse language blocks ======
# Support both <div class="lang-content"...> and <article class="lang-content"...>
$blocks = @{}
$isArticle = $src -match '<article class="lang-content'

foreach($lang in $langs) {
    if($isArticle) {
        # Article: <article class="lang-content active" data-content-lang="tr"> ... </article>
        # or <article class="lang-content" data-content-lang="xx"> ... </article>
        $pattern = '<article class="lang-content[^"]*"\s+data-content-lang="' + $lang + '">(.*?)</article>'
    } else {
        # Div: <div class="lang-content" data-content-lang="xx"> ... </div>
        # Also matches <div class="lang-content active" data-content-lang="xx">
        $pattern = '<div class="lang-content[^"]*"\s+data-content-lang="' + $lang + '">(.*?)</div>\s*(?=<!--|\s*<div class="lang-content"|<footer)'
    }
    $m = [regex]::Match($src, $pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
    if($m.Success) {
        $blocks[$lang] = $m.Groups[1].Value.Trim()
    } else {
        Write-Warning "BLOK BULUNAMADI: $lang in $Slug"
    }
}

Write-Output "AYRISTIRICI: $($blocks.Count)/9 blok okundu (article=$isArticle)"
if($blocks.Count -ne 9) { Write-Error "9 blok beklendi, $($blocks.Count) bulundu. DURUYORUM."; exit 1 }

# ====== STEP 2: Extract per-lang metadata from blocks ======
function Get-BlockMeta($blockHtml, $lang) {
    $meta = @{}
    # Title from h1
    if($blockHtml -match [regex]'<h1>(.*?)</h1>') { $meta['title'] = $Matches[1] -replace '<[^>]+>','' -replace ([regex]::Escape('&amp;')),'&' }
    # Tag from post-tag or .tag span
    if($blockHtml -match [regex]'class="post-tag">(.*?)</span>') { $meta['tag'] = $Matches[1] }
    elseif($blockHtml -match [regex]'class="tag">(.*?)</span>') { $meta['tag'] = $Matches[1] }
    # Date from post-meta or .meta
    if($blockHtml -match [regex]'class="post-meta"[^>]*>(.*?)</div>') { $meta['metaLine'] = $Matches[1] }
    elseif($blockHtml -match [regex]'class="meta"[^>]*>(.*?)</div>') { $meta['metaLine'] = $Matches[1] }
    # Description = first <p> text (trimmed)
    if($blockHtml -match [regex]'<p[^>]*>(.*?)</p>') {
        $desc = $Matches[1] -replace '<[^>]+>','' -replace ([regex]::Escape('&amp;')),'&'
        if($desc.Length -gt 160) { $desc = $desc.Substring(0, 157) + '...' }
        $meta['description'] = $desc
    }
    return $meta
}

# ====== STEP 3: Get original head metadata ======
# Published time
$publishedTime = '2026-07-29'
if($src -match 'article:published_time"\s+content="([^"]+)"') { $publishedTime = $Matches[1] -replace 'T.*$','' }

# Original CSS (style block)
$cssBlock = ''
if($src -match '(<style>.*?</style>)') {
    $cssBlock = $Matches[1]
    # For article template, we keep article-specific CSS
}

# Determine which CSS/layout to use — pilot (new) template
# We'll use the pilot's CSS for div-template posts, and keep article CSS for article posts
$pilotCss = ''
$pilotRef = Join-Path $blogDir "en\yapay-zeka-ile-lojistik-kargo-otomasyonu.html"
if(Test-Path $pilotRef) {
    $pilotSrc = [System.IO.File]::ReadAllText($pilotRef, [System.Text.Encoding]::UTF8)
    if($pilotSrc -match '(<style>.*?</style>)') { $pilotCss = $Matches[1] }
}

# ====== STEP 4: Build hamburger + supabase scripts (from pilot) ======
$hamburgerJs = @'
<script>
const bh=document.querySelector('.blog-hamburger'),bnl=document.querySelector('.blog-nav-links'),bl=document.querySelector('.blog-lang');
if(bh){bh.addEventListener('click',()=>{const o=!bnl.classList.contains('open');bnl.classList.toggle('open',o);bl&&bl.classList.toggle('open',o);const s=bh.querySelectorAll('span');bh.classList.toggle('active',o);if(o){s[0].style.transform='rotate(45deg) translate(5px,5px)';s[1].style.opacity='0';s[2].style.transform='rotate(-45deg) translate(5px,-5px)';requestAnimationFrame(()=>{bnl.style.top=bl?(70+bl.offsetHeight)+'px':'70px';});}else{s.forEach(x=>{x.style.transform='';x.style.opacity='';});bnl.style.top='';}});window.addEventListener('scroll',()=>{if(bnl.classList.contains('open')){bnl.classList.remove('open');bl&&bl.classList.remove('open');bh.classList.remove('active');bh.querySelectorAll('span').forEach(x=>{x.style.transform='';x.style.opacity='';});}});}
</script>
'@

$supabaseJs = @'
<script>
(function(){const SUPABASE_URL='https://glpwxyaqcaqyiupesyay.supabase.co';const SUPABASE_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdscHd4eWFxY2FxeWl1cGVzeWF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE3NDU1NDIsImV4cCI6MjA5NzMyMTU0Mn0.iuK71d5caVQzpRWAA0rfMy24Ne5KGsie9T7F6Ku5M5g';function rpc(fn,body){return fetch(SUPABASE_URL+'/rest/v1/rpc/'+fn,{method:'POST',headers:{'apikey':SUPABASE_KEY,'Authorization':'Bearer '+SUPABASE_KEY,'Content-Type':'application/json'},body:JSON.stringify(body||{})}).then(r=>r.ok?r.json():null);}function fmt(n){return(typeof n==='number')?n.toLocaleString('tr-TR'):n;}let vid=sessionStorage.getItem('kb_vid');if(!vid){vid='v_'+Date.now()+'_'+Math.random().toString(36).slice(2,9);sessionStorage.setItem('kb_vid',vid);}const _p=new URLSearchParams(location.search);if(_p.get('dev')==='1')localStorage.setItem('kb_ignore','1');const isInternal=navigator.webdriver||localStorage.getItem('kb_ignore')==='1';const elTF=document.getElementById('lcTotalFooter');const elOF=document.getElementById('lcOnlineFooter');function setT(v){const t=fmt(v);if(elTF)elTF.textContent=t;}function setO(v){const t=fmt(v);if(elOF)elOF.textContent=t;}if(isInternal){rpc('get_total').then(t=>{if(t!=null)setT(t);}).catch(()=>{});}else if(!sessionStorage.getItem('kb_counted')){rpc('increment_visit').then(t=>{sessionStorage.setItem('kb_counted','1');if(t!=null)setT(t);}).catch(()=>{});}else{rpc('get_total').then(t=>{if(t!=null)setT(t);}).catch(()=>{});}function beat(){rpc('heartbeat',{p_vid:vid}).then(o=>{if(o!=null)setO(o);}).catch(()=>{});}if(!isInternal){beat();setInterval(beat,20000);}else{const ro=()=>rpc('get_online').then(o=>{if(o!=null)setO(o);}).catch(()=>{});ro();setInterval(ro,20000);}})();
</script>
'@

# ====== STEP 5: hreflang block ======
function Get-Hreflang($slug) {
    $lines = @()
    $lines += "<link rel=""alternate"" hreflang=""tr"" href=""https://kilmanbilisim.com/blog/$slug.html""/>"
    foreach($l in $otherLangs) {
        $lines += "<link rel=""alternate"" hreflang=""$l"" href=""https://kilmanbilisim.com/blog/$l/$slug.html""/>"
    }
    $lines += "<link rel=""alternate"" hreflang=""x-default"" href=""https://kilmanbilisim.com/blog/$slug.html""/>"
    return $lines -join "`n"
}

# ====== STEP 6: Language selector nav ======
function Get-LangNav($slug, $activeLang) {
    $btns = @()
    # TR link (root)
    $trActive = if($activeLang -eq 'tr') { ' active' } else { '' }
    $btns += "<a href=""/blog/$slug.html"" class=""lang-btn$trActive"">TR</a>"
    foreach($l in $otherLangs) {
        $lUpper = $l.ToUpper()
        $cls = if($l -eq $activeLang) { ' active' } else { '' }
        $btns += "<a href=""/blog/$l/$slug.html"" class=""lang-btn$lUpper$cls"">$lUpper</a>"
    }
    return $btns -join ''
}

# Fix: lang-btn class shouldn't include uppercase lang
function Get-LangNav2($slug, $activeLang) {
    $btns = @()
    $trActive = if($activeLang -eq 'tr') { ' active' } else { '' }
    $btns += "<a href=""/blog/$slug.html"" class=""lang-btn$trActive"">TR</a>"
    foreach($l in $otherLangs) {
        $lUpper = $l.ToUpper()
        $cls = if($l -eq $activeLang) { ' active' } else { '' }
        $btns += "<a href=""/blog/$l/$slug.html"" class=""lang-btn$cls"">$lUpper</a>"
    }
    return $btns -join ''
}

# ====== STEP 7: Generate language pages ======
foreach($lang in $otherLangs) {
    $langDir = Join-Path $blogDir $lang
    if(-not (Test-Path $langDir)) { New-Item -ItemType Directory -Path $langDir -Force | Out-Null }
    
    $outFile = Join-Path $langDir "$Slug.html"
    $blockContent = $blocks[$lang]
    $meta = Get-BlockMeta $blockContent $lang
    
    $title = "$($meta['title']) — Kılman Bilişim"
    $desc = $meta['description']
    $canonical = "https://kilmanbilisim.com/blog/$lang/$Slug.html"
    $locale = $localeMap[$lang]
    $hreflang = Get-Hreflang $Slug
    $langNavHtml = Get-LangNav2 $Slug $lang
    
    # Build body content based on template type
    if($isArticle) {
        # Article template — content already has <header> and content inside <article>
        # We need to wrap in new-style layout (header + main)
        # Extract header and body from article content
        $headerMatch = [regex]::Match($blockContent, '<header>(.*?)</header>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
        $bodyAfterHeader = $blockContent
        if($headerMatch.Success) {
            $headerInner = $headerMatch.Groups[1].Value.Trim()
            $bodyAfterHeader = $blockContent.Substring($headerMatch.Index + $headerMatch.Length).Trim()
            # Convert old header format to new
            $headerHtml = "<header class=""post-header"">$headerInner</header>"
            # Replace .tag with .post-tag
            $headerHtml = $headerHtml -replace 'class="tag"', 'class="post-tag"'
            # Replace .meta with .post-meta
            $headerHtml = $headerHtml -replace 'class="meta"', 'class="post-meta"'
        } else {
            $headerHtml = ''
        }
        $mainBody = "<main class=""post-content"">`n$bodyAfterHeader`n</main>"
        $contentHtml = "$headerHtml`n$mainBody"
    } else {
        # Div template — content has <header class="post-header"> and <main class="post-content">
        $contentHtml = $blockContent
    }
    
    # Use pilot CSS for new pages (standardized)
    $useCss = if($pilotCss) { $pilotCss } else { $cssBlock }
    
    # Build JSON-LD
    $titleClean = ($meta['title'] -replace '"','\"')
    $descClean = ($desc -replace '"','\"')
    $jsonLd = @"
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "$titleClean",
  "description": "$descClean",
  "author": {"@type": "Organization", "name": "Kılman Bilişim Sistemleri", "url": "https://kilmanbilisim.com/"},
  "publisher": {"@type": "Organization", "name": "Kılman Bilişim Sistemleri", "logo": {"@type": "ImageObject", "url": "https://kilmanbilisim.com/logo.png"}},
  "datePublished": "$publishedTime",
  "dateModified": "$publishedTime",
  "mainEntityOfPage": {"@type": "WebPage", "@id": "$canonical"},
  "image": "https://kilmanbilisim.com/og-image.jpg",
  "inLanguage": "$lang",
  "url": "$canonical"
}
</script>
"@

    $titleEsc = $title -replace '&','&amp;'
    $descEsc = $desc -replace '&','&amp;'
    $ogTitle = $meta['title'] -replace '&','&amp;'
    
    $page = @"
<!DOCTYPE html>
<html lang="$lang">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>$titleEsc</title>
<meta name="description" content="$descEsc"/>
<meta name="author" content="Kılman Bilişim Sistemleri"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="$canonical"/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="$canonical"/>
<meta property="og:title" content="$ogTitle"/>
<meta property="og:description" content="$descEsc"/>
<meta property="og:locale" content="$locale"/>
<meta property="og:image" content="https://kilmanbilisim.com/og-image.jpg"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="$ogTitle"/>
<meta name="twitter:description" content="$descEsc"/>
<meta name="twitter:image" content="https://kilmanbilisim.com/og-image.jpg"/>
<meta property="article:published_time" content="$publishedTime"/>
$hreflang
$jsonLd
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
$useCss
</head>
<body>
<nav class="blog-nav"><div class="blog-nav-inner"><div class="blog-nav-left"><a href="/" class="blog-nav-logo">Kılman Bilişim</a><div class="blog-nav-links"><a href="/">$($navHome[$lang])</a><a href="/blog/" class="active">Blog</a></div></div><div class="blog-nav-right"><div class="blog-lang">$langNavHtml</div><div class="blog-hamburger" aria-label="Menu"><span></span><span></span><span></span></div></div></div></nav>

$contentHtml

<footer class="blog-footer">
<div style="text-align:center;margin-bottom:12px;font-size:0.9rem;color:#00D4FF;">👥 <span id="lcTotalFooter">—</span> &nbsp;·&nbsp; <span style="color:#22c55e;">●</span> <span id="lcOnlineFooter">—</span></div>
  <p>© <script>document.write(new Date().getFullYear())</script> Kılman Bilişim Sistemleri Ltd. Şti. $($footerRights[$lang])</p>
  <p style="margin-top:8px;"><a href="/gizlilik.html" style="color:#8B949E;font-size:0.82rem;">$($privacyText[$lang])</a></p>
</footer>
$hamburgerJs
$supabaseJs
</body>
</html>
"@

    [System.IO.File]::WriteAllText($outFile, $page, [System.Text.Encoding]::UTF8)
    Write-Output "URETILDI: $lang/$Slug.html"
}

# ====== STEP 8: Clean TR file ======
Write-Output "`nTR TEMIZLEME BASLIYOR: $Slug"

# Build new TR page with only TR content
$trMeta = Get-BlockMeta $blocks['tr'] 'tr'
$trHreflang = Get-Hreflang $Slug
$trLangNav = Get-LangNav2 $Slug 'tr'
$trCanonical = "https://kilmanbilisim.com/blog/$Slug.html"

if($isArticle) {
    $trBlock = $blocks['tr']
    $trHeaderMatch = [regex]::Match($trBlock, '<header>(.*?)</header>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    if($trHeaderMatch.Success) {
        $trHeaderInner = $trHeaderMatch.Groups[1].Value.Trim()
        $trBodyAfterHeader = $trBlock.Substring($trHeaderMatch.Index + $trHeaderMatch.Length).Trim()
        $trHeaderHtml = "<header class=""post-header"">$trHeaderInner</header>"
        $trHeaderHtml = $trHeaderHtml -replace 'class="tag"', 'class="post-tag"'
        $trHeaderHtml = $trHeaderHtml -replace 'class="meta"', 'class="post-meta"'
    } else {
        $trHeaderHtml = ''
        $trBodyAfterHeader = $trBlock
    }
    $trContentHtml = "$trHeaderHtml`n<main class=""post-content"">`n$trBodyAfterHeader`n</main>"
} else {
    $trContentHtml = $blocks['tr']
}

# Keep original TR head metadata (title, desc, etc.)
$trTitle = ''
if($src -match '<title>(.*?)</title>') { $trTitle = $Matches[1] }
$trDesc = ''
if($src -match '<meta name="description" content="(.*?)"') { $trDesc = $Matches[1] }
$trKeywords = ''
if($src -match '<meta name="keywords" content="(.*?)"') { $trKeywords = $Matches[1] }
$trOgTitle = ''
if($src -match 'og:title" content="(.*?)"') { $trOgTitle = $Matches[1] }
$trOgDesc = ''
if($src -match 'og:description" content="(.*?)"') { $trOgDesc = $Matches[1] }
$trTwTitle = ''
if($src -match 'twitter:title" content="(.*?)"') { $trTwTitle = $Matches[1] }
$trTwDesc = ''
if($src -match 'twitter:description" content="(.*?)"') { $trTwDesc = $Matches[1] }

# Original JSON-LD
$trJsonLd = ''
if($src -match '(<script type="application/ld\+json">.*?</script>)') { $trJsonLd = $Matches[1] }

# Use pilot CSS
$trUseCss = if($pilotCss) { $pilotCss } else { $cssBlock }

# Keywords line
$kwLine = ''
if($trKeywords) { $kwLine = "<meta name=""keywords"" content=""$trKeywords""/>" }

$trPage = @"
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>$trTitle</title>
<meta name="description" content="$trDesc"/>
$kwLine
<meta name="author" content="Kılman Bilişim Sistemleri"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="$trCanonical"/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="$trCanonical"/>
<meta property="og:title" content="$trOgTitle"/>
<meta property="og:description" content="$trOgDesc"/>
<meta property="og:locale" content="tr_TR"/>
<meta property="og:image" content="https://kilmanbilisim.com/og-image.jpg"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="$trTwTitle"/>
<meta name="twitter:description" content="$trTwDesc"/>
<meta name="twitter:image" content="https://kilmanbilisim.com/og-image.jpg"/>
<meta property="article:published_time" content="$publishedTime"/>
$trHreflang
$trJsonLd
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
$trUseCss
</head>
<body>
<nav class="blog-nav"><div class="blog-nav-inner"><div class="blog-nav-left"><a href="/" class="blog-nav-logo">Kılman Bilişim</a><div class="blog-nav-links"><a href="/">Ana Sayfa</a><a href="/blog/" class="active">Blog</a></div></div><div class="blog-nav-right"><div class="blog-lang">$trLangNav</div><div class="blog-hamburger" aria-label="Menü"><span></span><span></span><span></span></div></div></div></nav>

$trContentHtml

<footer class="blog-footer">
<div style="text-align:center;margin-bottom:12px;font-size:0.9rem;color:#00D4FF;">👥 <span id="lcTotalFooter">—</span> &nbsp;·&nbsp; <span style="color:#22c55e;">●</span> <span id="lcOnlineFooter">—</span></div>
  <p>© <script>document.write(new Date().getFullYear())</script> Kılman Bilişim Sistemleri Ltd. Şti. Tüm hakları saklıdır.</p>
  <p style="margin-top:8px;"><a href="/gizlilik.html" style="color:#8B949E;font-size:0.82rem;">Gizlilik Politikası</a></p>
</footer>
$hamburgerJs
$supabaseJs
</body>
</html>
"@

[System.IO.File]::WriteAllText($srcFile, $trPage, [System.Text.Encoding]::UTF8)
Write-Output "TR TEMIZLENDI: $Slug.html (sadece TR icerigi kaldi)"
Write-Output "`nTAMAM: $Slug icin 8 dil sayfasi uretildi + TR temizlendi"
