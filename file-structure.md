# Advanced Chat Application - File Structure

## Root Structure
```
chat-app/
├── frontend/                  # Next.js frontend application
├── services/                  # Backend microservices
│   ├── auth/                  # Authentication service
│   ├── chat/                  # Chat service
│   └── notification/          # Notification service
├── infrastructure/            # Infrastructure configuration
├── docker-compose.yml         # Local development environment
├── package.json               # Root package.json for monorepo
├── pnpm-workspace.yaml        # PNPM workspace configuration
└── README.md                  # Project documentation
```

## Frontend Structure
```
frontend/
├── app/                       # Next.js App Router
│   ├── (auth)/                # Authentication routes (grouped)
│   │   ├── login/             # Login page
│   │   ├── register/          # Registration page
│   │   └── layout.tsx         # Auth layout
│   ├── chat/                  # Chat routes
│   │   ├── [roomId]/          # Dynamic room route
│   │   ├── page.tsx           # Chat home page
│   │   └── layout.tsx         # Chat layout
│   ├── profile/               # User profile routes
│   │   └── page.tsx           # Profile page
│   ├── api/                   # API routes
│   ├── layout.tsx             # Root layout
│   └── page.tsx               # Home page
├── components/                # React components
│   ├── auth/                  # Authentication components
│   │   ├── login-form.tsx
│   │   └── register-form.tsx
│   ├── chat/                  # Chat components
│   │   ├── message-list.tsx
│   │   ├── message-input.tsx
│   │   ├── room-list.tsx
│   │   └── room-header.tsx
│   ├── profile/               # Profile components
│   │   └── profile-form.tsx
│   ├── ui/                    # UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   └── avatar.tsx
│   └── layout/                # Layout components
│       ├── header.tsx
│       ├── sidebar.tsx
│       └── footer.tsx
├── lib/                       # Utility functions and hooks
│   ├── api/                   # API client
│   │   ├── auth.ts
│   │   ├── chat.ts
│   │   └── notification.ts
│   ├── hooks/                 # Custom hooks
│   │   ├── use-auth.ts
│   │   ├── use-chat.ts
│   │   └── use-websocket.ts
│   ├── utils/                 # Utility functions
│   │   ├── date.ts
│   │   └── validation.ts
│   ├── types/                 # TypeScript types
│   │   ├── auth.ts
│   │   ├── chat.ts
│   │   └── notification.ts
│   └── context/               # React contexts
│       ├── auth-context.tsx
│       └── chat-context.tsx
├── public/                    # Static assets
│   ├── images/
│   ├── fonts/
│   └── favicon.ico
├── styles/                    # Global styles
│   └── globals.css
├── next.config.js             # Next.js configuration
├── tailwind.config.js         # Tailwind CSS configuration
├── tsconfig.json              # TypeScript configuration
└── package.json               # Frontend dependencies
```

## Auth Service Structure
```
services/auth/
├── app/                       # FastAPI application
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── auth.py            # Auth endpoints
│   │   └── users.py           # User endpoints
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration
│   │   ├── security.py        # Security utilities
│   │   └── exceptions.py      # Custom exceptions
│   ├── db/                    # Database
│   │   ├── __init__.py
│   │   ├── session.py         # Database session
│   │   └── repositories/      # Data access
│   │       ├── __init__.py
│   │       └── users.py       # User repository
│   ├── models/                # Domain models
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   └── token.py           # Token model
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py            # User schema
│   │   └── token.py           # Token schema
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── auth.py            # Auth service
│   │   └── user.py            # User service
│   └── main.py                # Application entry point
├── tests/                     # Tests
│   ├── __init__.py
│   ├── conftest.py            # Test configuration
│   ├── api/                   # API tests
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   └── test_users.py
│   └── services/              # Service tests
│       ├── __init__.py
│       ├── test_auth.py
│       └── test_user.py
├── alembic/                   # Database migrations
│   ├── versions/
│   └── env.py
├── Dockerfile                 # Docker configuration
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Python project configuration
└── README.md                  # Service documentation
```

## Chat Service Structure
```
services/chat/
├── app/                       # FastAPI application
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── rooms.py           # Room endpoints
│   │   └── messages.py        # Message endpoints
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration
│   │   ├── security.py        # Security utilities
│   │   └── exceptions.py      # Custom exceptions
│   ├── db/                    # Database
│   │   ├── __init__.py
│   │   ├── session.py         # Database session
│   │   └── repositories/      # Data access
│   │       ├── __init__.py
│   │       ├── rooms.py       # Room repository
│   │       └── messages.py    # Message repository
│   ├── models/                # Domain models
│   │   ├── __init__.py
│   │   ├── room.py            # Room model
│   │   └── message.py         # Message model
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── room.py            # Room schema
│   │   └── message.py         # Message schema
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── room.py            # Room service
│   │   └── message.py         # Message service
│   ├── websockets/            # WebSocket handlers
│   │   ├── __init__.py
│   │   ├── connection.py      # Connection management
│   │   └── events.py          # Event handlers
│   ├── events/                # Event handling
│   │   ├── __init__.py
│   │   ├── publisher.py       # Event publisher
│   │   └── handlers.py        # Event handlers
│   └── main.py                # Application entry point
├── tests/                     # Tests
│   ├── __init__.py
│   ├── conftest.py            # Test configuration
│   ├── api/                   # API tests
│   │   ├── __init__.py
│   │   ├── test_rooms.py
│   │   └── test_messages.py
│   └── services/              # Service tests
│       ├── __init__.py
│       ├── test_room.py
│       └── test_message.py
├── alembic/                   # Database migrations
│   ├── versions/
│   └── env.py
├── Dockerfile                 # Docker configuration
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Python project configuration
└── README.md                  # Service documentation
```

## Notification Service Structure
```
services/notification/
├── app/                       # FastAPI application
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── notifications.py   # Notification endpoints
│   │   └── preferences.py     # Preference endpoints
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration
│   │   ├── security.py        # Security utilities
│   │   └── exceptions.py      # Custom exceptions
│   ├── db/                    # Database
│   │   ├── __init__.py
│   │   ├── session.py         # Database session
│   │   └── repositories/      # Data access
│   │       ├── __init__.py
│   │       ├── notifications.py # Notification repository
│   │       └── preferences.py # Preference repository
│   ├── models/                # Domain models
│   │   ├── __init__.py
│   │   ├── notification.py    # Notification model
│   │   └── preference.py      # Preference model
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── notification.py    # Notification schema
│   │   └── preference.py      # Preference schema
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── notification.py    # Notification service
│   │   └── preference.py      # Preference service
│   ├── events/                # Event handling
│   │   ├── __init__.py
│   │   ├── consumer.py        # Event consumer
│   │   └── handlers.py        # Event handlers
│   ├── providers/             # Notification providers
│   │   ├── __init__.py
│   │   ├── email.py           # Email provider
│   │   ├── push.py            # Push notification provider
│   │   └── web.py             # Web notification provider
│   └── main.py                # Application entry point
├── tests/                     # Tests
│   ├── __init__.py
│   ├── conftest.py            # Test configuration
│   ├── api/                   # API tests
│   │   ├── __init__.py
│   │   ├── test_notifications.py
│   │   └── test_preferences.py
│   └── services/              # Service tests
│       ├── __init__.py
│       ├── test_notification.py
│       └── test_preference.py
├── alembic/                   # Database migrations
│   ├── versions/
│   └── env.py
├── Dockerfile                 # Docker configuration
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Python project configuration
└── README.md                  # Service documentation
```

## Infrastructure Structure
```
infrastructure/
├── docker/                    # Docker configurations
│   ├── traefik/               # API Gateway configuration
│   │   ├── traefik.yml
│   │   └── dynamic_conf.yml
│   ├── postgres/              # PostgreSQL configuration
│   │   └── init.sql
│   ├── redis/                 # Redis configuration
│   │   └── redis.conf
│   └── nats/                  # NATS configuration
│       └── nats.conf
├── kubernetes/                # Kubernetes manifests
│   ├── base/                  # Base configurations
│   │   ├── frontend.yaml
│   │   ├── auth-service.yaml
│   │   ├── chat-service.yaml
│   │   ├── notification-service.yaml
│   │   └── api-gateway.yaml
│   └── overlays/              # Environment-specific overlays
│       ├── dev/
│       ├── staging/
│       └── production/
├── terraform/                 # Terraform configurations
│   ├── modules/               # Reusable modules
│   │   ├── kubernetes/
│   │   ├── database/
│   │   ├── cache/
│   │   └── monitoring/
│   └── environments/          # Environment-specific configurations
│       ├── dev/
│       ├── staging/
│       └── production/
└── monitoring/                # Monitoring configurations
    ├── prometheus/
    │   └── prometheus.yml
    ├── grafana/
    │   └── dashboards/
    └── loki/
        └── loki.yml
``` 