"""Patch direto no disco — substitui a função stub pela versão completa."""
import pathlib, sys

file = pathlib.Path(__file__).parent / "PowerBI" / "bi_municipio_streamlit.py"
content = file.read_text(encoding="utf-8")

OLD = '''def render_produtividade_medica_page():
    st.markdown("## 📈 Produtividade Médica")
    st.info("Página em construção.")'''

NEW = '''def load_produtividade_data():
    base = Path(__file__).parent
    path = None
    for name in ["urgencia_tratado_validado.xlsx", "urgencia_tratado_final.xlsx"]:
        c = base / name
        if c.exists():
            path = c
            break
    empty = {k: pd.DataFrame() for k in ["kpi_diario","kpi_unidade","kpi_semanal","ranking","top5_geral","top5_upa2","top5_upa1"]}
    if path is None:
        return empty
    xl = pd.ExcelFile(path)
    def _s(n):
        return pd.read_excel(path, sheet_name=n) if n in xl.sheet_names else pd.DataFrame()
    kd = _s("KPI_DIARIO_GERAL")
    ku = _s("KPI_DIARIO_UNIDADE")
    ks = _s("KPI_SEMANAL_GERAL")
    rk = _s("RANKING_MEDICOS")
    t0 = _s("TOP5_GERAL")
    t2 = _s("TOP5_UPA_II")
    t1 = _s("TOP5_UPA_I")
    for df in [kd, ku]:
        if "Data" in df.columns:
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)
    for df in [ks]:
        for col in ["Semana_Inicio", "Semana_Fim"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
    num_cols = ["UPA II DE LUZI\\u00c2NIA","UPA I JARDIM ING\\u00c1","SAMU","Total_Geral_24h",
                "Total_24h_Final","Media_Hora_24h","Total_Semana_Geral","Total_Semana_UPA_II",
                "Total_Semana_UPA_I","Total_Atendimentos","Plantoes","Media_por_Plantao","Media_por_Hora"]
    for df in [kd, ku, ks, rk, t0, t2, t1]:
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
    return {"kpi_diario":kd,"kpi_unidade":ku,"kpi_semanal":ks,"ranking":rk,
            "top5_geral":t0,"top5_upa2":t2,"top5_upa1":t1}


def render_produtividade_medica_page():
    prod = load_produtividade_data()
    kd = prod["kpi_diario"].copy()
    ku = prod["kpi_unidade"].copy()
    ks = prod["kpi_semanal"].copy()
    rk = prod["ranking"].copy()
    t0 = prod["top5_geral"].copy()
    t2 = prod["top5_upa2"].copy()
    t1 = prod["top5_upa1"].copy()

    if kd.empty and rk.empty:
        st.warning("Arquivo urgencia_tratado_validado.xlsx n\\u00e3o encontrado na pasta do app.")
        return

    # Filtros internos (n\\u00e3o afetam sidebar global)
    data_min = kd["Data"].dropna().min().date() if "Data" in kd.columns and not kd["Data"].dropna().empty else None
    data_max = kd["Data"].dropna().max().date() if "Data" in kd.columns and not kd["Data"].dropna().empty else None

    st.markdown("#### Filtros")
    cf1, cf2 = st.columns([1, 2])
    with cf1:
        unid = st.selectbox("Unidade", ["Todas", "UPA II DE LUZI\\u00c2NIA", "UPA I JARDIM ING\\u00c1", "SAMU"], key="pm_unid")
    with cf2:
        if data_min and data_max:
            periodo = st.date_input("Per\\u00edodo", value=(data_min, data_max), min_value=data_min, max_value=data_max, key="pm_periodo")
        else:
            periodo = None
    st.divider()

    ini = fim = None
    if isinstance(periodo, (list, tuple)) and len(periodo) == 2:
        ini, fim = pd.to_datetime(periodo[0]), pd.to_datetime(periodo[1])
    elif isinstance(periodo, dt.date):
        ini = fim = pd.to_datetime(periodo)

    if ini is not None:
        if "Data" in kd.columns:
            kd = kd[(kd["Data"] >= ini) & (kd["Data"] <= fim)].copy()
        if "Data" in ku.columns:
            ku = ku[(ku["Data"] >= ini) & (ku["Data"] <= fim)].copy()
        if "Semana_Inicio" in ks.columns:
            ks = ks[(ks["Semana_Fim"] >= ini) & (ks["Semana_Inicio"] <= fim)].copy()

    if unid != "Todas":
        if "Unidade" in ku.columns:
            ku = ku[ku["Unidade"] == unid].copy()
        if "Unidade" in rk.columns:
            rk = rk[rk["Unidade"] == unid].copy()
        top5_ref = t2 if unid == "UPA II DE LUZI\\u00c2NIA" else (t1 if unid == "UPA I JARDIM ING\\u00c1" else t0)
    else:
        top5_ref = t0

    # KPIs
    serie = pd.to_numeric(kd.get("Total_Geral_24h", pd.Series(dtype=float)), errors="coerce").dropna()
    total = float(serie.sum()) if not serie.empty else 0.0
    media = float(serie.mean()) if not serie.empty else 0.0
    melhor = float(serie.max()) if not serie.empty else 0.0
    pior   = float(serie.min()) if not serie.empty else 0.0
    melhor_dia = pior_dia = "-"
    if not serie.empty and "Data" in kd.columns:
        v = kd[["Data","Total_Geral_24h"]].dropna()
        if not v.empty:
            melhor_dia = v.loc[v["Total_Geral_24h"].idxmax(),"Data"].strftime("%d/%m/%Y")
            pior_dia   = v.loc[v["Total_Geral_24h"].idxmin(),"Data"].strftime("%d/%m/%Y")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        top_kpi_card("Total do per\\u00edodo", f"{int(total):,}".replace(",","."), icon="\\U0001f4c8",
                     subtitle="Soma di\\u00e1ria geral", accent_color=SEMANTIC_COLORS["success"], subtitle_color=SEMANTIC_COLORS["success"])
    with k2:
        top_kpi_card("M\\u00e9dia di\\u00e1ria", f"{media:,.1f}".replace(",","."), icon="\\U0001f4c6",
                     subtitle="M\\u00e9dia Total_Geral_24h", accent_color=SEMANTIC_COLORS["primary"], subtitle_color=SEMANTIC_COLORS["primary"])
    with k3:
        top_kpi_card("Melhor dia", f"{int(melhor):,}".replace(",","."), icon="\\U0001f3c6",
                     subtitle=f"Data: {melhor_dia}", accent_color=SEMANTIC_COLORS["warning"], subtitle_color=SEMANTIC_COLORS["warning"])
    with k4:
        top_kpi_card("Pior dia", f"{int(pior):,}".replace(",","."), icon="\\U0001f4c9",
                     subtitle=f"Data: {pior_dia}", accent_color=SEMANTIC_COLORS["danger"], subtitle_color=SEMANTIC_COLORS["danger"])

    # Evolução diária
    section_start("Evolu\\u00e7\\u00e3o di\\u00e1ria", "Total de atendimentos por dia")
    if not kd.empty and "Data" in kd.columns and "Total_Geral_24h" in kd.columns:
        ln = kd[["Data","Total_Geral_24h"]].dropna().sort_values("Data")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ln["Data"], y=ln["Total_Geral_24h"], mode="lines+markers",
            line=dict(color=SEMANTIC_COLORS["primary"], width=3), marker=dict(size=6),
            hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Total: %{y:,.0f}<extra></extra>"))
        fig = apply_plotly_theme(fig, title="Atendimentos di\\u00e1rios", subtitle="KPI_DIARIO_GERAL",
                                 yaxis_title="Atendimentos", height=360, legend=False)
        plot(fig, "pm_evolucao")
    else:
        st.info("Sem dados para o per\\u00edodo selecionado.")
    section_end()

    # Produção por unidade
    section_start("Produ\\u00e7\\u00e3o por unidade", "UPA II \\u00b7 UPA I \\u00b7 SAMU")
    ucols = [c for c in ["UPA II DE LUZI\\u00c2NIA","UPA I JARDIM ING\\u00c1","SAMU"] if c in kd.columns]
    if ucols and not kd.empty and "Data" in kd.columns:
        plot_cols = ucols if unid == "Todas" else [c for c in ucols if c == unid]
        if plot_cols:
            lng = (kd[["Data"]+plot_cols]
                   .melt(id_vars="Data", var_name="Unidade", value_name="Atendimentos")
                   .dropna(subset=["Atendimentos","Data"]).sort_values("Data"))
            fig2 = px.line(lng, x="Data", y="Atendimentos", color="Unidade", markers=True,
                           color_discrete_sequence=[SEMANTIC_COLORS["series_1"],
                                                    SEMANTIC_COLORS["series_2"],
                                                    SEMANTIC_COLORS["series_3"]])
            fig2.update_traces(hovertemplate="<b>%{fullData.name}</b><br>%{x|%d/%m/%Y}<br>%{y:,.0f}<extra></extra>")
            fig2 = apply_plotly_theme(fig2, title="Atendimentos por unidade", subtitle="",
                                      yaxis_title="Atendimentos", height=360, legend=True, legend_orientation="h")
            plot(fig2, "pm_unidades")
    else:
        st.info("Sem dados por unidade.")
    section_end()

    # Semanal
    section_start("Produ\\u00e7\\u00e3o semanal", "Totais consolidados por semana")
    if not ks.empty and "Total_Semana_Geral" in ks.columns and "Semana_Inicio" in ks.columns:
        sp = ks.sort_values("Semana_Inicio").copy()
        sp["Semana"] = sp.apply(
            lambda r: f"{r['Semana_Inicio'].strftime('%d/%m')} \\u2013 {r['Semana_Fim'].strftime('%d/%m')}"
            if pd.notna(r.get("Semana_Inicio")) and pd.notna(r.get("Semana_Fim")) else "-", axis=1)
        fig3 = px.bar(sp, x="Semana", y="Total_Semana_Geral",
                      color_discrete_sequence=[SEMANTIC_COLORS["primary_soft"]])
        fig3.update_traces(marker_line_width=0,
                           hovertemplate="<b>%{x}</b><br>%{y:,.0f}<extra></extra>")
        fig3 = apply_plotly_theme(fig3, title="Produ\\u00e7\\u00e3o semanal geral", subtitle="KPI_SEMANAL_GERAL",
                                  yaxis_title="Atendimentos", height=340, legend=False)
        plot(fig3, "pm_semanal")
        if len(sp) >= 2:
            va = sp.iloc[-1]["Total_Semana_Geral"]
            vb = sp.iloc[-2]["Total_Semana_Geral"]
            if pd.notna(va) and pd.notna(vb) and vb != 0:
                st.caption(f"Varia\\u00e7\\u00e3o vs semana anterior: {((va-vb)/abs(vb))*100:+.1f}%".replace(".",","))
    else:
        st.info("Sem dados semanais.")
    section_end()

    # Top 5 + Tempos
    ca, cb = st.columns([1.2, 1])
    with ca:
        section_start("Top 5 m\\u00e9dicos", "Ranking dos 5 primeiros no per\\u00edodo")
        if not top5_ref.empty and "M\\u00e9dico" in top5_ref.columns and "Total_Atendimentos" in top5_ref.columns:
            fig4 = px.bar(top5_ref, y="M\\u00e9dico", x="Total_Atendimentos", orientation="h",
                          color="Total_Atendimentos",
                          color_continuous_scale=[SEMANTIC_COLORS["primary_soft"], SEMANTIC_COLORS["primary"]])
            fig4.update_traces(hovertemplate="<b>%{y}</b><br>%{x:,.0f} atendimentos<extra></extra>")
            fig4 = apply_plotly_theme(fig4, title="Top 5 por atendimentos", subtitle="",
                                      yaxis_title="", xaxis_title="Atendimentos", height=340, legend=False)
            plot(fig4, "pm_top5")
            n1 = str(top5_ref.iloc[0]["M\\u00e9dico"])
            v1 = float(top5_ref.iloc[0]["Total_Atendimentos"]) if pd.notna(top5_ref.iloc[0]["Total_Atendimentos"]) else 0
            st.success(f"\\U0001f947 {n1} \\u00b7 {int(v1):,} atendimentos".replace(",","."))
        else:
            st.info("Sem dados de Top 5.")
        section_end()
    with cb:
        section_start("Tempos assistenciais", "M\\u00e9dias do per\\u00edodo")
        tc = tp = "-"
        if not kd.empty:
            if "Tempo_Classificacao_Medio_hms" in kd.columns:
                s = kd["Tempo_Classificacao_Medio_hms"].dropna().astype(str)
                if not s.empty:
                    tc = s.iloc[-1]
            if "Tempo_Permanencia_Medio_hms" in kd.columns:
                s = kd["Tempo_Permanencia_Medio_hms"].dropna().astype(str)
                if not s.empty:
                    tp = s.iloc[-1]
        tc1, tc2 = st.columns(2)
        with tc1:
            top_kpi_card("Classifica\\u00e7\\u00e3o", tc, icon="\\u23f1\\ufe0f",
                         subtitle="Tempo m\\u00e9dio HH:MM",
                         accent_color=SEMANTIC_COLORS["warning"], subtitle_color=SEMANTIC_COLORS["warning"])
        with tc2:
            top_kpi_card("Perman\\u00eancia", tp, icon="\\U0001f552",
                         subtitle="Tempo m\\u00e9dio HH:MM",
                         accent_color=SEMANTIC_COLORS["danger"], subtitle_color=SEMANTIC_COLORS["danger"])
        section_end()

    # Ranking completo
    section_start("Ranking completo", "Todos os m\\u00e9dicos ordenados por atendimentos")
    if not rk.empty:
        rcols = [c for c in ["M\\u00e9dico","Unidade","Total_Atendimentos","Plantoes",
                              "Media_por_Plantao","Media_por_Hora"] if c in rk.columns]
        rv = rk.sort_values("Total_Atendimentos", ascending=False) if "Total_Atendimentos" in rk.columns else rk
        st.dataframe(rv[rcols].reset_index(drop=True), use_container_width=True)
    else:
        st.info("Sem dados de ranking.")
    section_end()'''

if OLD not in content:
    print("ERRO: trecho antigo nao encontrado no arquivo!")
    print("Procurando funcao existente...")
    for i, line in enumerate(content.splitlines()):
        if "render_produtividade_medica_page" in line:
            print(f"  Linha {i+1}: {line}")
    sys.exit(1)

content = content.replace(OLD, NEW)
file.write_text(content, encoding="utf-8")
print(f"OK — arquivo gravado ({len(content.splitlines())} linhas)")
