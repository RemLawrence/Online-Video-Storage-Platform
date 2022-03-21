DROP TABLE IF EXISTS video;
CREATE TABLE video (
  videoId      INT           NOT NULL AUTO_INCREMENT,
  videoTitle   VARCHAR(100)  NOT NULL,
  videoSize    float         NOT NULL,
  uploadDate   DATE          NOT NULL,
  userId       INT           NOT NULL,
  PRIMARY KEY (videoId),
  FOREIGN KEY (userId) REFERENCES user (userId)
);