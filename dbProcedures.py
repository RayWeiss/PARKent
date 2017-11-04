proc4 = """DELIMITER //
CREATE PROCEDURE validate_login
(IN username_to_validate VARCHAR(16), password_to_validate VARCHAR(16), OUT valid INT(1))
BEGIN
  IF EXISTS (
    SELECT name, password
    FROM user
    WHERE name = username_to_validate
        AND password = password_to_validate) THEN
  BEGIN
      SET valid = 1;
  END;
  ELSE
  BEGIN
      SET valid = 0;
  END;
  END IF;
END //
DELIMITER ;"""
