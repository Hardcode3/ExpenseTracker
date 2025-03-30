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
