#!/usr/bin/env python3
"""
Verifica os valores das médias do Mapa de Calor
"""
import pandas as pd
import numpy as np

f = r"c:\Users\Inovar Soluções\Documents\PowerBI\bi-municipio\PowerBI\data_raw\producao_consolidada_marco_2026_celk.xlsx"
df = pd.read_excel(f, dtype=str)
df.columns = [c.strip().upper() for c in df.columns]

# Parse dates with dayfirst=False (ISO format)
df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce", dayfirst=False)
df = df.dropna(subset=["DATA"])

# Filter for "UPA II Luziânia"
df_upa2 = df[df["UNIDADE"].str.upper().str.contains("LUZIANIA|UPA", na=False)].copy()

# Derive HORA and DIA_SEMANA
_dow_map = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 4: "Sexta", 5: "Sábado", 6: "Domingo"}
df_upa2["HORA"] = df_upa2["DATA"].dt.hour.astype(int)
df_upa2["DIA_SEMANA"] = df_upa2["DATA"].dt.dayofweek.map(_dow_map)

print("=" * 80)
print("VERIFICAÇÃO DE VALORES - MAPA DE CALOR - MAR/26")
print("=" * 80)
print(f"\nTotal de registros UPA II Luziânia: {len(df_upa2):,}")
print(f"\nDistribuição por dia da semana:")
dow_dist = df_upa2["DIA_SEMANA"].value_counts()
for day in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]:
    cnt = dow_dist.get(day, 0)
    print(f"  {day:12} : {cnt:5} registros")

print(f"\n" + "=" * 80)
print("DIAS ÚNICOS POR DIA DA SEMANA")
print("=" * 80)
dias_por_dow = df_upa2.groupby("DIA_SEMANA")["DATA"].apply(lambda s: s.dt.date.nunique())
for day in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]:
    n_dias = dias_por_dow.get(day, 0)
    print(f"  {day:12} : {n_dias} dias únicos")

print(f"\n" + "=" * 80)
print("MÉDIA POR HORA E DIA DA SEMANA (Métrica: Média/dia)")
print("=" * 80)

# Calculate count by HORA x DIA_SEMANA
contagem = (
    df_upa2.groupby(["HORA", "DIA_SEMANA"])
    .size()
    .reset_index(name="QTD")
    .pivot(index="HORA", columns="DIA_SEMANA", values="QTD")
    .fillna(0)
    .astype(int)
)

# Calculate average per day (divide by number of unique days)
media = contagem.div(dias_por_dow).round(1)

# Reindex to match display order
_DOW_ORDER = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
media = media.reindex(columns=_DOW_ORDER)
media = media.reindex(sorted(media.index))

# Add TOTAL row
total_row = contagem.sum(axis=0)
media_total = total_row / dias_por_dow
media_total = media_total.reindex(columns=_DOW_ORDER)
media_display = pd.concat([media, media_total.rename("TOTAL").to_frame().T])

print("\nPrimeiras 10 horas + TOTAL:")
print(media_display.head(11).to_string(float_format=lambda x: f"{x:.1f}"))

print(f"\n\nÚltimas horas:")
print(media_display.tail(10).to_string(float_format=lambda x: f"{x:.1f}"))

# Save to CSV for reference
media_display.to_csv(r"c:\Users\Inovar Soluções\Documents\PowerBI\bi-municipio\heatmap_valores_verificados.csv")
print(f"\n✓ Valores salvos em: heatmap_valores_verificados.csv")

# Show KPIs
print(f"\n" + "=" * 80)
print("KPIs EXIBIDOS NO PAINEL")
print("=" * 80)
media_sem_total = media
pico_hora_lbl = media_sem_total.sum(axis=1).idxmax()
pico_dia_lbl = media_sem_total.sum(axis=0).idxmax()
total_atend = int(contagem.sum().sum())
media_hora_val = round(media_sem_total.sum(axis=1).mean(), 1)

print(f"🔺 Hora de pico: {pico_hora_lbl:02d}:00 às {pico_hora_lbl:02d}:59")
print(f"📅 Dia de pico: {pico_dia_lbl}")
print(f"🔢 Total no período: {total_atend:,}")
print(f"⌀ Média/hora: {media_hora_val}")

print("\n" + "=" * 80)
