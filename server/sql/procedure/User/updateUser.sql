DELIMITER //
DROP PROCEDURE IF EXISTS updateUser //

CREATE PROCEDURE updateUser(
    ID INT,
    NAME VARCHAR(20),
    PWD VARCHAR(20), 
    EMAIL VARCHAR(50), 
    COUNTRY VARCHAR(50)
)

BEGIN
    SELECT * from user WHERE userId = ID;
    
    UPDATE user
    SET
        userName = NAME,
        userPwd = PWD,
        userEmail = EMAIL,
        userCountry = COUNTRY
    WHERE
        userId = ID;
END //
DELIMITER ;