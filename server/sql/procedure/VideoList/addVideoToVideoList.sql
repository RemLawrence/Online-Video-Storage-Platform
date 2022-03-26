DELIMITER //
DROP PROCEDURE IF EXISTS addVideoToVideoList //
CREATE PROCEDURE addVideoToVideoList
(
    USER_NAME VARCHAR(20),
    VIDEO_ID VARCHAR(36),
    VIDEOLIST_ID VARCHAR(36)
)

BEGIN
   DECLARE USER_ID VARCHAR(36);
   DECLARE INSERT_VIDEO_ID VARCHAR(36);
   DECLARE INSERT_VIDEOLIST_ID VARCHAR(36);
   DECLARE VIDEO_ENTRY_EXIST INT;

   SET USER_ID = (SELECT userId FROM user WHERE userName = USER_NAME LIMIT 1);
   /* Check if the video belongs to this user */
   SET INSERT_VIDEO_ID = (SELECT videoId FROM video WHERE userId = USER_ID AND videoId = VIDEO_ID LIMIT 1);
   /* Check if the videolist belongs to this user */
   SET INSERT_VIDEOLIST_ID = (SELECT videoListId FROM videolist WHERE userId = USER_ID AND videoListId = VIDEOLIST_ID LIMIT 1);
   
   /* Check if there's a duplicated entry */
   SET VIDEO_ENTRY_EXIST = (SELECT vv_id FROM video_videolist WHERE vv_videoId = INSERT_VIDEO_ID AND vv_videoListId = INSERT_VIDEOLIST_ID);

   IF(VIDEO_ENTRY_EXIST IS NULL) THEN
    /* Do the INSERT */
    INSERT INTO video_videolist (
        vv_userId,
        vv_videoId,
        vv_videoListId
        ) VALUES (
        USER_ID,
        INSERT_VIDEO_ID,
        INSERT_VIDEOLIST_ID
        );
    END IF;

    IF(ROW_COUNT() = 0) THEN
        SIGNAL SQLSTATE '52711'
            SET MESSAGE_TEXT = 'Unable to add video to videolist.';
    END IF;

   /* If the INSERT is successful, then this will return the Id for the record */
   SELECT LAST_INSERT_ID(); /* Specific to this session */

END //
DELIMITER ;
