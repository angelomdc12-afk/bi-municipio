#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

# Read directly from Excel
df = pd.read_excel(
    "PowerBI/data_raw/producao_consolidada_marco_2026_celk.xlsx",
    sheet_name=0,
    usecols="A:I",
    dtype=str,
)
print(f"Raw excel: {len(df)} rows, columns: {list(df.columns)}")

# Normalize columns
df.columns = [c.strip().upper() for c in df.columns]
print(f"After normalize: columns = {list(df.columns)}")

# Parse date
df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce", dayfirst=True)
df = df.dropna(subset=["DATA"])
print(f"After parse datetime: {len(df)} rows")

# Create DIA_SEMANA
_dow_map = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 4: "Sexta", 5: "Sábado", 6: "Domingo"}
df["DIA_SEMANA"] = df["DATA"].dt.dayofweek.map(_dow_map)
df["MES_LABEL"] = df["DATA"].dt.to_period("M").dt.strftime("%b/%y").str.capitalize()

print(f"\nMES_LABEL unique: {sorted(df['MES_LABEL'].unique().tolist())}")
print("\n=== Feb/26 DIA_SEMANA value_counts ===")
feb_data = df[df['MES_LABEL'] == 'Feb/26']
if not feb_data.empty:
    print(feb_data['DIA_SEMANA'].value_counts().sort_index())
    print(f"\nFirst 10 unique dates in Feb/26:")
    print(feb_data[['DATA', 'DIA_SEMANA']].drop_duplicates('DATA').sort_values('DATA').head(10).to_string())
else:
    print("  (no Feb/26 data found)")
