$ErrorActionPreference = 'Stop'
$path = "PowerBI/bi_municipio_streamlit.py"
$content = Get-Content -Raw -Encoding UTF8 $path

if ($content -notmatch 'def load_produtividade_data\(') {
$loader = @'

@st.cache_data(show_spinner=False)
def load_produtividade_data():
    path = Path(__file__).parent / "urgencia_tratado_validado.xlsx"
    if not path.exists():
        alt = Path(__file__).parent / "urgencia_tratado_final.xlsx"
        path = alt if alt.exists() else None

    if path is None:
        return {
            "kpi_diario": pd.DataFrame(),
            "kpi_semanal": pd.DataFrame(),
            "ranking": pd.DataFrame(),
        }

    xls = pd.ExcelFile(path)

    def _sheet(name):
        return pd.read_excel(path, sheet_name=name) if name in xls.sheet_names else pd.DataFrame()

    kpi_diario = _sheet("KPI_DIARIO_GERAL")
    kpi_semanal = _sheet("KPI_SEMANAL_GERAL")
    ranking = _sheet("RANKING_MEDICOS")

    if "Data" in kpi_diario.columns:
        kpi_diario["Data"] = pd.to_datetime(kpi_diario["Data"], errors="coerce", dayfirst=True)
    for col in ["Total_Geral_24h", "UPA II DE LUZIÂNIA", "UPA I JARDIM INGÁ", "SAMU"]:
        if col in kpi_diario.columns:
            kpi_diario[col] = pd.to_numeric(kpi_diario[col], errors="coerce")

    if "Semana_Inicio" in kpi_semanal.columns:
        kpi_semanal["Semana_Inicio"] = pd.to_datetime(kpi_semanal["Semana_Inicio"], errors="coerce", dayfirst=True)
    if "Semana_Fim" in kpi_semanal.columns:
        kpi_semanal["Semana_Fim"] = pd.to_datetime(kpi_semanal["Semana_Fim"], errors="coerce", dayfirst=True)
    if "Total_Semana_Geral" in kpi_semanal.columns:
        kpi_semanal["Total_Semana_Geral"] = pd.to_numeric(kpi_semanal["Total_Semana_Geral"], errors="coerce")

    for col in ["Total_Atendimentos", "Plantoes", "Media_por_Plantao", "Media_por_Hora"]:
        if col in ranking.columns:
            ranking[col] = pd.to_numeric(ranking[col], errors="coerce")

    return {
        "kpi_diario": kpi_diario,
        "kpi_semanal": kpi_semanal,
        "ranking": ranking,
    }
'@
$content = $content -replace 'def format_currency_br\(x\):', ($loader + "`r`ndef format_currency_br(x):")
}

if ($content -notmatch 'def render_produtividade_medica_page\(') {
$render = @'

def render_produtividade_medica_page():
    st.subheader("Produtividade Médica")

    prod = load_produtividade_data()
    kpi_diario = prod.get("kpi_diario", pd.DataFrame()).copy()
    kpi_semanal = prod.get("kpi_semanal", pd.DataFrame()).copy()
    ranking = prod.get("ranking", pd.DataFrame()).copy()

    if kpi_diario.empty and ranking.empty:
        st.warning("Arquivo de produtividade não encontrado ou sem dados válidos.")
        return

    data_min, data_max = None, None
    if "Data" in kpi_diario.columns and not kpi_diario["Data"].dropna().empty:
        data_min = kpi_diario["Data"].min().date()
        data_max = kpi_diario["Data"].max().date()

    section_start("Filtros da Produtividade", "Filtro exclusivo da página")
    c1, c2 = st.columns([1, 2])
    with c1:
        unidade_sel = st.selectbox("Unidade", ["Todas", "UPA II DE LUZIÂNIA", "UPA I JARDIM INGÁ", "SAMU"], key="prod_unidade")
    with c2:
        periodo = st.date_input("Período", value=(data_min, data_max) if data_min and data_max else None, key="prod_periodo")
    section_end()

    if isinstance(periodo, tuple) and len(periodo) == 2 and "Data" in kpi_diario.columns:
        ini = pd.to_datetime(periodo[0])
        fim = pd.to_datetime(periodo[1])
        kpi_diario = kpi_diario[(kpi_diario["Data"] >= ini) & (kpi_diario["Data"] <= fim)].copy()
        if not kpi_semanal.empty and "Semana_Inicio" in kpi_semanal.columns and "Semana_Fim" in kpi_semanal.columns:
            kpi_semanal = kpi_semanal[(kpi_semanal["Semana_Fim"] >= ini) & (kpi_semanal["Semana_Inicio"] <= fim)].copy()

    section_start("KPIs executivos", "Visão consolidada do período")
    serie_total = pd.to_numeric(kpi_diario.get("Total_Geral_24h", pd.Series(dtype=float)), errors="coerce").dropna()
    total = float(serie_total.sum()) if not serie_total.empty else 0.0
    media = float(serie_total.mean()) if not serie_total.empty else 0.0
    melhor = float(serie_total.max()) if not serie_total.empty else 0.0
    pior = float(serie_total.min()) if not serie_total.empty else 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        top_kpi_card("Total geral do período", format_int(total), icon="📈", subtitle="Soma de Total_Geral_24h")
    with c2:
        top_kpi_card("Média diária", format_int(media), icon="📆", subtitle="Média de Total_Geral_24h")
    with c3:
        top_kpi_card("Melhor dia", format_int(melhor), icon="🏆", subtitle="Maior valor diário")
    with c4:
        top_kpi_card("Pior dia", format_int(pior), icon="📉", subtitle="Menor valor diário")
    section_end()

    section_start("Evolução diária", "Total geral por dia")
    if not kpi_diario.empty and "Data" in kpi_diario.columns and "Total_Geral_24h" in kpi_diario.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=kpi_diario["Data"], y=kpi_diario["Total_Geral_24h"], mode="lines+markers", name="Total Geral 24h"))
        fig = apply_plotly_theme(fig, title="Evolução diária de atendimentos", subtitle="KPI_DIARIO_GERAL", yaxis_title="Atendimentos", height=360, legend=False)
        plot(fig, "produtividade_evolucao")
    else:
        st.info("Sem dados de evolução diária.")
    section_end()

    section_start("Produção semanal", "Total_Semana_Geral")
    if not kpi_semanal.empty and "Total_Semana_Geral" in kpi_semanal.columns:
        work = kpi_semanal.copy().sort_values("Semana_Inicio")
        work["semana_label"] = work.apply(lambda r: f"{r['Semana_Inicio']:%d/%m} - {r['Semana_Fim']:%d/%m}" if pd.notna(r.get("Semana_Inicio")) and pd.notna(r.get("Semana_Fim")) else "-", axis=1)
        fig = px.bar(work, x="semana_label", y="Total_Semana_Geral")
        fig = apply_plotly_theme(fig, title="Produção semanal geral", subtitle="KPI_SEMANAL_GERAL", yaxis_title="Atendimentos", height=340, legend=False)
        plot(fig, "produtividade_semanal")
    else:
        st.info("Sem dados semanais.")
    section_end()

    section_start("Ranking completo", "RANKING_MEDICOS")
    if not ranking.empty:
        if unidade_sel != "Todas" and "Unidade" in ranking.columns:
            ranking = ranking[ranking["Unidade"].astype(str) == unidade_sel].copy()
        if "Total_Atendimentos" in ranking.columns:
            ranking = ranking.sort_values("Total_Atendimentos", ascending=False)
        cols = [c for c in ["Médico", "Unidade", "Total_Atendimentos", "Plantoes", "Media_por_Plantao", "Media_por_Hora"] if c in ranking.columns]
        st.dataframe(ranking[cols].reset_index(drop=True), width="stretch")
    else:
        st.info("Sem dados de ranking.")
    section_end()
'@
$content = $content -replace 'st\.sidebar\.markdown\(\s*f"""', ($render + "`r`nst.sidebar.markdown(`r`n    f\"\"\"")
}

$content = $content -replace '(?s)paginas_administrativo = \[\s*"Metas do Plano",\s*"Gestão de Pessoas",\s*"Financeiro",\s*"Auditoria de Acesso",\s*\]', 'paginas_administrativo = [`r`n        "Metas do Plano",`r`n        "Gestão de Pessoas",`r`n        "Financeiro",`r`n        "Produtividade Médica",`r`n        "Auditoria de Acesso",`r`n    ]'

$content = $content -replace '"Metas do Plano": "📊",\s*\r?\n\s*"Auditoria de Acesso": "🛡️",', '"Metas do Plano": "📊",`r`n        "Produtividade Médica": "🩺",`r`n        "Auditoria de Acesso": "🛡️",'

$content = $content -replace 'elif pagina == "Financeiro":\s*\r?\n\s*render_financeiro_page\(financeiro_data, meses_selecionados\)\s*\r?\n\s*elif pagina == "Auditoria de Acesso":', 'elif pagina == "Financeiro":`r`n        render_financeiro_page(financeiro_data, meses_selecionados)`r`n`r`n    elif pagina == "Produtividade Médica":`r`n        render_produtividade_medica_page()`r`n`r`n    elif pagina == "Auditoria de Acesso":'

Set-Content -Path $path -Value $content -Encoding UTF8
Write-Output "PATCH_OK"