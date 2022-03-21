DELIMITER //
CREATE PROCEDURE delUserById
(
   /* Parameters */
   IN ID INT
)
BEGIN
   /* Do the DELETE */
   DELETE FROM user WHERE userId = ID;

END //
DELIMITER ;