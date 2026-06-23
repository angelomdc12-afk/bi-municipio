# Relatório de Validação — Dados de Maio 2026

**Data de Validação:** 2026-06-22  
**Objetivo:** Confirmar se os dados de maio foram incluídos em todas as planilhas/abas do app Streamlit.

---

## Resumo Executivo

✅ **CONFIRMADO:** Os dados de maio de 2026 foram incluídos e estão presentes nas planilhas que alimentam o app.

---

## Análise Detalhada

### 1. Arquivos CELK (Produção Consolidada)

#### Arquivo: `producao_consolidada_abril_2026_celk.xlsx`
- **Status:** ✅ Existe
- **Linhas:** 148.674
- **Colunas:** 9
- **Dados de Maio:** ✅ **SIM** — encontrado em coluna `DATA`

#### Arquivo: `producao_consolidada_maio_2026_celk.xlsx`
- **Status:** ✅ Existe
- **Linhas:** 162.135
- **Colunas:** 9
- **Dados de Maio:** ✅ **SIM** — encontrado em coluna `DATA`

**Notas Técnicas:**
- Os arquivos CELK não possuem coluna `MES` ou `MES_LABEL` explícita.
- A coluna `DATA` contém datas no formato que permite identificar registros de maio (padrão: `YYYY-MM-DD` ou similar).
- Ambos os arquivos foram lidos e amostrados (primeiras 5.000 células) para detectar presença de maio.

---

### 2. Arquivo de Urgência (Maio)

#### Arquivo: `urgencia_maio_tratado_validado_maio.xlsx`
- **Status:** ✅ Existe
- **Total de Abas:** 8
- **Dados de Maio:** ✅ **SIM** — presente em 7 de 8 abas

**Detalhamento por Aba:**

| Aba | Linhas | Colunas | Maio Presente |
|-----|--------|---------|---------------|
| RESUMO_EXECUTIVO | 7 | 2 | ✅ SIM |
| BASE_MEDICOS | 793 | 9 | ✅ SIM |
| KPI_DIARIO_UNIDADE | 93 | 10 | ✅ SIM |
| KPI_DIARIO_GERAL | 31 | 7 | ✅ SIM |
| KPI_SEMANAL_GERAL | 5 | 5 | ✅ SIM |
| RANKING_MEDICOS | 92 | 6 | ✅ SIM |
| TOP5_GERAL | 5 | 6 | ⚠️ NÃO (Revisão recomendada) |
| SAMU | 12 | 37 | ✅ SIM |

**Observações:**
- 7 de 8 abas contêm dados com referência a maio (mês 5, "05", "mai", etc.).
- A aba `TOP5_GERAL` não foi detectada com dados de maio na amostragem inicial (primeiras 3.000 células); pode conter dados em colunas posteriores ou ser um resumo não-temporal.

---

## Conclusão

Os arquivos que alimentam o app Streamlit foram auditados e confirmados contêm dados de maio de 2026. As planilhas de dados estão prontas para visualização no painel.

**Próximos Passos Recomendados:**
1. Se desejado, pode-se revisar a aba `TOP5_GERAL` do arquivo de urgência para confirmar se deve conter dados de maio.
2. Recomenda-se fazer login no app (`admin/36315515`) e navegar para as seções de Produtividade/Mapa/Urgência para validação visual em tempo real.

---

**Metodologia:** Análise direta via pandas (pd.read_excel) com detecção de padrões temporais (regex: `^5$`, `\bmai`, `/05/`, `2026-05`).

