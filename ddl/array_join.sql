-- [begin] Array join into string with separator.
DROP FUNCTION IF EXISTS ARRAY_JOIN;
DELIMITER $$
CREATE FUNCTION ARRAY_JOIN (
  arr JSON,
  separator_chars TEXT
) RETURNS TEXT
  COMMENT '`ARRAY_JOIN` function concatenates each elements of `arr` by `separator_chars`.'
  LANGUAGE SQL
  DETERMINISTIC
  NO SQL
  BEGIN
    DECLARE ret TEXT CHARSET utf8mb4 COLLATE utf8mb4_bin DEFAULT '';
    DECLARE idx_0 INT DEFAULT 0;

    IF JSON_TYPE(arr) = 'ARRAY' THEN
      SET separator_chars = COALESCE(separator_chars, ',');
      main: LOOP
        IF JSON_LENGTH(arr) = idx_0 THEN
          LEAVE main;
        END IF;
        SET ret = CONCAT(ret, CASE idx_0 WHEN 0 THEN '' ELSE separator_chars END);
        SET ret = CONCAT(ret, JSON_UNQUOTE(JSON_EXTRACT(arr, CONCAT('$[', idx_0, ']'))));
        SET idx_0 = idx_0 + 1;
      END LOOP;
    ELSE
      SET ret = NULL;
    END IF;
    RETURN ret;
  END;
$$
DELIMITER ;
-- [end] Array join into string with separator.