#!/bin/bash
# Comprehensive script to start all services for the chat application

echo -e "\e[32mStarting all services for the Chat Application...\e[0m"

# Set the base directory
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to start a service in a new terminal
start_service() {
    local service_name=$1
    local directory=$2
    local command=$3
    
    echo -e "\e[36mStarting $service_name...\e[0m"
    
    # Different terminal commands based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        osascript -e "tell application \"Terminal\" to do script \"cd '$directory' && echo 'Starting $service_name' && $command\""
    else
        # Linux - try different terminal emulators
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd '$directory' && echo 'Starting $service_name' && $command; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e "cd '$directory' && echo 'Starting $service_name' && $command; exec bash" &
        elif command -v konsole &> /dev/null; then
            konsole --new-tab -e bash -c "cd '$directory' && echo 'Starting $service_name' && $command; exec bash" &
        else
            echo -e "\e[31mNo supported terminal emulator found. Please start the service manually:\e[0m"
            echo -e "cd '$directory' && $command"
        fi
    fi
    
    # Wait a moment before starting the next service
    sleep 2
}

# Check if PostgreSQL is running
if command -v pg_isready &> /dev/null; then
    if ! pg_isready &> /dev/null; then
        echo -e "\e[33mPostgreSQL is not running. Please start it manually.\e[0m"
    else
        echo -e "\e[32mPostgreSQL is running.\e[0m"
    fi
else
    echo -e "\e[33mCould not check PostgreSQL status. Please ensure it's running.\e[0m"
fi

# Create databases if they don't exist
if command -v psql &> /dev/null; then
    echo -e "\e[33mCreating databases if they don't exist...\e[0m"
    
    databases=("auth" "chat" "notification")
    for db in "${databases[@]}"; do
        if ! psql -U postgres -lqt | cut -d \| -f 1 | grep -qw "$db"; then
            echo -e "\e[33mCreating database: $db\e[0m"
            psql -U postgres -c "CREATE DATABASE $db"
        fi
    done
else
    echo -e "\e[31mPostgreSQL command-line tools not found. Please create databases manually.\e[0m"
fi

# Check if Redis is running
if command -v redis-cli &> /dev/null; then
    if ! redis-cli ping &> /dev/null; then
        echo -e "\e[33mRedis is not running. If Redis is required, please start it manually.\e[0m"
    else
        echo -e "\e[32mRedis is running.\e[0m"
    fi
else
    echo -e "\e[33mRedis command-line tools not found. If Redis is required, please start it manually.\e[0m"
fi

# Start Auth Service
start_service "Auth Service" "$BASE_DIR/services/auth" "python3 run.py"

# Start Chat Service
start_service "Chat Service" "$BASE_DIR/services/chat" "python3 run.py"

# Start Notification Service
start_service "Notification Service" "$BASE_DIR/services/notification" "python3 run.py"

# Start the API Gateway
start_service "API Gateway" "$BASE_DIR" "python3 api-gateway.py"

# Start the frontend application
start_service "Frontend" "$BASE_DIR/frontend" "npm run dev"

echo -e "\e[32mAll services started!\e[0m"
echo -e "\e[33mAPI Gateway: http://localhost:8000\e[0m"
echo -e "\e[33mAuth Service: http://localhost:8001\e[0m"
echo -e "\e[33mChat Service: http://localhost:8002\e[0m"
echo -e "\e[33mNotification Service: http://localhost:8003\e[0m"
echo -e "\e[33mFrontend: http://localhost:3000\e[0m"

echo -e "\e[35mNote: This is a development setup. For production, use Docker Compose or a proper orchestration tool.\e[0m" 