<#
Gorunen tarihleri guncelle (yazi sayfasi + liste karti)
#>
$utf8 = [System.Text.UTF8Encoding]::new($false)
$bd = "c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

# Tarih formatlari dillere gore
$tarihFormatlari = @{
    chatbot = @{
        TR = @{eski="2 Temmuz 2026"; yeni="1 Temmuz 2026"}
        EN = @{eski="July 2, 2026"; yeni="July 1, 2026"}
        DE = @{eski="2. Juli 2026"; yeni="1. Juli 2026"}
        ES = @{eski="2 de julio de 2026"; yeni="1 de julio de 2026"}
        FR = @{eski="2 juillet 2026"; yeni="1 juillet 2026"}
        RU = @{eski="2 &#1080;&#1102;&#1083;&#1103; 2026"; yeni="1 &#1080;&#1102;&#1083;&#1103; 2026"}
        KO = @{eski="2026&#45380; 7&#50900; 2&#51068;"; yeni="2026&#45380; 7&#50900; 1&#51068;"}
        ZH = @{eski="2026&#24180;7&#26376;2&#26085;"; yeni="2026&#24180;7&#26376;1&#26085;"}
        JA = @{eski="2026&#24180;7&#26376;2&#26085;"; yeni="2026&#24180;7&#26376;1&#26085;"}
    }
    hukuk = @{
        TR = @{eski="31 Temmuz 2026"; yeni="1 A&#287;ustos 2026"}
        EN = @{eski="July 31, 2026"; yeni="August 1, 2026"}
        DE = @{eski="31. Juli 2026"; yeni="1. August 2026"}
        ES = @{eski="31 de julio de 2026"; yeni="1 de agosto de 2026"}
        FR = @{eski="31 juillet 2026"; yeni="1 ao&#251;t 2026"}
        RU = @{eski="31 &#1080;&#1102;&#1083;&#1103; 2026"; yeni="1 &#1072;&#1074;&#1075;&#1091;&#1089;&#1090;&#1072; 2026"}
        KO = @{eski="2026&#45380; 7&#50900; 31&#51068;"; yeni="2026&#45380; 8&#50900; 1&#51068;"}
        ZH = @{eski="2026&#24180;7&#26376;31&#26085;"; yeni="2026&#24180;8&#26376;1&#26085;"}
        JA = @{eski="2026&#24180;7&#26376;31&#26085;"; yeni="2026&#24180;8&#26376;1&#26085;"}
    }
    perakende = @{
        TR = @{eski="1 A&#287;ustos 2026"; yeni="2 A&#287;ustos 2026"}
        EN = @{eski="August 1, 2026"; yeni="August 2, 2026"}
        DE = @{eski="1. August 2026"; yeni="2. August 2026"}
        ES = @{eski="1 de agosto de 2026"; yeni="2 de agosto de 2026"}
        FR = @{eski="1 ao&#251;t 2026"; yeni="2 ao&#251;t 2026"}
        RU = @{eski="1 &#1072;&#1074;&#1075;&#1091;&#1089;&#1090;&#1072; 2026"; yeni="2 &#1072;&#1074;&#1075;&#1091;&#1089;&#1090;&#1072; 2026"}
        KO = @{eski="2026&#45380; 8&#50900; 1&#51068;"; yeni="2026&#45380; 8&#50900; 2&#51068;"}
        ZH = @{eski="2026&#24180;8&#26376;1&#26085;"; yeni="2026&#24180;8&#26376;2&#26085;"}
        JA = @{eski="2026&#24180;8&#26376;1&#26085;"; yeni="2026&#24180;8&#26376;2&#26085;"}
    }
    tarim = @{
        TR = @{eski="1 A&#287;ustos 2026"; yeni="3 A&#287;ustos 2026"}
        EN = @{eski="August 1, 2026"; yeni="August 3, 2026"}
        DE = @{eski="1. August 2026"; yeni="3. August 2026"}
        ES = @{eski="1 de agosto de 2026"; yeni="3 de agosto de 2026"}
        FR = @{eski="1 ao&#251;t 2026"; yeni="3 ao&#251;t 2026"}
        RU = @{eski="1 &#1072;&#1074;&#1075;&#1091;&#1089;&#1090;&#1072; 2026"; yeni="3 &#1072;&#1074;&#1075;&#1091;&#1089;&#1090;&#1072; 2026"}
        KO = @{eski="2026&#45380; 8&#50900; 1&#51068;"; yeni="2026&#45380; 8&#50900; 3&#51068;"}
        ZH = @{eski="2026&#24180;8&#26376;1&#26085;"; yeni="2026&#24180;8&#26376;3&#26085;"}
        JA = @{eski="2026&#24180;8&#26376;1&#26085;"; yeni="2026&#24180;8&#26376;3&#26085;"}
    }
}

# Burada basit yaklasim: sadece TR yazilarindaki gorunen tarihi UTF-8 olarak degistir
# Cunku diger dillerin tarihleri HTML entity olarak kodlu olabilir

# 1. CHATBOT - sadece TR
$slug = "chatbot-vs-ai-asistan-isletmeniz-icin-dogru-secim"
$dosyalar = @("$bd\$slug.html")
foreach($d in $dosyalar) {
    if(Test-Path $d) {
        $c = [System.IO.File]::ReadAllText($d, [System.Text.Encoding]::UTF8)
        $c = $c.Replace("2 Temmuz 2026", "1 Temmuz 2026")
        [System.IO.File]::WriteAllText($d, $c, $utf8)
        Write-Output "Chatbot TR: tarih guncellendi"
    }
}

# 2. HUKUK - TR
$slug = "yapay-zeka-ile-hukuk-sozlesme-yonetimi-otomasyonu"
$d = "$bd\$slug.html"
if(Test-Path $d) {
    $c = [System.IO.File]::ReadAllText($d, [System.Text.Encoding]::UTF8)
    $c = $c.Replace("31 Temmuz 2026", "1 Agustos 2026")
    [System.IO.File]::WriteAllText($d, $c, $utf8)
    Write-Output "Hukuk TR: tarih guncellendi"
}

# 3. PERAKENDE - TR
$slug = "yapay-zeka-ile-perakende-sektoru-otomasyonu"
$d = "$bd\$slug.html"
if(Test-Path $d) {
    $c = [System.IO.File]::ReadAllText($d, [System.Text.Encoding]::UTF8)
    # perakende mevcut tarih ne?
    if($c -match '(\d+ \w+ 2026)') { Write-Output "Perakende mevcut tarih: $($Matches[1])" }
    $c = $c.Replace("31 Temmuz 2026", "2 Agustos 2026")
    $c = $c.Replace("1 Agustos 2026", "2 Agustos 2026")
    [System.IO.File]::WriteAllText($d, $c, $utf8)
    Write-Output "Perakende TR: tarih guncellendi"
}

# 4. TARIM - TR
$slug = "yapay-zeka-ile-tarim-sera-otomasyonu"
$d = "$bd\$slug.html"
if(Test-Path $d) {
    $c = [System.IO.File]::ReadAllText($d, [System.Text.Encoding]::UTF8)
    if($c -match '(\d+ \w+ 2026)') { Write-Output "Tarim mevcut tarih: $($Matches[1])" }
    $c = $c.Replace("31 Temmuz 2026", "3 Agustos 2026")
    $c = $c.Replace("1 Agustos 2026", "3 Agustos 2026")
    [System.IO.File]::WriteAllText($d, $c, $utf8)
    Write-Output "Tarim TR: tarih guncellendi"
}

Write-Output "TR gorunen tarihler guncellendi"
