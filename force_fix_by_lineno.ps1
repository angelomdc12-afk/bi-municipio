$ErrorActionPreference = 'Stop'
$path = "PowerBI/bi_municipio_streamlit.py"
$lines = [System.Collections.Generic.List[string]]::new()
Get-Content -Encoding UTF8 $path | ForEach-Object { [void]$lines.Add($_) }

# Ajustes por linha (1-based): 3762, 3960, 3961
if ($lines.Count -ge 3762) { $lines[3761] = '        "Produtividade Médica",' }
if ($lines.Count -ge 3960) { $lines[3959] = '    elif pagina == "Produtividade Médica":' }
if ($lines.Count -ge 3961) { $lines[3960] = '        render_produtividade_medica_page()' }

# Inserir ícone após Metas do Plano se ainda não existir
$hasIcon = $false
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '"Produtividade Médica"\s*:') { $hasIcon = $true; break }
}
if (-not $hasIcon) {
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '"Metas do Plano"\s*:') {
            $lines.Insert($i + 1, '        "Produtividade Médica": "🩺",')
            break
        }
    }
}

Set-Content -Path $path -Value $lines -Encoding UTF8
Write-Output "FORCE_FIX_OK"