# Blog #31 ve #32 icin 8 dil sayfasi uretici
# TR kaynak dosyasindan meta degistirip govde cevirisini ekler
param(
    [Parameter(Mandatory=$true)][string]$Slug,
    [string]$BlogDir = (Split-Path -Parent $MyInvocation.MyCommand.Path)
)

$ErrorActionPreference = 'Stop'
$utf8 = [System.Text.UTF8Encoding]::new($false)
$srcFile = Join-Path $BlogDir "$Slug.html"
if(-not (Test-Path $srcFile)) { Write-Error "Kaynak dosya bulunamadi: $srcFile"; exit 1 }

$src = [System.IO.File]::ReadAllText($srcFile, [System.Text.Encoding]::UTF8)
$otherLangs = @('en','de','es','fr','ru','ko','zh','ja')

$localeMap = @{
    'en'='en_US'; 'de'='de_DE'; 'es'='es_ES'; 'fr'='fr_FR';
    'ru'='ru_RU'; 'ko'='ko_KR'; 'zh'='zh_CN'; 'ja'='ja_JP'
}
$htmlLangMap = @{
    'en'='en'; 'de'='de'; 'es'='es'; 'fr'='fr';
    'ru'='ru'; 'ko'='ko'; 'zh'='zh-Hans'; 'ja'='ja'
}
$navHome = @{
    'en'='Home'; 'de'='Startseite'; 'es'='Inicio'; 'fr'='Accueil';
    'ru'='&#1043;&#1083;&#1072;&#1074;&#1085;&#1072;&#1103;'; 'ko'='&#54856;'; 'zh'='&#39318;&#39029;'; 'ja'='&#12507;&#12540;&#12512;'
}
$footerRights = @{
    'en'='All rights reserved.'; 'de'='Alle Rechte vorbehalten.';
    'es'='Todos los derechos reservados.'; 'fr'='Tous droits r&#233;serv&#233;s.';
    'ru'='&#1042;&#1089;&#1077; &#1087;&#1088;&#1072;&#1074;&#1072; &#1079;&#1072;&#1097;&#1080;&#1097;&#1077;&#1085;&#1099;.'; 'ko'='&#47784;&#46304; &#44428;&#47532; &#48372;&#50976;.'; 'zh'='&#29256;&#26435;&#25152;&#26377;&#12290;'; 'ja'='&#20840;&#33879;&#20316;&#27177;&#25152;&#26377;&#12290;'
}
$privacyText = @{
    'en'='Privacy Policy'; 'de'='Datenschutz'; 'es'='Pol&#237;tica de Privacidad';
    'fr'='Politique de Confidentialit&#233;'; 'ru'='&#1055;&#1086;&#1083;&#1080;&#1090;&#1080;&#1082;&#1072; &#1082;&#1086;&#1085;&#1092;&#1080;&#1076;&#1077;&#1085;&#1094;&#1080;&#1072;&#1083;&#1100;&#1085;&#1086;&#1089;&#1090;&#1080;';
    'ko'='&#44060;&#51064;&#51221;&#48372; &#52376;&#47532;&#48169;&#52840;'; 'zh'='&#38544;&#31169;&#25919;&#31574;'; 'ja'='&#12503;&#12521;&#12452;&#12496;&#12471;&#12540;&#12509;&#12522;&#12471;&#12540;'
}

foreach($lang in $otherLangs) {
    $out = $src

    # 1. html lang
    $out = $out -replace '<html lang="tr">', "<html lang=`"$($htmlLangMap[$lang])`">"

    # 2. canonical
    $out = $out -replace ('href="https://kilmanbilisim.com/blog/' + [regex]::Escape($Slug) + '.html"'), "href=`"https://kilmanbilisim.com/blog/$lang/$Slug.html`""

    # 3. og:url
    $out = $out -replace ('content="https://kilmanbilisim.com/blog/' + [regex]::Escape($Slug) + '.html"'), "content=`"https://kilmanbilisim.com/blog/$lang/$Slug.html`""

    # 4. og:locale
    $out = $out -replace 'content="tr_TR"', "content=`"$($localeMap[$lang])`""

    # 5. inLanguage
    $out = $out -replace '"inLanguage": "tr"', "`"inLanguage`": `"$lang`""

    # 6. mainEntityOfPage + url in JSON-LD
    $out = $out -replace ('"@id": "https://kilmanbilisim.com/blog/' + [regex]::Escape($Slug) + '.html"'), "`"@id`": `"https://kilmanbilisim.com/blog/$lang/$Slug.html`""
    $out = $out -replace ('"url": "https://kilmanbilisim.com/blog/' + [regex]::Escape($Slug) + '.html"'), "`"url`": `"https://kilmanbilisim.com/blog/$lang/$Slug.html`""

    # 7. lang-btn active
    $out = $out -replace ("/$Slug.html`" class=`"lang-btn active`""), "/$Slug.html`" class=`"lang-btn`""
    $out = $out -replace ("/$lang/$Slug.html`" class=`"lang-btn`""), "/$lang/$Slug.html`" class=`"lang-btn active`""

    # 8. Nav home text
    $out = $out -replace '>Ana Sayfa</a>', ">$($navHome[$lang])</a>"

    # 9. Blog nav link - blog index
    $out = $out -replace 'href="/blog/" class="active"', "href=`"/blog/$lang/`" class=`"active`""

    # 10. Footer rights
    $out = $out -replace 'T&#252;m haklar&#305; sakl&#305;d&#305;r.', $footerRights[$lang]

    # 11. Privacy text
    $out = $out -replace 'Gizlilik Politikas&#305;', $privacyText[$lang]

    # Ensure target dir exists
    $targetDir = Join-Path $BlogDir $lang
    if(-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir -Force | Out-Null }

    $targetFile = Join-Path $targetDir "$Slug.html"
    [System.IO.File]::WriteAllText($targetFile, $out, $utf8)
    Write-Output "$lang : $targetFile"
}

Write-Output "--- 8 dil sayfasi olusturuldu ---"
