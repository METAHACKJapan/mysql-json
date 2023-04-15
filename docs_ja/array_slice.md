# ARRAY_SLICE(arr, start_index, end_index, step)

## 機能

与えられたJSON配列から、パラメータに指定された部分集合を要素とする新たなJSON配列を返却する。

- arr : JSON配列
- start_index : 正整数 もしくは 不定
  - `NULL`が与えられた場合、既定で`0`を採用する
- end_index : 正整数 もしくは 不定
  - `NULL`が与えられた場合、元JSON配列の要素数を採用する
- step : 正整数 もしくは 不定
  - `NULL`が与えられた場合、既定で`1`を採用する

`JSON_EXTRACT`組み込み関数および`->`/`->>`演算子は、パス引数として`[1..3]`表記をサポートしているが、Python風の飛び数付きの表現である`[3:2:3]`をサポートしていないため、本関数の機能がスーパーセットとなる。

## 使用例

### 開始と終了を指定せずに飛び数のみ指定した例(1)

```SQL
SELECT ARRAY_SLICE('[0, 1, 2, 3, 4, 5, 6]', NULL, NULL, 3);
```

| `result` |
|:--|
| `'[0, 3, 6]'` |

### 終了を指定しない例(2)

```SQL
SELECT ARRAY_SLICE('[0, 1, 2, 3, 4, 5, 6]', 3, NULL, 2);
```

| `result` |
|:--|
| `'[3, 5]'` |

### すべてのパラメータを指定した例(3)

```SQL
SELECT ARRAY_SLICE('[0, 1, 2, 3, 4, 5, 6]', 0, 4, 2);
```

| `result` |
|:--|
| `'[0, 2]'` |