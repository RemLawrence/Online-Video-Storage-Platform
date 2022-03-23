DELIMITER //
DROP PROCEDURE IF EXISTS delUserByName //

CREATE PROCEDURE delUserByName
(
   /* Parameters */
   IN NAME VARCHAR(20)
)

BEGIN
   SELECT * from user WHERE userName = NAME;
   /* Do the DELETE */
   DELETE FROM user WHERE userName = NAME;
END //
DELIMITER ;