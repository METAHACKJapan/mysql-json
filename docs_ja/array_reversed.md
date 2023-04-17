# ARRAY_REVERSE(arr)

## 機能

逆順の要素で構成したJSON配列を得る。

- arr : JSON配列
  
## 使用法

### 単純な要素での使い方

```SQL
SELECT ARRAY_REVERSE('["a", 2, true, false, 3]');
```

| `result` |
|:--|
| `'[3, false, true, 2, "a"]'` |
