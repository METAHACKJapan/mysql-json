# ARRAY_JOIN(arr, separator_chars)

## 機能

JSON配列を与えると、連結文字列によってその各要素が接続された文字列をTEXT型で返却する。

- arr : JSON配列
- separator_chars : TEXT型 もしくは 不定
  - もし`NULL`が指定された場合は、既定として`','`が採用される

## 使用例

### 単純な要素での利用法（第2引数がNULL）

```SQL
SELECT ARRAY_JOIN('["foo1", 2, null]', NULL) AS `result`;
```

| `result` |
|:--|
| `'foo1,2,null'` |

### 単純な要素での利用法

```SQL
SELECT ARRAY_JOIN('["foo1", 2, null]', '|') AS `result`;
```

| `result` |
|:--|
| `'foo1|2|null'` |

### 複雑な要素での利用法

This function doesn't parses elements recursively.

```SQL
SELECT ARRAY_JOIN('[false, true, null, ["foo1", "foo2"]]', NULL) AS `result`;
```

| `result` |
|:--|
| `'false,true,null,["foo1", "foo2"]'` |
