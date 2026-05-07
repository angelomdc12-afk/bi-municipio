import pathlib

file_path = pathlib.Path(r"C:\Users\Inovar Soluções\Documents\PowerBI\bi-municipio\PowerBI\bi_municipio_streamlit.py")
text = file_path.read_text(encoding="utf-8")

kpi_start = text.find("    # KPIs")
kpi_end = text.find("    # Evolução diária")
if kpi_start == -1 or kpi_end == -1 or kpi_end <= kpi_start:
    raise RuntimeError("Bloco de KPI não encontrado")

kpi_new = '''    # KPIs (respeitam a unidade selecionada)
    unidade_col_map = {
        "UPA II DE LUZIÂNIA": "UPA II DE LUZIÂNIA",
        "UPA I JARDIM INGÁ": "UPA I JARDIM INGÁ",
        "SAMU": "SAMU",
    }
    serie_coluna = "Total_Geral_24h" if unid == "Todas" else unidade_col_map.get(unid, "Total_Geral_24h")

    base_kpi = kd[["Data", serie_coluna]].copy() if "Data" in kd.columns and serie_coluna in kd.columns else pd.DataFrame(columns=["Data", serie_coluna])
    base_kpi = base_kpi.dropna(subset=["Data", serie_coluna])

    serie = pd.to_numeric(base_kpi.get(serie_coluna, pd.Series(dtype=float)), errors="coerce").dropna()
    total = float(serie.sum()) if not serie.empty else 0.0
    media = float(serie.mean()) if not serie.empty else 0.0
    melhor = float(serie.max()) if not serie.empty else 0.0
    pior = float(serie.min()) if not serie.empty else 0.0

    melhor_dia = pior_dia = "-"
    if not base_kpi.empty:
        melhor_dia = base_kpi.loc[base_kpi[serie_coluna].idxmax(), "Data"].strftime("%d/%m/%Y")
        pior_dia = base_kpi.loc[base_kpi[serie_coluna].idxmin(), "Data"].strftime("%d/%m/%Y")

    subtitulo_total = "Soma diária geral" if unid == "Todas" else f"Soma diária - {unid}"
    subtitulo_media = "Média Total_Geral_24h" if unid == "Todas" else f"Média diária - {unid}"

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        top_kpi_card("Total do período", f"{int(total):,}".replace(",","."), icon="📈",
                     subtitle=subtitulo_total, accent_color=SEMANTIC_COLORS["success"], subtitle_color=SEMANTIC_COLORS["success"])
    with k2:
        top_kpi_card("Média diária", f"{media:,.1f}".replace(",","."), icon="📆",
                     subtitle=subtitulo_media, accent_color=SEMANTIC_COLORS["primary"], subtitle_color=SEMANTIC_COLORS["primary"])
    with k3:
        top_kpi_card("Melhor dia", f"{int(melhor):,}".replace(",","."), icon="🏆",
                     subtitle=f"Data: {melhor_dia}", accent_color=SEMANTIC_COLORS["warning"], subtitle_color=SEMANTIC_COLORS["warning"])
    with k4:
        top_kpi_card("Pior dia", f"{int(pior):,}".replace(",","."), icon="📉",
                     subtitle=f"Data: {pior_dia}", accent_color=SEMANTIC_COLORS["danger"], subtitle_color=SEMANTIC_COLORS["danger"])

'''

text = text[:kpi_start] + kpi_new + text[kpi_end:]

sem_start = text.find("    # Semanal")
sem_end = text.find("    # Top 5 + Tempos")
if sem_start == -1 or sem_end == -1 or sem_end <= sem_start:
    raise RuntimeError("Bloco semanal não encontrado")

sem_new = '''    # Semanal
    section_start("Produção semanal", "Totais consolidados por semana")
    semanal_col_map = {
        "Todas": "Total_Semana_Geral",
        "UPA II DE LUZIÂNIA": "Total_Semana_UPA_II",
        "UPA I JARDIM INGÁ": "Total_Semana_UPA_I",
        "SAMU": "Total_Semana_SAMU",
    }
    semanal_col = semanal_col_map.get(unid, "Total_Semana_Geral")
    semanal_titulo = "Produção semanal geral" if unid == "Todas" else f"Produção semanal - {unid}"

    if not ks.empty and semanal_col in ks.columns and "Semana_Inicio" in ks.columns and "Semana_Fim" in ks.columns:
        sp = ks.sort_values("Semana_Inicio").copy()
        sp["Semana"] = sp.apply(
            lambda r: f"{r['Semana_Inicio'].strftime('%d/%m')} – {r['Semana_Fim'].strftime('%d/%m')}"
            if pd.notna(r.get("Semana_Inicio")) and pd.notna(r.get("Semana_Fim")) else "-", axis=1)
        fig3 = px.bar(sp, x="Semana", y=semanal_col,
                      color_discrete_sequence=[SEMANTIC_COLORS["primary_soft"]])
        fig3.update_traces(marker_line_width=0,
                           hovertemplate="<b>%{x}</b><br>%{y:,.0f}<extra></extra>")
        fig3 = apply_plotly_theme(fig3, title=semanal_titulo, subtitle="KPI_SEMANAL_GERAL",
                                  yaxis_title="Atendimentos", height=340, legend=False)
        plot(fig3, "pm_semanal")
        if len(sp) >= 2:
            va = sp.iloc[-1][semanal_col]
            vb = sp.iloc[-2][semanal_col]
            if pd.notna(va) and pd.notna(vb) and vb != 0:
                st.caption(f"Variação vs semana anterior: {((va-vb)/abs(vb))*100:+.1f}%".replace(".",","))
    else:
        st.info("Sem dados semanais.")
    section_end()

'''

text = text[:sem_start] + sem_new + text[sem_end:]
file_path.write_text(text, encoding="utf-8")
print("OK")
