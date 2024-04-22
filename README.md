# FastAPI Application with PostgreSQL

This repository contains a FastAPI application that demonstrates CRUD operations with a PostgreSQL database. It uses SQLAlchemy as the ORM for database interactions and psycopg2 for low-level database operations.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- CRUD operations for `Post` entities using FastAPI and SQLAlchemy.
- Data validation and serialization with Pydantic models.
- Integration with a PostgreSQL database.
- Dependency injection for managing database sessions.
- Error handling with appropriate HTTP responses.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database

## Installation

1. **Clone the repository**:

    ```shell
    git clone https://github.com/yourusername/fastapi-postgresql.git
    cd fastapi-postgresql
    ```

2. **Install dependencies**:

    ```shell
    pip install -r requirements.txt
    ```

3. **Set up PostgreSQL**:

    - Make sure you have a PostgreSQL database running locally.
    - Update the `SQLACHEMY_DATABASE_URL` in the script to match your PostgreSQL connection details.

## Usage

1. **Run the application**:

    ```shell
    uvicorn main:app --reload
    ```

2. **Access the application**:

    The application will be available at [http://localhost:8000/](http://localhost:8000/).

## Endpoints

- `GET /`: Root endpoint to check the application status.
- `GET /sqlalchemy`: Retrieve all posts from the database using SQLAlchemy.
- `GET /show_all_posts/`: Retrieve all posts from the database.
- `POST /posts/create`: Create a new post.
- `GET /posts/{post_id}`: Retrieve a specific post by ID.
- `DELETE /posts/delete/{post_id}`: Delete a post by ID.
- `PUT /posts/update/{id}`: Update a post by ID.

## Contributing

Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
