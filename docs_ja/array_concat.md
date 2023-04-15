# ARRAY_CONCAT(arr1, arr2)

## 機能

`arr1`と`arr2`を連結したJSON配列を返却する。

- arr1 : JSON配列
- arr2 : JSON配列

## 使用例

### 単純な要素での一般的な利用

```SQL
SELECT ARRAY_CONCAT('["foo1", 2, null]', '["foo2", false, -1.1]') AS `result`;
```

| `result` |
|:--|
| `'["foo1", 2, null, "foo2", false, -1.1]'` |

### 複雑な要素での一般的な利用

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

### 第1引数が不定の場合

```SQL
SELECT ARRAY_CONCAT(NULL, '["foo2", false, -1.1]') AS `result`;
```

| `result` |
|:--|
| `NULL` |

### 第2引数が不定の場合

```SQL
SELECT ARRAY_CONCAT('["foo1", 2, null]', NULL) AS `result`;
```

| `result` |
|:--|
| `NULL` |

### すべての引数が不定の場合

```SQL
SELECT ARRAY_CONCAT(NULL, NULL) AS `result`;
```

| `result` |
|:--|
| `NULL` |
