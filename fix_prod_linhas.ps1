$ErrorActionPreference = 'Stop'
$path = "PowerBI/bi_municipio_streamlit.py"
$lines = Get-Content -Encoding UTF8 $path

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'Produtividade M') {
        if ($lines[$i] -match 'paginas_administrativo') { continue }
    }

    if ($lines[$i] -match '^\s*"Produtividade M') {
        $lines[$i] = '        "Produtividade Médica",'
    }

    if ($lines[$i] -match '^\s*elif pagina == "Produtividade M') {
        $lines[$i] = '    elif pagina == "Produtividade Médica":'
    }

    if ($lines[$i] -match '^\s*render_produtividade_medica_page\(\)') {
        $lines[$i] = '        render_produtividade_medica_page()'
    }
}

$hasProdIcon = $false
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '"Produtividade Médica"\s*:') { $hasProdIcon = $true; break }
}

if (-not $hasProdIcon) {
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '"Metas do Plano"\s*:') {
            $pre = $lines[0..$i]
            $post = $lines[($i+1)..($lines.Count-1)]
            $lines = @($pre + '        "Produtividade Médica": "🩺",' + $post)
            break
        }
    }
}

Set-Content -Path $path -Value $lines -Encoding UTF8
Write-Output "FIX_OK"