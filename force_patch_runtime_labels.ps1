$ErrorActionPreference = "Stop"
$path = "PowerBI/bi_municipio_streamlit.py"
if (-not (Test-Path $path)) { throw "Arquivo nao encontrado: $path" }

$content = Get-Content -Raw -Encoding UTF8 $path
$content = [regex]::Replace($content, 'BUILD_TAG\s*=\s*"[^"]+"', 'BUILD_TAG = "PM-2026-04-27-08"', 1)
$content = [regex]::Replace($content, 'Login build: LG-2026-04-27-\d+', 'Login build: LG-2026-04-27-12', 1)
$content = [regex]::Replace($content, 'PAGINA_PRODUTIVIDADE\s*=\s*"[^"]+"', 'PAGINA_PRODUTIVIDADE = "Produtividade Médica UPAs"', 1)

Set-Content -Path $path -Encoding UTF8 -Value $content
Write-Host "Arquivo atualizado: $path"
Write-Host "BUILD_TAG/Login/PAGINA_PRODUTIVIDADE ajustados."