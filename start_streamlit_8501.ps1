param(
    [int]$Port = 8501,
    [switch]$OpenBrowser
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$appRelPath = "PowerBI/bi_municipio_streamlit.py"
if (-not (Test-Path $appRelPath)) {
    throw "App nao encontrado em $appRelPath"
}

Write-Host "[1/4] Encerrando processos antigos do app..." -ForegroundColor Cyan
$appProcs = Get-CimInstance Win32_Process | Where-Object {
    $_.Name -match "python|streamlit" -and $_.CommandLine -match "bi_municipio_streamlit.py"
}
foreach ($proc in $appProcs) {
    Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
}

Write-Host "[2/4] Garantindo porta $Port livre..." -ForegroundColor Cyan
$listeners = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty OwningProcess -Unique
foreach ($pid in $listeners) {
    if ($pid) {
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "[3/4] Aplicando configuracao de reload estavel..." -ForegroundColor Cyan
$env:STREAMLIT_SERVER_RUN_ON_SAVE = "true"
$env:STREAMLIT_SERVER_FILE_WATCHER_TYPE = "poll"
$env:STREAMLIT_SERVER_HEADLESS = "true"
$env:STREAMLIT_SERVER_PORT = "$Port"

$lastWrite = (Get-Item $appRelPath).LastWriteTime.ToString("dd/MM/yyyy HH:mm:ss")
Write-Host "Arquivo alvo: $appRelPath" -ForegroundColor DarkGray
Write-Host "Ultima alteracao: $lastWrite" -ForegroundColor DarkGray

if ($OpenBrowser) {
    $cacheBust = [DateTimeOffset]::Now.ToUnixTimeSeconds()
    Start-Process "http://localhost:$Port/?v=$cacheBust" | Out-Null
}

Write-Host "[4/4] Subindo Streamlit em localhost:$Port ..." -ForegroundColor Green
& streamlit run $appRelPath --server.port $Port --server.fileWatcherType poll --server.runOnSave true --server.headless true