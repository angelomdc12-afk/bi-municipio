
import datetime as dt
from io import BytesIO
from pathlib import Path

import openpyxl
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="BI Município", page_icon="📊", layout="wide")

st.markdown("""
<style>

/* ===== APP ===== */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(15,108,189,0.10), transparent 28%),
        linear-gradient(180deg, #F4F7FB 0%, #EEF3F8 100%);
}

.block-container {
    padding-top: 1.1rem;
    padding-bottom: 2rem;
    padding-left: 1.6rem;
    padding-right: 1.6rem;
    max-width: 100%;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #111827 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #FFFFFF !important;
    letter-spacing: -0.2px;
}

/* ===== TIPOGRAFIA ===== */
h1 {
    color: #0F172A !important;
    font-weight: 800 !important;
    letter-spacing: -0.7px;
    margin-bottom: 0.15rem;
}

h2, h3 {
    color: #0F172A !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
}

p, label, .stMarkdown, .stCaption {
    color: #334155;
}

/* ===== METRICAS NATIVAS ===== */
div[data-testid="stMetric"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid #E2E8F0;
    padding: 1rem;
    border-radius: 18px;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
}

/* ===== EXPANDER ===== */
details {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 0.35rem 0.8rem;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
}

/* ===== INPUTS ===== */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 12px !important;
    border-color: #CBD5E1 !important;
}

/* ===== PLOTLY CONTAINER ===== */
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 0.35rem 0.35rem 0.15rem 0.35rem;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
}

/* ===== SECTION CARD ===== */
.section-card {
    background: linear-gradient(180deg, #FFFFFF 0%, #FBFDFF 100%);
    border: 1px solid #E2E8F0;
    border-radius: 22px;
    padding: 1rem 1rem 0.6rem 1rem;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
    margin-bottom: 1rem;
}

.section-title {
    font-size: 1.06rem;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 0.2rem;
    letter-spacing: -0.3px;
}

.section-subtitle {
    font-size: 0.92rem;
    color: #64748B;
    margin-bottom: 1rem;
}

/* ===== HERO / TOPO ===== */
.hero-wrap {
    background: linear-gradient(135deg, #0F172A 0%, #12324A 50%, #0F6CBD 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 1.2rem 1.25rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 16px 36px rgba(15, 23, 42, 0.16);
}

.hero-title {
    color: #FFFFFF;
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -0.8px;
    margin-bottom: 0.2rem;
}

.hero-subtitle {
    color: rgba(255,255,255,0.82);
    font-size: 0.98rem;
    margin-bottom: 1rem;
}

.hero-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.hero-chip {
    background: rgba(255,255,255,0.12);
    color: #FFFFFF;
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 999px;
    padding: 0.42rem 0.78rem;
    font-size: 0.82rem;
    font-weight: 600;
    backdrop-filter: blur(6px);
}

.soft-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(148,163,184,0), rgba(148,163,184,0.45), rgba(148,163,184,0));
    margin: 0.6rem 0 1rem 0;
}

</style>
""", unsafe_allow_html=True)

MESES = ["MARÇO.26","ABRIL.26","MAIO.26","JUNHO.26","JULHO.26","AGOSTO.26","SETEMBRO.26","OUTUBRO.26","NOVEMBRO.26","DEZEMBRO.26","JANEIRO.27","FEVEREIRO.27"]
MESES_LABEL = {
    "MARÇO.26":"Mar/26","ABRIL.26":"Abr/26","MAIO.26":"Mai/26","JUNHO.26":"Jun/26","JULHO.26":"Jul/26","AGOSTO.26":"Ago/26",
    "SETEMBRO.26":"Set/26","OUTUBRO.26":"Out/26","NOVEMBRO.26":"Nov/26","DEZEMBRO.26":"Dez/26","JANEIRO.27":"Jan/27","FEVEREIRO.27":"Fev/27"
}
RISK_COLORS = {
    "NÃO URGENTE (AZUL)": "#1E3A8A",
    "POUCO URGENTE (VERDE)": "#16A34A",
    "URGENTE (AMARELO)": "#EAB308",
    "MUITO URGENTE (LARANJA)": "#F97316",
    "EMERGÊNCIA (VERMELHO)": "#DC2626",
    "NÃO INFORMADO": "#6B7280",
}

_plot_counter = 0
def plot(fig, prefix="grafico"):
    global _plot_counter
    _plot_counter += 1
    st.plotly_chart(fig, use_container_width=True, key=f"{prefix}_{_plot_counter}")

def local_excel_path():
    base = Path(__file__).parent
    names = [
        "dashboard_municipio.xlsx",
        "DASH BORD NOVO MUNICIPIO ATUALIZADO.xlsx",
        "DASH BORD NOVO MUNICIPIO ATUALIZADO.xlsm",
    ]
    for name in names:
        p = base / name
        if p.exists():
            return p
    found = sorted(base.glob("*.xlsx")) + sorted(base.glob("*.xlsm"))
    return found[0] if found else None

def normalize_value(v):
    if v in (None, ""):
        return None
    if isinstance(v, dt.timedelta):
        return round(v.total_seconds() / 60, 2)
    if isinstance(v, dt.time):
        return round(v.hour * 60 + v.minute + v.second / 60, 2)
    if isinstance(v, str):
        if v.startswith("#DIV/0"):
            return None
        vv = v.strip().replace(",", ".")
        try:
            return float(vv)
        except Exception:
            return v.strip()
    if isinstance(v, (int, float)):
        return float(v)
    return v

def row_values(ws, r, n=14):
    return [ws.cell(r, c).value for c in range(1, n+1)]

def is_month_row(vals):
    months = [str(v).strip().upper() for v in vals[2:14] if v is not None]
    return len(months) >= 3 and all(m in MESES for m in months)

def parse_sheet(ws, sheet_name):
    rows = []
    unidade = str(ws["A2"].value).strip() if ws["A2"].value else sheet_name
    painel = None
    meses = None

    for r in range(1, ws.max_row + 1):
        vals = row_values(ws, r)
        a, b = vals[0], vals[1]

        if is_month_row(vals):
            meses = [str(ws.cell(r, c).value).strip().upper() if ws.cell(r, c).value is not None else None for c in range(3, 15)]
            continue

        if not any(v is not None for v in vals[2:14]):
            continue

        a_str = a.strip() if isinstance(a, str) else None
        b_str = b.strip() if isinstance(b, str) else None

        # Ignore generic header row
        if a_str == "INDICADOR":
            continue

        if a_str and a_str not in ["META", "MÉDIA DIÁRIA", "MEDIA DIÁRIA", "MEDIA DIARIA"] and b_str:
            painel = a_str
            serie = b_str
        elif a_str and a_str not in ["META", "MÉDIA DIÁRIA", "MEDIA DIÁRIA", "MEDIA DIARIA"] and not b_str:
            painel = a_str
            serie = a_str
        elif a_str in ["META", "MÉDIA DIÁRIA", "MEDIA DIÁRIA", "MEDIA DIARIA"] and painel:
            serie = a_str
        elif b_str and painel:
            serie = b_str
        else:
            continue

        for i, c in enumerate(range(3, 15)):
            mes = meses[i] if meses and i < len(meses) else None
            rows.append({
                "aba": sheet_name,
                "unidade": unidade,
                "painel": painel,
                "serie": serie,
                "serie_norm": str(serie).strip().upper(),
                "mes": mes,
                "mes_label": MESES_LABEL.get(mes, mes),
                "valor": normalize_value(ws.cell(r, c).value),
            })

    df = pd.DataFrame(rows)
    if not df.empty:
        df["valor_num"] = pd.to_numeric(df["valor"], errors="coerce")
        df["mes"] = pd.Categorical(df["mes"], categories=MESES, ordered=True)
        df = df.sort_values(["unidade", "painel", "serie", "mes"])
    return df

@st.cache_data(show_spinner=False)
def load_workbook_data(file_bytes=None):
    if file_bytes is None:
        path = local_excel_path()
        if not path:
            return pd.DataFrame(), None
        wb = openpyxl.load_workbook(path, data_only=True)
        source_name = path.name
    else:
        wb = openpyxl.load_workbook(BytesIO(file_bytes), data_only=True)
        source_name = "upload.xlsx"

    sheet_order = [
        "INDICADORES UPA LUZIÂNIA",
        "INDICADORES UPA JARDIM INGÁ",
        "INDICADORES HMJI",
        "INDICADORES ATENÇÃO SECUNDÁRIA",
        "INDICADORES SAÚDE MENTAL",
        "INDICADORES ATENÇÃO PRIMÁRIA",
    ]
    frames = []
    for s in sheet_order:
        if s in wb.sheetnames:
            part = parse_sheet(wb[s], s)
            if not part.empty:
                frames.append(part)
    if not frames:
        return pd.DataFrame(), source_name
    data = pd.concat(frames, ignore_index=True)
    return data, source_name

def filter_panel(df, unidade, painel):
    return df[(df["unidade"] == unidade) & (df["painel"] == painel)].copy()

def format_int(x):
    if pd.isna(x):
        return "-"
    return f"{int(round(x)):,}".replace(",", ".")

def clean_card_value(value):
    if value is None:
        return "-"

    value = str(value)

    replacements = [
        "<div style='",
        '<div style="',
        "</div>",
        "<div>",
        "</span>",
        "<span>",
        "&nbsp;"
    ]
    for item in replacements:
        value = value.replace(item, "")

    import re
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value if value else "-"


def metric_sum(df, serie_norm=None, exclude_series_norm=None, month=None):
    work = df.copy()

    if month is not None:
        work = work[work["mes"] == month]

    if serie_norm is not None:
        if isinstance(serie_norm, str):
            serie_norm = [serie_norm]
        serie_norm = [str(x).strip().upper() for x in serie_norm]
        work = work[work["serie_norm"].isin(serie_norm)]

    if exclude_series_norm is not None:
        if isinstance(exclude_series_norm, str):
            exclude_series_norm = [exclude_series_norm]
        exclude_series_norm = [str(x).strip().upper() for x in exclude_series_norm]
        work = work[~work["serie_norm"].isin(exclude_series_norm)]

    work = work.dropna(subset=["valor_num"])

    if work.empty:
        return None

    return float(work["valor_num"].sum())


def latest_and_previous_month(df, serie_norm=None, exclude_series_norm=None):
    work = df.copy()

    if serie_norm is not None:
        if isinstance(serie_norm, str):
            serie_norm = [serie_norm]
        serie_norm = [str(x).strip().upper() for x in serie_norm]
        work = work[work["serie_norm"].isin(serie_norm)]

    if exclude_series_norm is not None:
        if isinstance(exclude_series_norm, str):
            exclude_series_norm = [exclude_series_norm]
        exclude_series_norm = [str(x).strip().upper() for x in exclude_series_norm]
        work = work[~work["serie_norm"].isin(exclude_series_norm)]

    work = work.dropna(subset=["mes", "valor_num"]).sort_values("mes")

    if work.empty:
        return None, None

    months = []
    for m in work["mes"].tolist():
        if m not in months:
            months.append(m)

    latest = months[-1] if months else None
    previous = months[-2] if len(months) >= 2 else None
    return latest, previous


def calc_delta_pct(current, previous):
    if current is None or previous is None:
        return None
    if pd.isna(current) or pd.isna(previous):
        return None
    if previous == 0:
        return None
    return ((current - previous) / previous) * 100


def build_kpi_context(df, serie_norm=None, exclude_series_norm=None, meta_series="META"):
    latest_month, previous_month = latest_and_previous_month(
        df,
        serie_norm=serie_norm,
        exclude_series_norm=exclude_series_norm
    )

    current_value = metric_sum(
        df,
        serie_norm=serie_norm,
        exclude_series_norm=exclude_series_norm,
        month=latest_month
    )

    previous_value = metric_sum(
        df,
        serie_norm=serie_norm,
        exclude_series_norm=exclude_series_norm,
        month=previous_month
    )

    total_value = metric_sum(
        df,
        serie_norm=serie_norm,
        exclude_series_norm=exclude_series_norm
    )

    meta_value = metric_sum(
        df,
        serie_norm=meta_series,
        month=latest_month
    )

    return {
        "latest_month": latest_month,
        "previous_month": previous_month,
        "latest_month_label": MESES_LABEL.get(latest_month, str(latest_month) if latest_month else "-"),
        "current": current_value,
        "previous": previous_value,
        "total": total_value,
        "meta": meta_value,
        "delta_pct": calc_delta_pct(current_value, previous_value),
    }


def card(
    title,
    value,
    icon="📊",
    subtitle="Indicador consolidado",
    delta_pct=None,
    delta_good_when="up",
    meta_value=None,
    footer_text=None
):
    value = clean_card_value(value)

    # ----- DELTA -----
    if delta_pct is None:
        delta_text = "Sem base comparativa"
        delta_bg = "#F8FAFC"
        delta_color = "#64748B"
        delta_border = "#E2E8F0"
    else:
        if delta_pct > 0:
            arrow = "↑"
        elif delta_pct < 0:
            arrow = "↓"
        else:
            arrow = "→"

        is_good = delta_pct >= 0 if delta_good_when == "up" else delta_pct <= 0

        delta_text = f"{arrow} {abs(delta_pct):.1f}% vs mês anterior"
        delta_bg = "#ECFDF5" if is_good else "#FEF2F2"
        delta_color = "#166534" if is_good else "#B91C1C"
        delta_border = "#BBF7D0" if is_good else "#FECACA"

    # ----- META -----
    meta_html = ""
    if meta_value is not None and not pd.isna(meta_value):
        numeric_value = pd.to_numeric(str(value).replace(".", "").replace(",", "."), errors="coerce")
        if pd.notna(numeric_value):
            meta_ok = numeric_value >= meta_value
            meta_bg = "#ECFDF5" if meta_ok else "#FFF7ED"
            meta_color = "#166534" if meta_ok else "#C2410C"
            meta_border = "#BBF7D0" if meta_ok else "#FED7AA"
            meta_label = f"Meta: {format_int(meta_value)}"
            meta_status = "atingida" if meta_ok else "abaixo"
            meta_html = f"""
                <div style="
                    display:inline-flex;
                    align-items:center;
                    gap:6px;
                    padding:6px 10px;
                    border-radius:999px;
                    background:{meta_bg};
                    border:1px solid {meta_border};
                    color:{meta_color};
                    font-size:12px;
                    font-weight:700;
                    white-space:nowrap;
                ">
                    🎯 {meta_label} · {meta_status}
                </div>
            """

    footer_html = ""
    if footer_text:
        footer_html = f"""
            <div style="
                margin-top:12px;
                padding-top:10px;
                border-top:1px solid #E2E8F0;
                font-size:12px;
                color:#64748B;
                font-weight:600;
            ">
                {footer_text}
            </div>
        """

    html = f"""
    <div style="
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid #E2E8F0;
        border-radius: 22px;
        padding: 18px 18px 16px 18px;
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
        min-height: 185px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    ">
        <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; margin-bottom:12px;">
                <div>
                    <div style="
                        font-size:12px;
                        font-weight:800;
                        color:#64748B;
                        text-transform:uppercase;
                        letter-spacing:0.7px;
                        margin-bottom:5px;
                    ">
                        {title}
                    </div>
                    <div style="
                        font-size:12px;
                        color:#94A3B8;
                        font-weight:500;
                    ">
                        {subtitle}
                    </div>
                </div>

                <div style="
                    width:46px;
                    height:46px;
                    border-radius:14px;
                    background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:21px;
                    flex-shrink:0;
                ">
                    {icon}
                </div>
            </div>

            <div style="
                font-size:34px;
                font-weight:800;
                color:#0F172A;
                line-height:1;
                margin-bottom:14px;
            ">
                {value}
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:8px;">
                <div style="
                    display:inline-flex;
                    align-items:center;
                    gap:6px;
                    padding:6px 10px;
                    border-radius:999px;
                    background:{delta_bg};
                    border:1px solid {delta_border};
                    color:{delta_color};
                    font-size:12px;
                    font-weight:700;
                    white-space:nowrap;
                ">
                    {delta_text}
                </div>

                {meta_html}
            </div>
        </div>

        {footer_html}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
def section_start(title, subtitle=""):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{title}</div>
            <div class="section-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True
    )

def section_end():
    st.markdown("</div>", unsafe_allow_html=True)

def hero_header(page_title, source_name, meses_selecionados):
    if not meses_selecionados:
        periodo = "Todos os meses"
    elif len(meses_selecionados) <= 4:
        periodo = " | ".join(meses_selecionados)
    else:
        periodo = " | ".join(meses_selecionados[:4]) + "..."

    data_ref = dt.datetime.now().strftime("%d/%m/%Y %H:%M")

    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-title">BI Município</div>
            <div class="hero-subtitle">
                Painel executivo de indicadores assistenciais 
            </div>
            <div class="hero-chip-row">
                <div class="hero-chip">Página: {page_title}</div>
                <div class="hero-chip">Período: {periodo}</div>
                <div class="hero-chip">Fonte: {source_name}</div>
                <div class="hero-chip">Atualizado em: {data_ref}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def apply_plotly_theme(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#334155", size=12),
        title_font=dict(color="#0F172A", size=16),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        margin=dict(l=20, r=20, t=45, b=20)
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#E2E8F0",
        tickfont=dict(color="#64748B")
    )
    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.20)",
        zeroline=False,
        tickfont=dict(color="#64748B")
    )
    return fig
def line_with_optional_meta(df, title, main_series=None, unit_suffix="", prefix="line"):
    st.markdown(f"**{title}**")
    work = df.dropna(subset=["valor_num"]).copy()
    fig = go.Figure()

    if main_series:
        main = work[work["serie_norm"] == main_series.upper()]
        if not main.empty:
            fig.add_trace(
                go.Scatter(
                    x=main["mes_label"],
                    y=main["valor_num"],
                    mode="lines+markers",
                    name=main_series
                )
            )
    else:
        for serie in work["serie"].dropna().unique():
            temp = work[work["serie"] == serie]
            fig.add_trace(
                go.Scatter(
                    x=temp["mes_label"],
                    y=temp["valor_num"],
                    mode="lines+markers",
                    name=str(serie)
                )
            )

    meta = work[work["serie_norm"] == "META"]
    if not meta.empty:
        fig.add_trace(
            go.Scatter(
                x=meta["mes_label"],
                y=meta["valor_num"],
                mode="lines+markers",
                name="Meta",
                line=dict(dash="dash")
            )
        )

    fig.update_layout(height=320, yaxis_title=unit_suffix)
    fig = apply_plotly_theme(fig)
    plot(fig, prefix)


def grouped_bar(df, title, color_map=None, barmode="group", unit_suffix="", prefix="bar"):
    st.markdown(f"**{title}**")
    work = df.dropna(subset=["valor_num"]).copy()
    if work.empty:
        st.info("Sem dados para este gráfico.")
        return

    fig = px.bar(
        work,
        x="mes_label",
        y="valor_num",
        color="serie",
        barmode=barmode,
        color_discrete_map=color_map or {}
    )

    fig.update_layout(height=360, legend_title_text="", yaxis_title=unit_suffix)
    fig = apply_plotly_theme(fig)
    plot(fig, prefix)

def stacked_bar(df, title, color_map=None, as_percent=False, prefix="stack"):
    st.markdown(f"**{title}**")
    work = df.dropna(subset=["valor_num"]).copy()
    if work.empty:
        st.info("Sem dados para este gráfico.")
        return

    pivot = work.pivot_table(
        index="mes_label",
        columns="serie",
        values="valor_num",
        aggfunc="sum"
    ).fillna(0)

    if as_percent:
        pivot = pivot.div(pivot.sum(axis=1).replace(0, pd.NA), axis=0) * 100

    fig = go.Figure()
    for serie in pivot.columns:
        fig.add_trace(
            go.Bar(
                x=pivot.index,
                y=pivot[serie],
                name=serie,
                marker_color=(color_map or {}).get(serie)
            )
        )

    fig.update_layout(
        barmode="stack",
        height=360,
        yaxis_title="%" if as_percent else "Quantidade"
    )
    fig = apply_plotly_theme(fig)
    plot(fig, prefix)

def pie_latest(df, title, color_map=None, prefix="pie"):
    st.markdown(f"**{title}**")
    work = df.dropna(subset=["valor_num"]).copy()
    if work.empty:
        st.info("Sem dados para este gráfico.")
        return

    latest_mes = work["mes"].dropna().max()
    latest = work[work["mes"] == latest_mes]
    if latest.empty:
        st.info("Sem dados para este gráfico.")
        return

    fig = px.pie(
        latest,
        names="serie",
        values="valor_num",
        color="serie",
        color_discrete_map=color_map or {}
    )

    fig.update_layout(height=360)
    fig = apply_plotly_theme(fig)
    plot(fig, prefix)
def render_upa_page(df, unidade):
    st.subheader(unidade)

    recep = filter_panel(df, unidade, "PACIENTES RECEPCIONADOS")
    atend_med = filter_panel(df, unidade, "ATENDIMENTOS MÉDICOS")
    risco = filter_panel(df, unidade, "ATENDIMENTOS POR CLASSIFICAÇÃO DE RISCO")
    perc_risco = filter_panel(df, unidade, "PERCENTUAL DE ATENDIMENTOS POR CLASSIFICAÇÃO DE RISCOS")
    espera = filter_panel(df, unidade, "TEMPO DE ESPERA PARA CLASSIFICAÇÃO DE RISCO")
    tempo_med = filter_panel(df, unidade, "TEMPO MÉDIO DE ESPERA DE ATENDIMENTO MÉDICO POR CLASSIFICAÇÃO DE RISCO")
    intern = filter_panel(df, unidade, "TEMPO DE PERMANÊNCIA DE PACIENTES INTERNADOS")
    semint = filter_panel(df, unidade, "TEMPO DE PERMANÊNCIA DE PACIENTES SEM INTERNAÇÃO")
    transf = filter_panel(df, unidade, "TRANSFERÊNCIAS (REMOÇÕES)")
    exames = filter_panel(df, unidade, "EXAMES INTERNOS")
    faixa = filter_panel(df, unidade, "ATENDIMENTOS DIVIDIDOS POR FAIXA ETARIA")
    origem = filter_panel(df, unidade, "ATENDIMENTOS DE  PACIENTES")
    obitos = filter_panel(df, unidade, "ÓBITOS")
    recep_ctx = build_kpi_context(recep, serie_norm="PACIENTES RECEPCIONADOS")
    atend_ctx = build_kpi_context(atend_med, serie_norm="ATENDIMENTOS MÉDICOS")
    obitos_ctx = build_kpi_context(obitos)
    exames_ctx = build_kpi_context(exames, exclude_series_norm="TOTAL")

    section_start("Resumo executivo", "Visão consolidada dos principais indicadores da unidade")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        card(
            "Pacientes recepcionados",
            format_int(recep_ctx["current"]),
            icon="👥",
            subtitle=f"Último mês selecionado • {recep_ctx['latest_month_label']}",
            delta_pct=recep_ctx["delta_pct"],
            delta_good_when="up",
            meta_value=recep_ctx["meta"],
            footer_text=f"Acumulado no período: {format_int(recep_ctx['total'])}"
        )

    with c2:
        card(
            "Atendimentos médicos",
            format_int(atend_ctx["current"]),
            icon="🩺",
            subtitle=f"Último mês selecionado • {atend_ctx['latest_month_label']}",
            delta_pct=atend_ctx["delta_pct"],
            delta_good_when="up",
            meta_value=atend_ctx["meta"],
            footer_text=f"Acumulado no período: {format_int(atend_ctx['total'])}"
        )

    with c3:
        card(
            "Óbitos",
            format_int(obitos_ctx["current"]),
            icon="⚠️",
            subtitle=f"Último mês selecionado • {obitos_ctx['latest_month_label']}",
            delta_pct=obitos_ctx["delta_pct"],
            delta_good_when="down",
            meta_value=None,
            footer_text=f"Acumulado no período: {format_int(obitos_ctx['total'])}"
        )

    with c4:
        card(
            "Exames internos",
            format_int(exames_ctx["current"]),
            icon="🧪",
            subtitle=f"Último mês selecionado • {exames_ctx['latest_month_label']}",
            delta_pct=exames_ctx["delta_pct"],
            delta_good_when="up",
            meta_value=None,
            footer_text=f"Acumulado no período: {format_int(exames_ctx['total'])}"
        )
    section_end()

    section_start("Produção assistencial", "Indicadores centrais de entrada e produção médica")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Pacientes recepcionados por mês + média diária**")
        fig = go.Figure()
        main = recep[recep["serie_norm"] == "PACIENTES RECEPCIONADOS"]
        avg = recep[recep["serie_norm"].isin(["MÉDIA DIÁRIA", "MEDIA DIÁRIA", "MEDIA DIARIA"])]

        if not main.empty:
            fig.add_trace(go.Bar(
                x=main["mes_label"],
                y=main["valor_num"],
                name="Pacientes recepcionados"
            ))
        if not avg.empty:
            fig.add_trace(go.Scatter(
                x=avg["mes_label"],
                y=avg["valor_num"],
                mode="lines+markers",
                name="Média diária"
            ))

        fig.update_layout(height=340)
        fig = apply_plotly_theme(fig)
        plot(fig, f"{unidade}_recep_media")

    with col2:
        line_with_optional_meta(
            atend_med,
            "Atendimentos médicos (comparando com a meta)",
            main_series="ATENDIMENTOS MÉDICOS",
            prefix=f"{unidade}_atend_med"
        )
    section_end()

    section_start("Risco e tempo assistencial", "Leitura da pressão assistencial, classificação e desempenho de atendimento")
    stacked_bar(
        risco[~risco["serie_norm"].eq("TOTAL DE ATENDIMENTOS")],
        "Atendimentos por classificação de risco",
        color_map=RISK_COLORS,
        prefix=f"{unidade}_risco_qtd"
    )

    stacked_bar(
        perc_risco[~perc_risco["serie_norm"].eq("TOTAL DE ATENDIMENTOS")],
        "Percentual de atendimentos por classificação de risco",
        color_map=RISK_COLORS,
        as_percent=True,
        prefix=f"{unidade}_risco_perc"
    )

    line_with_optional_meta(
        espera,
        "Tempo de espera para classificação de risco (comparando com a meta)",
        main_series="MÉDIA GERAL",
        unit_suffix="Minutos",
        prefix=f"{unidade}_espera_class"
    )

    st.markdown("**Tempo médio de espera de atendimento médico por classificação de risco**")
    med = tempo_med.dropna(subset=["valor_num"]).copy()
    fig = go.Figure()

    for serie in med["serie"].dropna().unique():
        temp = med[med["serie"] == serie]
        fig.add_trace(go.Scatter(
            x=temp["mes_label"],
            y=temp["valor_num"],
            mode="lines+markers",
            name=serie
        ))

    fig.update_layout(height=320, yaxis_title="Minutos")
    fig = apply_plotly_theme(fig)
    plot(fig, f"{unidade}_tempo_med_risco")
    section_end()

    section_start("Permanência, apoio e desfechos", "Indicadores operacionais complementares e perfil da demanda")
    col1, col2 = st.columns(2)
    with col1:
        grouped_bar(
            intern,
            "Tempo de permanência de pacientes internados",
            unit_suffix="Minutos",
            prefix=f"{unidade}_intern"
        )
    with col2:
        grouped_bar(
            semint,
            "Tempo de permanência de pacientes sem internação",
            unit_suffix="Minutos",
            prefix=f"{unidade}_semintern"
        )

    col1, col2 = st.columns(2)
    with col1:
        grouped_bar(transf, "Transferências (remoções)", prefix=f"{unidade}_transf")
    with col2:
        grouped_bar(
            exames[~exames["serie_norm"].eq("TOTAL")],
            "Exames internos",
            prefix=f"{unidade}_exames"
        )

    grouped_bar(
        faixa[~faixa["serie_norm"].eq("TOTAL")],
        "Atendimentos divididos por faixa etária",
        prefix=f"{unidade}_faixa"
    )

    col1, col2 = st.columns(2)
    with col1:
        grouped_bar(
            origem[~origem["serie_norm"].eq("TOTAL")],
            "Atendimentos de pacientes da cidade x outras cidades",
            prefix=f"{unidade}_origem_bar"
        )
    with col2:
        pie_latest(
            origem[~origem["serie_norm"].eq("TOTAL")],
            "Distribuição mais recente de pacientes por origem",
            prefix=f"{unidade}_origem_pie"
        )

    grouped_bar(obitos, "Óbitos", prefix=f"{unidade}_obitos")
    section_end()

def render_hmji(df):
    unidade = "HMJI"
    st.subheader(unidade)

    clin = filter_panel(df, unidade, "PACIENTES CLÍNICOS ATENDIDOS")
    obitos = filter_panel(df, unidade, "ÓBITOS")
    esp = filter_panel(df, unidade, "CONSULTAS ESPECIALIZADAS")
    exames = filter_panel(df, unidade, "EXAMES INTERNOS")
    cir = filter_panel(df, unidade, "PROCEDIMENTOS CIRÚRGICOS")
    anes = filter_panel(df, unidade, "ANESTESIAS")
    clin_ctx = build_kpi_context(clin, serie_norm="PACIENTES CLÍNICOS ATENDIDOS")
    obitos_ctx = build_kpi_context(obitos)
    cir_ctx = build_kpi_context(cir)

    c1, c2, c3 = st.columns(3)

    with c1:
        card(
            "Pacientes clínicos",
            format_int(clin_ctx["current"]),
            icon="🏥",
            subtitle=f"Último mês selecionado • {clin_ctx['latest_month_label']}",
            delta_pct=clin_ctx["delta_pct"],
            delta_good_when="up",
            meta_value=clin_ctx["meta"],
            footer_text=f"Acumulado no período: {format_int(clin_ctx['total'])}"
        )

    with c2:
        card(
            "Óbitos",
            format_int(obitos_ctx["current"]),
            icon="⚠️",
            subtitle=f"Último mês selecionado • {obitos_ctx['latest_month_label']}",
            delta_pct=obitos_ctx["delta_pct"],
            delta_good_when="down",
            meta_value=None,
            footer_text=f"Acumulado no período: {format_int(obitos_ctx['total'])}"
        )

    with c3:
        card(
            "Procedimentos cirúrgicos",
            format_int(cir_ctx["current"]),
            icon="🩹",
            subtitle=f"Último mês selecionado • {cir_ctx['latest_month_label']}",
            delta_pct=cir_ctx["delta_pct"],
            delta_good_when="up",
            meta_value=cir_ctx["meta"],
            footer_text=f"Acumulado no período: {format_int(cir_ctx['total'])}"
        )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Pacientes clínicos atendidos / média diária**")
        fig = go.Figure()
        main = clin[clin["serie_norm"] == "PACIENTES CLÍNICOS ATENDIDOS"]
        avg = clin[clin["serie_norm"].isin(["MÉDIA DIÁRIA", "MEDIA DIÁRIA", "MEDIA DIARIA"])]
        if not main.empty:
            fig.add_trace(go.Bar(x=main["mes_label"], y=main["valor_num"], name="Pacientes clínicos"))
        if not avg.empty:
            fig.add_trace(go.Scatter(x=avg["mes_label"], y=avg["valor_num"], mode="lines+markers", name="Média diária"))
        fig.update_layout(height=320)
        fig = apply_plotly_theme(fig)
        plot(fig, f"{unidade}_pacientes")

    with col2:
        grouped_bar(obitos, "Óbitos", prefix=f"{unidade}_obitos")

    grouped_bar(esp, "Consultas especializadas", prefix=f"{unidade}_esp")
    grouped_bar(exames[~exames["serie_norm"].eq("TOTAL")], "Exames internos", prefix=f"{unidade}_exames")
    grouped_bar(cir, "Procedimentos cirúrgicos", prefix=f"{unidade}_cir")
    grouped_bar(anes, "Anestesias", prefix=f"{unidade}_anes")

def render_generic(df, unidade, paineis):
    st.subheader(unidade)
    for i,painel in enumerate(paineis, start=1):
        grouped_bar(filter_panel(df, unidade, painel), painel.title(), prefix=f"{unidade}_{i}")

st.markdown("""
<h1 style="margin-bottom:0;">📊 BI Município</h1>
<p style="margin-top:0; color:#64748B; font-size:16px;">
Painel executivo de indicadores assistenciais
</p>
""", unsafe_allow_html=True)
uploaded = st.sidebar.file_uploader("Planilha base (.xlsx)", type=["xlsx"])
data, source_name = load_workbook_data(uploaded.getvalue()) if uploaded else load_workbook_data(None)

if data.empty:
    base = Path(__file__).parent
    encontrados = sorted([x.name for x in base.glob("*.xlsx")]) + sorted([x.name for x in base.glob("*.xlsm")])
    st.warning("Não encontrei uma planilha válida automaticamente. Envie um arquivo .xlsx na barra lateral ou deixe o Excel na mesma pasta do app.")
    if encontrados:
        st.info("Arquivos Excel encontrados na pasta do app: " + ", ".join(encontrados))
    else:
        st.info("Nenhum arquivo Excel foi encontrado na mesma pasta do app.")
    st.stop()

st.sidebar.success(f"Fonte: {source_name}")
st.sidebar.markdown("## Navegação")
pagina = st.sidebar.radio(
    "Selecione a página",
    ["UPA Luziânia", "UPA Jardim Ingá", "HMJI", "Atenção Secundária", "Saúde Mental", "Atenção Primária"]
)

st.sidebar.markdown("## Filtros")
meses_selecionados = st.sidebar.multiselect(
    "Período",
    [MESES_LABEL[m] for m in MESES],
    default=[MESES_LABEL[m] for m in MESES]
)
if meses_selecionados:
    data = data[data["mes_label"].isin(meses_selecionados)].copy()
hero_header(pagina, source_name, meses_selecionados)

if pagina == "UPA Luziânia":
    render_upa_page(data, "UPA DE LUZIÂNIA - UPA II")
elif pagina == "UPA Jardim Ingá":
    render_upa_page(data, "UPA JARDIM INGÁ - UPA I")
elif pagina == "HMJI":
    render_hmji(data)
elif pagina == "Atenção Secundária":
    render_generic(data, "ATENÇÃO SECUNDÁRIA", [
        "CONSULTAS ESPECIALIZADAS (CAIS)",
        "CONSULTAS ESPECIALIZADAS (MATERNO INFANTIL)",
        "CONSULTAS ESPECIALIZADAS (FARMÁCIA CENTRAL)",
    ])
elif pagina == "Saúde Mental":
    render_generic(data, "SAÚDE MENTAL", [
        "CONSULTAS ESPECIALIZADAS (CAPS II)",
        "CONSULTAS ESPECIALIZADAS (CAPS AD III)",
        "CONSULTAS ESPECIALIZADAS (CLÍNICA PSICOLOGIA)",
    ])
else:
    render_generic(data, "ATENÇÃO PRIMÁRIA", [
        "CONSULTAS MÉDICAS",
        "NÍVEL SUPERIOR (EXCETO MÉDICO)",
    ])

with st.expander("Base transformada"):
    st.dataframe(data, use_container_width=True, hide_index=True)
