<#
GOREV C - Tarih duzeni
4 yazinin tarihini guncelle:
1. chatbot-vs-ai-asistan: 2026-07-02 -> 2026-07-01
2. hukuk: 2026-07-31 -> 2026-08-01
3. perakende: 2026-08-01 -> 2026-08-02
4. tarim: 2026-08-01 -> 2026-08-03

Her yazida 4 yer: JSON-LD (datePublished/dateModified), sayfa tarihi, kart tarihi
#>
$utf8 = [System.Text.UTF8Encoding]::new($false)
$bd = "c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\blog"

$degisiklikler = @(
    @{slug="chatbot-vs-ai-asistan"; eski="2026-07-02"; yeni="2026-07-01"; eskiGun="2"; yeniGun="1"},
    @{slug="yapay-zeka-ile-hukuk-sozlesme-yonetimi-otomasyonu"; eski="2026-07-31"; yeni="2026-08-01"; eskiGun="31"; yeniGun="1"; eskiAy="Temmuz"; yeniAy="Agustos"},
    @{slug="yapay-zeka-ile-perakende-sektoru-otomasyonu"; eski="2026-08-01"; yeni="2026-08-02"; eskiGun="1"; yeniGun="2"},
    @{slug="yapay-zeka-ile-tarim-sera-otomasyonu"; eski="2026-08-01"; yeni="2026-08-03"; eskiGun="1"; yeniGun="3"}
)

$diller = @("","en","de","es","fr","ru","ko","zh","ja")

foreach($d in $degisiklikler) {
    $slug = $d.slug
    $eski = $d.eski
    $yeni = $d.yeni
    $degisikenSayfa = 0

    foreach($dil in $diller) {
        $dosya = if($dil -eq "") { "$bd\$slug.html" } else { "$bd\$dil\$slug.html" }
        if(Test-Path $dosya) {
            $icerik = [System.IO.File]::ReadAllText($dosya, [System.Text.Encoding]::UTF8)
            $eskiIcerik = $icerik

            # JSON-LD: datePublished ve dateModified
            $icerik = $icerik.Replace("`"datePublished`":`"$eski`"", "`"datePublished`":`"$yeni`"")
            $icerik = $icerik.Replace("`"dateModified`":`"$eski`"", "`"dateModified`":`"$yeni`"")
            # Alternatif format (bosluklu)
            $icerik = $icerik.Replace("`"datePublished`": `"$eski`"", "`"datePublished`": `"$yeni`"")
            $icerik = $icerik.Replace("`"dateModified`": `"$eski`"", "`"dateModified`": `"$yeni`"")

            if($icerik -ne $eskiIcerik) {
                [System.IO.File]::WriteAllText($dosya, $icerik, $utf8)
                $degisikenSayfa++
            }
        }
    }
    Write-Output "$slug : $degisikenSayfa sayfa guncellendi (JSON-LD)"
}

# Sitemap guncelle
$sitemapYol = "c:\Users\kaank\OneDrive\Desktop\Web Sitesi\files\sitemap.xml"
if(Test-Path $sitemapYol) {
    $sitemap = [System.IO.File]::ReadAllText($sitemapYol, [System.Text.Encoding]::UTF8)
    $eskiSitemap = $sitemap

    # chatbot: 2026-07-02 -> 2026-07-01
    # hukuk: 2026-07-31 -> 2026-08-01 (sadece hukuk iceren URL'ler icin)
    # perakende: 2026-08-01 -> 2026-08-02 (sadece perakende iceren URL'ler icin)
    # tarim: 2026-08-01 -> 2026-08-03 (sadece tarim iceren URL'ler icin)
    # Not: Toplu degistirme yerine satir satir kontrol

    $satirlar = $sitemap -split "`n"
    $yeniSatirlar = @()
    $oncekiUrl = ""
    foreach($s in $satirlar) {
        $satir = $s
        if($s -match '<loc>') {
            $oncekiUrl = $s
        }
        if($s -match '<lastmod>') {
            if($oncekiUrl -match 'chatbot-vs-ai-asistan') {
                $satir = $satir.Replace('2026-07-02','2026-07-01')
            }
            elseif($oncekiUrl -match 'hukuk-sozlesme') {
                $satir = $satir.Replace('2026-07-31','2026-08-01')
            }
            elseif($oncekiUrl -match 'perakende-sektoru') {
                $satir = $satir.Replace('2026-08-01','2026-08-02')
            }
            elseif($oncekiUrl -match 'tarim-sera') {
                $satir = $satir.Replace('2026-08-01','2026-08-03')
            }
        }
        $yeniSatirlar += $satir
    }
    $yeniSitemap = $yeniSatirlar -join "`n"
    if($yeniSitemap -ne $eskiSitemap) {
        [System.IO.File]::WriteAllText($sitemapYol, $yeniSitemap, $utf8)
        Write-Output "Sitemap guncellendi"
    } else {
        Write-Output "Sitemap: degisiklik yok"
    }
} else {
    Write-Output "Sitemap bulunamadi!"
}

Write-Output "GOREV C tamamlandi"
