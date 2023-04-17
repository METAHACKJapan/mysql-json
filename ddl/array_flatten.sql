-- [begin] Flatten array from hierarchical array.
DROP FUNCTION IF EXISTS ARRAY_FLATTEN;
DELIMITER $$
CREATE FUNCTION ARRAY_FLATTEN (
  arr JSON
) RETURNS JSON
  COMMENT '`ARRAY_FLATTEN` function returns new Array consists of arrays.'
  LANGUAGE SQL
  DETERMINISTIC
  NO SQL
  BEGIN
    DECLARE cnt INT UNSIGNED;
    DECLARE ret JSON;
    
    SET cnt = 0;

    IF JSON_TYPE(arr) = 'ARRAY' THEN
      SET ret = JSON_ARRAY();
      dequeue: LOOP
        BEGIN
          IF cnt > JSON_LENGTH(arr) THEN
            LEAVE dequeue;
          END IF;
          SELECT
              JSON_ARRAYAGG(`val`)
            INTO ret
            FROM (
              SELECT
                  `val`
                FROM JSON_TABLE(ret, '$[*]' COLUMNS(
                  `val` JSON PATH '$'
                )) AS `T1`
              UNION ALL
              SELECT
                  `val`
                FROM JSON_TABLE(JSON_EXTRACT(arr, CONCAT('$[', cnt, ']')), '$[*]' COLUMNS(
                  `val` JSON PATH '$'
                )) AS `T2`
            ) AS `U`
          ;
          SET cnt = cnt + 1;
        END;
      END LOOP dequeue;
      SET ret = COALESCE(ret, JSON_ARRAY());
    ELSE
      SET ret = NULL;
    END IF;
    RETURN ret;
  END;
$$
DELIMITER ;
-- [end] Flatten array from hierarchical array.
