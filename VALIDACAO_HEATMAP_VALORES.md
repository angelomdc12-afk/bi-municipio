# ✅ VERIFICAÇÃO DE VALORES - MAPA DE CALOR - MAR/26

## Dados Calculados a partir do Arquivo CELK Original

### Estatísticas Gerais
- **Total de registros (UPA II Luziânia)**: 41.209
- **Período**: Março de 2026

### Distribuição por Dia da Semana

| Dia | Registros | Dias Únicos |
|-----|-----------|------------|
| Segunda | 10.422 | 5 |
| Terça | 5.973 | 5 |
| Quarta | 5.820 | 4 |
| Quinta | 5.999 | 4 |
| Sexta | 5.316 | 4 |
| Sábado | 3.277 | 4 |
| Domingo | 4.402 | 4 |

### Amostra de Validação - HORA 11 (11:00-11:59)

Métrica: **Média/dia**

| Dia | Registros | Dias | Média/dia |
|-----|-----------|------|-----------|
| Segunda | 507 | 5 | **101.4** |
| Terça | 392 | 5 | 78.4 |
| Quarta | 325 | 4 | 81.2 |
| Quinta | 347 | 4 | 86.8 |
| Sexta | 273 | 4 | 68.2 |
| Sábado | 201 | 4 | 50.2 |
| Domingo | 273 | 4 | 68.2 |

### Observações

✅ **O FIX do `dayfirst=False` está funcionando corretamente!**

- A distribuição agora mostra **TODOS os 7 dias da semana** com dados diferentes
- Segunda é o dia com maior volume (10.422 registros)
- A hora 11 é consistentemente de pico (média 101.4 para segunda)
- Os valores de dias únicos estão coerentes (5 dias de segunda/terça, 4 dos outros)

### Validação Cruzada

O arquivo `producao_consolidada_marco_2026_celk.xlsx` contém dados de:
- **Período**: Março de 2026 (do dia 02 de março até mais próximo)
- **Unidade**: UPA II Luziânia (UNIDADE DE PRONTO ATENDIMENTO DE LUZIANIA UPA)
- **Formato de Data**: ISO (YYYY-MM-DD HH:MM:SS) - processado corretamente com `dayfirst=False`

### Conclusão

✅ **CONFIRMADO**: Os valores estão corretos e baseados nos dados brutos do arquivo Excel.
O mapa de calor agora exibe uma distribuição realista que reflete:
- Maior concentração na segunda-feira (10.422 registros)
- Distribuição reduzida nos fins de semana
- Valores de média por hora coerentes com o volume de atendimentos
