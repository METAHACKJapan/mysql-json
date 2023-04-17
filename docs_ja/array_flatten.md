# ARRAY_FLATTEN(arr)

## 機能

階層を持つJSON配列を平坦なJSON配列に変換する。

- arr : JSON配列
  
**再帰的な平坦化は行いません。**

## 使用例

### 単純な要素での使い方

```SQL
SELECT ARRAY_FLATTEN('[[1, 2, 3], ["a", "b", "c"], [true, false, null]]');
```

| `result` |
|:--|
| `'[1, 2, 3, "a", "b", "c", true, false, null]'` |

### スカラ値以外の要素を持つ配列での使い方

```SQL
SELECT ARRAY_FLATTEN('[[1, {"a": 1, "b": 2}, 3], [4, 5, 6]]');
```

| `result` |
|:--|
| `'[1, {"a": 1, "b": 2}, 3, 4, 5, 6]'` |

### `JSON_ARRAYAGG`組み込み関数と組み合わせる使い方

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
