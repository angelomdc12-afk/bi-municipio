#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

# Lê direto do arquivo
df = pd.read_excel(
    "PowerBI/data_raw/producao_consolidada_marco_2026_celk.xlsx",
    sheet_name=0,
    usecols="A:I",
    dtype=str,
)

# Normalize columns
df.columns = [c.strip().upper() for c in df.columns]

# Parse datetime
df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce", dayfirst=True)
df = df.dropna(subset=["DATA"])

# Create day of week mapping
_dow_map = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 4: "Sexta", 5: "Sábado", 6: "Domingo"}
df["DIA_SEMANA"] = df["DATA"].dt.dayofweek.map(_dow_map)
df["MES_LABEL"] = df["DATA"].dt.to_period("M").dt.strftime("%b/%y").str.capitalize()

print("=" * 60)
print("DIAGNÓSTICO DOS DADOS CELK")
print("=" * 60)
print(f"\nTotal de linhas: {len(df)}")
print(f"\nMeses encontrados:")
for mes in sorted(df['MES_LABEL'].unique()):
    count = len(df[df['MES_LABEL'] == mes])
    print(f"  {mes}: {count} registros")

print(f"\n=== MARCH/26 ===")
mar = df[df['MES_LABEL'] == 'Mar/26']
print(f"Total registros: {len(mar)}")
print(f"\nDistribuição por dia da semana:")
for dia in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]:
    count = len(mar[mar['DIA_SEMANA'] == dia])
    datas = mar[mar['DIA_SEMANA'] == dia]['DATA'].dt.date.nunique()
    print(f"  {dia:10s}: {count:5d} registros | {datas} datas únicas")

print(f"\nPrimeiras 10 datas em March/26 com dayofweek:")
sample = mar[['DATA', 'DIA_SEMANA']].drop_duplicates('DATA').sort_values('DATA').head(10)
print(sample.to_string(index=False))
