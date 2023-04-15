# ARRAY_UNIQUE(arr)

## Features

This function returns JSON Array consists of all unique sorted elements of `arr`.

- arr : JSON Array

## Examples

### Regular use for elements has different types

```SQL
SELECT ARRAY_UNIQUE('["foo1", 2, null, null, 2]') AS `result`;
```

| `result` |
|:--|
| `[null, 2, "foo1"]` |

### Regular use for simple elements(String)

```SQL
SELECT ARRAY_UNIQUE('["foo10", "foo1", "foo0", "foo5"]') AS `result`;
```

| `result` |
|:--|
| `["foo0", "foo1", "foo10", "foo5"]` |

### Regular use for simple elements(Number)

```SQL
SELECT ARRAY_UNIQUE('[1.5, -2, 3.14, 2.72]') AS `result`;
```

| `result` |
|:--|
| `[-2, 1.5, 2.72, 3.14]` |
