DELIMITER //
DROP PROCEDURE IF EXISTS updateVideoList //

CREATE PROCEDURE updateVideoList(
    USER_NAME VARCHAR(36),
    VIDEOLIST_ID VARCHAR(36),
    TITLE VARCHAR(100),
    DESCRIP VARCHAR(200)
)

BEGIN
    DECLARE USER_ID VARCHAR(36); 
    SET USER_ID = (SELECT userId from user WHERE userName = USER_NAME LIMIT 1);

    SELECT * from videolist WHERE videoListId = VIDEOLIST_ID AND userId = USER_ID;
    
    UPDATE videolist
    SET
        videoListTitle = TITLE,
        description = DESCRIP
    WHERE
        videoListId = VIDEOLIST_ID AND userId = USER_ID;
END //
DELIMITER ;