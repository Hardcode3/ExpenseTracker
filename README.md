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

### Migrating changes made to the database

#### Important notes about containers

If your Alembic setup is running inside a container (e.g., a Docker container), you can still check the Alembic state by executing commands inside the container:

```shell
docker exec -it fastapi_expense_backend sh
```

> [!CAUTION]
> Trying to execute alembic from the host machine instead of inside the container will result in an error:
> `sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not translate host name "db" to address: Name or service not known`
>
> This error is due to the fact that db is the name of the docker-compose service and also the host name.
> What would work is: "localhost" instead of "db", however the backend container would not be able to connect to the database url.


#### Generate a migration script

After making changes to your database models (schemas), you need to generate a migration script.

```shell
alembic revision --autogenerate -m "Changed expense to transaction table name"

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected removed index 'ix_transactions_id' on 'transactions'
INFO  [alembic.autogenerate.compare] Detected removed table 'transactions'
INFO  [alembic.ddl.postgresql] Detected sequence named 'expenses_id_seq' as owned by integer column 'expenses(id)', assuming SERIAL and omitting
INFO  [alembic.autogenerate.compare] Detected removed index 'ix_expenses_description' on 'expenses'
INFO  [alembic.autogenerate.compare] Detected removed index 'ix_expenses_id' on 'expenses'
INFO  [alembic.autogenerate.compare] Detected removed table 'expenses'
  Generating /app/alembic/versions/08290ef9350a_changed_expense_to_transaction_table_.py ...  done
```

- The --autogenerate flag will automatically compare your models with the current database schema and generate the necessary migration.
- The `-m` flag allows you to provide a message describing the migration (e.g., "Changed expense to transaction table name").

Alembic will generate a migration script in the `alembic/versions/` folder. Review the generated script to ensure it properly represents your intended changes.

For example, if you added a new field to your Transaction model, you should see something like this in the migration script:

```python
def upgrade():
    op.add_column('transactions', sa.Column('new_field', sa.String(), nullable=True))

def downgrade():
    op.drop_column('transactions', 'new_field')

```

#### Apply the migration script to the database

To apply the migration to your database, run the following command:

```shell
alembic upgrade head

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 65dd6b98e39b -> 08290ef9350a, Changed expense to transaction table name
```

After running the migration, you can verify the changes in your database by inspecting the tables or running queries.

#### Rollback if needed

Rollback the migration: If something goes wrong, you can downgrade to a previous revision:

```shell
alembic downgrade -1  # Go back 1 revision
```

#### Check the current version of the database schema

Check the current version: To see the current state of the database schema:

```shell
alembic current

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
08290ef9350a (head)
```
