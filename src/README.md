# Windows

To restore postgres db from sql dump file: 
Ender psql terminal.
```sh
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
\i [path-to-dump]
```

Needs `postgres` user and `postgres` db to work.

Set env variable: `$env:POSTGRES_PASS="[actual password]`