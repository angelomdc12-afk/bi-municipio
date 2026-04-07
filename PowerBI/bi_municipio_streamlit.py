import datetime as dt
from datetime import timedelta
from io import BytesIO
from pathlib import Path
import base64

import openpyxl
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
    
USUARIOS_APP = {
    "admin": "Mudar36315515#26%",
    "vittor": "patris2026",
    "wendel": "inovar2026",
    "guilherme": "patris2026",
    "denis": "inovar2026",
}
TEMPO_SESSAO_HORAS = 8

def render_login():
    st.markdown("""
    <style>
    .login-box {
        max-width: 420px;
        margin: 80px auto;
        padding: 32px 28px;
        background: white;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
        border: 1px solid #E5E7EB;
    }
        .login-title {
            text-align: center;
            font-size: 28px;
            font-weight: 800;
            color: #0F172A;
            margin-bottom: 8px;
        }
        .login-subtitle {
            text-align: center;
            font-size: 14px;
            color: #64748B;
            margin-bottom: 24px;
        }
/* ===== FILTRO DE PERÍODO / MULTISELECT ===== */

/* caixa externa do multiselect */
div[data-testid="stPlotlyChart"] {
    background: #071224;
    border: none;
    border-radius: 22px;
    padding: 0.35rem 0.35rem 0.15rem 0.35rem;
    box-shadow: none;
}
                
div[data-testid="stPlotlyChart"] > div {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}                

/* hover */
section[data-testid="stSidebar"] .stMultiSelect > div > div:hover {
    border-color: rgba(255,255,255,0.18) !important;
    background: rgba(255,255,255,0.08) !important;
}

/* foco */
section[data-testid="stSidebar"] .stMultiSelect > div > div:focus-within {
    border-color: #7CC0F2 !important;
    box-shadow: 0 0 0 1px rgba(124,192,242,0.35) !important;
    background: rgba(255,255,255,0.09) !important;
}

/* tags selecionadas */
section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] {
    background: rgba(255,255,255,0.14) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    padding: 3px 8px !important;
    margin: 3px !important;
}

/* texto dentro da tag */
section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] span {
    color: #FFFFFF !important;
    font-size: 13px !important;
}

/* botão x da tag */
section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] svg {
    fill: rgba(255,255,255,0.88) !important;
}

/* campo de digitação */
section[data-testid="stSidebar"] .stMultiSelect input {
    color: #FFFFFF !important;
}

/* placeholder */
section[data-testid="stSidebar"] .stMultiSelect input::placeholder {
    color: rgba(255,255,255,0.55) !important;
}

/* setinha do select */
section[data-testid="stSidebar"] .stMultiSelect svg {
    fill: rgba(255,255,255,0.75) !important;
}
/* ===== UPLOAD COMPACTO ===== */
section[data-testid="stSidebar"] .stFileUploader {
    padding: 6px !important;
    border-radius: 12px !important;
    margin-bottom: 10px !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

section[data-testid="stSidebar"] .stFileUploader section {
    padding: 8px 8px !important;
    border-radius: 10px !important;
    min-height: auto !important;
    background: rgba(5,10,20,0.82) !important;
}

section[data-testid="stSidebar"] .stFileUploader small {
    font-size: 10px !important;
    line-height: 1.2 !important;
}

section[data-testid="stSidebar"] .stFileUploader button {
    padding: 4px 8px !important;
    font-size: 11px !important;
    min-height: 30px !important;
    border-radius: 8px !important;
}

section[data-testid="stSidebar"] .stFileUploader label {
    font-size: 12px !important;
    margin-bottom: 4px !important;
}
st.sidebar.markdown("##### Atualizar base")
/* ===== UPLOAD COMO BOTÃO DISCRETO ===== */

/* remove caixa grande */
section[data-testid="stSidebar"] .stFileUploader section {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* remove texto padrão */
section[data-testid="stSidebar"] .stFileUploader small {
    display: none !important;
}

/* remove título padrão */
section[data-testid="stSidebar"] .stFileUploader label {
    display: none !important;
}

/* container geral */
section[data-testid="stSidebar"] .stFileUploader {
    margin-bottom: 10px !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
}

/* BOTÃO */
section[data-testid="stSidebar"] .stFileUploader button {
    width: 100% !important;
    background: linear-gradient(135deg, #1E6BA8 0%, #2B7BBB 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
    transition: all 0.2s ease !important;
}

/* hover */
section[data-testid="stSidebar"] .stFileUploader button:hover {
    background: linear-gradient(135deg, #2B7BBB 0%, #3C8ED1 100%) !important;
    transform: translateY(-1px);
}

/* quando arquivo carregado */
section[data-testid="stSidebar"] .stFileUploader div[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
}  
                /* ===== UPLOAD REALMENTE COMPACTO ===== */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    margin-bottom: 8px !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] > div {
    padding: 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    padding: 6px !important;
    min-height: auto !important;
    background: transparent !important;
    border: none !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] > div {
    padding: 0 !important;
    gap: 6px !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] small {
    display: none !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] div {
    font-size: 12px !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
    padding: 6px 10px !important;
    min-height: 32px !important;
    font-size: 12px !important;
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] .stFileUploader {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
} 
                /* ===== UPLOAD MAIS BAIXO E MENOR ===== */
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    min-height: 90px !important;
    padding: 8px 10px !important;
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] > div {
    min-height: 70px !important;
    gap: 4px !important;
    justify-content: center !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] div {
    font-size: 11px !important;
    line-height: 1.2 !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] small {
    display: none !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
    padding: 4px 8px !important;
    min-height: 28px !important;
    font-size: 11px !important;
    border-radius: 8px !important;
}     
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Acesso ao Painel</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Informe usuário e senha para continuar</div>', unsafe_allow_html=True)

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        entrar = st.button("Entrar", use_container_width=True)

    if entrar:
        usuario_ok = usuario in USUARIOS_APP
        senha_ok = usuario_ok and USUARIOS_APP[usuario] == senha

        if usuario_ok and senha_ok:
            st.session_state["autenticado"] = True
            st.session_state["usuario_logado"] = usuario
            st.session_state["login_em"] = dt.datetime.now()
            st.session_state["expira_em"] = dt.datetime.now() + timedelta(hours=TEMPO_SESSAO_HORAS)
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

    st.markdown('</div>', unsafe_allow_html=True)

def check_login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if st.session_state["autenticado"]:
        expira_em = st.session_state.get("expira_em")

        if expira_em and dt.datetime.now() > expira_em:
            st.session_state["autenticado"] = False
            st.session_state["usuario_logado"] = None
            st.session_state["login_em"] = None
            st.session_state["expira_em"] = None

    if not st.session_state["autenticado"]:
        render_login()
        st.stop()

st.set_page_config(page_title="Painel de Gestão Patris", page_icon="📊", layout="wide")

check_login()

st.set_page_config(page_title="Painel de Gestão Patris", page_icon="📊", layout="wide")

check_login()

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

LOGO_PATRIS = ASSETS_DIR / "patris.png"
LOGO_PREFEITURA = ASSETS_DIR / "prefeitura.png"
BACKGROUND_IMG = ASSETS_DIR / "background.png"

def image_to_base64(path):
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode("utf-8")

BACKGROUND_BASE64 = image_to_base64(BACKGROUND_IMG)

st.markdown(f"""
<style>

[data-testid="stAppViewContainer"] {{
    background-image:
        linear-gradient(rgba(239, 248, 255, 0.72), rgba(239, 248, 255, 0.82)),
        url("data:image/png;base64,{BACKGROUND_BASE64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-color: #EEF7FC;
}}

[data-testid="stMain"] {{
    background: transparent;
}}

/* ===== APP ===== */
.block-container {{
    padding-top: 1.1rem;
    padding-bottom: 2rem;
    padding-left: 1.6rem;
    padding-right: 1.6rem;
    max-width: 100%;
}}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0F4C81 0%, #0B2E4E 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}}

section[data-testid="stSidebar"] > div {{
    padding-top: 0.8rem;
}}

section[data-testid="stSidebar"] * {{
    color: #F8FAFC !important;
}}

/* MENU */
section[data-testid="stSidebar"] div[role="radiogroup"] label {{
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 10px;
    margin-bottom: 8px;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
    background: rgba(255,255,255,0.10);
}}

/* FILTROS */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background: rgba(255,255,255,0.06);
    border-radius: 12px;
}}

</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent

st.markdown("""
<style>

/* ===== APP ===== */
.block-container {{
    padding-top: 1.1rem;
    padding-bottom: 2rem;
    padding-left: 1.6rem;
    padding-right: 1.6rem;
    max-width: 100%;
}}

/* ===== SIDEBAR CLEAN (OPÇÃO 1) ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F4C81 0%, #0B2E4E 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* espaçamento geral */
section[data-testid="stSidebar"] > div {
    padding-top: 0.8rem;
}

/* textos */
section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

/* títulos */
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    font-weight: 800 !important;
    margin-bottom: 0.5rem;
}

/* ===== BLOCO UPLOAD ===== */
section[data-testid="stSidebar"] .stFileUploader {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px 12px 10px 12px;
    margin-bottom: 18px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
}

/* área interna do drag and drop */
section[data-testid="stSidebar"] .stFileUploader section {
    background: rgba(5,10,20,0.88) !important;
    border: 1px dashed rgba(255,255,255,0.10) !important;
    border-radius: 14px !important;
    padding: 18px 12px !important;
    min-height: auto !important;
}

/* texto principal do upload */
section[data-testid="stSidebar"] .stFileUploader section small,
section[data-testid="stSidebar"] .stFileUploader section div {
    color: #F8FAFC !important;
}

/* botão browse */
section[data-testid="stSidebar"] .stFileUploader button {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] .stFileUploader button:hover {
    background: rgba(255,255,255,0.16) !important;
    border-color: rgba(255,255,255,0.22) !important;
}

/* ===== RADIO (MENU) ===== */
section[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 10px 12px;
    margin-bottom: 8px;
    transition: all 0.18s ease;
}

/* hover menu */
section[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:hover {
    background: rgba(255,255,255,0.10);
    transform: translateX(3px);
}

/* texto menu */
section[data-testid="stSidebar"] div[role="radiogroup"] span {
    font-weight: 600;
}

/* ===== SELECT / FILTROS ===== */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
section[data-testid="stSidebar"] div[data-baseweb="input"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    min-height: 44px;
}

/* foco filtro */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
    border-color: #4DA3E6 !important;
}

/* ===== FILTRO DE PERÍODO ===== */

/* caixa principal do multiselect */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 16px !important;
    padding: 8px !important;
    min-height: 54px !important;
}

/* hover */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div:hover {
    border-color: rgba(255,255,255,0.18) !important;
    background: rgba(255,255,255,0.08) !important;
}

/* foco */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div:focus-within {
    border-color: #7CC0F2 !important;
    box-shadow: 0 0 0 1px rgba(124,192,242,0.35) !important;
}

/* tags selecionadas */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background: rgba(255,255,255,0.14) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    margin: 4px !important;
    padding: 2px 8px !important;
}

/* texto da tag */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] span {
    color: #FFFFFF !important;
    font-size: 13px !important;
}

/* ícone x */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] svg {
    fill: rgba(255,255,255,0.88) !important;
}

/* input interno */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] input {
    color: #FFFFFF !important;
}

/* placeholder */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] input::placeholder {
    color: rgba(255,255,255,0.60) !important;
}

/* ===== TEXTO AUXILIAR ===== */
section[data-testid="stSidebar"] small {
    color: rgba(255,255,255,0.65) !important;
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
    background: #071224 !important;
    border: none !important;
    border-radius: 22px !important;
    padding: 0.35rem 0.35rem 0.15rem 0.35rem !important;
    box-shadow: none !important;
}

div[data-testid="stPlotlyChart"] > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* ===== SECTION CARD ===== */
.section-card {
    background: transparent;
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
    background: linear-gradient(135deg, rgba(15,108,189,0.92) 0%, rgba(37,99,235,0.88) 100%);
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 24px;
    padding: 1.2rem 1.25rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 16px 36px rgba(15, 23, 42, 0.10);
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

MESES = [
    "MARCO.26", "ABRIL.26", "MAIO.26", "JUNHO.26",
    "JULHO.26", "AGOSTO.26", "SETEMBRO.26", "OUTUBRO.26",
    "NOVEMBRO.26", "DEZEMBRO.26", "JANEIRO.27", "FEVEREIRO.27"
]

MESES_LABEL = {
    "MARCO.26": "Mar/26",
    "ABRIL.26": "Abr/26",
    "MAIO.26": "Mai/26",
    "JUNHO.26": "Jun/26",
    "JULHO.26": "Jul/26",
    "AGOSTO.26": "Ago/26",
    "SETEMBRO.26": "Set/26",
    "OUTUBRO.26": "Out/26",
    "NOVEMBRO.26": "Nov/26",
    "DEZEMBRO.26": "Dez/26",
    "JANEIRO.27": "Jan/27",
    "FEVEREIRO.27": "Fev/27"
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

    # Excel pode entregar duração como timedelta
    if isinstance(v, dt.timedelta):
        return v.total_seconds() / 3600  # horas, sem arredondar

    # Excel pode entregar horário como dt.time
    if isinstance(v, dt.time):
        return v.hour + (v.minute / 60) + (v.second / 3600)  # horas, sem arredondar

    if isinstance(v, str):
        if v.startswith("#DIV/0"):
            return None

        vv = v.strip()

        # interpreta textos tipo 01:30 ou 01:30:00 como horas
        if ":" in vv:
            try:
                partes = vv.split(":")
                if len(partes) == 2:
                    h, m = partes
                    s = 0
                elif len(partes) == 3:
                    h, m, s = partes
                else:
                    h = m = s = None

                if h is not None:
                    return float(h) + float(m) / 60 + float(s) / 3600
            except Exception:
                pass

        vv = vv.replace(",", ".")
        try:
            return float(vv)
        except Exception:
            return v.strip()

    if isinstance(v, (int, float)):
        return float(v)

    return v


def normalize_text(value):
    if value is None:
        return None

    import unicodedata
    import re

    text = str(value).strip().upper()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = re.sub(r"\s+", " ", text).strip()

    return text if text else None


def row_values(ws, r, n=14):
    return [ws.cell(r, c).value for c in range(1, n + 1)]


def is_month_row(vals):
    months = [normalize_text(v) for v in vals[2:14] if v is not None]
    return len(months) >= 3 and all(m in MESES for m in months)


def parse_sheet(ws, sheet_name):
    rows = []
    unidade = str(ws["A2"].value).strip() if ws["A2"].value else sheet_name
    unidade_norm = normalize_text(unidade)

    painel = None
    painel_norm = None
    meses = None

    labels_especiais = {
        "META",
        "MEDIA DIARIA",
        "MÉDIA DIÁRIA",
        "MEDIA DIARIA",
    }

    for r in range(1, ws.max_row + 1):
        vals = row_values(ws, r)
        a, b = vals[0], vals[1]

        if is_month_row(vals):
            meses = [
                normalize_text(ws.cell(r, c).value) if ws.cell(r, c).value is not None else None
                for c in range(3, 15)
            ]
            continue

        if not any(v is not None for v in vals[2:14]):
            continue

        a_str = a.strip() if isinstance(a, str) else None
        b_str = b.strip() if isinstance(b, str) else None

        a_norm = normalize_text(a_str)
        b_norm = normalize_text(b_str)

        if a_norm == "INDICADOR":
            continue

        if a_norm and a_norm not in labels_especiais and b_norm:
            painel = a_str
            painel_norm = a_norm
            serie = b_str
        elif a_norm and a_norm not in labels_especiais and not b_norm:
            painel = a_str
            painel_norm = a_norm
            serie = a_str
        elif a_norm in labels_especiais and painel:
            serie = a_str
        elif b_norm and painel:
            serie = b_str
        else:
            continue

        serie_norm = normalize_text(serie)

        for i, c in enumerate(range(3, 15)):
            mes = meses[i] if meses and i < len(meses) else None
            rows.append({
                "aba": sheet_name,
                "unidade": unidade,
                "unidade_norm": unidade_norm,
                "painel": painel,
                "painel_norm": painel_norm,
                "serie": serie,
                "serie_norm": serie_norm,
                "mes": mes,
                "mes_label": MESES_LABEL.get(mes, mes),
                "valor": normalize_value(ws.cell(r, c).value),
            })

    df = pd.DataFrame(rows)
    if not df.empty:
        df["valor_num"] = pd.to_numeric(df["valor"], errors="coerce")
        df["mes"] = pd.Categorical(df["mes"], categories=MESES, ordered=True)
        df = df.sort_values(["unidade_norm", "painel_norm", "serie_norm", "mes"])
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
        "INDICADORES RH"
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


@st.cache_data(show_spinner=False)
def load_metas_data(file_bytes=None):
    colunas_padrao = [
        "categoria",
        "categoria_norm",
        "mes",
        "mes_label",
        "executado",
        "meta",
        "executado_total",
        "meta_total",
    ]

    if file_bytes is None:
        path = local_excel_path()
        if not path:
            return pd.DataFrame(columns=colunas_padrao)
        wb = openpyxl.load_workbook(path, data_only=True)
    else:
        wb = openpyxl.load_workbook(BytesIO(file_bytes), data_only=True)

    nome_aba = "METAS DO PLANO DE TRABALHO"
    if nome_aba not in wb.sheetnames:
        return pd.DataFrame(columns=colunas_padrao)

    ws = wb[nome_aba]

    rows = []
    meses = None
    categoria_atual = None

    for r in range(1, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 16)]

        linha_meses = [normalize_text(v) for v in vals[2:14] if v is not None]
        if len(linha_meses) >= 3 and all(m in MESES for m in linha_meses):
            meses = [normalize_text(v) if v is not None else None for v in vals[2:14]]
            continue

        col_b = vals[1]
        col_b_norm = normalize_text(col_b)

        if not col_b_norm:
            continue

        if col_b_norm == "TOTAL GERAL":
            continue

        # linha da categoria = executado
        if col_b_norm != "META":
            categoria_atual = str(col_b).strip()

            for i, c in enumerate(range(3, 15)):  # C:N
                mes = meses[i] if meses and i < len(meses) else None
                valor = normalize_value(ws.cell(r, c).value)
                valor_num = pd.to_numeric(pd.Series([valor]), errors="coerce").iloc[0]

                rows.append({
                    "categoria": categoria_atual,
                    "categoria_norm": normalize_text(categoria_atual),
                    "mes": mes,
                    "mes_label": MESES_LABEL.get(mes, mes),
                    "executado": float(valor_num) if pd.notna(valor_num) else 0.0,
                    "meta": None,
                    "executado_total": None,
                    "meta_total": None,
                })
            continue

        # linha META = meta
        if col_b_norm == "META" and categoria_atual and meses:
            for i, c in enumerate(range(3, 15)):  # C:N
                mes = meses[i] if i < len(meses) else None
                valor = normalize_value(ws.cell(r, c).value)
                valor_num = pd.to_numeric(pd.Series([valor]), errors="coerce").iloc[0]

                rows.append({
                    "categoria": categoria_atual,
                    "categoria_norm": normalize_text(categoria_atual),
                    "mes": mes,
                    "mes_label": MESES_LABEL.get(mes, mes),
                    "executado": None,
                    "meta": float(valor_num) if pd.notna(valor_num) else 0.0,
                    "executado_total": None,
                    "meta_total": None,
                })

    df = pd.DataFrame(rows, columns=colunas_padrao)

    if df.empty:
        return pd.DataFrame(columns=colunas_padrao)

    df["executado"] = pd.to_numeric(df["executado"], errors="coerce")
    df["meta"] = pd.to_numeric(df["meta"], errors="coerce")

    # evita bug do groupby com categorical
    df["mes"] = df["mes"].astype(str)
    df.loc[df["mes"].isin(["None", "nan"]), "mes"] = None

    resumo = (
        df.pivot_table(
            index=["categoria", "categoria_norm", "mes", "mes_label"],
            values=["executado", "meta"],
            aggfunc="max",
            dropna=False,
        )
        .reset_index()
    )

    resumo["mes_ord"] = resumo["mes"].apply(lambda x: MESES.index(x) if x in MESES else 999)
    resumo = resumo.sort_values(["categoria_norm", "mes_ord"]).drop(columns=["mes_ord"])

    totais = (
        resumo.groupby(["categoria", "categoria_norm"], dropna=False)[["executado", "meta"]]
        .sum(min_count=1)
        .reset_index()
        .rename(columns={
            "executado": "executado_total",
            "meta": "meta_total",
        })
    )

    resumo = resumo.merge(
        totais,
        on=["categoria", "categoria_norm"],
        how="left"
    )

    return resumo[colunas_padrao].reset_index(drop=True)

@st.cache_data(show_spinner=False)
def load_financeiro_data(file_bytes=None):
    colunas = [
        "grupo",
        "grupo_norm",
        "fornecedor",
        "fornecedor_norm",
        "mes",
        "mes_label",
        "valor",
        "valor_num",
    ]

    if file_bytes is None:
        path = local_excel_path()
        if not path:
            return pd.DataFrame(columns=colunas)
        wb = openpyxl.load_workbook(path, data_only=True)
    else:
        wb = openpyxl.load_workbook(BytesIO(file_bytes), data_only=True)

    nome_aba = "Financeiro"
    if nome_aba not in wb.sheetnames:
        return pd.DataFrame(columns=colunas)

    ws = wb[nome_aba]

    rows = []
    meses = None
    grupo_atual = None

    for r in range(1, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, 16)]  # A:O

        linha_meses = [normalize_text(v) for v in vals[2:14] if v is not None]
        if len(linha_meses) >= 3 and all(m in MESES for m in linha_meses):
            meses = [normalize_text(v) if v is not None else None for v in vals[2:14]]
            continue

        col_a = vals[0]
        col_b = vals[1]

        col_a_norm = normalize_text(col_a)
        col_b_norm = normalize_text(col_b)

        if not any(v not in (None, "") for v in vals[2:14]):
            continue

        # linha de grupo / seção
        if col_a_norm and col_a_norm != "TOTAL" and not col_b_norm:
            grupo_atual = str(col_a).strip()
            continue

        # ignora linha TOTAL geral do bloco
        if col_b_norm == "TOTAL":
            continue

        fornecedor = str(col_b).strip() if col_b else None
        if not fornecedor or not meses:
            continue

        for i, c in enumerate(range(3, 15)):  # C:N
            mes = meses[i] if i < len(meses) else None
            valor = normalize_value(ws.cell(r, c).value)
            valor_num = pd.to_numeric(pd.Series([valor]), errors="coerce").iloc[0]

            rows.append({
                "grupo": grupo_atual,
                "grupo_norm": normalize_text(grupo_atual),
                "fornecedor": fornecedor,
                "fornecedor_norm": normalize_text(fornecedor),
                "mes": mes,
                "mes_label": MESES_LABEL.get(mes, mes),
                "valor": valor,
                "valor_num": float(valor_num) if pd.notna(valor_num) else 0.0,
            })

    df = pd.DataFrame(rows, columns=colunas)

    if df.empty:
        return pd.DataFrame(columns=colunas)

    df["mes"] = pd.Categorical(df["mes"], categories=MESES, ordered=True)
    df = df.sort_values(["grupo_norm", "fornecedor_norm", "mes"]).reset_index(drop=True)
    return df


def format_currency_br(x):
    if x is None or pd.isna(x):
        return "R$ -"
    return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def financeiro_kpis(fin_df):
    work = fin_df.dropna(subset=["valor_num"]).copy()

    if work.empty:
        return {
            "total": 0.0,
            "media_mensal": 0.0,
            "maior_mes": 0.0,
            "fornecedores_ativos": 0,
        }

    total = float(work["valor_num"].sum())

    mensal = (
        work.groupby(["mes", "mes_label"], observed=False)["valor_num"]
        .sum()
        .reset_index()
        .sort_values("mes")
    )

    media_mensal = float(mensal["valor_num"].mean()) if not mensal.empty else 0.0
    maior_mes = float(mensal["valor_num"].max()) if not mensal.empty else 0.0

    fornecedores_ativos = int(
        work.groupby("fornecedor")["valor_num"].sum().gt(0).sum()
    )

    return {
        "total": total,
        "media_mensal": media_mensal,
        "maior_mes": maior_mes,
        "fornecedores_ativos": fornecedores_ativos,
    }


def render_financeiro_page(fin_df):
    st.subheader("Financeiro")

    if fin_df is None or fin_df.empty:
        st.warning("A aba 'Financeiro' não foi encontrada ou está vazia.")
        return

    work = fin_df.copy()

    # respeita o filtro global de período do app
    if "meses_selecionados" in globals() and "mes_label" in work.columns:
        work = work[work["mes_label"].isin(meses_selecionados)].copy()

    work = work.dropna(subset=["valor_num"])
    if work.empty:
        st.info("Sem dados financeiros para o período selecionado.")
        return

    kpis = financeiro_kpis(work)

    section_start(
        "Resumo financeiro",
        "Visão executiva da aba Financeiro com gastos consolidados no período filtrado"
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("Gasto total", format_currency_br(kpis["total"]), icon="💰", subtitle="Total no período")
    with c2:
        card("Média mensal", format_currency_br(kpis["media_mensal"]), icon="📊", subtitle="Média dos meses filtrados")
    with c3:
        card("Maior mês", format_currency_br(kpis["maior_mes"]), icon="📈", subtitle="Pico de gasto mensal")
    with c4:
        card("Fornecedores ativos", format_int(kpis["fornecedores_ativos"]), icon="🏢", subtitle="Com lançamento no período")
    section_end()

    mensal = (
        work.groupby(["mes", "mes_label"], observed=False)["valor_num"]
        .sum()
        .reset_index()
        .sort_values("mes")
    )

    section_start(
        "Evolução mensal dos gastos",
        "Tendência financeira consolidada por mês"
    )
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=mensal["mes_label"],
            y=mensal["valor_num"],
            name="Gasto mensal",
            marker_color=SEMANTIC_COLORS["realizado"],
            hovertemplate="<b>Gasto mensal</b><br>Mês: %{x}<br>Valor: R$ %{y:,.2f}<extra></extra>"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=mensal["mes_label"],
            y=mensal["valor_num"],
            mode="lines+markers",
            name="Tendência",
            line=dict(color=SEMANTIC_COLORS["media"], width=3),
            marker=dict(size=7, color=SEMANTIC_COLORS["media"]),
            hovertemplate="<b>Tendência</b><br>Mês: %{x}<br>Valor: R$ %{y:,.2f}<extra></extra>"
        )
    )
    fig = apply_plotly_theme(
        fig,
        title="Gasto total por mês",
        subtitle="Leitura mensal consolidada da aba Financeiro",
        yaxis_title="Valor (R$)",
        height=390,
        legend=True,
        legend_orientation="h"
    )
    fig = apply_month_axis_order(fig, mensal)
    plot(fig, "financeiro_mensal")
    section_end()

    fornecedores = (
        work.groupby("fornecedor", as_index=False)["valor_num"]
        .sum()
        .sort_values("valor_num", ascending=False)
    )

    top_fornecedores = fornecedores.head(10).copy()

    section_start(
        "Ranking de fornecedores",
        "Maiores gastos acumulados no período filtrado"
    )
    fig_top = go.Figure()
    fig_top.add_trace(
        go.Bar(
            x=top_fornecedores["valor_num"],
            y=top_fornecedores["fornecedor"],
            orientation="h",
            name="Total",
            marker_color=SEMANTIC_COLORS["primary_soft"],
            hovertemplate="<b>%{y}</b><br>Total: R$ %{x:,.2f}<extra></extra>"
        )
    )
    fig_top = apply_plotly_theme(
        fig_top,
        title="Top 10 fornecedores por gasto",
        subtitle="Ranking consolidado do período selecionado",
        yaxis_title="",
        height=430,
        legend=False
    )
    fig_top.update_layout(yaxis=dict(autorange="reversed"))
    plot(fig_top, "financeiro_top_fornecedores")
    section_end()

    composicao = top_fornecedores.copy()
    total_comp = composicao["valor_num"].sum()
    composicao["participacao_pct"] = (
        (composicao["valor_num"] / total_comp) * 100 if total_comp else 0
    )

    section_start(
        "Detalhamento analítico",
        "Tabela executiva com consolidação por fornecedor"
    )
    tabela = fornecedores.copy()
    tabela["Média mensal"] = tabela["valor_num"] / max(len(mensal), 1)
    tabela["Participação %"] = (
        (tabela["valor_num"] / tabela["valor_num"].sum()) * 100
        if tabela["valor_num"].sum() > 0 else 0
    )

    tabela_view = tabela.rename(columns={
        "fornecedor": "Fornecedor",
        "valor_num": "Total no período",
    }).copy()

    tabela_view["Total no período"] = tabela_view["Total no período"].apply(format_currency_br)
    tabela_view["Média mensal"] = tabela_view["Média mensal"].apply(format_currency_br)
    tabela_view["Participação %"] = tabela_view["Participação %"].apply(format_pct_br)

    st.dataframe(
        tabela_view[["Fornecedor", "Total no período", "Média mensal", "Participação %"]],
        use_container_width=True,
        hide_index=True
    )
    section_end()

def filter_panel(df, unidade, painel):
    unidade_norm = normalize_text(unidade)
    painel_norm = normalize_text(painel)

    # DEBUG TEMPORÁRIO (pode remover depois)
    df_test = df[df["unidade_norm"] == unidade_norm]

    # tenta match exato
    result = df_test[df_test["painel_norm"] == painel_norm]

    # 🔥 FALLBACK INTELIGENTE
    if result.empty:
        result = df_test[
            df_test["painel_norm"].str.contains(painel_norm, na=False)
        ]

    return result.copy()

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



def format_pct_br(x):
    if x is None or pd.isna(x):
        return "-"
    return f"{x:,.1f}%".replace(",", "X").replace(".", ",").replace("X", ".")


def format_compact_number(x):
    if x is None or pd.isna(x):
        return "-"
    x = float(x)
    if abs(x) >= 1000000:
        return f"{x / 1000000:,.1f} mi".replace(",", "X").replace(".", ",").replace("X", ".")
    if abs(x) >= 1000:
        return f"{x:,.0f}".replace(",", ".")
    if x.is_integer():
        return str(int(x))
    return f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_hours_hms(value):
    if value is None or pd.isna(value):
        return "-"

    total_seconds = int(round(float(value) * 3600))

    sign = "-" if total_seconds < 0 else ""
    total_seconds = abs(total_seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d}"


def time_tick_values(max_value):
    if max_value is None or pd.isna(max_value) or max_value <= 0:
        return [0, 0.25, 0.5, 0.75, 1.0]

    if max_value <= 1:
        step = 10 / 60  # 10 min
    elif max_value <= 3:
        step = 20 / 60  # 20 min
    elif max_value <= 6:
        step = 30 / 60  # 30 min
    elif max_value <= 12:
        step = 1.0      # 1h
    elif max_value <= 24:
        step = 2.0      # 2h
    else:
        step = 6.0      # 6h

    ticks = []
    current = 0.0
    limit = float(max_value) * 1.08

    while current <= limit + 1e-9:
        ticks.append(round(current, 6))
        current += step

    if not ticks:
        ticks = [0.0, round(float(max_value), 6)]

    return ticks


def line_time_chart(
    df,
    title,
    main_series=None,
    prefix="time_line",
    unidade=None
):
    work = df.dropna(subset=["valor_num"]).copy()
    if work.empty:
        st.info("Sem dados para este gráfico.")
        return

    fig = go.Figure()

    if main_series:
        main_norm = normalize_text(main_series)
        main = work[work["serie_norm"] == main_norm]

        if not main.empty:
            fig.add_trace(
                go.Scatter(
                    x=main["mes_label"],
                    y=main["valor_num"],
                    mode="lines+markers",
                    name=str(main_series),
                    line=dict(color=SEMANTIC_COLORS["realizado"], width=3.5),
                    marker=dict(size=7, color=SEMANTIC_COLORS["realizado"]),
                    customdata=main["valor_num"].apply(format_hours_hms),
                    hovertemplate="<b>%{fullData.name}</b><br>Mês: %{x}<br>Tempo: %{customdata}<extra></extra>"
                )
            )

        others = work[
            (~work["serie_norm"].eq(main_norm)) &
            (~work["serie_norm"].eq("META"))
        ].copy()

        for serie in others["serie"].dropna().unique().tolist():
            temp = others[others["serie"] == serie].copy()
            serie_color = semantic_color(serie, default=SEMANTIC_COLORS["neutral"])

            fig.add_trace(
                go.Scatter(
                    x=temp["mes_label"],
                    y=temp["valor_num"],
                    mode="lines+markers",
                    name=str(serie),
                    line=dict(color=serie_color, width=2.4),
                    marker=dict(size=6, color=serie_color),
                    customdata=temp["valor_num"].apply(format_hours_hms),
                    hovertemplate="<b>%{fullData.name}</b><br>Mês: %{x}<br>Tempo: %{customdata}<extra></extra>"
                )
            )
    else:
        series = work["serie"].dropna().unique().tolist()
        color_map = build_semantic_color_map(series)

        for serie in series:
            temp = work[work["serie"] == serie].copy()
            serie_color = semantic_color(serie, default=color_map.get(serie, SEMANTIC_COLORS["neutral"]))

            fig.add_trace(
                go.Scatter(
                    x=temp["mes_label"],
                    y=temp["valor_num"],
                    mode="lines+markers",
                    name=str(serie),
                    line=dict(color=serie_color, width=3 if "MÉDIA GERAL" in str(serie).upper() or "MEDIA GERAL" in str(serie).upper() else 2.4),
                    marker=dict(size=6, color=serie_color),
                    customdata=temp["valor_num"].apply(format_hours_hms),
                    hovertemplate="<b>%{fullData.name}</b><br>Mês: %{x}<br>Tempo: %{customdata}<extra></extra>"
                )
            )

    meta = work[work["serie_norm"] == "META"].copy()
    if not meta.empty:
        fig.add_trace(
            go.Scatter(
                x=meta["mes_label"],
                y=meta["valor_num"],
                mode="lines+markers",
                name="Meta",
                line=dict(color=SEMANTIC_COLORS["meta"], width=2, dash="dash"),
                marker=dict(size=5, color=SEMANTIC_COLORS["meta"]),
                customdata=meta["valor_num"].apply(format_hours_hms),
                hovertemplate="<b>Meta</b><br>Mês: %{x}<br>Tempo: %{customdata}<extra></extra>"
            )
        )

    fig = apply_plotly_theme(
        fig,
        title=title,
        subtitle=chart_subtitle(work, unidade),
        yaxis_title="Tempo (HH:MM:SS)",
        height=360,
        legend=True,
        legend_orientation="h"
    )

    max_y = work["valor_num"].max()
    ticks = time_tick_values(max_y)

    fig.update_yaxes(
        tickmode="array",
        tickvals=ticks,
        ticktext=[format_hours_hms(v) for v in ticks]
    )

    fig = apply_month_axis_order(fig, work)
    plot(fig, prefix)

def percent_atingido(executado, meta):
    if executado is None or meta is None or pd.isna(executado) or pd.isna(meta) or meta == 0:
        return None
    return (executado / meta) * 100


def status_meta(executado, meta):
    pct = percent_atingido(executado, meta)
    if pct is None:
        return "Sem base", SEMANTIC_COLORS["neutral"], None
    if executado > meta:
        return "Acima da meta", SEMANTIC_COLORS["success"], ((executado - meta) / meta) * 100
    if executado < meta:
        return "Abaixo da meta", SEMANTIC_COLORS["warning"], ((meta - executado) / meta) * 100
    return "Meta atingida", SEMANTIC_COLORS["info"], 0.0


def compute_executado_for_categoria(data, categoria, mes=None):
    work = data.copy()

    if mes is not None:
        work = work[work["mes"] == mes]

    work = work.dropna(subset=["valor_num"])
    if work.empty:
        return 0.0

    categoria_norm = str(categoria).strip().upper()

    def sum_mask(mask):
        subset = work[mask & work["valor_num"].notna()].copy()
        if subset.empty:
            return 0.0

        subset = subset[
            ~subset["serie_norm"].isin(
                ["META", "MÉDIA DIÁRIA", "MEDIA DIÁRIA", "MEDIA DIARIA", "TOTAL"]
            )
        ]
        return float(subset["valor_num"].sum()) if not subset.empty else 0.0

    painel_upper = work["painel"].astype(str).str.upper()
    painel_norm_upper = work["painel_norm"].astype(str).str.upper() if "painel_norm" in work.columns else painel_upper
    serie_upper = work["serie"].astype(str).str.upper() if "serie" in work.columns else work["serie_norm"].astype(str).str.upper()
    serie_norm_upper = work["serie_norm"].astype(str).str.upper()
    unidade_upper = work["unidade"].astype(str).str.upper()
    unidade_norm_upper = work["unidade_norm"].astype(str).str.upper() if "unidade_norm" in work.columns else unidade_upper

    # ATENÇÃO PRIMÁRIA
    if categoria_norm in ["ATENÇÃO PRIMÁRIA", "ATENCAO PRIMARIA"]:
        return sum_mask(
            unidade_upper.eq("ATENÇÃO PRIMÁRIA") |
            unidade_upper.eq("ATENCAO PRIMARIA") |
            unidade_norm_upper.eq("ATENÇÃO PRIMÁRIA") |
            unidade_norm_upper.eq("ATENCAO PRIMARIA")
        )

    # ATENÇÃO ESPECIALIZADA
    if categoria_norm in ["ATENÇÃO ESPECIALIZADA", "ATENCAO ESPECIALIZADA"]:
        return sum_mask(
            unidade_upper.eq("ATENÇÃO ESPECIALIZADA") |
            unidade_upper.eq("ATENCAO ESPECIALIZADA") |
            unidade_norm_upper.eq("ATENÇÃO ESPECIALIZADA") |
            unidade_norm_upper.eq("ATENCAO ESPECIALIZADA") |
            painel_upper.str.contains("ESPECIALIZ", na=False) |
            painel_norm_upper.str.contains("ESPECIALIZ", na=False)
        )

    # AÇÕES COLETIVA
    if categoria_norm == "AÇÕES COLETIVA":
        return sum_mask(
            painel_upper.str.contains("AÇÃO COLET", na=False) |
            painel_upper.str.contains("ACAO COLET", na=False) |
            painel_norm_upper.str.contains("AÇÃO COLET", na=False) |
            painel_norm_upper.str.contains("ACAO COLET", na=False) |
            serie_upper.str.contains("AÇÃO COLET", na=False) |
            serie_upper.str.contains("ACAO COLET", na=False) |
            serie_norm_upper.str.contains("AÇÃO COLET", na=False) |
            serie_norm_upper.str.contains("ACAO COLET", na=False)
        )

    # ODONTOLOGIA
    if categoria_norm == "ODONTOLOGIA":
        return sum_mask(
            painel_upper.str.contains("ODONTO", na=False) |
            painel_norm_upper.str.contains("ODONTO", na=False) |
            serie_upper.str.contains("ODONTO", na=False) |
            serie_norm_upper.str.contains("ODONTO", na=False)
        )

    # ENFERMAGEM
    if categoria_norm == "ENFERMAGEM":
        return sum_mask(
            painel_upper.str.contains("ENFERM", na=False) |
            painel_norm_upper.str.contains("ENFERM", na=False) |
            serie_upper.str.contains("ENFERM", na=False) |
            serie_norm_upper.str.contains("ENFERM", na=False)
        )

    # MÉDICOS
    if categoria_norm == "MÉDICOS":
        return sum_mask(
            painel_upper.str.contains("MÉDIC", na=False) |
            painel_upper.str.contains("MEDIC", na=False) |
            painel_norm_upper.str.contains("MÉDIC", na=False) |
            painel_norm_upper.str.contains("MEDIC", na=False) |
            serie_upper.str.contains("MÉDIC", na=False) |
            serie_upper.str.contains("MEDIC", na=False) |
            serie_norm_upper.str.contains("MÉDIC", na=False) |
            serie_norm_upper.str.contains("MEDIC", na=False) |
            serie_upper.str.contains("CONSULTAS MÉDICAS", na=False) |
            serie_upper.str.contains("CONSULTAS MEDICAS", na=False) |
            serie_norm_upper.str.contains("CONSULTAS MÉDICAS", na=False) |
            serie_norm_upper.str.contains("CONSULTAS MEDICAS", na=False)
        )

    # EQUIPE MULTIDISCIPLINAR (EXCETO MÉDICOS)
    if categoria_norm == "EQUIPE MULTIDISCIPLINAR (EXCETO MÉDICOS)":
        return sum_mask(
            painel_upper.eq("NÍVEL SUPERIOR (EXCETO MÉDICO)") |
            painel_upper.eq("NIVEL SUPERIOR (EXCETO MEDICO)") |
            painel_norm_upper.eq("NÍVEL SUPERIOR (EXCETO MÉDICO)") |
            painel_norm_upper.eq("NIVEL SUPERIOR (EXCETO MEDICO)") |
            serie_upper.str.contains("NUTRI", na=False) |
            serie_upper.str.contains("PSICOLOG", na=False) |
            serie_upper.str.contains("ASSISTENTE SOCIAL", na=False) |
            serie_upper.str.contains("FISIOTERAP", na=False) |
            serie_norm_upper.str.contains("NUTRI", na=False) |
            serie_norm_upper.str.contains("PSICOLOG", na=False) |
            serie_norm_upper.str.contains("ASSISTENTE SOCIAL", na=False) |
            serie_norm_upper.str.contains("FISIOTERAP", na=False)
        )

    return 0.0


def build_metas_panel(data, metas_df):
    if metas_df is None or metas_df.empty:
        return pd.DataFrame()

    painel = metas_df.copy()
    painel["executado"] = pd.to_numeric(painel["executado"], errors="coerce").fillna(0.0)
    painel["meta"] = pd.to_numeric(painel["meta"], errors="coerce").fillna(0.0)

    painel["atingido_pct"] = painel.apply(
        lambda x: percent_atingido(x["executado"], x["meta"]),
        axis=1
    )
    painel["saldo"] = painel["executado"] - painel["meta"]
    painel["saldo_pct"] = painel.apply(
        lambda x: ((x["saldo"] / x["meta"]) * 100)
        if pd.notna(x["meta"]) and x["meta"] not in [0, None]
        else None,
        axis=1
    )

    return painel


def meta_status_badge(executado, meta):
    label, color, variacao_pct = status_meta(executado, meta)
    if variacao_pct is None:
        detalhe = "Sem comparativo"
    elif executado > meta:
        detalhe = f"+{format_pct_br(abs(variacao_pct))}"
    elif executado < meta:
        detalhe = f"Falta {format_pct_br(abs(variacao_pct))}"
    else:
        detalhe = "100,0%"

    return label, color, detalhe


def render_meta_card(categoria, executado, meta, atingido_pct, saldo_pct):
    status_label, status_color, detalhe = meta_status_badge(executado, meta)

    if saldo_pct is None:
        saldo_texto = "Sem cálculo"
    elif saldo_pct > 0:
        saldo_texto = f"Excedeu {format_pct_br(abs(saldo_pct))}"
    elif saldo_pct < 0:
        saldo_texto = f"Falta {format_pct_br(abs(saldo_pct))}"
    else:
        saldo_texto = "Meta exata"

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
            border: 1px solid #E2E8F0;
            border-radius: 22px;
            padding: 18px 18px 16px 18px;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
            min-height: 210px;
            margin-bottom: 14px;
        ">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; margin-bottom:12px;">
                <div style="font-size:14px; font-weight:800; color:#0F172A; line-height:1.3;">{categoria}</div>
                <div style="background:{status_color}; color:#FFFFFF; font-size:11px; font-weight:700; padding:6px 10px; border-radius:999px; white-space:nowrap;">{status_label}</div>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px;">
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:16px; padding:10px;">
                    <div style="font-size:11px; color:#64748B; text-transform:uppercase; font-weight:700;">Executado</div>
                    <div style="font-size:26px; font-weight:800; color:#0F172A; margin-top:4px;">{format_compact_number(executado)}</div>
                </div>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:16px; padding:10px;">
                    <div style="font-size:11px; color:#64748B; text-transform:uppercase; font-weight:700;">Meta</div>
                    <div style="font-size:26px; font-weight:800; color:#0F172A; margin-top:4px;">{format_compact_number(meta)}</div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div style="font-size:13px; color:#64748B; font-weight:700;">% atingido</div>
                <div style="font-size:20px; font-weight:800; color:#0F6CBD;">{format_pct_br(atingido_pct)}</div>
            </div>
            <div style="height:8px; background:#E2E8F0; border-radius:999px; overflow:hidden; margin-bottom:10px;">
                <div style="width:{0 if atingido_pct is None else min(max(atingido_pct,0),100)}%; height:100%; background:{status_color};"></div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
                <div style="font-size:12px; color:#64748B;">{saldo_texto}</div>
                <div style="font-size:12px; color:{status_color}; font-weight:700;">{detalhe}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_metas_page(data, metas_df):
    st.subheader("Metas do Plano")

    if metas_df is None or metas_df.empty:
        st.warning("A aba 'METAS DO PLANO DE TRABALHO' não foi encontrada ou está vazia.")
        return

    painel_metas = build_metas_panel(data, metas_df)
    if painel_metas.empty:
        st.warning("Não foi possível montar o painel de metas com a base atual.")
        return

    resumo = (
        painel_metas.groupby("categoria", as_index=False)
        .agg({
            "executado": "sum",
            "meta": "sum",
        })
    )
    resumo["atingido_pct"] = resumo.apply(lambda x: percent_atingido(x["executado"], x["meta"]), axis=1)
    resumo["saldo"] = resumo["executado"] - resumo["meta"]
    resumo["saldo_pct"] = resumo.apply(
        lambda x: ((x["saldo"] / x["meta"]) * 100) if pd.notna(x["meta"]) and x["meta"] not in [0, None] else None,
        axis=1
    )

    total_meta = resumo["meta"].sum()
    total_executado = resumo["executado"].sum()
    total_pct = percent_atingido(total_executado, total_meta)
    total_saldo_pct = ((total_executado - total_meta) / total_meta) * 100 if total_meta else None

    section_start("Resumo geral das metas", "Comparativo consolidado entre executado e meta da aba Metas do Plano")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("Executado total", format_compact_number(total_executado), icon="📌", subtitle="Base disponível no período filtrado")
    with c2:
        card("Meta total", format_compact_number(total_meta), icon="🎯", subtitle="Somatório das metas filtradas")
    with c3:
        card("% atingido", format_pct_br(total_pct), icon="📈", subtitle="Executado em relação à meta")
    with c4:
        card("Saldo percentual", format_pct_br(total_saldo_pct), icon="⚖️", subtitle="Acima ou abaixo da meta")
    section_end()

    section_start("Painel por meta", "Cards executivos com executado, meta, percentual atingido e saldo")
    cols = st.columns(2)
    for idx, row in enumerate(resumo.itertuples(index=False)):
        with cols[idx % 2]:
            render_meta_card(row.categoria, row.executado, row.meta, row.atingido_pct, row.saldo_pct)
    section_end()

    serie_grafico = resumo.sort_values("atingido_pct", ascending=False).copy()
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=serie_grafico["categoria"],
            y=serie_grafico["executado"],
            name="Executado",
            marker_color=SEMANTIC_COLORS["realizado"],
            hovertemplate="<b>Executado</b><br>%{x}<br>%{y:,.0f}<extra></extra>"
        )
    )
    fig.add_trace(
        go.Bar(
            x=serie_grafico["categoria"],
            y=serie_grafico["meta"],
            name="Meta",
            marker_color=SEMANTIC_COLORS["meta"],
            hovertemplate="<b>Meta</b><br>%{x}<br>%{y:,.0f}<extra></extra>"
        )
    )
    fig = apply_plotly_theme(
        fig,
        title="Executado x Meta por categoria",
        subtitle="Comparativo consolidado conforme a base carregada",
        yaxis_title="Quantidade",
        height=430,
        legend=True,
        legend_orientation="h",
        tick_angle=-25
    )
    fig.update_layout(barmode="group")
    plot(fig, "metas_comparativo")

    tabela = resumo.copy()
    tabela["Executado"] = tabela["executado"].apply(format_compact_number)
    tabela["Meta"] = tabela["meta"].apply(format_compact_number)
    tabela["% Atingido"] = tabela["atingido_pct"].apply(format_pct_br)
    tabela["Saldo %"] = tabela["saldo_pct"].apply(format_pct_br)
    tabela = tabela[["categoria", "Executado", "Meta", "% Atingido", "Saldo %"]]
    tabela.columns = ["Meta do plano", "Executado", "Meta", "% atingido", "Saldo %"]

    with st.expander("Detalhamento das metas"):
        st.dataframe(tabela, use_container_width=True, hide_index=True)
        st.caption("Observação: o executado é calculado com base nos dados disponíveis na planilha carregada. Categorias sem produção correspondente na base atual permanecem zeradas.")
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
            st.image(str(LOGO_PATRIS), width=315)
        except Exception:
            st.empty()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            f"""
            <div class="hero-wrap">
                <div class="hero-title" style="width: 100%; text-align: center;">Painel de Gestão Patris</div>
                <div class="hero-subtitle" style="width: 100%; text-align: center;">
                   Gestão estratégica da produção assistencial e desempenho operacional
                </div>
                <div class="hero-chip-row" style="justify-content: center; display: flex;">
                    <div class="hero-chip">Página: {page_title}</div>
                    <div class="hero-chip">Período: {periodo}</div>
                    <div class="hero-chip">Atualizado em: {data_ref}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown('<div class="logo-slot">', unsafe_allow_html=True)
        try:
            st.image(str(LOGO_PREFEITURA), width=315)
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
    "axis": "#076BF7",
    "text": "#CFD7E2",
    "title": "#F6F7FB",
    "plot_bg": "#071224",

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
                    customdata=main["valor_num"].apply(format_hours_hms),
                    hovertemplate="<b>%{fullData.name}</b><br>Mês: %{x}<br>Tempo: %{customdata}<extra></extra>"
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
                    marker=dict(size=6, color=serie_color),
                    customdata=temp["valor_num"].apply(format_hours_hms),
                    hovertemplate="<b>%{fullData.name}</b><br>Mês: %{x}<br>Tempo: %{customdata}<extra></extra>"
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
                customdata=meta["valor_num"].apply(format_hours_hms),
                hovertemplate="<b>Meta</b><br>Mês: %{x}<br>Tempo: %{customdata}<extra></extra>"
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
        total_recep = recep[
           recep["serie_norm"].isin([
               "PACIENTES RECEPCIONADOS"
            ])
        ]["valor_num"].sum()

        card(
            "Pacientes recepcionados",
            format_int(total_recep),
            icon="👥",
            subtitle="Volume total no período"
        )

    with c2:
        total_atend_med = metric_sum(
            atend_med,
            exclude_series_norm=["META", "MÉDIA DIÁRIA", "MEDIA DIÁRIA", "MEDIA DIARIA", "TOTAL"]
        )

        card(
            "Atendimentos médicos",
            format_int(total_atend_med or 0),
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
    risco_plot = risco[
        ~risco["serie_norm"].str.contains("TOTAL", na=False)
    ].copy()

    # remove meses totalmente zerados
    if not risco_plot.empty:
        soma_mes_risco = risco_plot.groupby("mes_label")["valor_num"].sum(min_count=1)
        meses_validos_risco = soma_mes_risco[soma_mes_risco.fillna(0) > 0].index.tolist()
        risco_plot = risco_plot[risco_plot["mes_label"].isin(meses_validos_risco)].copy()

    grouped_bar(
        risco_plot,
        "Atendimentos por classificação de risco",
        color_map=RISK_COLORS,
        unit_suffix="Quantidade",
        prefix=f"{unidade}_risco_qtd",
        unidade=unidade
    )

    perc_plot = perc_risco[
        perc_risco["serie_norm"].str.contains("TOTAL", na=False)
    ].copy()

    # remove erros e meses vazios
    perc_plot = perc_plot[perc_plot["valor_num"].notna()].copy()

    if not perc_plot.empty:
        soma_mes_perc = perc_plot.groupby("mes_label")["valor_num"].sum(min_count=1)
        meses_validos_perc = soma_mes_perc[soma_mes_perc.fillna(0) > 0].index.tolist()
        perc_plot = perc_plot[perc_plot["mes_label"].isin(meses_validos_perc)].copy()

        # Excel percentual vem como fração (ex.: 0.65) -> converter para 65
        perc_plot["valor_num"] = perc_plot["valor_num"] * 100

    grouped_bar(
        perc_plot,
        "Percentual de atendimentos por classificação de risco",
        color_map=RISK_COLORS,
        unit_suffix="Percentual (%)",
        prefix=f"{unidade}_risco_perc",
        unidade=unidade
    )

    line_time_chart(
        espera,
        "Tempo de espera para classificação de risco vs meta",
        main_series="MÉDIA GERAL",
        prefix=f"{unidade}_espera_class",
        unidade=unidade
    )

    line_time_chart(
        tempo_med,
        "Tempo médio de espera de atendimento médico por classificação de risco",
        prefix=f"{unidade}_tempo_med_risco",
        unidade=unidade
    )
    section_end()

    section_start("Permanência, apoio e desfechos", "Indicadores operacionais complementares e perfil da demanda")
    col1, col2 = st.columns(2)
    with col1:
        line_time_chart(
            intern,
            "Tempo de permanência de pacientes internados",
            prefix=f"{unidade}_intern",
            unidade=unidade
        )
    with col2:
        line_time_chart(
            semint,
            "Tempo de permanência de pacientes sem internação",
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

    unit_df = df[df["unidade"] == unidade].copy()
    clin = df[
        (df["unidade"] == unidade) &
        (
            df["painel_norm"].str.contains("PACIENTES CLINICOS", na=False) |
            df["serie_norm"].str.contains("PACIENTES CLINICOS", na=False)
        )
    ].copy()

    meses_base = [m for m in unit_df["mes"].dropna().tolist() if pd.notna(m)]
    meses_base = list(dict.fromkeys(meses_base))

    if not meses_base:
        meses_base = [m for m in df["mes"].dropna().tolist() if pd.notna(m)]
        meses_base = list(dict.fromkeys(meses_base))

    def hmji_block(series_map, include_total=True):
        work = unit_df.copy()
        if work.empty:
            return pd.DataFrame()

        serie_upper = work["serie"].astype(str).str.strip().str.upper()

        aliases = {}
        for label, alias_list in series_map.items():
            aliases[label] = [str(x).strip().upper() for x in alias_list]

        selected_aliases = [item for values in aliases.values() for item in values]
        matched = work[serie_upper.isin(selected_aliases)].copy()

        if not matched.empty:
            matched["serie_canonica"] = matched["serie"].astype(str).str.strip().str.upper()
            for canonical, alias_list in aliases.items():
                matched.loc[
                    matched["serie_canonica"].isin(alias_list),
                    "serie_canonica"
                ] = canonical
        else:
            matched["serie_canonica"] = pd.Series(dtype=str)

        if "TOTAL" in aliases:
            if include_total:
                matched_total = matched[matched["serie_canonica"] == "TOTAL"].copy()
            else:
                matched_total = pd.DataFrame(columns=matched.columns)
            matched = matched[matched["serie_canonica"] != "TOTAL"].copy()
            if include_total and not matched_total.empty:
                matched = pd.concat([matched, matched_total], ignore_index=True)

        if meses_base:
            grid = pd.MultiIndex.from_product(
                [meses_base, list(series_map.keys())],
                names=["mes", "serie_canonica"]
            ).to_frame(index=False)
            grid["mes_label"] = grid["mes"].map(MESES_LABEL)
            base = matched.groupby(["mes", "mes_label", "serie_canonica"], as_index=False)["valor_num"].sum()
            merged = grid.merge(base, on=["mes", "mes_label", "serie_canonica"], how="left")
        else:
            merged = matched.groupby(["mes", "mes_label", "serie_canonica"], as_index=False)["valor_num"].sum()

        merged["valor_num"] = merged["valor_num"].fillna(0.0)
        merged["unidade"] = unidade
        merged["serie"] = merged["serie_canonica"]
        merged["serie_norm"] = merged["serie_canonica"]
        return merged.sort_values(["mes", "serie"])

    obitos = filter_panel(df, unidade, "ÓBITOS")
    obitos = obitos[obitos["serie_norm"].isin(["TOTAL", "ÓBITOS", "OBITOS"])].copy()
    esp = hmji_block({
        "CIRURGIA GERAL": ["CIRURGIA GERAL"],
        "UROLOGIA": ["UROLOGIA"],
        "GINECOLOGIA": ["GINECOLOGIA"],
    }, include_total=False)
    exames = hmji_block({
        "RAIO-X": ["RAIO-X"],
        "MAMOGRAFIAS": ["MAMOGRAFIAS"],
        "ULTRASOM": ["ULTRASOM"],
        "ELETROCARDIOGRAMA": ["ELETROCARDIOGRAMA"],
        "TOTAL": ["TOTAL"],
    }, include_total=True)
    cir = hmji_block({
        "CIRURGIAS GRANDES": ["CIRURGIAS GRANDES"],
        "BIÓPSIAS": ["BIÓPSIAS"],
        "VASECTOMIAS": ["VASECTOMIAS"],
        "PEQUENAS CIRURGIAS": ["PEQUENAS CIRURGIAS"],
    }, include_total=False)
    anes = hmji_block({
        "RAQUIANESTESIA": ["RAQUIANESTESIA"],
        "ANESTESIA GERAL": ["ANESTESIA GERAL"],
        "BLOQUEIO": ["BLOQUEIO", "BLOQUEIO "],
        "ANESTESIA LOCAL": ["ANESTESIA LOCAL"],
    }, include_total=False)

    c1, c2, c3 = st.columns(3)

    with c1:
        total_clin = clin[
            ~clin["serie_norm"].isin([
                "MÉDIA DIÁRIA",
                "MEDIA DIÁRIA",
                "MEDIA DIARIA",
                "TOTAL"
            ])
        ]["valor_num"].sum()

        card(
            "Pacientes clínicos",
            format_int(total_clin),
            icon="🏥",
            subtitle="Atendimentos no período"
        )

    with c2:
        total_obitos = obitos["valor_num"].sum()

        card(
            "Óbitos",
            format_int(total_obitos),
            icon="⚠️",
            subtitle="Apenas o total de óbitos"
        )

    with c3:
        card(
            "Procedimentos cirúrgicos",
            format_int(cir["valor_num"].sum()),
            icon="🩹",
            subtitle="CIRURGIAS GRANDES, BIÓPSIAS, VASECTOMIAS e PEQUENAS CIRURGIAS"
        )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Pacientes clínicos atendidos / média diária**")
        fig = go.Figure()

        main = clin[clin["serie_norm"].isin([
            "PACIENTES CLINICOS ATENDIDOS"
        ])]

        avg = clin[clin["serie_norm"].isin([
            "MÉDIA DIÁRIA",
            "MEDIA DIÁRIA",
            "MEDIA DIARIA"
        ])]

        if not main.empty:
            fig.add_trace(
                go.Bar(
                    x=main["mes_label"],
                    y=main["valor_num"],
                    name="Pacientes clínicos",
                    marker_color=SEMANTIC_COLORS["realizado_soft"],
                    hovertemplate="<b>Pacientes clínicos</b><br>Mês: %{x}<br>Total: %{y:,.0f}<extra></extra>"
                )
            )

        if not avg.empty:
            fig.add_trace(
                go.Scatter(
                    x=avg["mes_label"],
                    y=avg["valor_num"],
                    mode="lines+markers",
                    name="Média diária",
                    line=dict(color=SEMANTIC_COLORS["realizado"], width=3),
                    marker=dict(color=SEMANTIC_COLORS["realizado"], size=7),
                    hovertemplate="<b>Média diária</b><br>Mês: %{x}<br>Valor: %{y:,.1f}<extra></extra>"
                )
            )

        fig = apply_plotly_theme(
            fig,
            title="Pacientes clínicos atendidos / média diária",
            subtitle=chart_subtitle(clin, unidade),
            yaxis_title="Quantidade",
            height=360,
            legend=True,
            legend_orientation="h"
        )
        fig = apply_month_axis_order(fig, clin)
        plot(fig, f"{unidade}_pacientes")

    with col2:
       grouped_bar(
            obitos,
            "Óbitos",
            prefix=f"{unidade}_obitos",
            unidade=unidade
        )

    grouped_bar(esp, "Consultas especializadas", prefix=f"{unidade}_esp", unidade=unidade)
    grouped_bar(exames, "Exames internos", prefix=f"{unidade}_exames", unidade=unidade)
    grouped_bar(cir, "Procedimentos cirúrgicos", prefix=f"{unidade}_cir", unidade=unidade)
    grouped_bar(anes, "Anestesias", prefix=f"{unidade}_anes", unidade=unidade)

def render_generic(df, unidade, paineis):
    st.subheader(unidade)
    for i,painel in enumerate(paineis, start=1):
        grouped_bar(filter_panel(df, unidade, painel), painel.title(), prefix=f"{unidade}_{i}")

def rh_get_latest_month(panel_df):
    if panel_df is None or panel_df.empty:
        return None

    work = panel_df.copy()

    # considera apenas linhas com mês e valor numérico preenchido
    work = work.dropna(subset=["mes"]).copy()
    work = work[work["valor_num"].notna()].copy()

    if work.empty:
        return None

    return work["mes"].max()


def rh_get_value_and_meta(panel_df):
    if panel_df is None or panel_df.empty:
        return {
            "mes": None,
            "valor": None
        }

    latest_mes = rh_get_latest_month(panel_df)
    if latest_mes is None:
        return {
            "mes": None,
            "valor": None
        }

    recorte = panel_df[panel_df["mes"] == latest_mes].copy()
    if recorte.empty:
        return {
            "mes": latest_mes,
            "valor": None
        }

    valor_df = recorte[
        ~recorte["serie_norm"].isin(["META", "MÉDIA DIÁRIA", "MEDIA DIÁRIA", "MEDIA DIARIA", "TOTAL"])
    ].copy()

    # fallback: se o indicador vier com a própria série igual ao painel
    if valor_df.empty:
        valor_df = recorte.copy()

    valor_df = valor_df[valor_df["valor_num"].notna()].copy()

    valor = valor_df["valor_num"].sum() if not valor_df.empty else None

    if valor is not None and pd.isna(valor):
        valor = None

    return {
        "mes": latest_mes,
        "valor": float(valor) if valor is not None else None
    }


def rh_is_lower_better(nome_indicador):
    nome_norm = normalize_text(nome_indicador) or ""
    indicadores_menor_melhor = {
        "TAXA DE TURNOVER",
        "ABSENTEISMO",
        "ACIDENTES DE TRABALHO",
    }
    return nome_norm in indicadores_menor_melhor


def rh_compute_status(nome_indicador, valor, meta):
    """
    Regras:
    - sem meta -> neutro
    - maior é melhor:
        >=100% da meta = verde
        entre 85% e 99,9% = amarelo
        abaixo de 85% = vermelho
    - menor é melhor:
        <=100% da meta = verde
        até 115% da meta = amarelo
        acima de 115% = vermelho
    """
    if valor is None or meta is None or pd.isna(valor) or pd.isna(meta) or meta == 0:
        return {
            "status": "Sem meta",
            "cor": "#64748B",
            "pct": None,
            "comparacao": "Sem comparativo"
        }

    menor_melhor = rh_is_lower_better(nome_indicador)
    pct = (valor / meta) * 100

    if menor_melhor:
        if valor <= meta:
            status = "Meta atingida"
            cor = "#16A34A"
        elif valor <= meta * 1.15:
            status = "Atenção"
            cor = "#F59E0B"
        else:
            status = "Abaixo da meta"
            cor = "#DC2626"
    else:
        if valor >= meta:
            status = "Meta atingida"
            cor = "#16A34A"
        elif valor >= meta * 0.85:
            status = "Atenção"
            cor = "#F59E0B"
        else:
            status = "Abaixo da meta"
            cor = "#DC2626"

    diferenca = valor - meta
    if diferenca > 0:
        comparacao = f"+{rh_format_value(nome_indicador, abs(diferenca))} vs meta"
    elif diferenca < 0:
        comparacao = f"-{rh_format_value(nome_indicador, abs(diferenca))} vs meta"
    else:
        comparacao = "Em linha com a meta"

    return {
        "status": status,
        "cor": cor,
        "pct": pct,
        "comparacao": comparacao
    }

def rh_format_value(nome_indicador, valor):
    if valor is None or pd.isna(valor):
        return "-"

    nome_norm = normalize_text(nome_indicador) or ""

    # indicadores percentuais
    if (
        "%" in str(nome_indicador)
        or "TAXA" in nome_norm
        or "ABSENTEISMO" in nome_norm
    ):
        return f"{valor:,.1f}%".replace(",", "X").replace(".", ",").replace("X", ".")

    # números inteiros
    if float(valor).is_integer():
        return f"{int(valor):,}".replace(",", ".")

    # números decimais
    return f"{valor:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
RH_ICONS = {
    "TOTAL DE COLABORADORES CLT": "👥",
    "TOTAL DE MÉDICOS": "🩺",
    "TOTAL DE ENFERMAGEM": "💉",
    "ADMISSÕES": "📥",
    "DESLIGAMENTOS": "📤",
    "TAXA DE TURNOVER": "🔄",
    "ABSENTEÍSMO": "⏱️",
    "AFASTAMENTOS": "🏥",
    "ACIDENTES DE TRABALHO": "⚠️",
}

def render_rh_indicator_card(nome_indicador, panel_df):
    info = rh_get_value_and_meta(panel_df)

    valor = info["valor"]
    mes = info["mes"]

    icone = RH_ICONS.get(nome_indicador, "📊")
    titulo = f"{icone} {nome_indicador}"

    valor_fmt = rh_format_value(nome_indicador, valor)
    mes_fmt = MESES_LABEL.get(mes, "-") if mes is not None else "-"

    card_html = (
        f'<div style="'
        f'background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);'
        f'border: 1px solid #E2E8F0;'
        f'border-radius: 22px;'
        f'padding: 18px 18px 16px 18px;'
        f'box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);'
        f'min-height: 220px;'
        f'margin-bottom: 14px;'
        f'display:flex;'
        f'flex-direction:column;'
        f'justify-content:space-between;'
        f'">'

        f'<div>'
        f'  <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; margin-bottom:10px;">'
        f'      <div style="font-size:14px; font-weight:800; color:#0F172A; line-height:1.35;">'
        f'          {titulo}'
        f'      </div>'
        f'      <div style="'
        f'          background:#64748B;'
        f'          color:#FFFFFF;'
        f'          font-size:11px;'
        f'          font-weight:700;'
        f'          padding:6px 10px;'
        f'          border-radius:999px;'
        f'          white-space:nowrap;'
        f'      ">'
        f'          Sem meta'
        f'      </div>'
        f'  </div>'

        f'  <div style="font-size:12px; color:#64748B; margin-bottom:12px;">Referência: {mes_fmt}</div>'

        f'  <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:16px; padding:14px 12px;">'
        f'      <div style="font-size:11px; color:#64748B; font-weight:700; text-transform:uppercase; margin-bottom:6px;">Valor atual</div>'
        f'      <div style="font-size:30px; font-weight:800; color:#0F172A; line-height:1;">{valor_fmt}</div>'
        f'  </div>'
        f'</div>'

        f'<div style="margin-top:14px; font-size:12px; color:#94A3B8;">Indicador mensal consolidado</div>'

        f'</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)

def render_rh_page(df):
    unidade = "RH"
    st.subheader("Gestão de Pessoas")

    work_df = df.copy()

    # respeita o filtro lateral de período já existente no app
    if "mes_label" in work_df.columns and "meses_selecionados" in globals():
        work_df = work_df[work_df["mes_label"].isin(meses_selecionados)].copy()

    indicadores_rh = [
        "TOTAL DE COLABORADORES CLT",
        "TOTAL DE MÉDICOS",
        "TOTAL DE ENFERMAGEM",
        "ADMISSÕES",
        "DESLIGAMENTOS",
        "TAXA DE TURNOVER",
        "ABSENTEÍSMO",
        "AFASTAMENTOS",
        "ACIDENTES DE TRABALHO",
]

    paineis = {
        indicador: filter_panel(work_df, unidade, indicador)
        for indicador in indicadores_rh
    }

    section_start(
        "Painel de indicadores de RH",
        "Leitura executiva dos indicadores da aba INDICADORES RH com valor atual e referência mensal"
    )

    cols = st.columns(3)
    for idx, indicador in enumerate(indicadores_rh):
        with cols[idx % 3]:
            render_rh_indicator_card(indicador, paineis[indicador])

    section_end()

st.markdown("""
<h1 style="margin-bottom:0;">
<p style="margin-top:0; color:#64748B; font-size:16px;">
</p>
""", unsafe_allow_html=True)
# ===== BOTÃO PROFISSIONAL DE UPLOAD =====

st.sidebar.markdown("### Atualizar base")

col1, col2 = st.sidebar.columns([1,1])

with col1:
    abrir_upload = st.button("📂 Atualizar", use_container_width=True)

with col2:
    limpar_upload = st.button("✖", use_container_width=True)

if limpar_upload:
    st.session_state.pop("uploaded_file", None)
    st.rerun()

uploaded = None

if abrir_upload:
    uploaded = st.sidebar.file_uploader(
        "Selecionar arquivo",
        type=["xlsx"],
        key="upload_hidden"
    )
else:
    uploaded = st.session_state.get("uploaded_file", None)

# salva na sessão
if uploaded is not None:
    st.session_state["uploaded_file"] = uploaded
if "uploaded_file" in st.session_state:
    st.sidebar.success("Base atualizada")
else:
    st.sidebar.caption("Usando base local")
file_bytes = uploaded.getvalue() if uploaded else None
data, source_name = load_workbook_data(file_bytes) if uploaded else load_workbook_data(None)
metas_data = load_metas_data(file_bytes) if uploaded else load_metas_data(None)
financeiro_data = load_financeiro_data(file_bytes) if uploaded else load_financeiro_data(None)

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
    [
        "UPA Luziânia",
        "UPA Jardim Ingá",
        "HMJI",
        "Atenção Secundária",
        "Saúde Mental",
        "Atenção Primária",
        "Gestão de Pessoas",
        "Financeiro",
        "Metas do Plano"
    ]
)

st.sidebar.markdown("## Filtros")
meses_selecionados = st.sidebar.multiselect(
    "Período",
    [MESES_LABEL[m] for m in MESES],
    default=[MESES_LABEL[m] for m in MESES]
)

if "mes_label" in metas_data.columns:
    metas_data = metas_data[metas_data["mes_label"].isin(meses_selecionados)].copy()
else:
    metas_data = pd.DataFrame(columns=["indicador", "indicador_norm", "mes", "mes_label", "valor"])

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
elif pagina == "Atenção Primária":
    render_generic(data, "ATENÇÃO PRIMÁRIA", [
        "CONSULTAS MÉDICAS",
        "NÍVEL SUPERIOR (EXCETO MÉDICO)",
    ])
elif pagina == "Gestão de Pessoas":
    render_rh_page(data)
elif pagina == "Financeiro":
    render_financeiro_page(financeiro_data)
else:
    render_metas_page(data, metas_data)

with st.expander("Base transformada"):
    st.dataframe(data, use_container_width=True, hide_index=True)
