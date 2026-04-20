def apply_global_styles(st, background_base64):
    st.markdown(
        f"""
<style>

[data-testid="stAppViewContainer"] {{
    background-image:
        linear-gradient(rgba(239, 248, 255, 0.72), rgba(239, 248, 255, 0.82)),
        url("data:image/png;base64,{background_base64}");
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

/* ===== SIDEBAR CLEAN (OPCAO 1) ===== */
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

section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {{
    font-weight: 800 !important;
    margin-bottom: 0.5rem;
}}

section[data-testid="stSidebar"] .stFileUploader {{
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px 12px 10px 12px;
    margin-bottom: 18px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
}}

section[data-testid="stSidebar"] .stFileUploader section {{
    background: rgba(5,10,20,0.88) !important;
    border: 1px dashed rgba(255,255,255,0.10) !important;
    border-radius: 14px !important;
    padding: 18px 12px !important;
    min-height: auto !important;
}}

section[data-testid="stSidebar"] .stFileUploader section small,
section[data-testid="stSidebar"] .stFileUploader section div {{
    color: #F8FAFC !important;
}}

section[data-testid="stSidebar"] .stFileUploader button {{
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}}

section[data-testid="stSidebar"] .stFileUploader button:hover {{
    background: rgba(255,255,255,0.16) !important;
    border-color: rgba(255,255,255,0.22) !important;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"] {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 10px 12px;
    margin-bottom: 8px;
    transition: all 0.18s ease;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:hover {{
    background: rgba(255,255,255,0.10);
    transform: translateX(3px);
}}

section[data-testid="stSidebar"] div[role="radiogroup"] span {{
    font-weight: 600;
}}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
section[data-testid="stSidebar"] div[data-baseweb="input"] > div {{
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    min-height: 44px;
}}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {{
    border-color: #4DA3E6 !important;
}}

section[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div {{
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 16px !important;
    padding: 8px !important;
    min-height: 54px !important;
}}

section[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div:hover {{
    border-color: rgba(255,255,255,0.18) !important;
    background: rgba(255,255,255,0.08) !important;
}}

section[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div:focus-within {{
    border-color: #7CC0F2 !important;
    box-shadow: 0 0 0 1px rgba(124,192,242,0.35) !important;
}}

section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] {{
    background: rgba(255,255,255,0.14) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    margin: 4px !important;
    padding: 2px 8px !important;
}}

section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] span {{
    color: #FFFFFF !important;
    font-size: 13px !important;
}}

section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] svg {{
    fill: rgba(255,255,255,0.88) !important;
}}

section[data-testid="stSidebar"] [data-testid="stMultiSelect"] input {{
    color: #FFFFFF !important;
}}

section[data-testid="stSidebar"] [data-testid="stMultiSelect"] input::placeholder {{
    color: rgba(255,255,255,0.60) !important;
}}

section[data-testid="stSidebar"] small {{
    color: rgba(255,255,255,0.65) !important;
}}

h1 {{
    color: #0F172A !important;
    font-weight: 800 !important;
    letter-spacing: -0.7px;
    margin-bottom: 0.15rem;
}}

h2, h3 {{
    color: #0F172A !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
}}

p, label, .stMarkdown, .stCaption {{
    color: #334155;
}}

div[data-testid="stMetric"] {{
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid #E2E8F0;
    padding: 1rem;
    border-radius: 18px;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
}}

details {{
    background: #0B1220;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 0.35rem 0.8rem;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
}}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {{
    border-radius: 12px !important;
    border-color: #CBD5E1 !important;
}}

div[data-testid="stPlotlyChart"] {{
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%) !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 18px !important;
    padding: 0.45rem 0.45rem 0.25rem 0.45rem !important;
    box-shadow: 0 10px 22px rgba(15, 23, 42, 0.06) !important;
}}

div[data-testid="stPlotlyChart"] > div {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

.chart-exec-header {{
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid #E2E8F0;
    border-bottom: none;
    border-radius: 18px 18px 0 0;
    padding: 12px 14px 10px 14px;
    margin-bottom: -8px;
    box-shadow: 0 6px 14px rgba(15, 23, 42, 0.05);
}}

.chart-exec-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}}

.chart-exec-title {{
    font-size: 15px;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.25;
    letter-spacing: -0.2px;
}}

.chart-exec-subtitle {{
    font-size: 12px;
    color: #64748B;
    margin-top: 3px;
    line-height: 1.35;
}}

.chart-exec-chip {{
    white-space: nowrap;
    font-size: 11px;
    font-weight: 700;
    color: #0F6CBD;
    background: #EAF3FF;
    border: 1px solid #BFDBFE;
    border-radius: 999px;
    padding: 4px 9px;
}}

.chart-exec-chip-success {{
    color: #166534;
    background: #DCFCE7;
    border-color: #86EFAC;
}}

.chart-exec-chip-warning {{
    color: #92400E;
    background: #FEF3C7;
    border-color: #FCD34D;
}}

.chart-exec-chip-danger {{
    color: #991B1B;
    background: #FEE2E2;
    border-color: #FCA5A5;
}}

.chart-exec-chip-neutral {{
    color: #334155;
    background: #E2E8F0;
    border-color: #CBD5E1;
}}

.chart-exec-chip-info {{
    color: #0F6CBD;
    background: #EAF3FF;
    border-color: #BFDBFE;
}}

.section-card {{
    background: transparent;
}}

.section-title {{
    font-size: 1.06rem;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 0.2rem;
    letter-spacing: -0.3px;
}}

.section-subtitle {{
    font-size: 0.92rem;
    color: #64748B;
    margin-bottom: 1rem;
}}

.hero-wrap {{
    background: linear-gradient(135deg, rgba(15,108,189,0.92) 0%, rgba(37,99,235,0.88) 100%);
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 24px;
    padding: 1.2rem 1.25rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 16px 36px rgba(15, 23, 42, 0.10);
}}

.hero-title {{
    color: #FFFFFF;
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -0.8px;
    margin-bottom: 0.2rem;
}}

.hero-subtitle {{
    color: rgba(255,255,255,0.82);
    font-size: 0.98rem;
    margin-bottom: 1rem;
}}

.hero-chip-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}}

.hero-chip {{
    background: rgba(255,255,255,0.12);
    color: #FFFFFF;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 999px;
    padding: 0.42rem 0.78rem;
    font-size: 0.82rem;
    font-weight: 600;
    backdrop-filter: blur(6px);
}}

.soft-divider {{
    height: 1px;
    background: linear-gradient(90deg, rgba(148,163,184,0), rgba(148,163,184,0.45), rgba(148,163,184,0));
    margin: 0.6rem 0 1rem 0;
}}

</style>
""",
        unsafe_allow_html=True,
    )
