# Start-All.ps1
# Comprehensive script to start all services for the chat application

Write-Host "Starting all services for the Chat Application..." -ForegroundColor Green

# Function to create a new PowerShell window and run a command
function Start-ServiceInNewWindow {
    param (
        [string]$ServiceName,
        [string]$Directory,
        [string]$Command
    )
    
    Write-Host "Starting $ServiceName..." -ForegroundColor Cyan
    
    # Create a new PowerShell process
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Directory'; Write-Host 'Starting $ServiceName' -ForegroundColor Green; $Command"
}

# Set the base directory
$baseDir = $PSScriptRoot

# Check if PostgreSQL is installed and running
$pgService = Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue
if ($pgService -and $pgService.Status -ne "Running") {
    Write-Host "Starting PostgreSQL service..." -ForegroundColor Yellow
    Start-Service $pgService
    Start-Sleep -Seconds 5
}

# Create databases if they don't exist
# Note: This requires PostgreSQL to be installed and psql to be in the PATH
if (Get-Command "psql" -ErrorAction SilentlyContinue) {
    Write-Host "Creating databases if they don't exist..." -ForegroundColor Yellow
    
    $databases = @("auth", "chat", "notification")
    foreach ($db in $databases) {
        $dbExists = psql -U postgres -c "SELECT 1 FROM pg_database WHERE datname = '$db'" | Select-String -Pattern "1 row"
        if (-not $dbExists) {
            Write-Host "Creating database: $db" -ForegroundColor Yellow
            psql -U postgres -c "CREATE DATABASE $db"
        }
    }
} else {
    Write-Host "PostgreSQL command-line tools not found. Please create databases manually." -ForegroundColor Red
}

# Start Redis if installed
$redisService = Get-Service -Name "Redis*" -ErrorAction SilentlyContinue
if ($redisService -and $redisService.Status -ne "Running") {
    Write-Host "Starting Redis service..." -ForegroundColor Yellow
    Start-Service $redisService
    Start-Sleep -Seconds 2
} else {
    Write-Host "Redis service not found. If Redis is required, please start it manually." -ForegroundColor Yellow
}

# Start Auth Service
Start-ServiceInNewWindow -ServiceName "Auth Service" -Directory "$baseDir\services\auth" -Command "py run.py"

# Wait a moment before starting the next service
Start-Sleep -Seconds 2

# Start Chat Service
Start-ServiceInNewWindow -ServiceName "Chat Service" -Directory "$baseDir\services\chat" -Command "py run.py"

# Wait a moment before starting the next service
Start-Sleep -Seconds 2

# Start Notification Service
Start-ServiceInNewWindow -ServiceName "Notification Service" -Directory "$baseDir\services\notification" -Command "py run.py"

# Wait a moment before starting the next service
Start-Sleep -Seconds 2

# Start the API Gateway using our Python script
Start-ServiceInNewWindow -ServiceName "API Gateway" -Directory "$baseDir" -Command "py api-gateway.py"

# Wait a moment before starting the frontend
Start-Sleep -Seconds 2

# Start the frontend application
Start-ServiceInNewWindow -ServiceName "Frontend" -Directory "$baseDir\frontend" -Command "npm run dev"

Write-Host "All services started!" -ForegroundColor Green
Write-Host "API Gateway: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Auth Service: http://localhost:8001" -ForegroundColor Yellow
Write-Host "Chat Service: http://localhost:8002" -ForegroundColor Yellow
Write-Host "Notification Service: http://localhost:8003" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow

Write-Host "Note: This is a development setup. For production, use Docker Compose or a proper orchestration tool." -ForegroundColor Magenta 