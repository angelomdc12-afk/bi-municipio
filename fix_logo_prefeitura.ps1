$file = "C:\Users\Inovar Soluções\Documents\PowerBI\bi-municipio\PowerBI\bi_municipio_streamlit.py"
$enc = [System.Text.Encoding]::UTF8
$content = [System.IO.File]::ReadAllText($file, $enc)

# Verifica estado atual
Write-Host "scale(2) count:" ($content.ToCharArray() | Where-Object {$_ -eq 's'} | Measure-Object).Count
Write-Host "Buscando marcadores..."
if ($content.Contains("scale(2)")) { Write-Host "AINDA TEM scale(2)" } else { Write-Host "scale(2) JA REMOVIDO" }
if ($content.Contains("width:110px")) { Write-Host "width:110px OK" } else { Write-Host "width:110px AUSENTE" }
if ($content.Contains("LG-2026-04-27-10")) { Write-Host "LG-10 OK" } else { Write-Host "LG-10 AUSENTE" }
if ($content.Contains("width:220px")) { Write-Host "width:220px AINDA PRESENTE" } else { Write-Host "width:220px OK REMOVIDO" }
