-- [begin] JSON array slice into new JSON array.
DROP FUNCTION IF EXISTS ARRAY_SLICE;
DELIMITER $$
CREATE FUNCTION ARRAY_SLICE (
  arr JSON,
  start_index INT,
  end_index INT,
  step INT
) RETURNS JSON
  COMMENT '`ARRAY_SLICE` function returns sliced subset of the `arr`.'
  LANGUAGE SQL
  DETERMINISTIC
  NO SQL
  BEGIN
    DECLARE ret JSON DEFAULT JSON_ARRAY();

    IF (
      arr IS NULL
      OR JSON_TYPE(arr) <> 'ARRAY'
      OR start_index < 0
    ) THEN
      SET ret = NULL;
    ELSE
      SET start_index = COALESCE(start_index, 0);
      SET end_index = COALESCE(end_index, JSON_LENGTH(arr));
      SET step = COALESCE(step, 1);
      SELECT
          JSON_ARRAYAGG(`S`.`val`)
          INTO ret
        FROM (
          SELECT
              ROW_NUMBER() OVER () - 1 AS `idx`,
              `val`
            FROM JSON_TABLE(arr, '$[*]' COLUMNS(`val` JSON PATH '$')) AS `T`
        ) AS `S`
        WHERE
          `S`.`idx` >= start_index
          AND `S`.`idx` < end_index
          AND MOD(`S`.`idx` - start_index, step) = 0
      ;
    END IF;
    RETURN ret;
  END
$$
DELIMITER ;
-- [end] JSON array slice into new JSON array.