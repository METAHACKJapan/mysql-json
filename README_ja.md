# mysql-json

このプロジェクトは、MySQL 8.ｘで不十分と思われる以下のようなJSON関連関数を追加するもの。

- [STR_SPLIT_TO_JSON_ARRAY(source_chars TEXT, separator_chars TEXT)](/docs_ja/str_split_to_json_array.md)
  - 文字列（`source_chars`）を分割文字列（`separator_chars`）によって刻んだJSON配列に変換する
- [ARRAY_JOIN(arr JSON, separator_chars TEXT)](/docs_ja/array_join.md)
  - JSON配列を指定文字列で連結した文字列に変換する
- [ARRAY_SLICE(arr JSON, start_index INT, end_index, INT, step INT)](/docs_ja/array_slice.md)
  - JSON配列から新たな部分配列を得る
- [ARRAY_CONCAT(arr1 JSON, arr2 JSON)](/docs_ja/array_concat.md)
  - 2つのJSON配列を連結した新たなJSON配列を得る
- [ARRAY_UNIQUE(arr JSON)](/docs_ja/array_unique.md)
  - JSON配列の要素から重複を除去したソート済みの新たなJSON配列を得る

## インストール方法

これらの関数は、単一のスキーマにインストールしなければいけません。その方法には以下の2つのユースケースが考えられます。各関数の定義者（DEFINER）が関数の実行ユーザーであり、既定でDEFINERはインストールを実行したユーザーとなることに注意してください。

### 1. 専用の独立したスキーマにインストールする方法

以下のような場合に選択するとよいでしょう。

- あなたのMySQL 8.ｘインスタンスに複数のスキーマが存在している
- ほぼすべてのスキーマを対象としたクエリで、これらの関数を利用したい

このような場合には、独立した専用のスキーマにインストールするのがよいでしょう。

#### 1.a. インストール方法

```SQL
DROP SCHEMA IF EXISTS `json_util`;
CREATE SCHEMA `json_util`;
USE `json_util`;
SOURCE array_concat.sql;
SOURCE array_join.sql;
...
```

#### 1.b. 使い方

```SQL
USE `some_schema`;
SELECT
    `json_util`.ARRAY_JOIN(...),
    ...
  FROM ...
```

### 2. プロジェクト個別のスキーマにインストールする方法

以下のような場合に選択するとよいでしょう。

- 1つのスキーマを使うプロジェクトで、これらの関数を必要としている
- 複数のプロジェクトがそれぞれのスキーマを使っており、各プロジェクトで異なる関数セットやバージョンを使用する可能性がある

おおむね、こちらのインストール方法は権限の管理が楽なので、使い始めるコストは低いでしょう。

#### 2.a. インストール方法

```SQL
USE `target_schema`;
SOURCE array_concat.sql;
SOURCE array_join.sql;
...
```

#### 2.b. 使い方

```SQL
USE `target_schema`;
SELECT
    ARRAY_JOIN(...),
    ...
  FROM ...
```
