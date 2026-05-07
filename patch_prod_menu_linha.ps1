$ErrorActionPreference = 'Stop'
$path = "PowerBI/bi_municipio_streamlit.py"
$lines = [System.Collections.Generic.List[string]]::new()
Get-Content -Encoding UTF8 $path | ForEach-Object { [void]$lines.Add($_) }

function Find-LineIndex([string]$pattern) {
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match $pattern) { return $i }
    }
    return -1
}

if ((Find-LineIndex '^def render_produtividade_medica_page\(') -lt 0) {
    $idxMenu = Find-LineIndex '^\s*paginas_unidades = \['
    if ($idxMenu -gt 0) {
        $fn = [System.Collections.Generic.List[string]]::new()
        @(
            '',
            'def render_produtividade_medica_page():',
            '    st.subheader("Produtividade Médica")',
            '',
            '    base = Path(__file__).parent',
            '    path = base / "urgencia_tratado_validado.xlsx"',
            '    if not path.exists():',
            '        alt = base / "urgencia_tratado_final.xlsx"',
            '        path = alt if alt.exists() else None',
            '',
            '    if path is None:',
            '        st.warning("Arquivo de produtividade não encontrado.")',
            '        return',
            '',
            '    try:',
            '        diario = pd.read_excel(path, sheet_name="KPI_DIARIO_GERAL")',
            '        semanal = pd.read_excel(path, sheet_name="KPI_SEMANAL_GERAL")',
            '        ranking = pd.read_excel(path, sheet_name="RANKING_MEDICOS")',
            '    except Exception as e:',
            '        st.error(f"Erro ao ler base de produtividade: {e}")',
            '        return',
            '',
            '    if "Data" in diario.columns:',
            '        diario["Data"] = pd.to_datetime(diario["Data"], errors="coerce", dayfirst=True)',
            '    if "Total_Geral_24h" in diario.columns:',
            '        diario["Total_Geral_24h"] = pd.to_numeric(diario["Total_Geral_24h"], errors="coerce")',
            '',
            '    section_start("KPIs executivos", "Consolidado do período")',
            '    serie = pd.to_numeric(diario.get("Total_Geral_24h", pd.Series(dtype=float)), errors="coerce").dropna()',
            '    total = float(serie.sum()) if not serie.empty else 0.0',
            '    media = float(serie.mean()) if not serie.empty else 0.0',
            '    melhor = float(serie.max()) if not serie.empty else 0.0',
            '    pior = float(serie.min()) if not serie.empty else 0.0',
            '    c1, c2, c3, c4 = st.columns(4)',
            '    with c1:',
            '        top_kpi_card("Total geral do período", format_int(total), icon="📈", subtitle="Soma de Total_Geral_24h")',
            '    with c2:',
            '        top_kpi_card("Média diária", format_int(media), icon="📆", subtitle="Média de Total_Geral_24h")',
            '    with c3:',
            '        top_kpi_card("Melhor dia", format_int(melhor), icon="🏆", subtitle="Maior valor diário")',
            '    with c4:',
            '        top_kpi_card("Pior dia", format_int(pior), icon="📉", subtitle="Menor valor diário")',
            '    section_end()',
            '',
            '    section_start("Evolução diária", "Total geral de atendimentos por dia")',
            '    if not diario.empty and "Data" in diario.columns and "Total_Geral_24h" in diario.columns:',
            '        work = diario[["Data", "Total_Geral_24h"]].dropna().sort_values("Data")',
            '        fig = go.Figure()',
            '        fig.add_trace(go.Scatter(x=work["Data"], y=work["Total_Geral_24h"], mode="lines+markers", name="Total Geral 24h"))',
            '        fig = apply_plotly_theme(fig, title="Evolução diária", subtitle="KPI_DIARIO_GERAL", yaxis_title="Atendimentos", height=360, legend=False)',
            '        plot(fig, "produtividade_evolucao")',
            '    else:',
            '        st.info("Sem dados para evolução diária.")',
            '    section_end()',
            '',
            '    section_start("Ranking completo", "RANKING_MEDICOS")',
            '    if not ranking.empty:',
            '        if "Total_Atendimentos" in ranking.columns:',
            '            ranking["Total_Atendimentos"] = pd.to_numeric(ranking["Total_Atendimentos"], errors="coerce")',
            '            ranking = ranking.sort_values("Total_Atendimentos", ascending=False)',
            '        cols = [c for c in ["Médico", "Unidade", "Total_Atendimentos", "Plantoes", "Media_por_Plantao", "Media_por_Hora"] if c in ranking.columns]',
            '        st.dataframe(ranking[cols].reset_index(drop=True), width="stretch")',
            '    else:',
            '        st.info("Sem dados de ranking.")',
            '    section_end()',
            ''
        ) | ForEach-Object { [void]$fn.Add($_) }
        $lines.InsertRange($idxMenu, $fn)
    }
}

$idxAdmin = Find-LineIndex '^\s*paginas_administrativo = \['
if ($idxAdmin -ge 0) {
    $endAdmin = -1
    for ($i = $idxAdmin; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^\s*\]') { $endAdmin = $i; break }
    }
    if ($endAdmin -gt $idxAdmin) {
        $hasProd = $false
        for ($i = $idxAdmin; $i -le $endAdmin; $i++) {
            if ($lines[$i] -match 'Produtividade Médica') { $hasProd = $true; break }
        }
        if (-not $hasProd) {
            $insertAt = $endAdmin
            for ($i = $idxAdmin; $i -le $endAdmin; $i++) {
                if ($lines[$i] -match 'Auditoria de Acesso') { $insertAt = $i; break }
            }
            $lines.Insert($insertAt, '        "Produtividade Médica",')
        }
    }
}

$idxIconAud = Find-LineIndex '"Auditoria de Acesso"\s*:'
if ($idxIconAud -ge 0) {
    $hasIconProd = (Find-LineIndex '"Produtividade Médica"\s*:') -ge 0
    if (-not $hasIconProd) {
        $lines.Insert($idxIconAud, '        "Produtividade Médica": "🩺",')
    }
}

$idxAuditRoute = Find-LineIndex '^\s*elif pagina == "Auditoria de Acesso":'
$hasProdRoute = (Find-LineIndex '^\s*elif pagina == "Produtividade Médica":') -ge 0
if ($idxAuditRoute -ge 0 -and -not $hasProdRoute) {
    $routeBlock = [System.Collections.Generic.List[string]]::new()
    @(
        '    elif pagina == "Produtividade Médica":',
        '        render_produtividade_medica_page()',
        ''
    ) | ForEach-Object { [void]$routeBlock.Add($_) }
    $lines.InsertRange($idxAuditRoute, $routeBlock)
}

Set-Content -Path $path -Value $lines -Encoding UTF8
Write-Output "PATCH_LINE_OK"