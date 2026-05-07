$ErrorActionPreference = "Stop"
$path = "PowerBI/bi_municipio_streamlit.py"
if (-not (Test-Path $path)) { throw "Arquivo nao encontrado: $path" }

$label = "Produtividade M$([char]0xE9)dica UPAs"
$content = Get-Content -Raw -Encoding UTF8 $path
$content = $content.Replace("Produtividade MÃ©dica UPAs", $label)
$content = $content.Replace("Produtividade Medica UPAs", $label)

Set-Content -Path $path -Encoding UTF8 -Value $content
Write-Host "Encoding corrigido para: $label"
