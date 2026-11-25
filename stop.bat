@echo off
title Stop UniMate AI Assistant
echo [INFO] Stopping UniMate backend and frontend processes...

:: Stop processes listening on port 8000 and 5173
powershell -Command "
$ports = @(8000, 5173);
foreach ($port in $ports) {
    try {
        $pids = (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue).OwningProcess | Select-Object -Unique;
        foreach ($p in $pids) {
            if ($p -and $p -ne 0) {
                Write-Host \"Terminating process ID $p on port $port...\";
                Stop-Process -Id $p -Force -ErrorAction SilentlyContinue;
            }
        }
    } catch {}
}
"

echo [OK] All UniMate processes stopped safely.
