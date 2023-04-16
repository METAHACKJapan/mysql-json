-- [begin] Unite Arrays into new Array.
DROP FUNCTION IF EXISTS ARRAY_CONCAT;
DELIMITER $$
CREATE FUNCTION ARRAY_CONCAT (
  arr_1 JSON,
  arr_2 JSON
) RETURNS JSON
  COMMENT '`ARRAY_CONCAT` function unites two Arrays into one Array.'
  LANGUAGE SQL
  DETERMINISTIC
  NO SQL
  BEGIN
    DECLARE ret JSON DEFAULT NULL;

    IF JSON_TYPE(arr_1) = 'ARRAY'
      AND JSON_TYPE(arr_2) = 'ARRAY' THEN
      BEGIN
        IF JSON_LENGTH(arr_1) > 0
          OR JSON_LENGTH(arr_2) > 0 THEN
          SELECT
              JSON_ARRAYAGG(`S`.`val`)
              INTO ret
            FROM (
              SELECT
                  `T1`.`val`
                  FROM JSON_TABLE(arr_1, '$[*]' COLUMNS (`val` JSON PATH '$')) AS `T1`
              UNION ALL
              SELECT
                  `T2`.`val`
                  FROM JSON_TABLE(arr_2, '$[*]' COLUMNS (`val` JSON PATH '$')) AS `T2`
            ) AS `S`;
        ELSE
          SET ret = '[]';
        END IF;
      END;
    ELSE
      SET ret = NULL;
    END IF;
    RETURN ret;
  END;
$$
DELIMITER ;
-- [end] Unite Arrays into new Array.