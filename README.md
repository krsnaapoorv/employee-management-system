# Employee Management System

A REST API for managing employees, built with **Flask**, **SQLAlchemy**, and **PostgreSQL**. The project follows a layered architecture: controllers, services, repositories, models, and Marshmallow schemas for request validation.

## Features

- CRUD operations for employees
- Request validation with Marshmallow and webargs
- PostgreSQL persistence via Flask-SQLAlchemy
- Database migrations support with Flask-Migrate

## Tech Stack

| Layer | Technology |
|-------|------------|
| API | Flask 3 |
| ORM | Flask-SQLAlchemy |
| Validation | Marshmallow, webargs |
| Database | PostgreSQL (psycopg2) |
| Migrations | Flask-Migrate |

## Project Structure

```
employee-management-system/
├── application.py              # App entry point and configuration
├── requirements.txt
├── .env                        # Environment variables (not committed)
├── app/
│   ├── controllers/            # HTTP routes (API layer)
│   ├── services/               # Business logic
│   ├── repositories/           # Data access (`models/` registry + `employee_dao/` definitions)
│   ├── schemas/                # Marshmallow request/response schemas and validations
│   ├── utils/                  # Shared exceptions
│   └── extensions.py           # SQLAlchemy and Migrate instances
├── tests/                      # Unit tests (flat layout)
├── employee.yaml               # OpenAPI documentation
```

## Prerequisites

- **Python 3.10+**
- **PostgreSQL** installed and running locally (or a remote instance)
- **pip** and **venv**

## Environment Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd employee-management-system
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (this file is ignored by git):

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/employees_db
```

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | SQLAlchemy database connection URI | `postgresql://user:pass@localhost:5432/employees_db` |

**Connection URI format:**

```
postgresql://<username>:<password>@<host>:<port>/<database_name>
```

## Database Configuration

### 1. Create the PostgreSQL database

Connect to PostgreSQL and create a database for the application:

```sql
CREATE DATABASE employees_db;
```

Using `psql`:

```bash
psql -U postgres
CREATE DATABASE employees_db;
\q
```

### 2. Run database migrations

Schema changes are managed with **Flask-Migrate** (Alembic). Tables are **not** created automatically on app startup — run migrations before starting the API.

Model classes live under `app/repositories/models/employee_dao/`. Each new model should be imported in `app/repositories/models/__init__.py` so `import app.repositories.models` in `application.py` registers them with Alembic without naming them in the entry file.

**First-time setup** (from the project root with `.venv` activated):

```bash
# One-time: initialize the migrations folder (skip if migrations/ already exists)
flask --app application db init

# Generate a migration from your models
flask --app application db migrate -m "Initial migration"

# Apply migrations to the database
flask --app application db upgrade
```

**After changing models:**

```bash
flask --app application db migrate -m "Describe your change"
flask --app application db upgrade
```

**Employee table (`employee`):**

| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer | Primary key |
| `name` | String(100) | Required |
| `email` | String(120) | Required, unique |
| `department` | String(100) | Required |
| `date_joined` | Date | Required |

## Running the Application

### Start the server

Ensure migrations have been applied (`flask --app application db upgrade`), then:

```bash
python application.py
```

The API listens on:

- **URL:** `http://localhost:8080`
- **Host:** `0.0.0.0`
- **Port:** `8080`

You should see:

```
Starting Flask application...
```

### Verify the server

Open a browser or use curl:

```bash
curl http://localhost:8080/employees
```

## API Documentation

OpenAPI 3 specification: [`employee.yaml`](employee.yaml)

Import into [Swagger Editor](https://editor.swagger.io/) or Postman (**Import** → **File** → `employee.yaml`) to explore the API interactively.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/employees` | Create an employee |
| `GET` | `/employees` | List all employees |
| `GET` | `/employees/<id>` | Get employee by ID |
| `PUT` | `/employees/<id>` | Update employee (partial body allowed) |
| `DELETE` | `/employees/<id>` | Delete employee |

### Example requests

**Create employee — `POST /employees`**

```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "department": "Engineering",
  "date_joined": "2024-01-15"
}
```

**Update employee — `PUT /employees/1`**

```json
{
  "name": "Jane Smith",
  "department": "Product"
}
```

Set the header `Content-Type: application/json` for `POST` and `PUT` requests.

### Response codes

| Code | Meaning |
|------|---------|
| `200` | Success |
| `201` | Employee created |
| `400` | Business validation error (e.g. duplicate email) |
| `404` | Employee not found |
| `422` | Request body failed schema validation |
| `500` | Server error |

## Running Tests

Unit tests mock dependencies between layers:

| File | Layer | Mocks |
|------|-------|-------|
| `tests/test_repository.py` | Repository | SQLAlchemy `db.session` and `Employee` |
| `tests/test_service.py` | Service | `EmployeeRepository` |
| `tests/test_controller.py` | Controller | `EmployeeService` |

```bash
pytest
```

```bash
pytest -v
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'app'` | Run commands from the project root with the virtual environment activated |
| Database connection refused | Ensure PostgreSQL is running and `DATABASE_URL` in `.env` is correct |
| `relation "employee" does not exist` | Run `flask --app application db upgrade` to apply migrations |
| Port 8080 already in use | Stop the other process or change the port in `application.py` |


