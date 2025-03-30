# ExpenseTracker

Simple backend expense tracker (personal experiment)

## Contributing

### Configure environment variables

In order to run properly and run safe, the code needs multiple environment variables.

A `.env` file must be created at the root of the project to load secrets to memory.

Here is an exhaustive list of variables that must be defined:

- DB_HOST (db, docker-compose container name)
- DB_PORT (often 5432 for postgres)
- DB_USER
- DB_PASSWORD
- DB_NAME: expense_db

These environment variables are used:

- to define alembic `sqlalchemy.url` privately
- to define sql engine in `app.core.database`: `engine = create_engine(DATABASE_URL)`

> [!CAUTION]
> Do not version your `.env` file.

## Common Debug

### Check that your host machine has access to the api hosted in a container

Outside Docker (on your host machine): The correct way to access the service is:

- `http://localhost:8000`
- `http://127.0.0.1:8000`

```shell
curl -v http://localhost:8000/docs
```

### Check that your container has access to the the api hosted locally

Inside Docker: FastAPI binds to `0.0.0.0`, allowing access from anywhere inside the container.

```shell
docker exec -it fastapi_expense_backend sh
```

then in the opened container shell:

```shell
curl -v http://0.0.0.0:8000/docs
```

### Check that alembic is up

```shell
docker exec -it fastapi_expense_backend alembic current
```
