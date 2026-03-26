
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
    background: #0B1220;
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
    background: #0B1220;
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
    border: 1px solid rgba(255,255,255,0.05);
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
    border: 1px solid rgba(255,255,255,0.05);
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

def format_delta_pct(delta):
    if delta is None or pd.isna(delta):
        return "—"
    return f"{delta:+.1f}%".replace(".", ",")

def delta_arrow(delta):
    if delta is None or pd.isna(delta):
        return "•"
    if delta > 0:
        return "↑"
    if delta < 0:
        return "↓"
    return "→"

def delta_color(delta, inverse=False):
    """
    inverse=False: maior é melhor
    inverse=True: menor é melhor
    """
    if delta is None or pd.isna(delta):
        return SEMANTIC_COLORS["neutral"]

    if inverse:
        if delta < 0:
            return SEMANTIC_COLORS["success"]
        if delta > 0:
            return SEMANTIC_COLORS["danger"]
        return SEMANTIC_COLORS["warning"]

    if delta > 0:
        return SEMANTIC_COLORS["success"]
    if delta < 0:
        return SEMANTIC_COLORS["danger"]
    return SEMANTIC_COLORS["warning"]

def format_meta_line(current=None, meta=None):
    if current is None or meta is None or pd.isna(current) or pd.isna(meta):
        return "Meta: —"

    diff = current - meta
    status = "acima"
    if diff < 0:
        status = "abaixo"
    elif diff == 0:
        status = "em linha"

    return (
        f"Meta: {clean_card_value(meta)}"
        f" • {status} em {clean_card_value(abs(diff)) if diff != 0 else '0'}"
    )

def card(title, value, icon="📊", subtitle="Indicador consolidado"):
    value = clean_card_value(value)

    html = (
        '<div style="'
        'background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);'
        'border: 1px solid #E2E8F0;'
        'border-radius: 20px;'
        'padding: 18px 18px 16px 18px;'
        'box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);'
        'min-height: 130px;'
        'display: flex;'
        'flex-direction: column;'
        'justify-content: space-between;'
        '">'
            '<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">'
                '<div>'
                    f'<div style="font-size: 13px; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">{title}</div>'
                    f'<div style="font-size: 12px; color: #94A3B8;">{subtitle}</div>'
                '</div>'
                f'<div style="width: 42px; height: 42px; border-radius: 12px; background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%); display:flex; align-items:center; justify-content:center; font-size: 20px;">{icon}</div>'
            '</div>'
            f'<div style="font-size: 32px; font-weight: 800; color: #0F172A; line-height: 1; margin-top: 8px;">{value}</div>'
        '</div>'
    )

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
        """
        <style>
        .hero-wrap {
            background: linear-gradient(135deg, #0F172A 0%, #12324A 50%, #0F6CBD 100%);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 24px;
            padding: 1.15rem 1.25rem;
            margin-top: 0.2rem;
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
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 999px;
            padding: 0.42rem 0.78rem;
            font-size: 0.82rem;
            font-weight: 600;
            backdrop-filter: blur(6px);
        }

        .logo-slot {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            padding-top: 0.35rem;
        }
        .logo-left {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            margin-top: 80px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1.2, 6, 1.2])

    with col1:
        st.markdown('<div class="logo-left">', unsafe_allow_html=True)
        try:
            st.image("assets/patris.png", width=315)
        except Exception:
            st.empty()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
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

    with col3:
        st.markdown('<div class="logo-slot">', unsafe_allow_html=True)
        try:
            st.image("assets/prefeitura.png", width=315)
        except Exception:
            st.empty()
        st.markdown("</div>", unsafe_allow_html=True)
SEMANTIC_COLORS = {
    # identidade base
    "primary": "#0F6CBD",
    "primary_soft": "#93C5FD",
    "secondary": "#0F172A",

    # estados
    "success": "#16A34A",
    "warning": "#F59E0B",
    "danger": "#DC2626",
    "neutral": "#64748B",
    "info": "#0891B2",

    # leitura executiva
    "realizado": "#0F6CBD",
    "realizado_soft": "#93C5FD",
    "media": "#38BDF8",
    "meta": "#94A3B8",
    "alerta": "#DC2626",
    "bom": "#16A34A",
    "atencao": "#F59E0B",
    "critico": "#DC2626",

    # apoio visual
    "grid": "rgba(148,163,184,0.14)",
    "axis": "#94A3B8",
    "text": "#CFD7E2",
    "title": "#F6F7FB",
    "plot_bg": "#0F172A",

    # séries neutras
    "series_1": "#0F6CBD",
    "series_2": "#16A34A",
    "series_3": "#F59E0B",
    "series_4": "#DC2626",
    "series_5": "#7C3AED",
    "series_6": "#0891B2",
    "series_7": "#64748B",
}

APP_COLORS = {
    "primary": SEMANTIC_COLORS["primary"],
    "primary_soft": SEMANTIC_COLORS["primary_soft"],
    "secondary": SEMANTIC_COLORS["secondary"],
    "success": SEMANTIC_COLORS["success"],
    "warning": SEMANTIC_COLORS["warning"],
    "danger": SEMANTIC_COLORS["danger"],
    "neutral": SEMANTIC_COLORS["neutral"],
    "grid": SEMANTIC_COLORS["grid"],
    "axis": SEMANTIC_COLORS["axis"],
    "text": SEMANTIC_COLORS["text"],
    "title": SEMANTIC_COLORS["title"],
    "plot_bg": SEMANTIC_COLORS["plot_bg"],
}

DEFAULT_CHART_COLORS = [
    SEMANTIC_COLORS["series_1"],
    SEMANTIC_COLORS["series_2"],
    SEMANTIC_COLORS["series_3"],
    SEMANTIC_COLORS["series_4"],
    SEMANTIC_COLORS["series_5"],
    SEMANTIC_COLORS["series_6"],
    SEMANTIC_COLORS["series_7"],
]

def semantic_color(name, default=None):
    if not name:
        return default or SEMANTIC_COLORS["neutral"]

    key = str(name).strip().upper()

    # meta / referência
    if "META" in key:
        return SEMANTIC_COLORS["meta"]

    # médias
    if "MÉDIA" in key or "MEDIA" in key:
        return SEMANTIC_COLORS["media"]

    # alertas / eventos críticos
    if "ÓBITO" in key or "OBITO" in key:
        return SEMANTIC_COLORS["danger"]

    # risco
    if key in RISK_COLORS:
        return RISK_COLORS[key]

    # séries principais comuns
    if "ATENDIMENTOS MÉDICOS" in key:
        return SEMANTIC_COLORS["realizado"]

    if "PACIENTES RECEPCIONADOS" in key:
        return SEMANTIC_COLORS["realizado_soft"]

    if "MÉDIA GERAL" in key or "MEDIA GERAL" in key:
        return SEMANTIC_COLORS["media"]

    return default or SEMANTIC_COLORS["neutral"]

def build_semantic_color_map(series_list):
    palette = [
        SEMANTIC_COLORS["series_1"],
        SEMANTIC_COLORS["series_2"],
        SEMANTIC_COLORS["series_3"],
        SEMANTIC_COLORS["series_4"],
        SEMANTIC_COLORS["series_5"],
        SEMANTIC_COLORS["series_6"],
        SEMANTIC_COLORS["series_7"],
    ]

    color_map = {}
    fallback_idx = 0

    for serie in series_list:
        forced = semantic_color(serie, default=None)
        if forced is not None and forced != SEMANTIC_COLORS["neutral"]:
            color_map[serie] = forced
        else:
            color_map[serie] = palette[fallback_idx % len(palette)]
            fallback_idx += 1

    return color_map

def apply_plotly_theme(
    fig,
    title=None,
    subtitle=None,
    yaxis_title="",
    height=360,
    legend=True,
    legend_orientation="h",
    tick_angle=0
):
    full_title = ""
    if title:
        full_title = f"<b>{title}</b>"
        if subtitle:
            full_title += f"<br><span style='font-size:12px; color:#64748B; font-weight:400'>{subtitle}</span>"

    fig.update_layout(
        title=dict(
            text=full_title,
            x=0.0,
            xanchor="left",
            y=0.97,
            yanchor="top"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=APP_COLORS["plot_bg"],
        font=dict(
            family="Inter, Segoe UI, Arial, sans-serif",
            color=APP_COLORS["text"],
            size=12
        ),
        title_font=dict(
            color=APP_COLORS["title"],
            size=18
        ),
        colorway=DEFAULT_CHART_COLORS,
        height=height,
        margin=dict(l=30, r=18, t=78, b=72),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#CBD5E1",
            font=dict(color="#0F172A", size=12)
        ),
        bargap=0.30,
        bargroupgap=0.10
    )

    first_x_len = 0
    try:
        if fig.data and hasattr(fig.data[0], "x") and fig.data[0].x is not None:
            first_x_len = len(fig.data[0].x)
    except Exception:
        first_x_len = 0

    auto_tick_angle = 0 if first_x_len <= 5 else -45

    fig.update_xaxes(
        title_text="",
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(color="#64748B", size=10.5),
        tickangle=auto_tick_angle if tick_angle == 0 else tick_angle,
        automargin=True,
        ticklabeloverflow="allow"
    )

    fig.update_yaxes(
        title_text=yaxis_title,
        showgrid=True,
        gridcolor=APP_COLORS["grid"],
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickfont=dict(color="#64748B", size=11),
        title_font=dict(color="#64748B", size=12),
        automargin=True
    )

    if legend:
        fig.update_layout(
            showlegend=True,
            legend=dict(
                title="",
                orientation=legend_orientation,
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0,
                font=dict(size=11, color="#64748B"),
                traceorder="normal"
            )
        )
    else:
        fig.update_layout(showlegend=False)

    return fig
def chart_subtitle(df, unidade=None):
    meses = [m for m in df.get("mes_label", pd.Series(dtype=str)).dropna().unique().tolist()]
    if not meses:
        periodo_txt = "Sem período"
    elif len(meses) == 1:
        periodo_txt = meses[0]
    else:
        periodo_txt = f"{meses[0]} a {meses[-1]}"

    if unidade:
        return f"{unidade} • {periodo_txt}"
    return periodo_txt

def ordered_month_labels(df):
    if df is None or df.empty or "mes" not in df.columns:
        return []

    meses_validos = (
        df["mes"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    meses_ordenados = [m for m in MESES if m in meses_validos]
    return [MESES_LABEL.get(m, m) for m in meses_ordenados]


def apply_month_axis_order(fig, df):
    ordered_labels = ordered_month_labels(df)
    if not ordered_labels:
        return fig

    fig.update_xaxes(
        type="category",
        categoryorder="array",
        categoryarray=ordered_labels,
        tickmode="array",
        tickvals=ordered_labels,
        ticktext=ordered_labels
    )
    return fig

def truncate_series_name(name, max_len=28):
    name = str(name)
    return name if len(name) <= max_len else name[:max_len-3] + "..."


def clean_trace_names(fig):
    return fig


def smart_legend_visibility(df, max_series_horizontal=5):
    n = df["serie"].dropna().nunique() if "serie" in df.columns else 0
    return n > 1, ("h" if n <= max_series_horizontal else "h") 
def line_with_optional_meta(
    df,
    title,
    main_series=None,
    unit_suffix="",
    prefix="line",
    unidade=None
):
    work = df.dropna(subset=["valor_num"]).copy()
    if work.empty:
        st.info("Sem dados para este gráfico.")
        return

    fig = go.Figure()

    if main_series:
        main = work[work["serie_norm"] == str(main_series).upper()]
        if not main.empty:
            main_color = semantic_color(main_series, default=SEMANTIC_COLORS["realizado"])

            fig.add_trace(
                go.Scatter(
                    x=main["mes_label"],
                    y=main["valor_num"],
                    mode="lines+markers",
                    name=str(main_series).title(),
                    line=dict(color=main_color, width=3.5),
                    marker=dict(size=7, color=main_color),
                    hovertemplate="<b>%{fullData.name}</b><br>Mês: %{x}<br>Valor: %{y:,.1f}<extra></extra>"
                )
            )

        others = work[
            (~work["serie_norm"].eq(str(main_series).upper())) &
            (~work["serie_norm"].eq("META"))
        ]

        for serie in others["serie"].dropna().unique().tolist():
            temp = others[others["serie"] == serie]
            serie_color = semantic_color(serie, default=SEMANTIC_COLORS["neutral"])

            fig.add_trace(
                go.Scatter(
                    x=temp["mes_label"],
                    y=temp["valor_num"],
                    mode="lines+markers",
                    name=str(serie),
                    line=dict(color=serie_color, width=2),
                    marker=dict(size=5, color=serie_color),
                    opacity=0.65,
                    hovertemplate="<b>%{fullData.name}</b><br>Mês: %{x}<br>Valor: %{y:,.1f}<extra></extra>"
                )
            )
    else:
        series = work["serie"].dropna().unique().tolist()
        color_map = build_semantic_color_map(series)

        for serie in series:
            temp = work[work["serie"] == serie]
            serie_color = color_map.get(serie, SEMANTIC_COLORS["neutral"])

            fig.add_trace(
                go.Scatter(
                    x=temp["mes_label"],
                    y=temp["valor_num"],
                    mode="lines+markers",
                    name=str(serie),
                    line=dict(color=serie_color, width=2.4),
                    marker=dict(size=5.5, color=serie_color),
                    opacity=0.9 if semantic_color(serie, default=None) else 0.72,
                    hovertemplate="<b>%{fullData.name}</b><br>Mês: %{x}<br>Valor: %{y:,.1f}<extra></extra>"
                )
            )

    meta = work[work["serie_norm"] == "META"]
    if not meta.empty:
        meta_color = SEMANTIC_COLORS["meta"]
        fig.add_trace(
            go.Scatter(
                x=meta["mes_label"],
                y=meta["valor_num"],
                mode="lines+markers",
                name="Meta",
                line=dict(color=meta_color, width=2, dash="dash"),
                marker=dict(size=5, color=meta_color),
                hovertemplate="<b>Meta</b><br>Mês: %{x}<br>Valor: %{y:,.1f}<extra></extra>"
            )
        )

    fig = apply_plotly_theme(
        fig,
        title=title,
        subtitle=chart_subtitle(work, unidade),
        yaxis_title=unit_suffix,
        height=350,
        legend=True,
        legend_orientation="h"
    )

    fig = apply_month_axis_order(fig, work)

    plot(fig, prefix)


def grouped_bar(
    df,
    title,
    color_map=None,
    barmode="group",
    unit_suffix="",
    prefix="bar",
    unidade=None
):
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

    fig.update_traces(
        marker_line_width=0,
        hovertemplate="<b>%{fullData.name}</b><br>Mês: %{x}<br>Valor: %{y:,.0f}<extra></extra>"
    )

    fig = apply_plotly_theme(
        fig,
        title=title,
        subtitle=chart_subtitle(work, unidade),
        yaxis_title=unit_suffix,
        height=380,
        legend=True,
        legend_orientation="h"
    )

    fig = apply_month_axis_order(fig, work)

    plot(fig, prefix)


def stacked_bar(
    df,
    title,
    color_map=None,
    as_percent=False,
    prefix="stack",
    unidade=None
):
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
                name=str(serie),
                marker_color=(color_map or {}).get(serie),
                hovertemplate=f"<b>{serie}</b><br>Mês: %{{x}}<br>Valor: %{{y:.1f}}{'%' if as_percent else ''}<extra></extra>"
            )
        )

    fig = apply_plotly_theme(
        fig,
        title=title,
        subtitle=chart_subtitle(work, unidade),
        yaxis_title="Percentual (%)" if as_percent else "Quantidade",
        height=390,
        legend=True,
        legend_orientation="h"
    )

    fig.update_layout(barmode="stack")

    if as_percent:
        fig.update_yaxes(range=[0, 100])

    fig = apply_month_axis_order(fig, work)

    plot(fig, prefix)


def pie_latest(df, title, color_map=None, prefix="pie", unidade=None):
    work = df.dropna(subset=["valor_num"]).copy()
    if work.empty:
        st.info("Sem dados para este gráfico.")
        return

    latest_mes = work["mes"].dropna().max()
    latest = work[work["mes"] == latest_mes].copy()
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

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hole=0.45,
        sort=False,
        hovertemplate="<b>%{label}</b><br>Valor: %{value:,.0f}<br>Participação: %{percent}<extra></extra>"
    )

    fig = apply_plotly_theme(
        fig,
        title=title,
        subtitle=f"{unidade + ' • ' if unidade else ''}{MESES_LABEL.get(latest_mes, latest_mes)}",
        height=380,
        legend=True,
        legend_orientation="h"
    )

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

    section_start("Resumo executivo", "Visão consolidada dos principais indicadores da unidade")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        card(
            "Pacientes recepcionados",
            format_int(recep["valor_num"].sum()),
            icon="👥",
            subtitle="Volume total no período"
        )

    with c2:
        card(
            "Atendimentos médicos",
            format_int(atend_med[atend_med["serie_norm"] == "ATENDIMENTOS MÉDICOS"]["valor_num"].sum()),
            icon="🩺",
            subtitle="Produção médica consolidada"
        )

    with c3:
        card(
            "Óbitos",
            format_int(obitos["valor_num"].sum()),
            icon="⚠️",
            subtitle="Ocorrências registradas"
        )

    with c4:
        card(
            "Exames internos",
            format_int(exames[~exames["serie_norm"].eq("TOTAL")]["valor_num"].sum()),
            icon="🧪",
            subtitle="Procedimentos realizados"
        )
    section_end()

    section_start("Produção assistencial", "Indicadores centrais de entrada e produção médica")
    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()

        main = recep[recep["serie_norm"] == "PACIENTES RECEPCIONADOS"]
        avg = recep[recep["serie_norm"].isin(["MÉDIA DIÁRIA", "MEDIA DIÁRIA", "MEDIA DIARIA"])]

        if not main.empty:
            fig.add_trace(
                go.Bar(
                    x=main["mes_label"],
                    y=main["valor_num"],
                    name="Pacientes recepcionados",
                    marker_color=APP_COLORS["primary_soft"],
                    hovertemplate="<b>Pacientes recepcionados</b><br>Mês: %{x}<br>Total: %{y:,.0f}<extra></extra>"
            )
        )

        if not avg.empty:
            fig.add_trace(
                go.Scatter(
                    x=avg["mes_label"],
                    y=avg["valor_num"],
                    mode="lines+markers",
                    name="Média diária",
                    line=dict(color=APP_COLORS["primary"], width=3),
                    marker=dict(color=APP_COLORS["primary"], size=7),
                    hovertemplate="<b>Média diária</b><br>Mês: %{x}<br>Valor: %{y:,.1f}<extra></extra>"
               )
           )

        fig = clean_trace_names(fig)

        fig = apply_plotly_theme(
            fig,
            title="Pacientes recepcionados por mês",
            subtitle=chart_subtitle(recep, unidade) + " • total mensal + média diária",
            yaxis_title="Quantidade",
            height=380,
            legend=True,
            legend_orientation="h"
        )

        fig = apply_month_axis_order(fig, recep)

        plot(fig, f"{unidade}_recep_media")
    
    with col2:
        line_with_optional_meta(
            atend_med,
            "Atendimentos médicos vs meta",
            main_series="ATENDIMENTOS MÉDICOS",
            prefix=f"{unidade}_atend_med",
            unidade=unidade
        )
    section_end()

    section_start("Risco e tempo assistencial", "Leitura da pressão assistencial, classificação e desempenho de atendimento")
    stacked_bar(
        risco[~risco["serie_norm"].eq("TOTAL DE ATENDIMENTOS")],
        "Atendimentos por classificação de risco",
        color_map=RISK_COLORS,
        prefix=f"{unidade}_risco_qtd",
        unidade=unidade
    )

    stacked_bar(
        perc_risco[~perc_risco["serie_norm"].eq("TOTAL DE ATENDIMENTOS")],
        "Percentual de atendimentos por classificação de risco",
        color_map=RISK_COLORS,
        as_percent=True,
        prefix=f"{unidade}_risco_perc",
        unidade=unidade
    )

    line_with_optional_meta(
        espera,
        "Tempo de espera para classificação de risco vs meta",
        main_series="MÉDIA GERAL",
        unit_suffix="Minutos",
        prefix=f"{unidade}_espera_class",
        unidade=unidade
    )

    st.markdown("**Tempo médio de espera de atendimento médico por classificação de risco**")
    med = tempo_med.dropna(subset=["valor_num"]).copy()
    fig = go.Figure()

    series_med = med["serie"].dropna().unique().tolist()
    med_color_map = build_semantic_color_map(series_med)

    for serie in series_med:
        temp = med[med["serie"] == serie]
        serie_color = semantic_color(serie, default=med_color_map.get(serie, SEMANTIC_COLORS["neutral"]))

        fig.add_trace(
            go.Scatter(
                x=temp["mes_label"],
                y=temp["valor_num"],
                mode="lines+markers",
                name=serie,
                line=dict(color=serie_color, width=3 if "MÉDIA GERAL" in str(serie).upper() or "MEDIA GERAL" in str(serie).upper() else 2.4),
                marker=dict(size=6, color=serie_color),
                opacity=1 if "MÉDIA GERAL" in str(serie).upper() or "MEDIA GERAL" in str(serie).upper() else 0.88,
                hovertemplate="<b>%{fullData.name}</b><br>Mês: %{x}<br>Valor: %{y:,.1f}<extra></extra>"
            )
        ) 
    fig = clean_trace_names(fig)
    fig = apply_plotly_theme(
        fig,
        title="Tempo médio de espera de atendimento médico por classificação de risco",
        subtitle=chart_subtitle(med, unidade),
        yaxis_title="Minutos",
        height=360,
        legend=True,
        legend_orientation="h"
    )

    fig = apply_month_axis_order(fig, med)

    plot(fig, f"{unidade}_tempo_med_risco")
    section_end()

    section_start("Permanência, apoio e desfechos", "Indicadores operacionais complementares e perfil da demanda")
    col1, col2 = st.columns(2)
    with col1:
        grouped_bar(
            intern,
            "Tempo de permanência de pacientes internados",
            unit_suffix="Minutos",
            prefix=f"{unidade}_intern",
            unidade=unidade
        )
    with col2:
        grouped_bar(
            semint,
            "Tempo de permanência de pacientes sem internação",
            unit_suffix="Minutos",
            prefix=f"{unidade}_semintern",
            unidade=unidade
        )

    col1, col2 = st.columns(2)
    with col1:
        grouped_bar(
            transf,
            "Transferências (remoções)",
            prefix=f"{unidade}_transf",
            unidade=unidade
        )
    with col2:
        grouped_bar(
            exames[~exames["serie_norm"].eq("TOTAL")],
            "Exames internos",
            prefix=f"{unidade}_exames",
            unidade=unidade
        )

        grouped_bar(
            faixa[~faixa["serie_norm"].eq("TOTAL")],
            "Atendimentos divididos por faixa etária",
            prefix=f"{unidade}_faixa",
            unidade=unidade
        )

    col1, col2 = st.columns(2)
    with col1:
        grouped_bar(
            origem[~origem["serie_norm"].eq("TOTAL")],
            "Atendimentos de pacientes da cidade x outras cidades",
            prefix=f"{unidade}_origem_bar",
            unidade=unidade
        )
    with col2:
        pie_latest(
            origem[~origem["serie_norm"].eq("TOTAL")],
            "Distribuição mais recente de pacientes por origem",
            prefix=f"{unidade}_origem_pie",
            unidade=unidade
        )

        grouped_bar(
            obitos,
            "Óbitos",
            prefix=f"{unidade}_obitos",
            unidade=unidade
        )
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

    c1, c2, c3 = st.columns(3)

    with c1:
        card(
            "Pacientes clínicos",
            format_int(clin[clin["serie_norm"] == "PACIENTES CLÍNICOS ATENDIDOS"]["valor_num"].sum()),
            icon="🏥",
            subtitle="Atendimentos no período"
        )

    with c2:
        card(
            "Óbitos",
            format_int(obitos["valor_num"].sum()),
            icon="⚠️",
            subtitle="Eventos registrados"
        )

    with c3:
        card(
            "Procedimentos cirúrgicos",
            format_int(cir["valor_num"].sum()),
            icon="🩹",
            subtitle="Produção cirúrgica"
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
        fig = apply_month_axis_order(fig, clin)
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
<h1 style="margin-bottom:0;">
<p style="margin-top:0; color:#64748B; font-size:16px;">
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
