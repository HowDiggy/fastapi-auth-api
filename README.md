# FastAPI Authentication API

A robust and secure standalone authentication and user management API built with Python, FastAPI, and PostgreSQL. This project is containerized with Docker and follows modern API development best practices.

## Features

- **Secure User Registration:** `POST /users/` endpoint with robust password hashing using `passlib` and `bcrypt`.
- **JWT-Based Authentication:** Standard `POST /token` endpoint (OAuth2 Password Flow) that returns a signed JSON Web Token (JWT).
- **Protected Routes:** A `GET /users/me` endpoint to demonstrate how to protect routes and retrieve data for the currently authenticated user.
- **Secure Profile Updates:** A `PUT /users/me` endpoint that allows users to update their profile information after re-verifying their password.
- **Modular & Scalable Architecture:** Code is organized by concern (`crud`, `routers`, `schemas`, `security`) for maintainability.
- **Containerized Environment:** The entire application stack (API + PostgreSQL database) is managed with Docker and Docker Compose for a consistent and reproducible development environment.
- **Secure Configuration:** Manages secrets and configuration via environment variables and a `.env` file, powered by Pydantic-Settings.

## Tech Stack

- **Backend:** Python 3.13, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.0
- **Data Validation:** Pydantic
- **Containerization:** Docker, Docker Compose
- **Security:** `passlib[bcrypt]` for password hashing, `python-jose` for JWTs

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup & Configuration

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/HowDiggy/fastapi-auth-api
    cd fastapi-auth-api
    ```

2.  **Create the environment file:**
    The application requires a `.env` file in the project root for configuration. You can create one from the example template.
    ```bash
    # (If you create a .env.example file, this is the command)
    # cp .env.example .env
    ```
    Your `.env` file must contain the following variables:

    ```env
    # Generate a strong secret key using: openssl rand -hex 32
    SECRET_KEY="<your_generated_secret_key>"
    DATABASE_URL="postgresql+psycopg://user:password@db:5432/fastapi_auth_db"
    ```

### Running the Application

1.  **Build and run the services using Docker Compose:**
    ```bash
    docker compose up --build
    ```
    You can add the `-d` flag to run the containers in the background.

2.  **Access the API:**
    The API will be available at `http://localhost:8000`.
    The interactive documentation (Swagger UI) is available at **`http://localhost:8000/docs`**.

## API Endpoints Overview

- `POST /users/`: Register a new user.
- `POST /token`: Log in to receive a JWT access token.
- `GET /users/me/`: Get the profile of the currently authenticated user.
- `PUT /users/me/`: Update the email of the currently authenticated user.