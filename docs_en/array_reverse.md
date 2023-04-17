# ARRAY_REVERSE(arr)

## Features

This function returns JSON array has reversed elements.

- arr : JSON Array
  
## Examples

### Regular use for simple elements

```SQL
SELECT ARRAY_REVERSE('["a", 2, true, false, 3]');
```

| `result` |
|:--|
| `'[3, false, true, 2, "a"]'` |
