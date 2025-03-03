# Start-Services.ps1
# Script to start all backend services for the chat application

Write-Host "Starting all backend services..." -ForegroundColor Green

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

# Start API Gateway (if available as a standalone service)
# For now, we'll create a simple proxy using Python's http.server
Start-ServiceInNewWindow -ServiceName "Simple API Gateway" -Directory "$baseDir" -Command "py api-gateway.py"

Write-Host "All services started!" -ForegroundColor Green
Write-Host "API Gateway: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Auth Service: http://localhost:8001" -ForegroundColor Yellow
Write-Host "Chat Service: http://localhost:8002" -ForegroundColor Yellow
Write-Host "Notification Service: http://localhost:8003" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow

# Note: This script doesn't start database services like PostgreSQL, Redis, or NATS
# You'll need to have those running separately or modify this script to include them 