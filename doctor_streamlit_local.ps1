param(
    [int]$Port = 8501
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$appRelPath = "PowerBI/bi_municipio_streamlit.py"
$rootConfig = ".streamlit/config.toml"
$powerBiConfig = "PowerBI/.streamlit/config.toml"

Write-Host "=== STREAMLIT DOCTOR (LOCAL) ===" -ForegroundColor Cyan
Write-Host "Repositorio: $repoRoot"
Write-Host "Porta alvo: $Port"

if (Test-Path $appRelPath) {
    $item = Get-Item $appRelPath
    Write-Host "App: $appRelPath"
    Write-Host "Ultima alteracao app: $($item.LastWriteTime.ToString('dd/MM/yyyy HH:mm:ss'))"
} else {
    Write-Host "App nao encontrado: $appRelPath" -ForegroundColor Red
}

Write-Host "\n-- Configuracoes --" -ForegroundColor Yellow
Write-Host "Root config existe: $([bool](Test-Path $rootConfig))"
Write-Host "PowerBI config existe: $([bool](Test-Path $powerBiConfig))"

Write-Host "\n-- Processos streamlit/python do app --" -ForegroundColor Yellow
$procs = Get-CimInstance Win32_Process | Where-Object {
    $_.Name -match "python|streamlit" -and $_.CommandLine -match "streamlit|bi_municipio_streamlit.py"
}
if ($procs) {
    $procs | Select-Object ProcessId, Name, CommandLine | Format-Table -AutoSize
} else {
    Write-Host "Nenhum processo do app encontrado"
}

Write-Host "\n-- Porta $Port --" -ForegroundColor Yellow
$portInfo = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
if ($portInfo) {
    $portInfo | Select-Object LocalAddress, LocalPort, State, OwningProcess | Format-Table -AutoSize
} else {
    Write-Host "Nenhum listener na porta $Port"
}

Write-Host "\n-- Integridade de funcao SAMU --" -ForegroundColor Yellow
if (Test-Path $appRelPath) {
    $match = Select-String -Path $appRelPath -Pattern '^def render_samu_page\(' -AllMatches
    Write-Host "Ocorrencias de render_samu_page: $($match.Count)"
    $metas = Select-String -Path $appRelPath -Pattern 'Metas mensais priorit|60\.5|148\.5|USA TERRESTRE|SEM ENVIO DE VIATURA' -AllMatches
    Write-Host "Marcadores de meta encontrados: $($metas.Count)"
}

Write-Host "\nDiagnostico concluido." -ForegroundColor Green