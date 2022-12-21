# STR_SPLIT_TO_JSON_ARRAY

## Features

This function returns JSON Array which elements are splitted by the separator.

- source_chars : TEXT or NULL
  - TEXT must be JSON Array or JSON Object.
  - If `NULL` is set, always returns `'null'`.
- separator_chars : TEXT or NULL
  - If `NULL` is set, use default as `','`.

**This function's name is unstable because of less of my naming skill.**

## Examples

### Regular use (omit separator parameter)

```SQL
SELECT STR_SPLIT_TO_JSON_ARRAY('foo1,2,null,foo2,false,-1.1', NULL) AS `result`;
```

| `result` |
|:--|
| `'["foo1", "2", "null", "foo2", "false", "-1.1"]'` |

### Regular use

```SQL
SELECT STR_SPLIT_TO_JSON_ARRAY('foo1, 2, null, foo2, false, -1.1', ', ') AS `result`;
```

| `result` |
|:--|
| `'["foo1", "2", "null", "foo2", "false", "-1.1"]'` |

### Combination use with `GROUP_CONCAT` builtin function

```SQL
WITH
  `CTE` AS ( /* This CTE is simulation of any entities. */
    SELECT
        `val`
      FROM JSON_TABLE('["c,a", "c", "b", "a", "c"]', '$[*]' COLUMNS (
        `val` TEXT PATH '$'
      )) AS `T`
  )
SELECT
    STR_SPLIT_TO_JSON_ARRAY(
      GROUP_CONCAT(DISTINCT `val` ORDER BY `val` ASC SEPARATOR '|'),
      '|'
    ) AS `result`
  FROM `CTE`
;
```

| `result` |
|:--|
| `'["a", "b", "c", "c,a"]'` |
