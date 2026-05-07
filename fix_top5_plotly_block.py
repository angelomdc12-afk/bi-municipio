from pathlib import Path

file_path = Path(r"C:\Users\Inovar Soluções\Documents\PowerBI\bi-municipio\PowerBI\bi_municipio_streamlit.py")
lines = file_path.read_text(encoding="utf-8").splitlines()

start = None
end = None
for i, line in enumerate(lines):
    if 'fig4.update_traces(hovertemplate="<b>%{y}</b><br>%{x:,.0f} atendimentos<extra></extra>")' in line:
        start = i
        break

if start is None:
    raise RuntimeError("Linha de inicio do bloco Top5 nao encontrada")

for j in range(start + 1, min(start + 30, len(lines))):
    if 'n1 = str(top5_ref.iloc[0][' in lines[j]:
        end = j
        break

if end is None:
    raise RuntimeError("Linha de fim do bloco Top5 nao encontrada")

replacement = [
    '            fig4.update_traces(hovertemplate="<b>%{y}</b><br>%{x:,.0f} atendimentos<extra></extra>")',
    '            fig4 = apply_plotly_theme(fig4, title="Top 5 por atendimentos", subtitle="",',
    '                                      yaxis_title="", height=340, legend=False)',
    '            fig4.update_xaxes(title_text="Atendimentos")',
    '            plot(fig4, "pm_top5")',
    '            n1 = str(top5_ref.iloc[0]["Médico"])',
]

new_lines = lines[:start] + replacement + lines[end + 1:]
file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
print("OK")
