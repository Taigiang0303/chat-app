# Chat Application

A microservices-based chat application with authentication, real-time messaging, and notifications.

## Architecture

This application consists of several microservices:

- **Auth Service**: Handles user authentication and authorization (Port 8001)
- **Chat Service**: Manages chat rooms and messages (Port 8002)
- **Notification Service**: Sends notifications to users (Port 8003)
- **API Gateway**: Routes requests to the appropriate microservices (Port 8000)
- **Frontend**: React-based user interface (Port 3000)

## Prerequisites

- Node.js and npm for the frontend
- Python 3.8+ for the backend services
- PostgreSQL database
- Redis (optional, for caching and pub/sub)

## Setup Instructions

### 1. Install Dependencies

For each service, install the required dependencies:

```bash
# Frontend dependencies
cd frontend
npm install

# Backend dependencies (for each service)
cd services/auth
pip install -r requirements.txt

cd ../chat
pip install -r requirements.txt

cd ../notification
pip install -r requirements.txt
```

### 2. Database Setup

Ensure PostgreSQL is installed and running. The script will attempt to create the necessary databases, but you can also create them manually:

```sql
CREATE DATABASE auth;
CREATE DATABASE chat;
CREATE DATABASE notification;
```

### 3. Starting the Application

#### Option 1: Using the PowerShell Script (Recommended for Windows)

Run the provided PowerShell script to start all services:

```powershell
# From the project root
.\start-all.ps1
```

This script will:
- Check if PostgreSQL is running and start it if needed
- Create the necessary databases if they don't exist
- Start all backend services in separate windows
- Start the API Gateway
- Start the frontend application

#### Option 2: Manual Startup

If you prefer to start services manually:

1. Start the Auth Service:
```bash
cd services/auth
py run.py  # On Windows
# OR
python3 run.py  # On Linux/Mac
```

2. Start the Chat Service:
```bash
cd services/chat
py run.py  # On Windows
# OR
python3 run.py  # On Linux/Mac
```

3. Start the Notification Service:
```bash
cd services/notification
py run.py  # On Windows
# OR
python3 run.py  # On Linux/Mac
```

4. Start the API Gateway:
```bash
# On Windows
py api-gateway.py

# On Linux/Mac
python3 api-gateway.py
```

5. Start the Frontend:
```bash
cd frontend
npm run dev
```

## Accessing the Application

Once all services are running, you can access:

- Frontend: http://localhost:3000
- API Gateway: http://localhost:8000
- Auth Service: http://localhost:8001
- Chat Service: http://localhost:8002
- Notification Service: http://localhost:8003

## Troubleshooting

### Connection Issues

If you encounter connection issues:

1. Ensure all services are running
2. Check that the ports are not being used by other applications
3. Verify that the API Gateway is correctly routing requests
4. Check the console output of each service for error messages

### Database Issues

If you encounter database issues:

1. Ensure PostgreSQL is running
2. Verify that the databases exist
3. Check the database connection settings in each service

### API Gateway Issues

If the API Gateway is not routing requests correctly:

1. Check the console output for routing information
2. Verify that the service endpoints in `api-gateway.py` match your actual service URLs
3. Ensure CORS headers are properly set if accessing from a different domain

### Python Command Issues

If you encounter errors with the Python command on Windows, try using `py` instead of `python`.

On Linux/Mac, use `python3` instead of `python` if needed.

### ASGI Import Errors

If you see an error like "Error loading ASGI app. Could not import module 'main'", make sure you're using the correct import path.

The correct import path for all services is `app.main:app` (not `main:app`).

This is because the FastAPI application is located in the `app/main.py` file within each service directory.

### API Gateway Connection Issues

If you encounter connection issues with the API Gateway:

1. Ensure all services are running
2. Check that the ports are not being used by other applications
3. Verify that the API Gateway is correctly routing requests
4. Check the console output of the API Gateway for error messages

## Development Notes

### Python Package Structure

This application uses a specific Python package structure:

- Each service is organized as a Python package with `app` as the main package
- The `run.py` script in each service directory sets up the Python path correctly
- This ensures that imports like `from app.core.config import settings` work properly

When developing:
1. Always use the `run.py` script to start services instead of calling Uvicorn directly
2. Keep the package structure consistent across services
3. Use absolute imports starting with `app.` in your code

### API Gateway Notes

- The API Gateway is a simple implementation for development purposes. For production, consider using a more robust solution like Traefik, Kong, or Nginx.
- The PowerShell script is designed for Windows environments. For Linux/Mac, use the provided bash script `start-all.sh`.
- For production deployment, consider using Docker Compose or Kubernetes for orchestration. 