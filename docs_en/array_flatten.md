# ARRAY_FLATTEN(arr)

## Features

This function returns hierarchical JSON array into flatten JSON array.

- arr : JSON Array
  
**This function does NOT flatten recursively.**

## Examples

### Regular use for simple elements

```SQL
SELECT ARRAY_FLATTEN('[[1, 2, 3], ["a", "b", "c"], [true, false, null]]');
```

| `result` |
|:--|
| `'[1, 2, 3, "a", "b", "c", true, false, null]'` |

### Regular use for complexed elements

```SQL
SELECT ARRAY_FLATTEN('[[1, {"a": 1, "b": 2}, 3], [4, 5, 6]]');
```

| `result` |
|:--|
| `'[1, {"a": 1, "b": 2}, 3, 4, 5, 6]'` |

### Combination with `JSON_ARRAYAGG` builtin function

```SQL
WITH
  `CTE` AS (
    SELECT
        "odd" AS `grp`,
        "a" AS `col_1`,
        1 AS `col_2`
    UNION ALL
    SELECT
        "even" AS `grp`,
        "b" AS `col_1`,
        2 AS `col_2`
    UNION ALL
    SELECT
        "odd" AS `grp`,
        "c" AS `col_1`,
        3 AS `col_2`
  )
SELECT
    `grp`,
    JSON_ARRAYAGG(JSON_ARRAY(`col_1`, `col_2`)) AS `aggregated`,
    ARRAY_FLATTEN(JSON_ARRAYAGG(JSON_ARRAY(`col_1`, `col_2`))) AS `flatten`
  FROM `CTE`
  GROUP BY `grp`
;
```

| `grp` | `aggregated` | `flatten` |
|:--|:--|:--|
| `'even'` | `'[["b", 2]]'` | `'["b", 2]'` |
| `'odd'` | `'[["a", 1], ["c", 3]]'` | `'["a", 1, "c", 3]'` |
