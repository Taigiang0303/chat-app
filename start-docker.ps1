# Script to start Docker Desktop and run Docker Compose
# This script checks if Docker Desktop is running and starts it if needed

Write-Host "Checking if Docker Desktop is running..." -ForegroundColor Cyan

$dockerDesktopProcess = Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue

if (-not $dockerDesktopProcess) {
    Write-Host "Docker Desktop is not running. Attempting to start it..." -ForegroundColor Yellow
    
    # Check if Docker Desktop is installed
    $dockerDesktopPath = "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe"
    $dockerDesktopPathX86 = "${env:ProgramFiles(x86)}\Docker\Docker\Docker Desktop.exe"
    
    if (Test-Path $dockerDesktopPath) {
        Start-Process $dockerDesktopPath
        Write-Host "Docker Desktop is starting. Please wait..." -ForegroundColor Yellow
    } elseif (Test-Path $dockerDesktopPathX86) {
        Start-Process $dockerDesktopPathX86
        Write-Host "Docker Desktop is starting. Please wait..." -ForegroundColor Yellow
    } else {
        Write-Host "Docker Desktop executable not found. Please make sure Docker Desktop is installed." -ForegroundColor Red
        Write-Host "You can download it from: https://www.docker.com/products/docker-desktop" -ForegroundColor Red
        exit 1
    }
    
    # Wait for Docker Desktop to start
    Write-Host "Waiting for Docker Desktop to initialize (this may take a minute)..." -ForegroundColor Yellow
    $attempts = 0
    $maxAttempts = 30
    
    do {
        Start-Sleep -Seconds 5
        $attempts++
        Write-Host "." -NoNewline -ForegroundColor Yellow
        
        # Check if Docker is responsive
        $dockerRunning = $false
        try {
            $dockerInfo = docker info 2>$null
            if ($LASTEXITCODE -eq 0) {
                $dockerRunning = $true
            }
        } catch {
            # Do nothing, just continue waiting
        }
        
    } until ($dockerRunning -or $attempts -ge $maxAttempts)
    
    Write-Host ""
    
    if ($dockerRunning) {
        Write-Host "Docker Desktop is now running!" -ForegroundColor Green
    } else {
        Write-Host "Timed out waiting for Docker Desktop to start. Please start it manually." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Docker Desktop is already running." -ForegroundColor Green
}

# Check if Docker is responsive
try {
    $dockerInfo = docker info
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Docker is installed but not responding. Please check Docker Desktop status." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Error checking Docker status: $_" -ForegroundColor Red
    exit 1
}

Write-Host "Docker is ready! Starting services with Docker Compose..." -ForegroundColor Cyan

# Run Docker Compose
Write-Host "Running 'docker-compose up' to start all services..." -ForegroundColor Cyan
docker-compose up

# Note: If you want to run in detached mode, uncomment the line below and comment the line above
# docker-compose up -d 