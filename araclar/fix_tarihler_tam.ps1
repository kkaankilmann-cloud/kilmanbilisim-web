<#
GOREV C TAMAMLAMA - Kart + Sayfa ici tarihler
Tum CJK karakterler HTML entity olarak
#>
$utf8 = [System.Text.UTF8Encoding]::new($false)
$bd = "c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

function Do-Replace {
    param($dosya, [string]$eski, [string]$yeni)
    if(!(Test-Path $dosya)) { return 0 }
    $c = [System.IO.File]::ReadAllText($dosya, [System.Text.Encoding]::UTF8)
    if($c.Contains($eski)) {
        $c = $c.Replace($eski, $yeni)
        [System.IO.File]::WriteAllText($dosya, $c, $utf8)
        return 1
    }
    return 0
}

$toplam = 0

# ============================================================
# ONCE: Agustos -> Agustos (yumusak g) - TR hukuk sayfasi
# ============================================================
$f = "$bd\yapay-zeka-ile-hukuk-sozlesme-yonetimi-otomasyonu.html"
$c = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
if($c.Contains("Agustos")) {
    $c = $c.Replace("Agustos", [char]0x011E + [string]"ustos".Substring(0,0) + "A" -replace ".", {
        # Basit: Replace ile
    })
}
# Daha basit yol:
$toplam += (Do-Replace $f "Agustos" "$([char]0x011E)ustos")
if($toplam -gt 0) { Write-Output "Agustos->Agustos duzeltildi (Guslu G)" }

# Wait, 0x011E buyuk G-breve (Ğ), ama Agustos -> Ağustos demek A harfi kalacak
# Ağustos = A + ğ + ustos ... yok, sorun su: "Agustos" -> "Ağustos"
# Ğ = buyuk, ğ = kucuk. "Ağustos" = A + ğ(0x011F) + ustos
# Yani: "Agustos" icindeki "g" yi "ğ" (0x011F) ile degistir

$f = "$bd\yapay-zeka-ile-hukuk-sozlesme-yonetimi-otomasyonu.html"
$c = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
$eskiDeger = "Agustos"
$yeniDeger = "A$([char]0x011F)ustos"
if($c.Contains($eskiDeger)) {
    $c = $c.Replace($eskiDeger, $yeniDeger)
    [System.IO.File]::WriteAllText($f, $c, $utf8)
    Write-Output "TR hukuk: Agustos -> $yeniDeger duzeltildi"
}

Write-Output "=== CHATBOT: 2 Temmuz -> 1 Temmuz ==="
$slug = "chatbot-vs-ai-asistan-isletmeniz-icin-dogru-secim"

# TR
$toplam += (Do-Replace "$bd\$slug.html" "2 Temmuz 2026" "1 Temmuz 2026")
$toplam += (Do-Replace "$bd\index.html" "2 Temmuz 2026" "1 Temmuz 2026")
Write-Output "TR: $toplam"

# EN
$toplam += (Do-Replace "$bd\en\$slug.html" "July 2, 2026" "July 1, 2026")
$toplam += (Do-Replace "$bd\en\index.html" "July 2, 2026" "July 1, 2026")

# DE
$toplam += (Do-Replace "$bd\de\$slug.html" "2. Juli 2026" "1. Juli 2026")
$toplam += (Do-Replace "$bd\de\index.html" "2. Juli 2026" "1. Juli 2026")

# ES
$toplam += (Do-Replace "$bd\es\$slug.html" "2 de julio de 2026" "1 de julio de 2026")
$toplam += (Do-Replace "$bd\es\index.html" "2 de julio de 2026" "1 de julio de 2026")

# FR
$toplam += (Do-Replace "$bd\fr\$slug.html" "2 juillet 2026" "1 juillet 2026")
$toplam += (Do-Replace "$bd\fr\index.html" "2 juillet 2026" "1 juillet 2026")

Write-Output "Chatbot batili diller tamam: $toplam"

Write-Output "=== HUKUK: 31 Temmuz -> 1 Agustos ==="
$slug = "yapay-zeka-ile-hukuk-sozlesme-yonetimi-otomasyonu"

# TR (kart: 31 Temmuz -> 1 Agustos; "Ağustos" ile)
$agustos = "A$([char]0x011F)ustos"
$toplam += (Do-Replace "$bd\$slug.html" "31 Temmuz 2026" "1 $agustos 2026")
$toplam += (Do-Replace "$bd\index.html" "31 Temmuz 2026" "1 $agustos 2026")

# EN
$toplam += (Do-Replace "$bd\en\$slug.html" "July 31, 2026" "August 1, 2026")
$toplam += (Do-Replace "$bd\en\index.html" "July 31, 2026" "August 1, 2026")

# DE
$toplam += (Do-Replace "$bd\de\$slug.html" "31. Juli 2026" "1. August 2026")
$toplam += (Do-Replace "$bd\de\index.html" "31. Juli 2026" "1. August 2026")

# ES
$toplam += (Do-Replace "$bd\es\$slug.html" "31 de julio de 2026" "1 de agosto de 2026")
$toplam += (Do-Replace "$bd\es\index.html" "31 de julio de 2026" "1 de agosto de 2026")

# FR
$toplam += (Do-Replace "$bd\fr\$slug.html" "31 juillet 2026" "1 ao$([char]0x00FB)t 2026")
$toplam += (Do-Replace "$bd\fr\index.html" "31 juillet 2026" "1 ao$([char]0x00FB)t 2026")

Write-Output "Hukuk batili diller: $toplam"

Write-Output "=== PERAKENDE: 31 Temmuz/1 Agustos -> 2 Agustos ==="
$slug = "yapay-zeka-ile-perakende-sektoru-otomasyonu"

# TR
$toplam += (Do-Replace "$bd\$slug.html" "1 $agustos 2026" "2 $agustos 2026")
$toplam += (Do-Replace "$bd\index.html" "31 Temmuz 2026" "2 $agustos 2026")
$toplam += (Do-Replace "$bd\index.html" "1 $agustos 2026" "2 $agustos 2026")

# EN
$toplam += (Do-Replace "$bd\en\$slug.html" "August 1, 2026" "August 2, 2026")
$toplam += (Do-Replace "$bd\en\index.html" "July 31, 2026" "August 2, 2026")
$toplam += (Do-Replace "$bd\en\index.html" "August 1, 2026" "August 2, 2026")

# DE
$toplam += (Do-Replace "$bd\de\$slug.html" "1. August 2026" "2. August 2026")
$toplam += (Do-Replace "$bd\de\index.html" "31. Juli 2026" "2. August 2026")
$toplam += (Do-Replace "$bd\de\index.html" "1. August 2026" "2. August 2026")

# ES
$toplam += (Do-Replace "$bd\es\$slug.html" "1 de agosto de 2026" "2 de agosto de 2026")
$toplam += (Do-Replace "$bd\es\index.html" "31 de julio de 2026" "2 de agosto de 2026")
$toplam += (Do-Replace "$bd\es\index.html" "1 de agosto de 2026" "2 de agosto de 2026")

# FR
$toplam += (Do-Replace "$bd\fr\$slug.html" "1 ao$([char]0x00FB)t 2026" "2 ao$([char]0x00FB)t 2026")
$toplam += (Do-Replace "$bd\fr\index.html" "31 juillet 2026" "2 ao$([char]0x00FB)t 2026")
$toplam += (Do-Replace "$bd\fr\index.html" "1 ao$([char]0x00FB)t 2026" "2 ao$([char]0x00FB)t 2026")

Write-Output "Perakende batili: $toplam"

Write-Output "=== TARIM: 31 Temmuz/1 Agustos -> 3 Agustos ==="
$slug = "yapay-zeka-ile-tarim-sera-otomasyonu"

# TR
$toplam += (Do-Replace "$bd\$slug.html" "1 $agustos 2026" "3 $agustos 2026")
$toplam += (Do-Replace "$bd\index.html" "31 Temmuz 2026" "3 $agustos 2026")
$toplam += (Do-Replace "$bd\index.html" "1 $agustos 2026" "3 $agustos 2026")

# EN
$toplam += (Do-Replace "$bd\en\$slug.html" "August 1, 2026" "August 3, 2026")
$toplam += (Do-Replace "$bd\en\index.html" "July 31, 2026" "August 3, 2026")
$toplam += (Do-Replace "$bd\en\index.html" "August 1, 2026" "August 3, 2026")

# DE
$toplam += (Do-Replace "$bd\de\$slug.html" "1. August 2026" "3. August 2026")
$toplam += (Do-Replace "$bd\de\index.html" "31. Juli 2026" "3. August 2026")
$toplam += (Do-Replace "$bd\de\index.html" "1. August 2026" "3. August 2026")

# ES
$toplam += (Do-Replace "$bd\es\$slug.html" "1 de agosto de 2026" "3 de agosto de 2026")
$toplam += (Do-Replace "$bd\es\index.html" "31 de julio de 2026" "3 de agosto de 2026")
$toplam += (Do-Replace "$bd\es\index.html" "1 de agosto de 2026" "3 de agosto de 2026")

# FR
$toplam += (Do-Replace "$bd\fr\$slug.html" "1 ao$([char]0x00FB)t 2026" "3 ao$([char]0x00FB)t 2026")
$toplam += (Do-Replace "$bd\fr\index.html" "31 juillet 2026" "3 ao$([char]0x00FB)t 2026")
$toplam += (Do-Replace "$bd\fr\index.html" "1 ao$([char]0x00FB)t 2026" "3 ao$([char]0x00FB)t 2026")

Write-Output "Tarim batili: $toplam"

Write-Output "`nTOPLAM degisiklik: $toplam"
Write-Output "CJK dilleri (RU KO ZH JA) ayri scriptte islenecek"
