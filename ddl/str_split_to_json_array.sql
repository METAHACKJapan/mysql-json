-- [begin] Stored Function to split string into JSON array.
DROP FUNCTION IF EXISTS STR_SPLIT_TO_JSON_ARRAY;
DELIMITER $$
CREATE FUNCTION STR_SPLIT_TO_JSON_ARRAY (
  source_chars TEXT,
  separator_chars TEXT
) RETURNS JSON
  COMMENT '`STR_SPLIT_TO_JSON_ARRAY` function splits `source_chars` into JSON array by `separator_chars`.'
  LANGUAGE SQL
  DETERMINISTIC
  NO SQL
  BEGIN
    DECLARE ret JSON DEFAULT JSON_ARRAY();
    DECLARE buff TEXT CHARSET utf8mb4 DEFAULT CAST(source_chars AS CHAR CHARACTER SET utf8mb4) COLLATE utf8mb4_bin;
    DECLARE sep TEXT CHARSET utf8mb4 DEFAULT CAST(COALESCE(separator_chars, ',') AS CHAR CHARACTER SET utf8mb4) COLLATE utf8mb4_bin;
    DECLARE found_idx INT;
    DECLARE found_str TEXT;

    main: LOOP
      IF source_chars IS NULL THEN
        SET ret = CAST('null' AS JSON);
        LEAVE main;
      END IF;
      IF LENGTH(buff) = 0 THEN
        LEAVE main;
      END IF;
      SELECT INSTR(buff, sep) INTO found_idx;
      IF found_idx = 0 THEN
        SET found_str = buff;
        SET buff = '';
      ELSEIF found_idx > 0 THEN
        SET found_str = SUBSTR(buff, 1, found_idx - 1);
        SET buff = SUBSTR(buff, found_idx + CHAR_LENGTH(sep));
      END IF;
      SET ret = JSON_ARRAY_APPEND(ret, '$', found_str);
    END LOOP main;
    RETURN ret;
  END
$$
DELIMITER ;
-- [end] Stored Function to split string into JSON array.
