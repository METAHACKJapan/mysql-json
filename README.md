# mysql-json

This project includes stored functions for MySQL 8.x below:

- [STR_SPLIT_TO_JSON_ARRAY(source_chars TEXT, separator_chars TEXT)](/docs_en/str_split_to_json_array.md)
  - String may be splitted into JSON array by separator.
- [ARRAY_JOIN(arr JSON, separator_chars TEXT)](/docs_en/array_join.md)
  - JSON array may be concatenated into string by separator.
- [ARRAY_SLICE(arr JSON, start_index INT, end_index, INT, step INT)](/docs_en/array_slice.md)
  - JSON array may be sliced into JSON array as subset.
- [ARRAY_CONCAT(arr1 JSON, arr2 JSON)](/docs_en/array_concat.md)
  - Concatenate 2 arrays into the new array.
- [ARRAY_UNIQUE(arr JSON)](/docs_en/array_unique.md)
  - Unique and Sort array into the new array.
- [ARRAY_FLATTEN(arr JSON)](/docs_en/array_flatten.md)
  - Flatten first child elements of each element on `arr` as JSON array, not recursively.

Documents in other languages below:

- [Japanese](README_ja.md)

## How to install

Each functions must be installed in one schema. We think about 2 use cases.

### 1. Install on the Independent Schema

This use case maybe applicable:

- Your MySQL 8.x instance has many schemas.
- Query for almost all schemas needs JSON utility functions incl. this package.

Where schema to be installed these stored functions should be the independent special schema.

#### Installation on One Schema

```SQL
DROP SCHEMA IF EXISTS `json_util`;
CREATE SCHEMA `json_util`;
USE `json_util`;
SOURCE array_concat.sql;
SOURCE array_join.sql;
...
```

#### Usage example on Any Schema

```SQL
USE `some_schema`;
SELECT
    `json_util`.ARRAY_JOIN(...),
    ...
  FROM ...
```

### 2. Install on your project schema

This use case maybe applicable:

- Your project that needs these functions relies on one schema.
- Your projects use each schema but each project needs varies functions set or version.

Probably this way is easy to manage, thus is suitable for the 1st step.

#### Installation on the project Schema

```SQL
USE `target_schema`;
SOURCE array_concat.sql;
SOURCE array_join.sql;
...
```

#### Usage example on the project Schema

```SQL
USE `target_schema`;
SELECT
    `json_util`.ARRAY_JOIN(...),
    ...
  FROM ...
```
