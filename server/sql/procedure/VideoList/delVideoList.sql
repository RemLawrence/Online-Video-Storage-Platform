DELIMITER //
DROP PROCEDURE IF EXISTS delVideoList //

CREATE PROCEDURE delVideoList
(
    IN USER_NAME VARCHAR(20),
    IN VIDEOLIST_ID VARCHAR(36)
)

BEGIN
    DECLARE USER_ID VARCHAR(36); 
    SET USER_ID = (SELECT userId from user WHERE userName = USER_NAME LIMIT 1); 

    SELECT * from videolist WHERE userId = USER_ID AND videoListId = VIDEOLIST_ID;
    /* Delete all the videos linked to this videolist first */
    DELETE FROM video_videolist WHERE vv_videoListId = VIDEOLIST_ID;
    /* Then do the deletion for the videolist row */
    DELETE FROM videolist WHERE userId = USER_ID AND videoListId = VIDEOLIST_ID;
END //
DELIMITER ;