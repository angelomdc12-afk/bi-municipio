$ErrorActionPreference = 'Stop'
$path = "PowerBI/bi_municipio_streamlit.py"
$lines = [System.Collections.Generic.List[string]]::new()
Get-Content -Encoding UTF8 $path | ForEach-Object { [void]$lines.Add($_) }

# 1) Garantir item no menu administrativo em ASCII
$idxAdmin = -1
$idxAdminEnd = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^\s*paginas_administrativo = \[') { $idxAdmin = $i; continue }
    if ($idxAdmin -ge 0 -and $idxAdminEnd -lt 0 -and $lines[$i] -match '^\s*\]') { $idxAdminEnd = $i; break }
}
if ($idxAdmin -ge 0 -and $idxAdminEnd -gt $idxAdmin) {
    # remove quaisquer linhas antigas de produtividade
    for ($i = $idxAdminEnd - 1; $i -gt $idxAdmin; $i--) {
        if ($lines[$i] -match 'Produtividade') { $lines.RemoveAt($i) }
    }
    # inserir antes de Auditoria
    $insertAt = $idxAdminEnd
    for ($i = $idxAdmin; $i -le $idxAdminEnd; $i++) {
        if ($lines[$i] -match 'Auditoria de Acesso') { $insertAt = $i; break }
    }
    $lines.Insert($insertAt, '        "Produtividade Medica",')
}

# 2) Garantir ícone
$idxMetaIcon = -1
$hasProdIcon = $false
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '"Metas do Plano"\s*:') { $idxMetaIcon = $i }
    if ($lines[$i] -match '"Produtividade Medica"\s*:') { $hasProdIcon = $true }
}
if (-not $hasProdIcon -and $idxMetaIcon -ge 0) {
    $lines.Insert($idxMetaIcon + 1, '        "Produtividade Medica": "🩺",')
}

# 3) Ajustar rota para aceitar ambos rótulos
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'elif pagina == "Produtividade') {
        $lines[$i] = '    elif pagina in ["Produtividade Medica", "Produtividade Médica"]:'
        if ($i + 1 -lt $lines.Count) { $lines[$i + 1] = '        render_produtividade_medica_page()' }
    }
}

# Se não existir rota, inserir antes da auditoria
$hasProdRoute = $false
$idxAuditRoute = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'elif pagina in \["Produtividade Medica"') { $hasProdRoute = $true }
    if ($lines[$i] -match '^\s*elif pagina == "Auditoria de Acesso":') { $idxAuditRoute = $i }
}
if (-not $hasProdRoute -and $idxAuditRoute -ge 0) {
    $lines.Insert($idxAuditRoute, '    elif pagina in ["Produtividade Medica", "Produtividade Médica"]:')
    $lines.Insert($idxAuditRoute + 1, '        render_produtividade_medica_page()')
    $lines.Insert($idxAuditRoute + 2, '')
}

# 4) Forçar disponibilidade independente de permissão
$idxPagDispEnd = -1
$idxPagDispStart = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^\s*paginas_disponiveis = \[') { $idxPagDispStart = $i; continue }
    if ($idxPagDispStart -ge 0 -and $idxPagDispEnd -lt 0 -and $lines[$i] -match '^\s*\]') { $idxPagDispEnd = $i; break }
}
if ($idxPagDispEnd -ge 0) {
    $already = $false
    for ($i = $idxPagDispEnd; $i -lt [Math]::Min($idxPagDispEnd + 6, $lines.Count); $i++) {
        if ($lines[$i] -match 'Produtividade Medica') { $already = $true; break }
    }
    if (-not $already) {
        $lines.Insert($idxPagDispEnd + 1, '')
        $lines.Insert($idxPagDispEnd + 2, '    if "Produtividade Medica" not in paginas_disponiveis:')
        $lines.Insert($idxPagDispEnd + 3, '        paginas_disponiveis.append("Produtividade Medica")')
    }
}

Set-Content -Path $path -Value $lines -Encoding UTF8
Write-Output "ENFORCE_ASCII_OK"