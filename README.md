# CuraPulse REST API

CuraPulse is a hospital management system that has been enhanced to work with Django REST Framework. This project provides a scalable and efficient RESTful API for managing hospital-related data.

## Features

- User Management
- Appointment Scheduling
- Authentication using Django's built-in system
- RESTful APIs for all functionalities
- Token-based Authentication (JWT)
- Swagger UI Documentation

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

### Authentication

CuraPulse uses JWT (JSON Web Token) for token-based authentication. Users can authenticate by obtaining tokens with the following endpoint:

- **Obtain Token:**  
    `POST /auth/token/`  
    Use this endpoint to obtain a new JWT token.

- **Refresh Token:**  
    `POST /auth/token/refresh/`  
    Use this endpoint to refresh an expired JWT token.

- **Verify Token:**  
    `POST /auth/token/verify/`  
    Use this endpoint to verify the validity of a JWT token.

### User Management

| Method | Endpoint             | Description               |
|--------|----------------------|---------------------------|
| POST   | /profile/register/    | Register a new user        |
| GET    | /profile/             | Retrieve user profile      |

### Appointments

| Method | Endpoint                       | Description                   |
|--------|--------------------------------|-------------------------------|
| GET    | /appointments/list/            | List all appointments         |
| POST   | /appointments/list/            | Schedule a new appointment    |
| GET    | /appointments/\<int:id\>/      | Retrieve appointment details  |
| GET    | /appointments/count/           | Get total appointment count   |

## Swagger Documentation

CuraPulse provides Swagger-based documentation to explore and test the API. The documentation can be accessed at:

- **Swagger UI:** `/swagger/`
- **ReDoc UI (Optional):** `/redoc/`

## Running in Debug Mode

To enable debugging during development, ensure that `DEBUG = True` is set in your Django `settings.py`. You can use Django Debug Toolbar for detailed error reporting.

```python
# settings.py

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```
