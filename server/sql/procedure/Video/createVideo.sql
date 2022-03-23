DELIMITER //
DROP PROCEDURE IF EXISTS createVideo //
CREATE PROCEDURE createVideo
(
    USER_ID INT,
    TITLE VARCHAR(100),
    SIZE FLOAT
)

BEGIN
   /* Do the INSERT */
   INSERT INTO video (
      videoTitle, 
      videoSize, 
      likes, 
      uploadDate,
      userId
   ) VALUES (
      TITLE,
      SIZE,
      0,
      CURDATE(),
      USER_ID
   );
   IF(ROW_COUNT() = 0) THEN
      SIGNAL SQLSTATE '52711'
        SET MESSAGE_TEXT = 'Unable to create user.';
   END IF;

   /* If the INSERT is successful, then this will return the Id for the record */
   SELECT LAST_INSERT_ID(); /* Specific to this session */

END //
DELIMITER ;
