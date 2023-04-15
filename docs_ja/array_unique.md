# ARRAY_UNIQUE(arr)

## 使い方

`arr`引数に指定されたJSON配列から、要素が一意でソートされた新しい配列を返却する。

- arr : JSON配列

## 使用例

### 異なる型の要素での使用例

```SQL
SELECT ARRAY_UNIQUE('["foo1", 2, null, null, 2]') AS `result`;
```

| `result` |
|:--|
| `[null, 2, "foo1"]` |

### 単純な要素での使用例(文字列)

```SQL
SELECT ARRAY_UNIQUE('["foo10", "foo1", "foo0", "foo5"]') AS `result`;
```

| `result` |
|:--|
| `["foo0", "foo1", "foo10", "foo5"]` |

### 単純な要素での使用例(数値)

```SQL
SELECT ARRAY_UNIQUE('[1.5, -2, 3.14, 2.72]') AS `result`;
```

| `result` |
|:--|
| `[-2, 1.5, 2.72, 3.14]` |
