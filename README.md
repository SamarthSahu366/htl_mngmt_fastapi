
## Project Overview

- Tech Stack: 
  - FastAPI
  - PostgreSQL
  - Alembic
  - JWT (JSON Web Tokens) for Authentication

- Database: 
  - The project uses a PostgreSQL database.
  - It contains three main tables:
    - Users: Stores user details (e.g., email, password, admin status).
    - Rooms: Stores information about rooms (e.g., room ID, location, price, status).
    - Bookings: Stores booking information (e.g., user email, payment status, check-out date).

- API Endpoints: 
  - GET, POST, DELETE, PUT routes for interacting with the database.
  - Routes are protected using JWT tokens to ensure that only authenticated users can access certain endpoints.
  - Some routes (like adding, updating, or deleting rooms) are protected and accessible only by admin users.
  
- Authentication: 
  - JWT tokens are used to authenticate users.
  - Tokens are passed in the headers of requests for protection of routes.
  - The `verify_token` function checks the validity of tokens and identifies the user.

- Database Management: 
  - Alembic is used for database migrations to manage schema changes.
  - You can use Alembic to upgrade or downgrade the database schema.

- Folder Structure: 
  - The project follows a well-organized folder structure for easy maintainability.
    - models: Contains the database models (User, Room, Booking).
    - schemas: Contains Pydantic models for data validation.
    - routes: Contains the API route logic (e.g., user-related, room-related, etc.).
    - db: Contains the database connection and utility functions like getting the session.
    - dependencies: Contains helper functions like token verification.

- Environment:
  - The project uses a .env file to store sensitive information like database URL and JWT secret key.
  - Ensure to add your PostgreSQL database URI and secret key in the .env file.

- How to Run: 
  - Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
  - Set up your database (PostgreSQL).
  - Run Alembic migrations to create the database schema:
    ```bash
    alembic upgrade head
    ```
  - Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
