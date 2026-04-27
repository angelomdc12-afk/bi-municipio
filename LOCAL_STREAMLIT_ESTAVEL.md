# Operacao Local Estavel (localhost:8501)

Este guia elimina o problema de "atualizei o codigo, mas a tela nao mudou".

## Causa raiz mais comum

1. Processo antigo do Streamlit continua vivo em segundo plano.
2. Novo processo sobe em outro contexto/terminal e nao substitui o anterior.
3. Execucao feita de diretorio diferente, com comportamento de watcher/config diferente.
4. Porta 8501 fica ocupada por instancia anterior.

## Solucao definitiva adotada

1. Script unico de start com reinicio limpo: `start_streamlit_8501.ps1`
2. Diagnostico rapido: `doctor_streamlit_local.ps1`
3. Config `poll + runOnSave` em dois pontos:
   - `.streamlit/config.toml`
   - `PowerBI/.streamlit/config.toml`
4. Marcador visual de build no app (sidebar):
   - `Build local: dd/mm/aaaa hh:mm:ss | Tag: ...`

## Como iniciar (padrao oficial)

No terminal, sempre na raiz do repo:

```powershell
powershell -ExecutionPolicy Bypass -File .\start_streamlit_8501.ps1 -Port 8501 -OpenBrowser
```

Esse comando:

1. Mata processos antigos do app.
2. Libera a porta 8501.
3. Forca watcher por polling.
4. Sobe o Streamlit ja na porta correta.

## Como validar rapidamente

1. Verifique a sidebar: o campo `Build local` deve mudar apos salvar arquivo.
2. Rode o doctor quando houver duvida:

```powershell
powershell -ExecutionPolicy Bypass -File .\doctor_streamlit_local.ps1 -Port 8501
```

## Regra de ouro

Nao subir o app por comandos manuais variados em terminais diferentes.
Use sempre o script `start_streamlit_8501.ps1`.