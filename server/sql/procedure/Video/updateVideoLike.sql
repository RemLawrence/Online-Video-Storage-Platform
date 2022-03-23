DELIMITER //
DROP PROCEDURE IF EXISTS updateVideoLike //

CREATE PROCEDURE updateVideoLike(
    USER_NAME VARCHAR(20),
    VIDEO_ID VARCHAR(36),
    UPDATED_LIKES FLOAT
)

BEGIN
    DECLARE USER_ID VARCHAR(36); 
    SET USER_ID = (SELECT userId from user WHERE userName = USER_NAME LIMIT 1); 

    SELECT * from video WHERE videoId = VIDEO_ID AND userId = USER_ID;
    
    UPDATE video
    SET
        likes = UPDATED_LIKES
    WHERE
        videoId = VIDEO_ID AND userId = USER_ID;
END //
DELIMITER ;