DROP TABLE IF EXISTS user;
CREATE TABLE user (
  userId      INT         NOT NULL AUTO_INCREMENT,
  userName    VARCHAR(20) NOT NULL,
  userPwd     VARCHAR(20) NOT NULL,
  userEmail   VARCHAR(50) NOT NULL,
  userCountry VARCHAR(50) DEFAULT NULL,
  createDate  DATE        NOT NULL,
  PRIMARY KEY (userId)
);
