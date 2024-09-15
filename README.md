# CuraPulse REST API

CuraPulse is a hospital management system that has been enhanced to work with Django REST Framework. This project provides a scalable and efficient RESTful API for managing hospital-related data.

## Features

- User Management
- Appointments scheduling
- Authentication using Django's built-in system
- RESTful APIs for all functionalities
- Token-based authentication 
- Swagger UI

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/okusjid/CuraPulse.git
    cd CuraPulse
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables (recommended):

    ```bash
    cp .env.example .env
    ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

## API Endpoints

| Method | Endpoint             | Description                   |
|--------|----------------------|-------------------------------|
| GET    | /api/appointments/    | List all appointments         |
| POST   | /api/appointments/    | Schedule a new appointment    |

## Authentication

CuraPulse uses Django's default authentication system. API users can authenticate using token-based authentication by obtaining tokens with the following endpoint:

```bash
POST /api-token-auth/
```
