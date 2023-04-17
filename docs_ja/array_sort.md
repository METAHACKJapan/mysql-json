# ARRAY_SORT(arr)

## 機能

要素を昇順に並び替えたJSON配列を返却する。

- arr : JSON Array
  
## 使用法

### 単純な要素での使い方

```SQL
SELECT ARRAY_SORT('["b", "a", null, true, 3, false, 1, null]');
```

| `result` |
|:--|
| `'[null, null, 1, 3, "a", "b", false, true]'` |
