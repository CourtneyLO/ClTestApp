# Database Setup Locally

**Install postgresql** (if you don't have it already):

```
$ make install-postgresql
```

**Start postgresql**:

```
$ make start-db
```

**Restart postgresql**:

```
$ make restart-db
```

**Create a database user**:

```
$ make db-user
```

- Add password created in this step to the .env file (use the .example.env file for assistance).

**Create a database with that user**:

```
$ make db
```

**Access the db**:

```
$ make access-db
```

- Password is the one used when creating the user

- There should be no tables as you have not yet run the migrate (this is the next step)

**Stop postgresql**:

```
$ make stop-db
```

If you need assistance with some of the basic Postgresql commands see [here](./POSTGRESQL-COMMANDS.md)
