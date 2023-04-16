-- [begin] Array consists only Unique members.
DROP FUNCTION IF EXISTS ARRAY_UNIQUE;
DELIMITER $$
CREATE FUNCTION ARRAY_UNIQUE (
  arr JSON
) RETURNS JSON
  COMMENT '`ARRAY_UNIQUE` function returns new Array consists of unique members.'
  LANGUAGE SQL
  DETERMINISTIC
  NO SQL
  BEGIN
    DECLARE ret JSON;

    IF JSON_TYPE(arr) = 'ARRAY' THEN
      WITH
        `CTE_SRC` AS (
          SELECT DISTINCT
              `val`
            FROM JSON_TABLE(arr, '$[*]' COLUMNS(
              `val` JSON PATH '$'
            )) AS `T`
            ORDER BY `val` ASC
        )
      SELECT
          COALESCE(JSON_ARRAYAGG(`val`), '[]')
        INTO ret
        FROM `CTE_SRC`
      ;
    ELSE
      SET ret = NULL;
    END IF;
    RETURN ret;
  END;
$$
DELIMITER ;
-- [end] Array consists only Unique members.
