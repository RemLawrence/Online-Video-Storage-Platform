DELIMITER //
DROP PROCEDURE IF EXISTS updateUser //

CREATE PROCEDURE updateUser(
    PREV_NAME VARCHAR(20),
    NAME VARCHAR(20),
    PWD VARCHAR(20), 
    EMAIL VARCHAR(50), 
    COUNTRY VARCHAR(50)
)

BEGIN
    /* DECLARE USER_ID VARCHAR(36); */
    /* SET USER_ID = (SELECT userId from user WHERE userName = NAME); */
    SELECT * from user WHERE userName = PREV_NAME;
    
    UPDATE user
    SET
        userName = NAME,
        userPwd = PWD,
        userEmail = EMAIL,
        userCountry = COUNTRY
    WHERE
        userName = PREV_NAME;
END //
DELIMITER ;