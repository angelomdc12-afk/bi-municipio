$ErrorActionPreference = 'Stop'
$path = "PowerBI/bi_municipio_streamlit.py"
$lines = Get-Content -Encoding UTF8 $path

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'elif pagina == "Produtividade M') {
        $lines[$i] = '    elif pagina == "Produtividade Médica":'
        if ($i + 1 -lt $lines.Count -and $lines[$i + 1] -match 'render_produtividade_medica_page') {
            $lines[$i + 1] = '        render_produtividade_medica_page()'
        }
    }

    if ($lines[$i] -match '^\s*"Produtividade M.*",\s*$') {
        $lines[$i] = '        "Produtividade Médica",'
    }
}

$hasProdInAdmin = $false
$idxAdmin = -1
$idxAdminEnd = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^\s*paginas_administrativo = \[') { $idxAdmin = $i; continue }
    if ($idxAdmin -ge 0 -and $idxAdminEnd -lt 0 -and $lines[$i] -match '^\s*\]') { $idxAdminEnd = $i; break }
}
if ($idxAdmin -ge 0 -and $idxAdminEnd -gt $idxAdmin) {
    for ($i = $idxAdmin; $i -le $idxAdminEnd; $i++) {
        if ($lines[$i] -match 'Produtividade Médica') { $hasProdInAdmin = $true; break }
    }
    if (-not $hasProdInAdmin) {
        $insertAt = $idxAdminEnd
        for ($i = $idxAdmin; $i -le $idxAdminEnd; $i++) {
            if ($lines[$i] -match 'Auditoria de Acesso') { $insertAt = $i; break }
        }
        $pre = $lines[0..($insertAt-1)]
        $post = $lines[$insertAt..($lines.Count-1)]
        $lines = @($pre + '        "Produtividade Médica",' + $post)
    }
}

$hasProdIcon = $false
$idxMetaIcon = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '"Produtividade Médica"\s*:') { $hasProdIcon = $true }
    if ($lines[$i] -match '"Metas do Plano"\s*:') { $idxMetaIcon = $i }
}
if (-not $hasProdIcon -and $idxMetaIcon -ge 0) {
    $pre = $lines[0..$idxMetaIcon]
    $post = $lines[($idxMetaIcon+1)..($lines.Count-1)]
    $lines = @($pre + '        "Produtividade Médica": "🩺",' + $post)
}

Set-Content -Path $path -Value $lines -Encoding UTF8
Write-Output "FIX2_OK"