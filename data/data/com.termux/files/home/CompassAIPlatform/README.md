# Compass AI Platform

This repository contains the complete codebase for the Compass AI Platform, a robust, secure, and scalable software solution designed to accelerate end-to-end development.

## Features

-   **Backend:** Node.js with Express, JWT authentication, RESTful APIs, WebSockets, and gRPC support.
-   **Frontend:** React-based responsive and modular UI.
-   **CI/CD:** Automated pipelines using GitHub Actions for continuous integration and deployment.
-   **Databases:** Integrated support for PostgreSQL (relational) and MongoDB (NoSQL).
-   **AI Integration:** Placeholder for embedded AI for recommendations and internal automations (e.g., TensorFlow.js, LangChain).
-   **Documentation:** Automatically generated technical documentation (Swagger, Docz - *planned*).
-   **Deployment:** Docker and Kubernetes ready for containerized deployment.

## Getting Started

### Prerequisites

-   Node.js (v18 or higher)
-   npm (v8 or higher)
-   Docker and Docker Compose

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd CompassAIPlatform
    ```

2.  **Backend Setup:**

    ```bash
    cd backend
    npm install
    cd ..
    ```

3.  **Frontend Setup:**

    ```bash
    cd frontend
    npm install
    cd ..
    ```

### Running the Application (Development)

1.  **Start Dockerized Databases:**

    ```bash
    docker-compose -f deployment/docker-compose.yml up -d postgres mongodb
    ```

2.  **Start Backend:**

    ```bash
    cd backend
    npm run dev
    # Or npm start for production mode
    cd ..
    ```

3.  **Start Frontend:**

    ```bash
    cd frontend
    npm start
    cd ..
    ```

    The frontend will typically be available at `http://localhost:3000` (or another port if configured).

### Running with Docker Compose (Production-like)

```bash
docker-compose -f deployment/docker-compose.yml up --build
```

This will build and run all services (backend, frontend, postgres, mongodb) in Docker containers.

## API Documentation (Swagger)

*Planned: Swagger UI will be available at `/api-docs` on the backend once implemented.*

## Project Structure

```
CompassAIPlatform/
├── backend/                # Node.js backend services
│   ├── src/
│   │   ├── routes/         # API routes (auth, api)
│   │   ├── grpc/           # gRPC service definitions
│   │   └── server.js       # Main backend application
│   └── package.json
├── frontend/               # React frontend application
│   ├── public/
│   ├── src/
│   │   ├── components/     # Reusable UI components (planned)
│   │   └── App.js          # Main frontend application
│   └── package.json
├── cicd/                   # CI/CD configurations (GitHub Actions)
│   └── .github/
│       └── workflows/
│           └── main.yml
├── database/               # Database configurations and schemas
│   ├── postgresql_config.md
│   └── mongodb_config.md
├── ai_integration/         # AI model integration code
│   └── ai_module.py
├── deployment/             # Docker and Kubernetes deployment files
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── docker-compose.yml
├── docs/                   # Project documentation (Swagger, general docs)
│   └── swagger.yaml
└── README.md
```

## Contributing

Contributions are welcome! Please see `CONTRIBUTING.md` (planned) for guidelines.

## License

This project is licensed under the MIT License - see the `LICENSE` file (planned) for details.
