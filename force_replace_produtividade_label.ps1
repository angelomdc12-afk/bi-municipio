$ErrorActionPreference = "Stop"
$path = "PowerBI/bi_municipio_streamlit.py"
if (-not (Test-Path $path)) { throw "Arquivo nao encontrado: $path" }

$content = Get-Content -Raw -Encoding UTF8 $path
$old = "Produtividade UPAs"
$new = "Produtividade Médica UPAs"
$count = ([regex]::Matches($content, [regex]::Escape($old))).Count
$content = $content.Replace($old, $new)

Set-Content -Path $path -Encoding UTF8 -Value $content
Write-Host "Substituicoes realizadas: $count"
Write-Host "Rotulo novo aplicado: $new"
