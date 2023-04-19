# ARRAY_SORT(arr)

## 機能

要素を昇順に並び替えたJSON配列を返却する。

- arr : JSON Array
  
## 使用例

### 単純な要素での使い方

```SQL
SELECT ARRAY_SORT('["b", "a", null, true, 3, false, 1, null]');
```

| `result` |
|:--|
| `'[null, null, 1, 3, "a", "b", false, true]'` |

### `JSON_ARRAYAGG`組み込み関数と組み合わせの使い方

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
