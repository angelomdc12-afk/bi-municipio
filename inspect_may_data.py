import pandas as pd
from pathlib import Path
import json

base = Path(__file__).resolve().parent
data_raw = base / 'PowerBI' / 'data_raw'
results = {}

# CELK files
celk_files = sorted(data_raw.glob('producao_consolidada_*.xlsx'))
results['celk_files'] = [str(p.relative_to(base)) for p in celk_files]
results['celk_summary'] = {}

for p in celk_files:
    try:
        df = pd.read_excel(p, sheet_name=0, dtype=str)
    except Exception as e:
        results['celk_summary'][str(p.name)] = {'error': str(e)}
        continue
    months_found = set()
    # try to detect date-like columns
    for col in df.columns:
        try:
            ser = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
            ser = ser.dropna()
            if not ser.empty:
                months_found.update(ser.dt.month.unique().tolist())
        except Exception:
            pass
    results['celk_summary'][str(p.name)] = {
        'rows': int(df.shape[0]),
        'cols': int(df.shape[1]),
        'months_present': sorted(list(months_found))
    }

# Urgencia files
app_dir = base / 'PowerBI'
urg_files = sorted(app_dir.glob('urgencia*validado*.xlsx'))
results['urgencia_files'] = [str(p.relative_to(base)) for p in urg_files]
results['urg_summary'] = {}

for p in urg_files:
    try:
        xls = pd.ExcelFile(p)
        sheets = xls.sheet_names
        summary = {'sheets': sheets}
        # check common sheets used by app
        for name in ['KPI_DIARIO_GERAL','KPI_DIARIO_UNIDADE','KPI_SEMANAL_GERAL']:
            if name in sheets:
                df = pd.read_excel(p, sheet_name=name, dtype=str)
                months = set()
                for col in df.columns:
                    try:
                        ser = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
                        ser = ser.dropna()
                        if not ser.empty:
                            months.update(ser.dt.month.unique().tolist())
                    except Exception:
                        pass
                summary[name] = {'rows': int(df.shape[0]), 'cols': int(df.shape[1]), 'months_present': sorted(list(months))}
        results['urg_summary'][str(p.name)] = summary
    except Exception as e:
        results['urg_summary'][str(p.name)] = {'error': str(e)}

print(json.dumps(results, ensure_ascii=False, indent=2))
