# ARRAY_SORT(arr)

## Features

This function returns JSON array sorted in ascending order.

- arr : JSON Array
  
## Examples

### Regular use for simple elements

```SQL
SELECT ARRAY_SORT('["b", "a", null, true, 3, false, 1, null]');
```

| `result` |
|:--|
| `'[null, null, 1, 3, "a", "b", false, true]'` |
