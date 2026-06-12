# Resource Share Site - Stop Script
# Usage: .\stop.ps1

$ErrorActionPreference = "Continue"
$logDir = Join-Path $PSScriptRoot "logs"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Resource Share Site - Stop All" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Stop-ServiceByName($name, $pidFile) {
    if (Test-Path $pidFile) {
        $rawContent = Get-Content $pidFile -Raw
        if ([string]::IsNullOrWhiteSpace($rawContent)) {
            Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
            Write-Host ("  [SKIP] " + $name + " empty pid file") -ForegroundColor Gray
            return
        }
        $procId = [int]($rawContent.Trim())
        $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
        if ($proc) {
            try {
                $children = Get-CimInstance Win32_Process -Filter ("ParentProcessId=" + $procId) -ErrorAction SilentlyContinue
                foreach ($child in $children) {
                    Stop-Process -Id $child.ProcessId -Force -ErrorAction SilentlyContinue
                }
                Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 1
                Write-Host ("  [OK] " + $name + " PID:" + $procId + " stopped") -ForegroundColor Green
            } catch {
                Write-Host ("  [WARN] " + $name + " error") -ForegroundColor Yellow
            }
        } else {
            Write-Host ("  [SKIP] " + $name + " PID:" + $procId + " not running") -ForegroundColor Gray
        }
        Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    } else {
        Write-Host ("  [SKIP] " + $name + " no pid file") -ForegroundColor Gray
    }
}

Write-Host "Stopping services..." -ForegroundColor Yellow

Stop-ServiceByName "Admin(5174)" (Join-Path $logDir "admin.pid")
Stop-ServiceByName "Web(5173)" (Join-Path $logDir "web.pid")
Stop-ServiceByName "API(8000)" (Join-Path $logDir "api.pid")

Write-Host ""
Write-Host "Checking remaining processes..." -ForegroundColor Yellow

$portsToCheck = @(8000, 5173, 5174)
foreach ($port in $portsToCheck) {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($connections) {
        $procIds = $connections | Select-Object -ExpandProperty OwningProcess -Unique
        foreach ($procId in $procIds) {
            if ($procId -ne 0) {
                $p = Get-Process -Id $procId -ErrorAction SilentlyContinue
                if ($p) {
                    Write-Host ("  Kill: " + $p.ProcessName + " PID:" + $procId + " Port:" + $port) -ForegroundColor Yellow
                    Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
                }
            }
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  All services stopped!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
