# User Service

## Description

The User Service is one of 3 microservices for the Ada Developers Academy Cloud Curriculum e-commerce application. It handles the creation and management of user accounts in the e-commerce system.
### Data Models

- **User** — represents a customer account, containing `first_name`, `last_name`, `email`, and `is_admin`

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/users/` | Create a new user |
| GET | `/users/` | Get all users (supports query filters) |
| GET | `/users/<id>` | Get a single user by ID |
| GET | `/users/email` | Get a single user by email |
| PUT | `/users/<id>` | Update a user by ID |
| DELETE | `/users/<id>` | Delete a user by ID |

## Prerequisites

- Python 3.13+
- PostgreSQL
- AWS account or local AWS credentials (for SQS consumer)

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd user-service
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/user_service_db
SQLALCHEMY_TEST_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/user_service_test_db
```

### 5. Create the database

```bash
psql -U postgres

# Inside psql CLI
CREATE DATABASE user_service_db;
CREATE DATABASE user_service_test_db;
```

### 6. Run database migrations

```bash
flask db upgrade
```

## Running the App

```bash
flask run --debug
```

## Running Tests

```bash
pytest
```
