# Requirements for the test

This set of tests requires below:

- You must prepare `/dsn.json` file to determine target MySQL schema.
  - Template for this file is provided as `/dsn_template.json`.
- You must prepare MySQL instance prepared as:
  - Test user to be set on the `/dsn.json` file must have privileges below:
    - `CREATE ROUTINE`
    - `DROP`
    - `ALTER ROUTINE`
    - `SELECT`
    - **`SUPER` privilege is not recommended.**
  - Global variable `log_bin_trust_function_creators` must be set as `'ON'`.
    - USE `my.cnf` or `SET PERSIST` syntax.
  - `mysql` command
    - Set `PATH` environment too.
