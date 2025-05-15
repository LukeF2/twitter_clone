# Twitter Clone

[![Tests](https://github.com/LukeF2/twitter_clone/actions/workflows/test.yml/badge.svg)](https://github.com/LukeF2/twitter_clone/actions/workflows/test.yml)

A full-stack Twitter clone built with Flask and PostgreSQL, featuring real-time updates, full-text search, and like functionality.

## Features

- User authentication (signup, login, logout)
- Tweet creation and viewing
- Like/unlike tweets
- Full-text search with relevance ranking
- Pagination for tweets
- Real-time updates
- Responsive design

## Prerequisites

- Docker
- Docker Compose
- Git

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd twitter_clone
```

2. Create a `.env.dev` file in the root directory:
```bash
echo "DATABASE=postgres" > .env.dev
echo "SQL_HOST=db" >> .env.dev
echo "SQL_PORT=5432" >> .env.dev
echo "FLASK_DEBUG=1" >> .env.dev
echo "POSTGRES_USER=hello_flask" >> .env.dev
echo "POSTGRES_PASSWORD=hello_flask" >> .env.dev
echo "POSTGRES_DB=hello_flask_dev" >> .env.dev
```

3. Build and start the containers:
```bash
docker compose up -d --build
```

4. The application will be available at:
   - Web interface: http://localhost:1147

## Connecting to the Web Server

### Local Access
If you're running the application locally, you can access it at:
- http://localhost:1147
-  
## Database

The application uses PostgreSQL with the following features:
- Full-text search using RUM indexes
- Efficient querying with proper indexing
- Data generation scripts for testing

### Database Connection
- Host: localhost (or server IP)
- Port: 5432
- Database: hello_flask_dev
- Username: hello_flask
- Password: hello_flask

## Development

### Running Tests
The application includes automated tests that can be run using GitHub Actions or locally:

```bash
# Run tests locally
docker compose exec web pytest
```

### Data Generation
The application includes scripts for generating test data:
- `generate_data.sql`: Generates a large dataset for production
- `generate_test_data.sql`: Generates a small dataset (100 rows) for testing

