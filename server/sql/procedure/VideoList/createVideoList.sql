DELIMITER //
DROP PROCEDURE IF EXISTS createVideoList //
CREATE PROCEDURE createVideoList
(
    USER_NAME VARCHAR(20),
    TITLE VARCHAR(100),
    DESCRIP VARCHAR(200)
)

BEGIN
   DECLARE USER_ID VARCHAR(36);
   SET USER_ID = (SELECT userId FROM user WHERE userName = USER_NAME LIMIT 1);
   /* Do the INSERT */
   INSERT INTO videolist (
      videoListId,
      videoListTitle,
      description,
      userId
   ) VALUES (
      UUID(),
      TITLE,
      DESCRIP,
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
