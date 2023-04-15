# ARRAY_SLICE(arr, start_index, end_index, step)

## Features

This function returns JSON Array sliced from source JSON Array.

- arr : JSON Array
- start_index : INT UNSIGNED or `NULL`
  - If `NULL` is set, use `0` as default.
- end_index : INT UNSIGNED or `NULL`
  - If `NULL` is set, use length of `arr`.
- step : INT UNSIGNED or `NULL`
  - If `NULL` is set, use `1` as default.

Also `JSON_EXTRACT` builtin function or `->` / `->>` operators supports `[1..3]` notation, but not supports Python-like slice notation like `[3:2:3]`.

## Examples

### Regular use for simple elements(1)

```SQL
SELECT ARRAY_SLICE('[0, 1, 2, 3, 4, 5, 6]', NULL, NULL, 3);
```

| `result` |
|:--|
| `'[0, 3, 6]'` |

### Regular use for simple elements(2)

```SQL
SELECT ARRAY_SLICE('[0, 1, 2, 3, 4, 5, 6]', 3, NULL, 2);
```

| `result` |
|:--|
| `'[3, 5]'` |

### Regular use for simple elements(3)

```SQL
SELECT ARRAY_SLICE('[0, 1, 2, 3, 4, 5, 6]', 0, 4, 2);
```

| `result` |
|:--|
| `'[0, 2]'` |

