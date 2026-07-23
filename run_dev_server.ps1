# InfraIndex Smart Dev Server Launcher (Docker + DB + API)
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host " Starting InfraIndex Platform Dev Environment...  " -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan

Set-Location "C:\Users\GAME\Desktop\uno-km\dev\AMEVA-Memory-Price-Check"

# 1. Activate Virtual Environment
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    & .\.venv\Scripts\Activate.ps1
}

# 2. Check if Docker is installed and running
$dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
if ($dockerCmd) {
    Write-Host "[Docker Check] Checking Docker status..." -ForegroundColor Yellow
    docker info 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[Docker Launch] Docker daemon is OFF. Starting Docker Desktop..." -ForegroundColor Magenta
        $dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        if (Test-Path $dockerPath) {
            Start-Process $dockerPath
            Write-Host "[Docker Launch] Waiting for Docker to start..." -NoNewline -ForegroundColor Yellow
            $retries = 0
            while ($retries -lt 25) {
                Start-Sleep -Seconds 3
                docker info 2>&1 | Out-Null
                if ($LASTEXITCODE -eq 0) { break }
                $retries++
                Write-Host "." -NoNewline -ForegroundColor Yellow
            }
            Write-Host ""
        } else {
            Write-Host "[Docker Warning] Docker Desktop path not found. Running without container auto-start." -ForegroundColor Red
        }
    }

    # 3. Ensure Containers are Running (PostgreSQL + Redis)
    docker info 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[Docker Compose] Ensuring PostgreSQL & Redis containers are UP..." -ForegroundColor Cyan
        docker compose --env-file .env -f infrastructure/docker/docker-compose.yml up -d db redis
        $env:USE_REAL_DB="True"

        # 4. Run Alembic Database Migrations
        Write-Host "[DB Migration] Syncing DB schemas..." -ForegroundColor Green
        alembic -c alembic.ini upgrade head
    }
} else {
    Write-Host "[Notice] Docker not installed. Running in Serverless/JSON mode." -ForegroundColor Gray
}

# 5. Launch Uvicorn API Server
Write-Host "[API Server] Launching Uvicorn Server on http://127.0.0.1:8000 ..." -ForegroundColor Green
uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 --reload
