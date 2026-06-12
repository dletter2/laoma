# Resource Share Site - Start Script
# Usage: .\start.ps1

$ErrorActionPreference = "Continue"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Resource Share Site - Start All" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Test-Port($port) {
    try {
        $conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
        return $null -ne $conn
    } catch {
        return $false
    }
}

Write-Host "[Check] Dependencies..." -ForegroundColor Yellow

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "  [ERROR] node not found" -ForegroundColor Red
    exit 1
}
Write-Host ("  Node:   " + (node --version)) -ForegroundColor Green

$venvPython = Join-Path $ProjectRoot "resource-api\venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "  [ERROR] venv not found at $venvPython" -ForegroundColor Red
    Write-Host "  Run: cd resource-api; python -m venv venv; .\venv\Scripts\activate; pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}
Write-Host ("  Python: " + (& $venvPython --version)) -ForegroundColor Green
Write-Host ""

$ports = @(8000, 5173, 5174)
$portNames = @("API", "Web", "Admin")
for ($i = 0; $i -lt $ports.Count; $i++) {
    if (Test-Port $ports[$i]) {
        Write-Host ("  [WARN] Port " + $ports[$i] + " in use (" + $portNames[$i] + ")") -ForegroundColor Yellow
    }
}
Write-Host ""

$logDir = Join-Path $PSScriptRoot "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

Write-Host "[1/3] Starting API (port 8000)..." -ForegroundColor Yellow
$apiDir = Join-Path $ProjectRoot "resource-api"
$apiLog = Join-Path $logDir "api.log"
$apiPidFile = Join-Path $logDir "api.pid"
$apiErrLog = Join-Path $logDir "api_error.log"

$apiProcess = Start-Process -FilePath $venvPython -ArgumentList @("-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload") -WorkingDirectory $apiDir -WindowStyle Hidden -RedirectStandardOutput $apiLog -RedirectStandardError $apiErrLog -PassThru
$apiProcess.Id | Out-File -FilePath $apiPidFile -Encoding ascii
Start-Sleep -Seconds 3
if (!$apiProcess.HasExited) {
    Write-Host ("  [OK] API started PID:" + $apiProcess.Id) -ForegroundColor Green
} else {
    Write-Host "  [ERROR] API failed to start. Check $apiErrLog" -ForegroundColor Red
}

Write-Host "[2/3] Starting Web (port 5173)..." -ForegroundColor Yellow
$webDir = Join-Path $ProjectRoot "resource-web"
$webLog = Join-Path $logDir "web.log"
$webPidFile = Join-Path $logDir "web.pid"
$webErrLog = Join-Path $logDir "web_error.log"

$webProcess = Start-Process -FilePath "cmd.exe" -ArgumentList @("/c", "npm", "run", "dev") -WorkingDirectory $webDir -WindowStyle Hidden -RedirectStandardOutput $webLog -RedirectStandardError $webErrLog -PassThru
$webProcess.Id | Out-File -FilePath $webPidFile -Encoding ascii
Start-Sleep -Seconds 3
if (!$webProcess.HasExited) {
    Write-Host ("  [OK] Web started PID:" + $webProcess.Id) -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Web failed to start. Check $webErrLog" -ForegroundColor Red
}

Write-Host "[3/3] Starting Admin (port 5174)..." -ForegroundColor Yellow
$adminDir = Join-Path $ProjectRoot "resource-admin"
$adminLog = Join-Path $logDir "admin.log"
$adminPidFile = Join-Path $logDir "admin.pid"
$adminErrLog = Join-Path $logDir "admin_error.log"

$adminProcess = Start-Process -FilePath "cmd.exe" -ArgumentList @("/c", "npm", "run", "dev") -WorkingDirectory $adminDir -WindowStyle Hidden -RedirectStandardOutput $adminLog -RedirectStandardError $adminErrLog -PassThru
$adminProcess.Id | Out-File -FilePath $adminPidFile -Encoding ascii
Start-Sleep -Seconds 3
if (!$adminProcess.HasExited) {
    Write-Host ("  [OK] Admin started PID:" + $adminProcess.Id) -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Admin failed to start. Check $adminErrLog" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  All services started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Web:   http://localhost:5173/" -ForegroundColor White
Write-Host "  Admin: http://localhost:5174/admin/" -ForegroundColor White
Write-Host "  API:   http://localhost:8000/" -ForegroundColor White
Write-Host "  Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "  Default login: admin / admin123" -ForegroundColor Yellow
Write-Host ""
