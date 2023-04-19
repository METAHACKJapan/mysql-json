# ARRAY_SORT(arr)

## Features

This function returns JSON array sorted in ascending order.

- arr : JSON Array
  
## Examples

### Regular use for simple elements

```SQL
SELECT ARRAY_SORT('["b", "a", null, true, 3, false, 1, null]');
```

| `result` |
|:--|
| `'[null, null, 1, 3, "a", "b", false, true]'` |

### Combination with JSON_ARRAYAGG builtin function

```SQL
WITH
  `CTE` AS (
    SELECT
        CAST('3' AS JSON) AS `value_json`
    UNION ALL
    SELECT
        CAST('1' AS JSON) AS `value_json`
    UNION ALL
    SELECT
        CAST('"b"' AS JSON) AS `value_json`
    UNION ALL
    SELECT
        CAST('"F"' AS JSON) AS `value_json`
  )
SELECT
    JSON_TYPE(`value_json`) AS `type`,
    JSON_ARRAYAGG(`value_json`) AS `aggregated`,
    ARRAY_SORT(JSON_ARRAYAGG(`value_json`)) AS `sorted`
  FROM `CTE`
  GROUP BY `type`
;
```

| `type` | `aggregated` | `sorted` |
|:--|:--|:--|
| `'INTEGER'` | `'[3, 1]'` | `'[1, 3]'` |
| `'STRING'` | `'["b", "F"]'` | `'["F", "b"]'` |
