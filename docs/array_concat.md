# ARRAY_CONCAT

## Features

This function returns JSON Array consists of all elements of `arr1` and `arr2`.

- arr1 : JSON Array
- arr2 : JSON Array

## Examples

### Regular use for simple elements

```SQL
SELECT ARRAY_CONCAT('["foo1", 2, null]', '["foo2", false, -1.1]') AS `result`;
```

| `result` |
|:--|
| `'["foo1", 2, null, "foo2", false, -1.1]'` |

### Regular use for complexed elements

```SQL
SELECT
  ARRAY_CONCAT(
    '[
      "foo1",
      [
        2,
        null
      ]
    ]',
    '[
      {
        "foo2":false
      }
    ]'
  ) AS `result`;
```

| `result` |
|:--|
| `'["foo1", [2, null], {"foo2":false}]'` |

### Parameter 1 is `NULL`

```SQL
SELECT ARRAY_CONCAT(NULL, '["foo2", false, -1.1]') AS `result`;
```

| `result` |
|:--|
| `NULL` |

### Parameter 2 is `NULL`

```SQL
SELECT ARRAY_CONCAT('["foo1", 2, null]', NULL) AS `result`;
```

| `result` |
|:--|
| `NULL` |

### All parameters are `NULL`

```SQL
SELECT ARRAY_CONCAT(NULL, NULL) AS `result`;
```

| `result` |
|:--|
| `NULL` |
