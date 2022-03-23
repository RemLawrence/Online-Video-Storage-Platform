DROP TABLE IF EXISTS video;
CREATE TABLE video (
  videoId      VARCHAR(36)   NOT NULL,
  videoTitle   VARCHAR(100)  NOT NULL,
  videoSize    FLOAT         NOT NULL,
  likes        INT           NOT NULL,
  uploadDate   DATE          NOT NULL,
  userId       VARCHAR(36)   NOT NULL,
  PRIMARY KEY (videoId),
  FOREIGN KEY (userId) REFERENCES user (userId)
);