#!/usr/bin/env pwsh
# gen_blog_list.ps1 — Blog liste sayfasi ureteci v2
# Kullanim: powershell -ExecutionPolicy Bypass -File gen_blog_list.ps1
# TR index.html'den kartlari okur, her dilin yazi sayfasindan ceviri ceker
# Artik blogTranslations sozlugune BAGIMLI DEGIL

$ErrorActionPreference = 'Stop'
$blogDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

# ASCII olmayan karakterleri HTML entity'ye cevir (surrogate-aware)
function To-Entity([string]$s) {
    if (-not $s) { return $s }
    $sb = [System.Text.StringBuilder]::new($s.Length * 2)
    for ($i = 0; $i -lt $s.Length; $i++) {
        $c = $s[$i]
        if ([char]::IsHighSurrogate($c) -and ($i + 1) -lt $s.Length -and [char]::IsLowSurrogate($s[$i + 1])) {
            $cp = [char]::ConvertToUtf32($c, $s[$i + 1])
            [void]$sb.Append("&#$cp;")
            $i++
        }
        elseif ([int]$c -gt 127) {
            [void]$sb.Append("&#$([int]$c);")
        }
        else {
            [void]$sb.Append($c)
        }
    }
    return $sb.ToString()
}

# Meta attribute icindeki duz cift tirnaklari &quot; yap
function Escape-MetaQuotes([string]$s) {
    if (-not $s) { return $s }
    return $s.Replace('"', '&quot;')
}

# ─── STATIK METINLER (gomulu — bozulma riski sifir) ───
$statics = @{
    'tr' = @{ back_home='Ana Sayfaya D'+[char]246+'n'; blog_title='Blog'; blog_sub='Yapay zeka, otomasyon ve dijital d'+[char]246+'n'+[char]252+[char]351+[char]252+'m hakk'+[char]305+'nda g'+[char]252+'ncel yaz'+[char]305+'lar, rehberler ve sekt'+[char]246+'r analizleri.'; read_more='Devam'+[char]305+'n'+[char]305+' Oku '+[char]8594; footer_rights='T'+[char]252+'m haklar'+[char]305+' sakl'+[char]305+'d'+[char]305+'r.'; privacy_link='Gizlilik Politikas'+[char]305 }
    'en' = @{ back_home='Home'; blog_title='Blog'; blog_sub='Latest articles, guides and industry analysis on AI, automation and digital transformation.'; read_more='Read More '+[char]8594; footer_rights='All rights reserved.'; privacy_link='Privacy Policy' }
    'de' = @{ back_home='Startseite'; blog_title='Blog'; blog_sub='Aktuelle Artikel, Leitf'+[char]228+'den und Branchenanalysen zu KI, Automatisierung und digitaler Transformation.'; read_more='Weiterlesen '+[char]8594; footer_rights='Alle Rechte vorbehalten.'; privacy_link='Datenschutzrichtlinie' }
    'es' = @{ back_home='Inicio'; blog_title='Blog'; blog_sub='Art'+[char]237+'culos, gu'+[char]237+'as y an'+[char]225+'lisis del sector sobre inteligencia artificial, automatizaci'+[char]243+'n y transformaci'+[char]243+'n digital.'; read_more='Leer M'+[char]225+'s '+[char]8594; footer_rights='Todos los derechos reservados.'; privacy_link='Pol'+[char]237+'tica de Privacidad' }
    'fr' = @{ back_home='Accueil'; blog_title='Blog'; blog_sub="Articles, guides et analyses sectorielles sur l'IA, l'automatisation et la transformation num"+[char]233+"rique."; read_more='Lire la suite '+[char]8594; footer_rights='Tous droits r'+[char]233+'serv'+[char]233+'s.'; privacy_link='Politique de Confidentialit'+[char]233 }
    'ru' = @{ back_home=[char]1075+[char]1083+[char]1072+[char]1074+[char]1085+[char]1091+[char]1102; blog_title=[char]1041+[char]1083+[char]1086+[char]1075; blog_sub=[char]1057+[char]1090+[char]1072+[char]1090+[char]1100+[char]1080+', '+[char]1088+[char]1091+[char]1082+[char]1086+[char]1074+[char]1086+[char]1076+[char]1089+[char]1090+[char]1074+[char]1072+' '+[char]1080+' '+[char]1086+[char]1090+[char]1088+[char]1072+[char]1089+[char]1083+[char]1077+[char]1074+[char]1099+[char]1077+' '+[char]1086+[char]1073+[char]1079+[char]1086+[char]1088+[char]1099+' '+[char]1087+[char]1086+' '+[char]1048+[char]1048+', '+[char]1072+[char]1074+[char]1090+[char]1086+[char]1084+[char]1072+[char]1090+[char]1080+[char]1079+[char]1072+[char]1094+[char]1080+[char]1080+' '+[char]1080+' '+[char]1094+[char]1080+[char]1092+[char]1088+[char]1086+[char]1074+[char]1086+[char]1081+' '+[char]1090+[char]1088+[char]1072+[char]1085+[char]1089+[char]1092+[char]1086+[char]1088+[char]1084+[char]1072+[char]1094+[char]1080+[char]1080+'.'; read_more=[char]1063+[char]1080+[char]1090+[char]1072+[char]1090+[char]1100+' '+[char]1076+[char]1072+[char]1083+[char]1077+[char]1077+' '+[char]8594; footer_rights=[char]1042+[char]1089+[char]1077+' '+[char]1087+[char]1088+[char]1072+[char]1074+[char]1072+' '+[char]1079+[char]1072+[char]1097+[char]1080+[char]1097+[char]1077+[char]1085+[char]1099+'.'; privacy_link=[char]1055+[char]1086+[char]1083+[char]1080+[char]1090+[char]1080+[char]1082+[char]1072+' '+[char]1082+[char]1086+[char]1085+[char]1092+[char]1080+[char]1076+[char]1077+[char]1085+[char]1094+[char]1080+[char]1072+[char]1083+[char]1100+[char]1085+[char]1086+[char]1089+[char]1090+[char]1080 }
    'ko' = @{ back_home=[char]54856; blog_title=[char]48660+[char]47196+[char]44536; blog_sub='AI, '+[char]51088+[char]46041+[char]54868+' '+[char]48143+' '+[char]46356+[char]51648+[char]53560+' '+[char]51204+[char]54872+[char]50640+' '+[char]45824+[char]54620+' '+[char]52572+[char]49888+' '+[char]44592+[char]49324+', '+[char]44032+[char]51060+[char]46300+' '+[char]48143+' '+[char]50629+[char]44228+' '+[char]48516+[char]49437+'.'; read_more=[char]45908+' '+[char]51069+[char]44592+' '+[char]8594; footer_rights=[char]47784+[char]46304+' '+[char]44428+[char]47532+' '+[char]48372+[char]50976+'.'; privacy_link=[char]44060+[char]51064+[char]51221+[char]48372+' '+[char]52376+[char]47532+[char]48169+[char]52840 }
    'zh' = @{ back_home=[char]39318+[char]39029; blog_title=[char]21338+[char]23458; blog_sub=[char]20851+[char]20110+[char]20154+[char]24037+[char]26234+[char]33021+[char]12289+[char]33258+[char]21160+[char]21270+[char]21644+[char]25968+[char]23383+[char]21270+[char]36716+[char]22411+[char]30340+[char]26368+[char]26032+[char]25991+[char]31456+[char]12289+[char]25351+[char]21335+[char]21644+[char]34892+[char]19994+[char]20998+[char]26512+[char]12290; read_more=[char]38405+[char]35835+[char]26356+[char]22810+' '+[char]8594; footer_rights=[char]29256+[char]26435+[char]25152+[char]26377+[char]12290; privacy_link=[char]38544+[char]31169+[char]25919+[char]31574 }
    'ja' = @{ back_home=[char]12507+[char]12540+[char]12512; blog_title=[char]12502+[char]12525+[char]12464; blog_sub='AI'+[char]12289+[char]12458+[char]12540+[char]12488+[char]12513+[char]12540+[char]12471+[char]12519+[char]12531+[char]12289+[char]12487+[char]12472+[char]12479+[char]12523+[char]12488+[char]12521+[char]12531+[char]12473+[char]12501+[char]12457+[char]12540+[char]12513+[char]12540+[char]12471+[char]12519+[char]12531+[char]12395+[char]38306+[char]12377+[char]12427+[char]26368+[char]26032+[char]35352+[char]20107+[char]12289+[char]12460+[char]12452+[char]12489+[char]12289+[char]26989+[char]30028+[char]20998+[char]26512+[char]12290; read_more=[char]32154+[char]12365+[char]12434+[char]35501+[char]12416+' '+[char]8594; footer_rights=[char]20840+[char]33879+[char]20316+[char]27177+[char]25152+[char]26377+[char]12290; privacy_link=[char]12503+[char]12521+[char]12452+[char]12496+[char]12471+[char]12540+[char]12509+[char]12522+[char]12471+[char]12540 }
}

$langs = @('tr','en','de','es','fr','ru','ko','zh','ja')
Write-Host "Statik metinler hazir: $($statics.Count) dil"

# ─── TR INDEX.HTML OKU ───
$trFile = Join-Path $blogDir 'index.html'
$trContent = [System.IO.File]::ReadAllText($trFile, [System.Text.Encoding]::UTF8)

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
    # Tag (TR metin — entity olabilir)
    $tagMatch = [regex]::Match($cardHtml, 'blog-card-tag[^>]*>([^<]+)')
    $trTag = if ($tagMatch.Success) { $tagMatch.Groups[1].Value.Trim() } else { '' }
    # Title (TR)
    $titleMatch = [regex]::Match($cardHtml, '<h2><a[^>]+>([^<]+)</a></h2>')
    $trTitle = if ($titleMatch.Success) { $titleMatch.Groups[1].Value.Trim() } else { '' }
    # Desc (TR)
    $descMatch = [regex]::Match($cardHtml, '<p>([^<]+)</p>')
    $trDesc = if ($descMatch.Success) { $descMatch.Groups[1].Value.Trim() } else { '' }
    # Date (TR)
    $calEmoji = [string][char]0xD83D + [string][char]0xDCC5
    $dateMatch = [regex]::Match($cardHtml, [regex]::Escape($calEmoji) + '\s*(.+?)</span>')
    if (-not $dateMatch.Success) {
        $dateMatch = [regex]::Match($cardHtml, [regex]::Escape('&#128197;') + '\s*(.+?)</span>')
    }
    $dateStr = if ($dateMatch.Success) { $dateMatch.Groups[1].Value.Trim() } else { '' }
    # Read time (TR metin)
    $readMatch = [regex]::Match($cardHtml, '&#9201;&#65039;\s*([^<]+)')
    $trReadTime = if ($readMatch.Success) { '&#9201;&#65039; ' + $readMatch.Groups[1].Value.Trim() } else { '' }

    $cards += [PSCustomObject]@{
        Slug      = $slug
        TrTag     = $trTag
        TrTitle   = $trTitle
        TrDesc    = $trDesc
        Date      = $dateStr
        TrRead    = $trReadTime
    }
}

# ─── CSS CIKAR (style tag arasi) ───
$cssMatch = [regex]::Match($trContent, '(?s)<style>(.*?)</style>')
$cssBlock = if ($cssMatch.Success) { $cssMatch.Groups[1].Value } else { '' }

# lang-btn CSS'i ekle
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
    foreach ($l in @('en','de','es','fr','ru','ko','zh-Hans','ja')) {
        $hrefLang = $l
        $urlLang = $l -replace '-Hans',''
        $lines += "<link rel=`"alternate`" hreflang=`"$hrefLang`" href=`"$baseUrl/blog/$urlLang/`"/>"
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

# ─── YERELLESTIRILMIS TARIH CEK ───
$dateCache = @{}
function Get-LocalizedDate($lang, $card) {
    $cacheKey = "$lang|$($card.Slug)"
    if ($dateCache.ContainsKey($cacheKey)) { return $dateCache[$cacheKey] }

    if ($lang -eq 'tr') {
        $dateCache[$cacheKey] = $card.Date
        return $card.Date
    }

    $postFile = Join-Path $blogDir "$lang\$($card.Slug).html"
    if (Test-Path $postFile) {
        $postContent = [System.IO.File]::ReadAllText($postFile, [System.Text.Encoding]::UTF8)
        $calEmoji = [string][char]0xD83D + [string][char]0xDCC5
        $dm = [regex]::Match($postContent, [regex]::Escape($calEmoji) + '\s*([^<]+)</span>')
        if (-not $dm.Success) {
            $dm = [regex]::Match($postContent, [regex]::Escape('&#128197;') + '\s*([^<]+)</span>')
        }
        if ($dm.Success) {
            $localDate = To-Entity $dm.Groups[1].Value.Trim()
            $dateCache[$cacheKey] = $localDate
            return $localDate
        }
    }

    $dateCache[$cacheKey] = $card.Date
    return $card.Date
}

# ─── YAZI SAYFASINDAN CEVIRILERI CEK ───
$postCache = @{}
function Get-PostTranslation($lang, $slug) {
    $cacheKey = "$lang|$slug"
    if ($postCache.ContainsKey($cacheKey)) { return $postCache[$cacheKey] }

    $postFile = if ($lang -eq 'tr') { Join-Path $blogDir "$slug.html" } else { Join-Path $blogDir "$lang\$slug.html" }
    $result = @{ Title = ''; Desc = ''; ReadTime = ''; Tag = '' }

    if (Test-Path $postFile) {
        $pc = [System.IO.File]::ReadAllText($postFile, [System.Text.Encoding]::UTF8)
        # og:title
        $tm = [regex]::Match($pc, 'og:title"\s*content="([^"]+)"')
        if ($tm.Success) { $result.Title = $tm.Groups[1].Value }
        # og:description
        $dm = [regex]::Match($pc, 'og:description"\s*content="([^"]+)"')
        if ($dm.Success) { $result.Desc = $dm.Groups[1].Value }
        # Tag (post-tag, blog-card-tag veya blog-tag sinifinden)
        $tagM = [regex]::Match($pc, '(?s)class="post-tag"[^>]*>(.+?)</span>')
        if (-not $tagM.Success) { $tagM = [regex]::Match($pc, '(?s)blog-card-tag[^>]*>(.+?)</span>') }
        if (-not $tagM.Success) { $tagM = [regex]::Match($pc, '(?s)blog-tag[^>]*>(.+?)</span>') }
        if ($tagM.Success) { $result.Tag = $tagM.Groups[1].Value.Trim() }
        # Read time
        $timeEmoji = [string][char]0x23F1 + [string][char]0xFE0F
        $rtm = [regex]::Match($pc, [regex]::Escape($timeEmoji) + '\s*([^<]+)')
        if (-not $rtm.Success) {
            $rtm = [regex]::Match($pc, '&#9201;&#65039;\s*([^<]+)')
        }
        if ($rtm.Success) { $result.ReadTime = $rtm.Groups[1].Value.Trim() }
    }

    $postCache[$cacheKey] = $result
    return $result
}

# ─── TAG CEVIRILERI (gomulu tablo — yazı sayfalarında tag yok) ───
# TR'deki tag'i anahtar olarak kullan, ceviriyi buradan al
$tagTranslations = @{
    'en' = @{}; 'de' = @{}; 'es' = @{}; 'fr' = @{}; 'ru' = @{}; 'ko' = @{}; 'zh' = @{}; 'ja' = @{}
}
# Tag cevirilerini her dilin yazi sayfasindaki blog-card-tag'dan cek
# Ama yazi sayfalarinda blog-card-tag yok — tag sadece liste kartlarinda.
# Cozum: TR tag'ini tum dillerde kullan (emoji + kisa kategori adi evrensel)
# veya tag cevirilerini gomulu tut

# ─── KART HTML URET ───
function Get-CardHtml($lang, $card) {
    $st = $statics[$lang]
    if (-not $st) { return '' }

    # Yazı sayfasından çeviriyi çek (tüm diller için)
    $trans = Get-PostTranslation $lang $card.Slug

    # Tag: karttan gelen varsa kullan, yoksa yazı sayfasından çek
    $tag = $card.TrTag
    if (-not $tag -and $trans.Tag) { $tag = To-Entity $trans.Tag }
    if (-not $tag) { $tag = '' }

    # Title: karttan gelen varsa kullan, yoksa yazı sayfasından çek
    if ($lang -eq 'tr') {
        $title = if ($card.TrTitle) { $card.TrTitle } elseif ($trans.Title) { To-Entity $trans.Title } else { '' }
        $desc = if ($card.TrDesc) { $card.TrDesc } elseif ($trans.Desc) { To-Entity $trans.Desc } else { '' }
        $readTime = if ($card.TrRead) { $card.TrRead } elseif ($trans.ReadTime) { To-Entity ([char]0x23F1 + [char]0xFE0F + ' ' + $trans.ReadTime) } else { '' }
    } else {
        $title = if ($trans.Title) { To-Entity $trans.Title } elseif ($card.TrTitle) { $card.TrTitle } else { '' }
        $desc = if ($trans.Desc) { To-Entity $trans.Desc } elseif ($card.TrDesc) { $card.TrDesc } else { '' }
        $readTime = if ($trans.ReadTime) { To-Entity ([char]0x23F1 + [char]0xFE0F + ' ' + $trans.ReadTime) } elseif ($card.TrRead) { $card.TrRead } else { '' }
    }

    $readMore = To-Entity $st.read_more
    $href = if ($lang -eq 'tr') { "/blog/$($card.Slug).html" } else { "/blog/$lang/$($card.Slug).html" }

    return @"
  <article class="blog-card">
    <div class="blog-card-meta">
      <span class="blog-card-tag">$tag</span>
      <span>&#128197; $(Get-LocalizedDate $lang $card)</span>
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
    $st = $statics[$lang]
    $isAlt = $lang -ne 'tr'
    $canonical = if ($isAlt) { "$baseUrl/blog/$lang/" } else { "$baseUrl/blog/" }
    $blogTitle = To-Entity $st.blog_title
    $blogSub = Escape-MetaQuotes (To-Entity $st.blog_sub)
    $footerRights = To-Entity $st.footer_rights
    $privacyLink = To-Entity $st.privacy_link
    $ogLocale = $localeMap[$lang]
    $navHome = To-Entity $st.back_home
    $blogLinkText = 'Blog'

    # Kartlar
    $cardHtmlParts = @()
    foreach ($c in $cards) {
        $cardHtmlParts += Get-CardHtml $lang $c
    }
    $allCards = $cardHtmlParts -join "`n"

    $hreflang = Get-HreflangBlock
    $langNav = Get-LangNav $lang
    $blogMenuHref = if ($isAlt) { "/blog/$lang/" } else { '/blog/' }

    $html = @"
<!DOCTYPE html>
<html lang="$(if($lang -eq 'zh'){'zh-Hans'}else{$lang})">
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
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Blog",
  "@id": "$canonical",
  "url": "$canonical",
  "name": "$blogTitle &#8212; K&#305;lman Bili&#351;im",
  "description": "$blogSub",
  "inLanguage": "$(if($lang -eq 'zh'){'zh-Hans'}else{$lang})",
  "publisher": {
    "@type": "Organization",
    "name": "K&#305;lman Bili&#351;im Sistemleri",
    "url": "https://kilmanbilisim.com/",
    "logo": {
      "@type": "ImageObject",
      "url": "https://kilmanbilisim.com/og-image.jpg"
    }
  }
}
</script>
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
    [System.IO.File]::WriteAllText($outFile, $html, $utf8NoBom)
    Write-Host "  [OK] /blog/$lang/index.html ($($html.Length) char)" -ForegroundColor Green
}

# ═══════════════════════════════════════════════
# ADIM 2 — TR liste sayfasini guncelle
# ═══════════════════════════════════════════════
Write-Host "`n=== ADIM 2: TR liste sayfasi guncelle ===" -ForegroundColor Cyan
$trHtml = Build-ListPage 'tr'
[System.IO.File]::WriteAllText($trFile, $trHtml, $utf8NoBom)
Write-Host "  [OK] /blog/index.html ($($trHtml.Length) char)" -ForegroundColor Green

# ═══════════════════════════════════════════════
# ADIM 3 — Yazi sayfalarinda Blog menu linki
# ═══════════════════════════════════════════════
Write-Host "`n=== ADIM 3: Yazi sayfalarinda Blog menu linki ===" -ForegroundColor Cyan
$fixedMenuLinks = 0
foreach ($lang in $altLangs) {
    $dir = Join-Path $blogDir $lang
    $files = Get-ChildItem $dir -Filter "*.html" | Where-Object { $_.Name -ne 'index.html' }
    foreach ($f in $files) {
        $c = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
        $newBlogHref = "/blog/$lang/"
        $updated = $c -replace '(<a\s+href=")(/blog/(?:[a-z]{2}/)?)("\s*(?:class="[^"]*")?\s*>Blog</a>)', "`${1}$newBlogHref`${3}"
        if ($updated -ne $c) {
            [System.IO.File]::WriteAllText($f.FullName, $updated, $utf8NoBom)
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
    [System.IO.File]::WriteAllText($sitemapFile, $sitemapContent, $utf8NoBom)
    Write-Host "  [OK] Sitemap guncellendi" -ForegroundColor Green
} else {
    Write-Host "  [SKIP] Sitemap zaten guncel" -ForegroundColor Yellow
}

$urlCount = ([regex]::Matches($sitemapContent, '<loc>')).Count
Write-Host "  Sitemap URL sayisi: $urlCount"

# ═══════════════════════════════════════════════
# ADIM 5 — Yazma sonrasi dogrulama
# ═══════════════════════════════════════════════
Write-Host "`n=== ADIM 5: Kodlama dogrulamasi ===" -ForegroundColor Cyan
$badChars = @([char]0x251C, [char]0x2500, [char]0x255D, [char]0x253C, [char]0x00BA, [char]0x00AA, [char]0x00D2, [char]0x00D5, [char]0x00D9, [char]0x00DB, [char]0x00D4, [char]0x00E5, [char]0x00C6)
$allClean = $true
$checkFiles = @("$blogDir\index.html")
foreach ($l in $altLangs) { $checkFiles += "$blogDir\$l\index.html" }

foreach ($cf in $checkFiles) {
    $content = [System.IO.File]::ReadAllText($cf, [System.Text.Encoding]::UTF8)
    $bad = 0
    foreach ($bc in $badChars) { $bad += ([regex]::Matches($content, [regex]::Escape([string]$bc))).Count }
    $rel = $cf.Replace($blogDir, '').TrimStart('\')
    if ($bad -gt 0) {
        Write-Host "  [FAIL] $rel — $bad bozuk karakter!" -ForegroundColor Red
        $allClean = $false
    } else {
        Write-Host "  [OK] $rel" -ForegroundColor Green
    }
}

if ($allClean) {
    Write-Host "`n=== TAMAMLANDI ===" -ForegroundColor Green
} else {
    Write-Host "`n=== UYARI: Bozuk karakter tespit edildi! ===" -ForegroundColor Red
}
Write-Host "  8 dil sayfasi + TR guncelleme + $fixedMenuLinks menu linki + sitemap"
