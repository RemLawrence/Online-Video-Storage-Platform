DELIMITER //
DROP PROCEDURE IF EXISTS createUser //
CREATE PROCEDURE createUser
(
   NAME VARCHAR(20),
   PWD VARCHAR(20), 
   EMAIL VARCHAR(50), 
   COUNTRY VARCHAR(50)
)
BEGIN

   /* Do the INSERT */
   INSERT INTO user (
      userName, 
      userPwd, 
      userEmail, 
      userCountry,
      createDate
   ) VALUES (
      NAME,
      PWD,
      EMAIL,
      COUNTRY,
      CURDATE()
   );
   IF(ROW_COUNT() = 0) THEN
      SIGNAL SQLSTATE '52711'
        SET MESSAGE_TEXT = 'Unable to create user.';
   END IF;

   /* If the INSERT is successful, then this will return the Id for the record */
   SELECT LAST_INSERT_ID(); /* Specific to this session */

END //
DELIMITER ;
