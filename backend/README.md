# Admission Pilot - Backend

This is the Python FastAPI backend for Admission Pilot.

## Setup

1. **Virtual Environment**
   ```bash
   python -m venv .venv
   ```
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or using pip with pyproject.toml:
   ```bash
   pip install -e .[dev]
   ```

3. **Environment Variables**
   Copy `.env.example` to `.env` and fill in the values:
   ```bash
   cp .env.example .env
   ```

## Running the Server

```bash
uvicorn app.main:app --reload
```
API will be available at `http://localhost:8000`
Swagger documentation at `http://localhost:8000/docs`

## Docker

To build and run standalone:
```bash
docker build -t admission-pilot-backend .
docker run -p 8000:8000 admission-pilot-backend
```

## Structure
- `app/`: Core application logic (API, models, schemas, crud).
- `tests/`: Unit and integration tests.
- `logs/`: Application logs.
- `migrations/`: Alembic database migrations.
