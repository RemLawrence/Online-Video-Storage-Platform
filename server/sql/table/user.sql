DROP TABLE IF EXISTS user;
CREATE TABLE user (
  userId      VARCHAR(36) NOT NULL,
  userName    VARCHAR(20) NOT NULL UNIQUE,
  userPwd     VARCHAR(20) NOT NULL,
  userEmail   VARCHAR(50) NOT NULL,
  userCountry VARCHAR(50) DEFAULT NULL,
  createDate  DATE        NOT NULL,
  PRIMARY KEY (userId)
);
