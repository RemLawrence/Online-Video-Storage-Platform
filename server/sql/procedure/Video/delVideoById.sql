DELIMITER //
DROP PROCEDURE IF EXISTS delVideoById //

CREATE PROCEDURE delVideoById
(
    IN USER_NAME VARCHAR(20),
    IN VIDEO_ID VARCHAR(36)
)

BEGIN
    DECLARE USER_ID VARCHAR(36); 
    SET USER_ID = (SELECT userId from user WHERE userName = USER_NAME LIMIT 1); 

    SELECT * from video WHERE userId = USER_ID AND videoId = VIDEO_ID;
    /* Delete all the videos from the videolists first */
    DELETE FROM video_videolist WHERE vv_videoId = VIDEO_ID;
    /* Do the DELETE for the video table itself */
    DELETE FROM video WHERE userId = USER_ID AND videoId = VIDEO_ID;
END //
DELIMITER ;