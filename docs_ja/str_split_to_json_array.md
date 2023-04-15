# STR_SPLIT_TO_JSON_ARRAY(source_chars, separator_chars)

## 機能

文字列の入力から、指定文字列で分割された文字列要素で構成されるJSON配列を返却する。

- source_chars : TEXT型 もしくは 不定
  - `NULL`が指定された場合、常に`'null'`を返却する。
- separator_chars : TEXT型 もしくは 不定
  - `NULL`が指定された場合、既定で`','`が採用される。

**この関数名は作者のネーミングセンスのなさから、変更の可能性がある。**

## 使用例

### 分割文字列を既定にした一般的な使い方

```SQL
SELECT STR_SPLIT_TO_JSON_ARRAY('foo1,2,null,foo2,false,-1.1', NULL) AS `result`;
```

| `result` |
|:--|
| `'["foo1", "2", "null", "foo2", "false", "-1.1"]'` |

### 一般的な使い方

```SQL
SELECT STR_SPLIT_TO_JSON_ARRAY('foo1, 2, null, foo2, false, -1.1', ', ') AS `result`;
```

| `result` |
|:--|
| `'["foo1", "2", "null", "foo2", "false", "-1.1"]'` |

### `GROUP_CONCAT`組み込み関数と併用した使い方

`JSON_ARRAYAGG`関数とは違い、`GROUP_CONCAT`関数が`DISTINCT`指定や`ORDER BY`指定可能であることを利用したクエリの例。

```SQL
WITH
  `CTE` AS ( /* このCTE部がどこかのテーブルをSELECTしてきた体のもの */
    SELECT
        `val`
      FROM JSON_TABLE('["c,a", "c", "b", "a", "c"]', '$[*]' COLUMNS (
        `val` TEXT PATH '$'
      )) AS `T`
  )
SELECT
    STR_SPLIT_TO_JSON_ARRAY(
      GROUP_CONCAT(DISTINCT `val` ORDER BY `val` ASC SEPARATOR '|'),
      '|'
    ) AS `result`
  FROM `CTE`
;
```

| `result` |
|:--|
| `'["a", "b", "c", "c,a"]'` |
