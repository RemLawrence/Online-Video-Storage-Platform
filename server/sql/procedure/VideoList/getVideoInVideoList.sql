DELIMITER //
DROP PROCEDURE IF EXISTS getVideoInVideoList //

CREATE PROCEDURE getVideoInVideoList(
    USER_NAME VARCHAR(36),
    VIDEOLIST_ID VARCHAR(36)
)

BEGIN
    DECLARE USER_ID VARCHAR(36); 
    SET USER_ID = (SELECT userId from user WHERE userName = USER_NAME LIMIT 1); 
    
    SELECT * from video_videolist WHERE vv_userId = USER_ID AND vv_videoListId = VIDEOLIST_ID;
END //
DELIMITER ;