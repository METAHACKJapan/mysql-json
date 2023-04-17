-- [begin] Array sort asc.
DROP FUNCTION IF EXISTS ARRAY_SORT;
DELIMITER $$
CREATE FUNCTION ARRAY_SORT (
  arr JSON
) RETURNS JSON
  COMMENT '`ARRAY_SORT` function returns new Array ascendantly sorted.'
  LANGUAGE SQL
  DETERMINISTIC
  NO SQL
  BEGIN
    DECLARE ret JSON;

    IF JSON_TYPE(arr) = 'ARRAY' THEN
      BEGIN
        SELECT
            JSON_ARRAYAGG(`val`)
          INTO ret
          FROM (
            SELECT
                `val`
              FROM (
                SELECT
                    RANK() OVER (
                    ORDER BY `val` ASC
                    ) AS `rnk`,
                    `val`
                  FROM JSON_TABLE(arr, '$[*]' COLUMNS(
                    `val` JSON PATH '$'
                )) AS `T`
              ) AS `O`
              ORDER BY `rnk` ASC
          ) AS `S`
        ;
        SET ret = COALESCE(ret, JSON_ARRAY());
      END;
    ELSE
      SET ret = NULL;
    END IF;
    RETURN ret;
  END;
$$
DELIMITER ;
-- [end] Array sort asc.
