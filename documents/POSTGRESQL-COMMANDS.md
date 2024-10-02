# Postgresql Commands

- These are some of the basic Postgresql commands, just to get started.

To see all databases

```
$ psql postgres
```

List all databases:

```
# \l
```

Connect to database:

```
# \c <database_name>
```

Show tables:

```
# \dt
```

More information of tables:

```
# \dt+
```

Quit:

```
#\q
```

Delete Database:

```
# DROP DATABASE <database name>;
```

Delete User Role:

```
# DROP DROP role <database username>;
```

Connect Issue:

If you get the below and restarting the postgres does not work, do the following:

error:
```
psql: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: No such file or directory
	Is the server running locally and accepting connections on that socket?
```

Solution option:

In a sperate tab, run:

```
$ /usr/local/opt/postgresql/bin/postgres -D /usr/local/var/postgres
```

You will not be able to access your database
