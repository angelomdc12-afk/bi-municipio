param(
    [int]$Port = 8501,
    [switch]$Strict
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$appRelPath = "PowerBI/bi_municipio_streamlit.py"
$appFullPath = if (Test-Path $appRelPath) { (Resolve-Path $appRelPath).Path } else { "" }
$rootConfig = ".streamlit/config.toml"
$powerBiConfig = "PowerBI/.streamlit/config.toml"
$stateFile = ".streamlit/last_start_$Port.hash"

$issues = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]

Write-Host "=== STREAMLIT DOCTOR (LOCAL) ===" -ForegroundColor Cyan
Write-Host "Repositorio: $repoRoot"
Write-Host "Porta alvo: $Port"

if (Test-Path $appRelPath) {
    $item = Get-Item $appRelPath
    Write-Host "App: $appRelPath"
    Write-Host "Caminho real app: $appFullPath"
    Write-Host "Ultima alteracao app: $($item.LastWriteTime.ToString('dd/MM/yyyy HH:mm:ss'))"
    $hash = (Get-FileHash -Algorithm SHA256 -Path $appRelPath).Hash
    Write-Host "SHA256 app: $hash"

    $loginBuildLine = Select-String -Path $appRelPath -Pattern 'Login build:' | Select-Object -First 1
    if ($loginBuildLine) {
        Write-Host "Login build no disco: $($loginBuildLine.Line.Trim())"
    } else {
        $warnings.Add("Marcador 'Login build' nao encontrado no disco.") | Out-Null
    }

    if (Test-Path $stateFile) {
        $lastStartHash = (Get-Content -Raw -Encoding UTF8 $stateFile).Trim()
        Write-Host "SHA256 ultimo start($Port): $lastStartHash"
        if ($lastStartHash -ne $hash) {
            $warnings.Add("Hash atual difere do ultimo start: ha alteracao no disco ainda nao aplicada no processo.") | Out-Null
        }
    } else {
        $warnings.Add("Arquivo de estado nao encontrado: $stateFile") | Out-Null
    }
} else {
    Write-Host "App nao encontrado: $appRelPath" -ForegroundColor Red
    $issues.Add("App alvo nao encontrado no caminho esperado.") | Out-Null
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

    if ($appFullPath) {
        $matchedProc = $procs | Where-Object {
            $_.CommandLine -and (
                $_.CommandLine -match [regex]::Escape($appRelPath) -or
                $_.CommandLine -match [regex]::Escape($appFullPath)
            )
        }
        if (-not $matchedProc) {
            $issues.Add("Ha processo Streamlit/Python ativo, mas nenhum aponta para o app alvo ($appRelPath).") | Out-Null
        }
    }
} else {
    Write-Host "Nenhum processo do app encontrado"
    $warnings.Add("Nenhum processo Streamlit/Python do app foi encontrado.") | Out-Null
}

Write-Host "\n-- Porta $Port --" -ForegroundColor Yellow
$portInfo = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
if ($portInfo) {
    $portInfo | Select-Object LocalAddress, LocalPort, State, OwningProcess | Format-Table -AutoSize
} else {
    Write-Host "Nenhum listener na porta $Port"
    $warnings.Add("Nenhum listener na porta $Port.") | Out-Null
}

Write-Host "\n-- Integridade de funcao SAMU --" -ForegroundColor Yellow
if (Test-Path $appRelPath) {
    $match = Select-String -Path $appRelPath -Pattern '^def render_samu_page\(' -AllMatches
    Write-Host "Ocorrencias de render_samu_page: $($match.Count)"
    if ($match.Count -ne 1) {
        $issues.Add("Integridade SAMU: esperado 1 render_samu_page, encontrado $($match.Count).") | Out-Null
    }
    $metas = Select-String -Path $appRelPath -Pattern 'Metas mensais priorit|60\.5|148\.5|USA TERRESTRE|SEM ENVIO DE VIATURA' -AllMatches
    Write-Host "Marcadores de meta encontrados: $($metas.Count)"
    if ($metas.Count -lt 3) {
        $warnings.Add("Marcadores de meta abaixo do esperado: $($metas.Count).") | Out-Null
    }
    $loginBuild = Select-String -Path $appRelPath -Pattern 'Login build:' -AllMatches
    Write-Host "Marcador Login build encontrado: $($loginBuild.Count)"
    if ($loginBuild.Count -lt 1) {
        $issues.Add("Marcador Login build nao encontrado no app.") | Out-Null
    }
}

Write-Host "\n-- Resumo de Integridade --" -ForegroundColor Yellow
if ($warnings.Count -gt 0) {
    Write-Host "Avisos: $($warnings.Count)" -ForegroundColor Yellow
    foreach ($w in $warnings) {
        Write-Host " - $w" -ForegroundColor Yellow
    }
} else {
    Write-Host "Avisos: 0"
}

if ($issues.Count -gt 0) {
    Write-Host "Falhas: $($issues.Count)" -ForegroundColor Red
    foreach ($i in $issues) {
        Write-Host " - $i" -ForegroundColor Red
    }
    if ($Strict) {
        throw "Doctor strict falhou com $($issues.Count) falha(s)."
    }
    Write-Host "\nDiagnostico concluido com FALHAS." -ForegroundColor Red
} else {
    Write-Host "Falhas: 0" -ForegroundColor Green
    Write-Host "\nDiagnostico concluido. Integridade OK." -ForegroundColor Green
}