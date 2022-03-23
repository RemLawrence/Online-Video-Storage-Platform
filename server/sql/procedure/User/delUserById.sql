DELIMITER //
DROP PROCEDURE IF EXISTS delUserById //

CREATE PROCEDURE delUserById
(
   /* Parameters */
   IN ID INT
)

BEGIN
   SELECT * from user WHERE userId = ID;
   /* Do the DELETE */
   DELETE FROM user WHERE userId = ID;
END //
DELIMITER ;