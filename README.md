# Advanced Chat Application

A modern, type-safe chat application built with Next.js, FastAPI, and Supabase.

## Project Overview

This project implements a scalable, real-time chat application with robust authentication, message management, and notifications using domain-driven design principles and modern architectural patterns.

## Features

- Real-time messaging with WebSockets
- User authentication and authorization
- Group and direct messaging
- File sharing and attachments
- Notifications and read receipts
- Responsive design for all devices
- Dark mode support

## Tech Stack

### Frontend

- Next.js 14 with App Router
- TypeScript
- Tailwind CSS with ShadcnUI
- TanStack Query for data fetching
- Zustand for state management
- Zod for validation

### Backend

- FastAPI (Python)
- Pydantic for data validation
- SQLModel for database access
- JWT for authentication
- WebSockets for real-time communication
- NATS JetStream for event streaming

### Infrastructure

- Supabase PostgreSQL
- Redis for caching
- Docker for containerization
- Traefik for API Gateway
- Kubernetes for orchestration (production)

## Getting Started

### Prerequisites

- Node.js 18+
- PNPM 8+
- Python 3.10+
- Docker and Docker Compose

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/advanced-chat-application.git
cd advanced-chat-application
```

2. Install dependencies:

```bash
pnpm install
```

3. Start the development environment:

```bash
pnpm docker:up
pnpm dev
```

4. Open your browser and navigate to `http://localhost:3000`

## Project Structure

The project follows a monorepo structure:

- `frontend/`: Next.js application
- `services/`: Backend microservices
  - `auth/`: Authentication service
  - `chat/`: Chat service
  - `notification/`: Notification service
- `infrastructure/`: Infrastructure configuration

## Development Workflow

1. Create a feature branch from `develop`
2. Implement your changes
3. Write tests
4. Submit a pull request to `develop`
5. After review, changes will be merged

## License

This project is licensed under the MIT License - see the LICENSE file for details. 