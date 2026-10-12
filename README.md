# User Management REST API

A beginner-friendly CRUD API built with Python, FastAPI, Pydantic, SQLAlchemy and SQLite.

## Features
- Create, list, get, update and delete users
- Required name and city
- Email format validation and unique email
- Age restricted to 18–60
- Correct 404 response for missing users and 409 for duplicate emails
- Optional filters: `GET /users?city=Coimbatore` and `GET /users?is_active=true`
- Interactive Swagger UI at `/docs`
- SQLite database file `users.db` is created automatically

## Run in VS Code
1. Extract the ZIP file.
2. Open the extracted `fastapi_user_api` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Run these commands one at a time:

   ```bash
   python -m venv .venv
   ```

   Windows:
   ```bash
   .venv\\Scripts\\python -m pip install -r requirements.txt
   .venv\\Scripts\\python -m uvicorn main:app --reload
   ```

   If `python` is not recognized, try `py` in the first command and use `.venv\\Scripts\\python` for the rest.

5. Open `http://127.0.0.1:8000/docs` in your browser.

Keep the VS Code terminal running while testing.

## Test in Swagger
1. Open `POST /users` → **Try it out** and enter:
   ```json
   {
     "name": "Ravi Kumar",
     "email": "ravi@example.com",
     "age": 25,
     "city": "Coimbatore",
     "is_active": true
   }
   ```
2. Click **Execute**. A successful response should be `201`.
3. Create a second user with another email.
4. Test `GET /users`, `GET /users/1`, `PUT /users/1`, and `DELETE /users/1`.
5. Test errors:
   - Create another user with `ravi@example.com` → `409 Email already exists`
   - Request `/users/99999` → `404 User not found`
   - Set age to `15` or use an invalid email → `422` validation error
6. Test filters with `GET /users?city=Coimbatore` and `GET /users?is_active=true`.

## Database
SQLite creates `users.db` in the project folder automatically when the application starts. It contains a `users` table.

## Project files
- `main.py`: API endpoints and HTTP error responses
- `database.py`: SQLite connection and database sessions
- `models.py`: SQLAlchemy table definition
- `schemas.py`: request/response validation
- `crud.py`: database create/read/update/delete operations
- `requirements.txt`: Python packages
