$ErrorActionPreference = 'Stop'
$path = "PowerBI/bi_municipio_streamlit.py"
$lines = [System.Collections.Generic.List[string]]::new()
Get-Content -Encoding UTF8 $path | ForEach-Object { [void]$lines.Add($_) }

if ($lines.Count -ge 3762) { $lines[3761] = '        "Produtividade Medica",' }
if ($lines.Count -ge 3964) { $lines[3963] = '    elif pagina in ["Produtividade Medica", "Produtividade Médica"]:' }
if ($lines.Count -ge 3965) { $lines[3964] = '        render_produtividade_medica_page()' }

$hasIcon = $false
for ($i=0; $i -lt $lines.Count; $i++) { if ($lines[$i] -match '"Produtividade Medica"\s*:') { $hasIcon = $true; break } }
if (-not $hasIcon) {
    for ($i=0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '"Metas do Plano"\s*:') {
            $lines.Insert($i+1, '        "Produtividade Medica": "🩺",')
            break
        }
    }
}

Set-Content -Path $path -Value $lines -Encoding UTF8
Write-Output "FINAL_FIX_OK"