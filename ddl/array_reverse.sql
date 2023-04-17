-- [begin] Array reversed.
DROP FUNCTION IF EXISTS ARRAY_REVERSE;
DELIMITER $$
CREATE FUNCTION ARRAY_REVERSE (
  arr JSON
) RETURNS JSON
  COMMENT '`ARRAY_REVERSE` function returns new Array has reversed elements.'
  LANGUAGE SQL
  DETERMINISTIC
  NO SQL
  BEGIN
    DECLARE ret JSON;
    DECLARE cnt INT;
    DECLARE len INT;

    IF JSON_TYPE(arr) = 'ARRAY' THEN
      BEGIN
        SET cnt = JSON_LENGTH(arr);
        SET len = JSON_LENGTH(arr);
        SET ret = JSON_ARRAY();
        filo: LOOP
          SET cnt = cnt - 1;
          IF cnt >= 0 THEN
            SET ret = JSON_ARRAY_INSERT(ret,
              CONCAT('$[', len, ']'),
              JSON_EXTRACT(arr, CONCAT('$[', cnt, ']'))
            );
          ELSE
            LEAVE filo;
          END IF;
        END LOOP filo;
      END;
    ELSE
      SET ret = NULL;
    END IF;
    RETURN ret;
  END;
$$
DELIMITER ;
-- [end] Array reversed.
