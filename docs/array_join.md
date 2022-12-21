# ARRAY_JOIN

## Features

This function returns TEXT each of array elements joined by the separator text.

- arr : JSON Array
- separator_chars : TEXT or NULL
  - If `NULL` is set, use default as `','`.

## Examples

### Regular use for simple elements (omit second parameter)

```SQL
SELECT ARRAY_JOIN('["foo1", 2, null]', NULL) AS `result`;
```

| `result` |
|:--|
| `'foo1,2,null'` |

### Regular use for simple elements

```SQL
SELECT ARRAY_JOIN('["foo1", 2, null]', '|') AS `result`;
```

| `result` |
|:--|
| `'foo1|2|null'` |

### Regular use for complexed elements (omit second parameter)

This function doesn't parses elements recursively.

```SQL
SELECT ARRAY_JOIN('[false, true, null, ["foo1", "foo2"]]', NULL) AS `result`;
```

| `result` |
|:--|
| `'false,true,null,["foo1", "foo2"]'` |
