import pandas as pd
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

df = pd.read_excel('PowerBI/data_raw/producao_consolidada_marco_2026_celk.xlsx', sheet_name=0, dtype=str)
df.columns = [c.strip().upper() for c in df.columns]
df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce', dayfirst=True)
df = df.dropna(subset=['DATA'])

dow_map = {0: 'Segunda', 1: 'Terça', 2: 'Quarta', 3: 'Quinta', 4: 'Sexta', 5: 'Sábado', 6: 'Domingo'}
df['DIA_SEMANA'] = df['DATA'].dt.dayofweek.map(dow_map)
df['MES_LABEL'] = df['DATA'].dt.to_period('M').dt.strftime('%b/%y').str.capitalize()

print('=' * 60)
print('DIAGNÓSTICO - March/26')
print('=' * 60)
mar = df[df['MES_LABEL'] == 'Mar/26']
print(f'\nTotal registros: {len(mar)}')
print(f'\nDistribuição por dia da semana:')
counts = mar['DIA_SEMANA'].value_counts().sort_index()
for dia, count in counts.items():
    print(f'  {dia:10s}: {count:6d}')

print(f'\nDatas únicas por dia:')
for dia in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]:
    subset = mar[mar['DIA_SEMANA'] == dia]
    if len(subset) > 0:
        unique_dates = subset['DATA'].dt.date.nunique()
        print(f'  {dia:10s}: {unique_dates:2d} datas')

print(f'\nPrimeiras 10 datas em March/26:')
unique_dates = sorted(mar['DATA'].dt.date.unique())
for d in unique_dates[:10]:
    dow_idx = pd.to_datetime(d).dayofweek
    dow_name = dow_map[dow_idx]
    count = len(mar[mar['DATA'].dt.date == d])
    print(f'  {d} ({dow_name:10s}): {count} regs')
