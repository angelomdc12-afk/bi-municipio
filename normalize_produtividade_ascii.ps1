$ErrorActionPreference = "Stop"
$path = "PowerBI/bi_municipio_streamlit.py"
if (-not (Test-Path $path)) { throw "Arquivo nao encontrado: $path" }

$label = "Produtividade Medica UPAs"
$content = Get-Content -Raw -Encoding UTF8 $path
$content = $content.Replace("Produtividade MÃ©dica UPAs", $label)
$content = $content.Replace("Produtividade Médica UPAs", $label)
$content = $content.Replace("Produtividade UPAs", $label)

Set-Content -Path $path -Encoding UTF8 -Value $content
Write-Host "Label normalizado para ASCII: $label"
