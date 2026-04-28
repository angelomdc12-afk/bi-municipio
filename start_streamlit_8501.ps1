param(
    [int]$Port = 8501,
    [switch]$OpenBrowser,
    [switch]$Force,
    [switch]$AllowUnchangedCode
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$appRelPath = "PowerBI/bi_municipio_streamlit.py"
if (-not (Test-Path $appRelPath)) {
    throw "App nao encontrado em $appRelPath"
}
$appFullPath = (Resolve-Path $appRelPath).Path
$stateDir = Join-Path $repoRoot ".streamlit"
$stateFile = Join-Path $stateDir ("last_start_{0}.hash" -f $Port)

Write-Host "[0/4] Validando arquivo alvo..." -ForegroundColor Cyan
$hash = (Get-FileHash -Algorithm SHA256 -Path $appFullPath).Hash
$loginBuildLine = Select-String -Path $appFullPath -Pattern 'Login build:' -SimpleMatch | Select-Object -First 1
Write-Host "Arquivo alvo: $appRelPath" -ForegroundColor DarkGray
Write-Host "Caminho real: $appFullPath" -ForegroundColor DarkGray
Write-Host "SHA256: $hash" -ForegroundColor DarkGray
if ($loginBuildLine) {
    Write-Host "Marcador login no disco: $($loginBuildLine.Line.Trim())" -ForegroundColor DarkGray
}

if (-not (Test-Path $stateDir)) {
    New-Item -Path $stateDir -ItemType Directory -Force | Out-Null
}

$lastHash = ""
if (Test-Path $stateFile) {
    $lastHash = (Get-Content -Raw -Encoding UTF8 $stateFile).Trim()
}

if ($lastHash -and $lastHash -eq $hash -and -not $AllowUnchangedCode) {
    Write-Host "ERRO: Arquivo NAO foi alterado desde ultimo start em porta $Port!" -ForegroundColor Red
    Write-Host "SHA256 atual:     $hash" -ForegroundColor Red
    Write-Host "SHA256 anterior:  $lastHash" -ForegroundColor Red
    Write-Host "" -ForegroundColor Red
    Write-Host "Se voce fez edicoes:" -ForegroundColor Yellow
    Write-Host "  1. Aguarde autosave (500ms) ou pressione Ctrl+S" -ForegroundColor Yellow
    Write-Host "  2. Rode o start novamente depois de salvar" -ForegroundColor Yellow
    Write-Host "" -ForegroundColor Yellow
    Write-Host "Regras de seguranca deste script:" -ForegroundColor Cyan
    Write-Host "  -Force NAO ignora hash (serve para limpeza de processo/porta)." -ForegroundColor Cyan
    Write-Host "  -AllowUnchangedCode libera restart com hash igual (uso excepcional)." -ForegroundColor Cyan
    Write-Host "" -ForegroundColor Cyan
    Write-Host "Exemplo (somente debug, sem alteracao de codigo):" -ForegroundColor Magenta
    Write-Host "  ./start_streamlit_8501.ps1 -Port $Port -Force -AllowUnchangedCode" -ForegroundColor Magenta
    throw "Start bloqueado: hash inalterado. Salve o arquivo ou use -AllowUnchangedCode explicitamente."
}

if ($AllowUnchangedCode -and $lastHash -and $lastHash -eq $hash) {
    Write-Host "AVISO: -AllowUnchangedCode passado. Reiniciando mesmo com hash identico." -ForegroundColor Magenta
}

Write-Host "[0/4] Validando sintaxe Python (py_compile)..." -ForegroundColor Cyan
$pyCompileOutput = python -m py_compile $appFullPath 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Falha de sintaxe detectada. Start cancelado para evitar subir versao quebrada." -ForegroundColor Red
    $pyCompileOutput | ForEach-Object { Write-Host $_ -ForegroundColor Red }
    throw "py_compile falhou para $appRelPath"
}
Write-Host "py_compile: OK" -ForegroundColor Green
Set-Content -Path $stateFile -Value $hash -Encoding UTF8

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

$lastWrite = (Get-Item $appFullPath).LastWriteTime.ToString("dd/MM/yyyy HH:mm:ss")
Write-Host "Ultima alteracao: $lastWrite" -ForegroundColor DarkGray

if ($OpenBrowser) {
    $cacheBust = [DateTimeOffset]::Now.ToUnixTimeSeconds()
    Start-Process "http://localhost:$Port/?v=$cacheBust" | Out-Null
}

Write-Host "[4/4] Subindo Streamlit em localhost:$Port ..." -ForegroundColor Green
& streamlit run $appRelPath --server.port $Port --server.fileWatcherType poll --server.runOnSave true --server.headless true